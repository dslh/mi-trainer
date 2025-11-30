"""Entry point for MI Trainer."""

import argparse
import asyncio
import sys

from mi_trainer.app import MITrainerApp
from mi_trainer.storage.scenarios import load_scenario_by_name, list_all_scenarios


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="MI Trainer - Practice Motivational Interviewing with AI feedback"
    )
    parser.add_argument(
        "--scenario", "-s",
        help="Name of scenario to load",
    )
    parser.add_argument(
        "--load", "-l",
        help="Path to session file to load",
    )
    parser.add_argument(
        "--list-scenarios",
        action="store_true",
        help="List available scenarios and exit",
    )
    return parser.parse_args()


def list_scenarios() -> None:
    """Print available scenarios."""
    scenarios = list_all_scenarios()
    if not scenarios:
        print("No scenarios available. Run the app and use /new <description> to create one.")
        return

    print("Available scenarios:\n")
    for s in scenarios:
        print(f"  {s.name}")
        print(f"    {s.description}")
        print(f"    Resistance: {s.resistance_level}/5")
        print()


def main() -> None:
    """Main entry point."""
    args = parse_args()

    if args.list_scenarios:
        list_scenarios()
        return

    # Load scenario if specified
    scenario = None
    if args.scenario:
        scenario = load_scenario_by_name(args.scenario)
        if not scenario:
            print(f"Scenario not found: {args.scenario}")
            print("Use --list-scenarios to see available scenarios.")
            sys.exit(1)

    # Create and run app
    app = MITrainerApp()

    try:
        asyncio.run(app.run(scenario=scenario, load_path=args.load))
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
