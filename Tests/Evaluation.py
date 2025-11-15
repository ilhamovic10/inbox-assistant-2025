"""
Evaluation metrics for Inbox Assistant
"""
from typing import Dict, List, Any
import json
from agent import InboxAssistant
from examples_sample_messages import SAMPLE_MESSAGES, MESSAGE_METADATA


def calculate_accuracy(predictions: List[str], expected: List[str]) -> float:
    """Calculate classification accuracy."""
    if len(predictions) != len(expected):
        return 0.0
    correct = sum(1 for p, e in zip(predictions, expected) if p == e)
    return correct / len(predictions) if predictions else 0.0


def calculate_tone_overlap(predicted_tones: List[str], expected_tones: List[str]) -> float:
    """Calculate tone detection overlap (Jaccard similarity)."""
    if not predicted_tones or not expected_tones:
        return 0.0

    pred_set = set(str(t).lower() for t in predicted_tones)
    exp_set = set(str(t).lower() for t in expected_tones)

    intersection = pred_set.intersection(exp_set)
    union = pred_set.union(exp_set)

    return len(intersection) / len(union) if union else 0.0


def evaluate_single_message(
    message_key: str, 
    message: str, 
    assistant: InboxAssistant
) -> Dict[str, Any]:
    """Evaluate system on a single message."""

    metadata = MESSAGE_METADATA.get(message_key, {})

    try:
        result = assistant.process_message_sync(message)
    except Exception as e:
        return {
            "error": str(e),
            "message_key": message_key
        }

    predicted_urgency = result.get("urgency", "Unknown")
    predicted_tone = result.get("tone", [])
    action_items = result.get("action_items", [])

    metrics = {
        "message_key": message_key,
        "urgency_correct": predicted_urgency == metadata.get("expected_urgency"),
        "tone_overlap": calculate_tone_overlap(
            predicted_tone if isinstance(predicted_tone, list) else [predicted_tone],
            metadata.get("expected_tone", [])
        ),
        "has_actions": len(action_items) > 0 and action_items[0] != "No action required",
        "expected_actions": metadata.get("should_have_actions", False),
        "language_detected": result.get("language", "unknown"),
        "expected_language": metadata.get("language", "en")
    }

    metrics["action_detection_correct"] = (
        metrics["has_actions"] == metrics["expected_actions"]
    )

    metrics["language_correct"] = (
        metrics["language_detected"] == metrics["expected_language"]
    )

    return metrics


def evaluate_system(
    test_messages: Dict[str, str] = None,
    verbose: bool = True
) -> Dict[str, Any]:
    """Evaluate the complete Inbox Assistant system."""

    if test_messages is None:
        test_messages = SAMPLE_MESSAGES

    assistant = InboxAssistant()
    results = []

    if verbose:
        print("="*70)
        print("EVALUATING INBOX ASSISTANT")
        print("="*70)
        print(f"\nProcessing {len(test_messages)} test messages...\n")

    for msg_key, message in test_messages.items():
        if verbose:
            print(f"Testing: {msg_key}...", end=" ")

        metrics = evaluate_single_message(msg_key, message, assistant)
        results.append(metrics)

        if verbose:
            if "error" in metrics:
                print(f"❌ ERROR: {metrics['error']}")
            else:
                urgency_check = "✅" if metrics["urgency_correct"] else "❌"
                print(f"{urgency_check}")

    aggregated = {
        "total_messages": len(results),
        "urgency_accuracy": sum(r.get("urgency_correct", 0) for r in results) / len(results),
        "avg_tone_overlap": sum(r.get("tone_overlap", 0) for r in results) / len(results),
        "action_detection_accuracy": sum(
            r.get("action_detection_correct", 0) for r in results
        ) / len(results),
        "language_accuracy": sum(r.get("language_correct", 0) for r in results) / len(results),
        "error_rate": sum(1 for r in results if "error" in r) / len(results),
        "individual_results": results
    }

    if verbose:
        print("\n" + "="*70)
        print("EVALUATION RESULTS")
        print("="*70)
        print(f"\nUrgency Classification Accuracy: {aggregated['urgency_accuracy']:.1%}")
        print(f"Tone Detection Overlap: {aggregated['avg_tone_overlap']:.1%}")
        print(f"Action Detection Accuracy: {aggregated['action_detection_accuracy']:.1%}")
        print(f"Language Detection Accuracy: {aggregated['language_accuracy']:.1%}")
        print(f"Error Rate: {aggregated['error_rate']:.1%}")
        print("\n" + "="*70)

    return aggregated


def export_results(results: Dict[str, Any], filename: str = "evaluation_results.json"):
    """Export evaluation results to JSON file."""
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults exported to {filename}")


if __name__ == "__main__":
    results = evaluate_system(verbose=True)
    export_results(results)
