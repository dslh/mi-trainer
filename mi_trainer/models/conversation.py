"""Conversation tree data model."""

from datetime import datetime
from typing import Literal, Optional
import uuid

from pydantic import BaseModel, Field

from mi_trainer.models.feedback import CoachFeedback


class ConversationNode(BaseModel):
    """A single message in the conversation tree."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    role: Literal["user", "client"] = Field(description="Who sent this message")
    content: str = Field(description="The message content")
    timestamp: datetime = Field(default_factory=datetime.now)
    parent_id: Optional[str] = Field(default=None, description="ID of parent node")
    children: list[str] = Field(
        default_factory=list, description="IDs of child nodes"
    )
    coach_feedback: Optional[CoachFeedback] = Field(
        default=None, description="Coach feedback for user messages"
    )


class ConversationTree(BaseModel):
    """A tree of conversation nodes supporting branching."""

    nodes: dict[str, ConversationNode] = Field(
        default_factory=dict, description="All nodes by ID"
    )
    root_id: Optional[str] = Field(default=None, description="ID of root node")
    current_id: Optional[str] = Field(
        default=None, description="ID of current position in tree"
    )

    def add_message(
        self,
        role: Literal["user", "client"],
        content: str,
        coach_feedback: Optional[CoachFeedback] = None,
    ) -> ConversationNode:
        """Add a new message as a child of the current node."""
        node = ConversationNode(
            role=role,
            content=content,
            parent_id=self.current_id,
            coach_feedback=coach_feedback,
        )

        self.nodes[node.id] = node

        if self.current_id is None:
            self.root_id = node.id
        else:
            self.nodes[self.current_id].children.append(node.id)

        self.current_id = node.id
        return node

    def get_current_node(self) -> Optional[ConversationNode]:
        """Get the current node."""
        if self.current_id is None:
            return None
        return self.nodes.get(self.current_id)

    def get_path_to_current(self) -> list[ConversationNode]:
        """Get the path from root to current node."""
        if self.current_id is None:
            return []

        path = []
        node_id = self.current_id
        while node_id is not None:
            node = self.nodes[node_id]
            path.append(node)
            node_id = node.parent_id

        return list(reversed(path))

    def rewind(self, steps: int = 1) -> Optional[ConversationNode]:
        """Move back up the tree by the given number of steps."""
        if self.current_id is None:
            return None

        node_id = self.current_id
        for _ in range(steps):
            node = self.nodes.get(node_id)
            if node is None or node.parent_id is None:
                break
            node_id = node.parent_id

        self.current_id = node_id
        return self.nodes.get(node_id)

    def goto(self, node_id: str) -> Optional[ConversationNode]:
        """Jump to a specific node by ID."""
        if node_id in self.nodes:
            self.current_id = node_id
            return self.nodes[node_id]
        return None

    def get_branches_at_current(self) -> list[ConversationNode]:
        """Get all child branches from the current node."""
        if self.current_id is None:
            return []
        current = self.nodes.get(self.current_id)
        if current is None:
            return []
        return [self.nodes[child_id] for child_id in current.children]

    def get_conversation_for_llm(self) -> list[dict[str, str]]:
        """Get the conversation path formatted for LLM context."""
        path = self.get_path_to_current()
        return [
            {"role": "assistant" if node.role == "client" else "user", "content": node.content}
            for node in path
        ]

    def is_empty(self) -> bool:
        """Check if the tree has no messages."""
        return len(self.nodes) == 0
