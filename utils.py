"""
Utility functions for Inbox Assistant
"""
import json
from typing import Dict, Any, List
from langdetect import detect, LangDetectException


def detect_language(text: str) -> str:
    """Detect the language of input text."""
    try:
        return detect(text)
    except LangDetectException:
        return "en"


def format_agent_output(output: Dict[str, Any]) -> str:
    """Format agent output for display."""
    formatted = "\n" + "="*60 + "\n"
    formatted += "INBOX ASSISTANT ANALYSIS\n"
    formatted += "="*60 + "\n\n"

    if "summary" in output:
        formatted += f"📝 SUMMARY:\n{output['summary']}\n\n"

    if "urgency" in output:
        urgency_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        emoji = urgency_emoji.get(output['urgency'], "⚪")
        formatted += f"{emoji} URGENCY: {output['urgency']}\n\n"

    if "tone" in output:
        formatted += f"😊 TONE: {output['tone']}\n\n"

    if "draft_reply" in output:
        formatted += f"✉️ SUGGESTED REPLY:\n{output['draft_reply']}\n\n"

    if "action_items" in output:
        formatted += "✅ ACTION ITEMS:\n"
        items = output['action_items']
        if isinstance(items, list):
            for i, item in enumerate(items, 1):
                formatted += f"  {i}. {item}\n"
        else:
            formatted += f"  {items}\n"
        formatted += "\n"

    formatted += "="*60 + "\n"
    return formatted


def parse_json_response(response_text: str) -> Dict[str, Any]:
    """Parse JSON from agent response, handling formatting issues."""
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        if "```json" in response_text:
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            json_str = response_text[start:end].strip()
            return json.loads(json_str)
        elif "```" in response_text:
            start = response_text.find("```") + 3
            end = response_text.find("```", start)
            json_str = response_text[start:end].strip()
            return json.loads(json_str)
        else:
            return {}


def validate_urgency(urgency: str) -> str:
    """Validate and normalize urgency level."""
    urgency = urgency.strip().capitalize()
    if urgency not in ["High", "Medium", "Low"]:
        return "Medium"
    return urgency


def extract_action_items(text: str) -> List[str]:
    """Extract action items from text using heuristics."""
    action_items = []

    action_verbs = [
        "send", "submit", "complete", "review", "update", 
        "schedule", "prepare", "confirm", "respond", "call",
        "email", "follow up", "check", "verify", "provide"
    ]

    lines = text.split("\n")
    for line in lines:
        line_lower = line.lower()
        if any(verb in line_lower for verb in action_verbs):
            if len(line.strip()) > 10:
                action_items.append(line.strip())

    return action_items if action_items else ["No specific action items detected"]


def truncate_text(text: str, max_length: int = 1000) -> str:
    """Truncate text to maximum length while preserving word boundaries."""
    if len(text) <= max_length:
        return text

    truncated = text[:max_length]
    last_space = truncated.rfind(" ")
    if last_space > 0:
        truncated = truncated[:last_space]

    return truncated + "..."
