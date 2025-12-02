"""Main application orchestration."""

import asyncio
from datetime import datetime
from typing import Optional

from prompt_toolkit import Application
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.patch_stdout import patch_stdout

from mi_trainer.agents import ClientAgent, CoachAgent, ScenarioBuilderAgent
from mi_trainer.models import Scenario, ConversationTree
from mi_trainer.models.feedback import CoachFeedback
from mi_trainer.storage.sessions import Session, create_session, save_session, load_session, list_sessions
from mi_trainer.storage.scenarios import list_all_scenarios, load_scenario_by_name, save_user_scenario
from mi_trainer.ui.layout import AppLayout


class MITrainerApp:
    """Main MI Trainer application."""

    def __init__(self):
        self.session: Optional[Session] = None
        self.client_agent: Optional[ClientAgent] = None
        self.coach_agent = CoachAgent()
        self.scenario_builder = ScenarioBuilderAgent()

        # UI
        self.layout = AppLayout(on_input=self._handle_input)

        # Key bindings
        self.kb = self._create_key_bindings()

        # Application
        self.app = Application(
            layout=self.layout.layout,
            key_bindings=self.kb,
            style=self.layout.get_style(),
            editing_mode=EditingMode.VI,
            full_screen=True,
            mouse_support=True,
        )

        # State
        self._running = True

    def _create_key_bindings(self) -> KeyBindings:
        """Create application key bindings."""
        kb = KeyBindings()

        @kb.add("c-c")
        @kb.add("c-q")
        def exit_app(event):
            """Exit the application."""
            self._running = False
            event.app.exit()

        @kb.add("c-s")
        def save(event):
            """Save current session."""
            if self.session:
                asyncio.create_task(self._save_session())

        # Scroll conversation pane
        @kb.add("pageup")
        @kb.add("c-up")
        def scroll_conv_up(event):
            """Scroll conversation pane up."""
            self.layout.conversation_pane.container.vertical_scroll -= 3

        @kb.add("pagedown")
        @kb.add("c-down")
        def scroll_conv_down(event):
            """Scroll conversation pane down."""
            self.layout.conversation_pane.container.vertical_scroll += 3

        # Scroll feedback pane (with shift modifier)
        @kb.add("s-pageup")
        @kb.add("s-up")
        def scroll_feedback_up(event):
            """Scroll feedback pane up."""
            self.layout.feedback_pane.container.vertical_scroll -= 3

        @kb.add("s-pagedown")
        @kb.add("s-down")
        def scroll_feedback_down(event):
            """Scroll feedback pane down."""
            self.layout.feedback_pane.container.vertical_scroll += 3

        return kb

    def _handle_input(self, text: str) -> None:
        """Handle user input (called from input area)."""
        # Schedule async processing - this is called from sync context
        asyncio.create_task(self._process_input(text))

    async def run(self, scenario: Optional[Scenario] = None, load_path: Optional[str] = None) -> None:
        """Run the application."""
        # Initialize session
        if load_path:
            self.session = load_session(load_path)
            self.layout.conversation_pane.load_conversation(self.session.conversation)
            self.layout.feedback_pane.show_info(f"Loaded session: {self.session.scenario.name}")
        elif scenario:
            self.session = create_session(scenario)
        else:
            # Show scenario selection
            await self._show_scenario_selection()

        if self.session:
            self.client_agent = ClientAgent(self.session.scenario)
            self.layout.set_status(f"Scenario: {self.session.scenario.name} | /help for commands")

            # Get opening if conversation is empty
            if self.session.conversation.is_empty():
                await self._get_client_opening()

        # Run the application
        await self.app.run_async()

    async def _show_scenario_selection(self) -> None:
        """Show scenario selection interface."""
        scenarios = list_all_scenarios()

        if not scenarios:
            self.layout.feedback_pane.show_info(
                "No scenarios found. Use /new <description> to create one."
            )
            return

        # For now, just list scenarios in feedback pane
        self.layout.feedback_pane.show_info("Available scenarios:")
        for i, s in enumerate(scenarios, 1):
            self.layout.feedback_pane.show_info(f"  {i}. {s.name} - {s.description[:50]}...")

        self.layout.feedback_pane.show_info("\nUse /scenario <name> to select one.")

    async def _get_client_opening(self) -> None:
        """Get the client's opening statement."""
        if not self.client_agent:
            return

        self.layout.conversation_pane.start_streaming("client")
        self.layout.set_status("Client is speaking...")

        opening = await self.client_agent.get_opening()
        self.layout.conversation_pane.finish_streaming()
        self.layout.conversation_pane.add_message("client", opening)

        # Add to conversation tree
        self.session.conversation.add_message("client", opening)

        self.layout.set_status(f"Scenario: {self.session.scenario.name} | /help for commands")
        self.app.invalidate()

    async def _process_input(self, text: str) -> None:
        """Process user input."""
        if text.startswith("/"):
            await self._handle_command(text)
        else:
            await self._handle_message(text)

    async def _handle_command(self, text: str) -> None:
        """Handle a slash command."""
        parts = text[1:].split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        handlers = {
            "help": self._cmd_help,
            "hint": self._cmd_hint,
            "debrief": self._cmd_debrief,
            "quit": self._cmd_quit,
            "save": self._cmd_save,
            "load": self._cmd_load,
            "scenario": self._cmd_scenario,
            "new": self._cmd_new,
            "rewind": self._cmd_rewind,
            "branches": self._cmd_branches,
            "goto": self._cmd_goto,
        }

        handler = handlers.get(command)
        if handler:
            await handler(args)
        else:
            self.layout.feedback_pane.show_error(f"Unknown command: {command}")

        self.app.invalidate()

    async def _handle_message(self, text: str) -> None:
        """Handle a conversation message."""
        if not self.session or not self.client_agent:
            self.layout.feedback_pane.show_error("No active session. Use /scenario to start.")
            return

        # Add user message to tree
        self.session.conversation.add_message("user", text)
        self.layout.conversation_pane.add_message("user", text)

        # Get conversation history for LLM
        conversation = self.session.conversation.get_conversation_for_llm()

        # Run coach and client in parallel
        self.layout.set_status("Processing...")
        self.app.invalidate()

        # Start both tasks
        coach_task = asyncio.create_task(self._run_coach(conversation, text))
        client_task = asyncio.create_task(self._run_client(conversation))

        # Wait for both to complete
        feedback, client_response = await asyncio.gather(coach_task, client_task)

        # Store feedback on the user's node
        current = self.session.conversation.get_current_node()
        if current and current.role == "client":
            # Get the user's node (parent of current)
            path = self.session.conversation.get_path_to_current()
            if len(path) >= 2:
                user_node = path[-2]
                user_node.coach_feedback = feedback

        self.layout.set_status(f"Scenario: {self.session.scenario.name} | /help for commands")
        self.app.invalidate()

    async def _run_coach(self, conversation: list[dict], user_message: str) -> CoachFeedback:
        """Run the coach agent and update UI."""
        self.layout.feedback_pane.start_streaming()

        full_response = ""
        async for chunk in self.coach_agent.analyze_streaming(conversation, user_message):
            full_response += chunk
            self.layout.feedback_pane.append_streaming(chunk)
            self.app.invalidate()

        self.layout.feedback_pane.finish_streaming()

        # Parse the response into structured feedback
        feedback = self.coach_agent._parse_feedback(full_response)
        self.layout.feedback_pane.show_feedback(feedback)
        self.app.invalidate()

        return feedback

    async def _run_client(self, conversation: list[dict]) -> str:
        """Run the client agent and update UI."""
        self.layout.conversation_pane.start_streaming("client")

        full_response = ""
        async for chunk in self.client_agent.respond(conversation):
            full_response += chunk
            self.layout.conversation_pane.append_streaming(chunk)
            self.app.invalidate()

        self.layout.conversation_pane.finish_streaming()

        # Add to conversation tree
        self.session.conversation.add_message("client", full_response)

        return full_response

    # Command handlers

    async def _cmd_help(self, args: str) -> None:
        """Show help information."""
        help_text = """Commands:
  /help          - Show this help
  /hint          - Get technique suggestion
  /debrief       - Full session analysis
  /quit          - Exit (prompts to save)
  /save          - Save current session
  /load <name>   - Load a saved session
  /scenario [n]  - List or select scenario
  /new <desc>    - Generate new scenario
  /rewind [n]    - Go back n messages
  /branches      - Show branches
  /goto <id>     - Jump to node"""
        self.layout.feedback_pane.show_info(help_text)

    async def _cmd_hint(self, args: str) -> None:
        """Get a hint about what technique to try next."""
        if not self.session or self.session.conversation.is_empty():
            self.layout.feedback_pane.show_error("No conversation yet. Start talking first!")
            return

        self.layout.feedback_pane.show_info("Thinking...")
        self.layout.set_status("Getting hint...")
        self.app.invalidate()

        conversation = self.session.conversation.get_conversation_for_llm()
        hint = await self.coach_agent.get_hint(conversation)

        self.layout.feedback_pane.show_info(f"Hint: {hint}")
        self.layout.set_status(f"Scenario: {self.session.scenario.name} | /help for commands")

    async def _cmd_debrief(self, args: str) -> None:
        """Get a full session debrief."""
        if not self.session or self.session.conversation.is_empty():
            self.layout.feedback_pane.show_error("No conversation to debrief yet!")
            return

        # Check if there's enough conversation to debrief
        conversation = self.session.conversation.get_conversation_for_llm()
        if len(conversation) < 4:
            self.layout.feedback_pane.show_error("Have a longer conversation first (at least 2 exchanges).")
            return

        self.layout.feedback_pane.clear()
        self.layout.feedback_pane.show_info("Analyzing session... (this may take a moment)")
        self.layout.set_status("Generating debrief...")
        self.app.invalidate()

        debrief = await self.coach_agent.get_debrief(conversation)

        self.layout.feedback_pane.clear()
        self.layout.feedback_pane.show_info(debrief)
        self.layout.set_status(f"Scenario: {self.session.scenario.name} | /help for commands")

    async def _cmd_quit(self, args: str) -> None:
        """Quit the application."""
        if self.session and not self.session.conversation.is_empty():
            self.layout.feedback_pane.show_info("Saving session before exit...")
            await self._save_session()
        self._running = False
        self.app.exit()

    async def _cmd_save(self, args: str) -> None:
        """Save the current session."""
        await self._save_session()

    async def _save_session(self) -> None:
        """Save the current session to disk."""
        if self.session:
            path = save_session(self.session)
            self.layout.feedback_pane.show_info(f"Session saved: {path.name}")

    async def _cmd_load(self, args: str) -> None:
        """Load a saved session."""
        sessions = list_sessions()
        if not sessions:
            self.layout.feedback_pane.show_info("No saved sessions found.")
            return

        if not args:
            self.layout.feedback_pane.show_info("Saved sessions:")
            for i, (path, name, date) in enumerate(sessions, 1):
                self.layout.feedback_pane.show_info(
                    f"  {i}. {name} ({date.strftime('%Y-%m-%d %H:%M')})"
                )
            self.layout.feedback_pane.show_info("\nUse /load <number> to load.")
            return

        try:
            idx = int(args) - 1
            if 0 <= idx < len(sessions):
                path, _, _ = sessions[idx]
                self.session = load_session(path)
                self.client_agent = ClientAgent(self.session.scenario)
                self.layout.conversation_pane.clear()
                self.layout.conversation_pane.load_conversation(self.session.conversation)
                self.layout.feedback_pane.show_info(f"Loaded: {self.session.scenario.name}")
                self.layout.set_status(f"Scenario: {self.session.scenario.name} | /help for commands")
            else:
                self.layout.feedback_pane.show_error("Invalid session number.")
        except ValueError:
            self.layout.feedback_pane.show_error("Please specify a session number.")

    async def _cmd_scenario(self, args: str) -> None:
        """List or select a scenario."""
        scenarios = list_all_scenarios()

        if not scenarios:
            self.layout.feedback_pane.show_info("No scenarios found. Use /new <description> to create one.")
            return

        if not args:
            self.layout.feedback_pane.show_info("Available scenarios:")
            for i, s in enumerate(scenarios, 1):
                self.layout.feedback_pane.show_info(f"  {i}. {s.name}")
            self.layout.feedback_pane.show_info("\nUse /scenario <number> or /scenario <name>")
            return

        # Try to load by number or name
        scenario = None
        try:
            idx = int(args) - 1
            if 0 <= idx < len(scenarios):
                scenario = scenarios[idx]
        except ValueError:
            scenario = load_scenario_by_name(args)

        if scenario:
            self.session = create_session(scenario)
            self.client_agent = ClientAgent(scenario)
            self.layout.conversation_pane.clear()
            self.layout.feedback_pane.clear()
            self.layout.feedback_pane.show_info(f"Starting scenario: {scenario.name}")
            self.layout.set_status(f"Scenario: {scenario.name} | /help for commands")
            await self._get_client_opening()
        else:
            self.layout.feedback_pane.show_error(f"Scenario not found: {args}")

    async def _cmd_new(self, args: str) -> None:
        """Generate a new scenario from description."""
        if not args:
            self.layout.feedback_pane.show_error("Please provide a description: /new <description>")
            return

        self.layout.feedback_pane.show_info("Generating scenario...")
        self.layout.set_status("Generating scenario...")
        self.app.invalidate()

        try:
            scenario = await self.scenario_builder.build_scenario(args)
            save_user_scenario(scenario)
            self.layout.feedback_pane.show_info(f"Created scenario: {scenario.name}")
            self.layout.feedback_pane.show_info("Use /scenario to select it.")
        except Exception as e:
            self.layout.feedback_pane.show_error(f"Failed to generate scenario: {e}")

        self.layout.set_status(f"Scenario: {self.session.scenario.name if self.session else 'None'} | /help for commands")

    async def _cmd_rewind(self, args: str) -> None:
        """Rewind the conversation."""
        if not self.session:
            self.layout.feedback_pane.show_error("No active session.")
            return

        steps = 1
        if args:
            try:
                steps = int(args)
            except ValueError:
                self.layout.feedback_pane.show_error("Invalid number of steps.")
                return

        node = self.session.conversation.rewind(steps)
        if node:
            self.layout.conversation_pane.clear()
            self.layout.conversation_pane.load_conversation(self.session.conversation)
            self.layout.feedback_pane.show_info(f"Rewound {steps} step(s).")

            # Show branches if any
            branches = self.session.conversation.get_branches_at_current()
            if branches:
                self.layout.feedback_pane.show_info(f"{len(branches)} branch(es) from here.")
        else:
            self.layout.feedback_pane.show_info("Already at the beginning.")

    async def _cmd_branches(self, args: str) -> None:
        """Show branches at current point."""
        if not self.session:
            self.layout.feedback_pane.show_error("No active session.")
            return

        branches = self.session.conversation.get_branches_at_current()
        if not branches:
            self.layout.feedback_pane.show_info("No branches from current position.")
            return

        self.layout.feedback_pane.show_info(f"Branches from current point:")
        for i, node in enumerate(branches, 1):
            preview = node.content[:50] + "..." if len(node.content) > 50 else node.content
            self.layout.feedback_pane.show_info(f"  {i}. [{node.role}] {preview}")
        self.layout.feedback_pane.show_info("\nUse /goto <node_id> to jump to a branch.")

    async def _cmd_goto(self, args: str) -> None:
        """Go to a specific node."""
        if not self.session:
            self.layout.feedback_pane.show_error("No active session.")
            return

        if not args:
            self.layout.feedback_pane.show_error("Please specify a node ID.")
            return

        # Try as branch number first
        branches = self.session.conversation.get_branches_at_current()
        try:
            idx = int(args) - 1
            if 0 <= idx < len(branches):
                node = self.session.conversation.goto(branches[idx].id)
                if node:
                    self.layout.conversation_pane.clear()
                    self.layout.conversation_pane.load_conversation(self.session.conversation)
                    self.layout.feedback_pane.show_info(f"Jumped to branch {idx + 1}.")
                return
        except ValueError:
            pass

        # Try as node ID
        node = self.session.conversation.goto(args)
        if node:
            self.layout.conversation_pane.clear()
            self.layout.conversation_pane.load_conversation(self.session.conversation)
            self.layout.feedback_pane.show_info(f"Jumped to node {args}.")
        else:
            self.layout.feedback_pane.show_error(f"Node not found: {args}")
