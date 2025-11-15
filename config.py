"""
Configuration settings for Inbox Assistant
"""
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")

APP_NAME = "inbox_assistant"
DEFAULT_USER_ID = "user_001"

AGENTS_CONFIG = {
    "summarizer": {
        "name": "SummarizerAgent",
        "output_key": "summary",
        "description": "Summarizes long messages into concise key points"
    },
    "urgency_classifier": {
        "name": "UrgencyClassifierAgent", 
        "output_key": "urgency",
        "description": "Classifies message urgency as High, Medium, or Low"
    },
    "tone_analyzer": {
        "name": "ToneAnalyzerAgent",
        "output_key": "tone",
        "description": "Analyzes the emotional tone and formality of messages"
    },
    "reply_generator": {
        "name": "ReplyGeneratorAgent",
        "output_key": "draft_reply",
        "description": "Generates contextually appropriate draft replies"
    },
    "next_step_planner": {
        "name": "NextStepPlannerAgent",
        "output_key": "action_items",
        "description": "Extracts actionable tasks and next steps"
    }
}

URGENCY_LEVELS = ["High", "Medium", "Low"]

TONE_CATEGORIES = [
    "Formal", "Informal", "Friendly", "Polite", 
    "Direct", "Angry", "Appreciative", "Urgent", 
    "Neutral", "Professional", "Casual"
]

EVALUATION_METRICS = {
    "summarization": ["rouge", "length_ratio"],
    "classification": ["accuracy", "precision", "recall", "f1"],
    "generation": ["relevance", "coherence"]
}
