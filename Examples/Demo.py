"""
Demo script for Inbox Assistant
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agent import InboxAssistant, analyze_and_print
from examples_sample_messages import SAMPLE_MESSAGES, get_sample_message
from utils import format_agent_output


def run_demo():
    """Run demonstration of Inbox Assistant on sample messages."""

    print("="*70)
    print("INBOX ASSISTANT - MULTI-AGENT AI SYSTEM DEMO")
    print("="*70)
    print("\nThis demo showcases a 5-agent pipeline for intelligent message processing:")
    print("  1. Summarization Agent")
    print("  2. Urgency Classifier Agent")
    print("  3. Tone Analyzer Agent")
    print("  4. Reply Generator Agent")
    print("  5. Next-Step Planner Agent")
    print("\n" + "="*70 + "\n")

    demo_samples = [
        "urgent_technical",
        "medium_request", 
        "angry_customer",
        "friendly_casual"
    ]

    assistant = InboxAssistant()

    for i, sample_key in enumerate(demo_samples, 1):
        message = get_sample_message(sample_key)

        print(f"\n{'='*70}")
        print(f"DEMO {i}/{len(demo_samples)}: {sample_key.replace('_', ' ').title()}")
        print(f"{'='*70}\n")

        print("📧 ORIGINAL MESSAGE:")
        print("-" * 70)
        print(message)
        print("-" * 70)

        print("\n🤖 PROCESSING WITH MULTI-AGENT PIPELINE...\n")

        try:
            result = assistant.process_message_sync(message)
            print(format_agent_output(result))
        except Exception as e:
            print(f"❌ Error processing message: {str(e)}")
            print("Make sure you have set GOOGLE_API_KEY in your .env file\n")

    print("="*70)
    print("DEMO COMPLETE")
    print("="*70)


def interactive_mode():
    """Interactive mode for testing custom messages."""

    print("="*70)
    print("INBOX ASSISTANT - INTERACTIVE MODE")
    print("="*70)
    print("\nEnter a message to analyze (or 'quit' to exit):")
    print("For multi-line input, enter '---' on a new line when done\n")

    assistant = InboxAssistant()

    while True:
        print("\n" + "-"*70)
        print("Enter message (or 'quit' to exit):")

        lines = []
        while True:
            try:
                line = input()
                if line.lower() == 'quit':
                    print("\nExiting interactive mode. Goodbye!")
                    return
                if line == '---':
                    break
                lines.append(line)
            except EOFError:
                return

        message = '\n'.join(lines).strip()

        if not message:
            print("Empty message, please try again.")
            continue

        print("\n🤖 PROCESSING...\n")

        try:
            result = assistant.process_message_sync(message)
            print(format_agent_output(result))
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print("Make sure GOOGLE_API_KEY is set correctly\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Inbox Assistant Demo")
    parser.add_argument(
        '--mode', 
        choices=['demo', 'interactive'], 
        default='demo',
        help='Run mode: demo (preset examples) or interactive (custom input)'
    )

    args = parser.parse_args()

    if args.mode == 'interactive':
        interactive_mode()
    else:
        run_demo()
