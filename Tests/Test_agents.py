"""
Unit tests for Inbox Assistant agents
"""
import pytest
from agent import (
    create_summarizer_agent,
    create_urgency_classifier_agent,
    create_tone_analyzer_agent,
    create_reply_generator_agent,
    create_next_step_planner_agent,
    InboxAssistant
)
from examples_sample_messages import SAMPLE_MESSAGES, MESSAGE_METADATA
from utils import detect_language, parse_json_response, validate_urgency


class TestAgentCreation:
    """Test that all agents are created correctly."""

    def test_create_summarizer(self):
        agent = create_summarizer_agent()
        assert agent.name == "SummarizerAgent"
        assert agent.output_key == "summary"
        assert agent.model is not None

    def test_create_urgency_classifier(self):
        agent = create_urgency_classifier_agent()
        assert agent.name == "UrgencyClassifierAgent"
        assert agent.output_key == "urgency"

    def test_create_tone_analyzer(self):
        agent = create_tone_analyzer_agent()
        assert agent.name == "ToneAnalyzerAgent"
        assert agent.output_key == "tone"

    def test_create_reply_generator(self):
        agent = create_reply_generator_agent()
        assert agent.name == "ReplyGeneratorAgent"
        assert agent.output_key == "draft_reply"

    def test_create_next_step_planner(self):
        agent = create_next_step_planner_agent()
        assert agent.name == "NextStepPlannerAgent"
        assert agent.output_key == "action_items"


class TestUtilityFunctions:
    """Test utility functions."""

    def test_language_detection_english(self):
        text = "This is an English message."
        lang = detect_language(text)
        assert lang == "en"

    def test_language_detection_spanish(self):
        text = "Este es un mensaje en español."
        lang = detect_language(text)
        assert lang == "es"

    def test_parse_json_response_valid(self):
        json_str = '{"urgency": "High", "reasoning": "Test"}'
        result = parse_json_response(json_str)
        assert result["urgency"] == "High"
        assert "reasoning" in result

    def test_validate_urgency_valid(self):
        assert validate_urgency("High") == "High"
        assert validate_urgency("medium") == "Medium"
        assert validate_urgency("  low  ") == "Low"

    def test_validate_urgency_invalid(self):
        assert validate_urgency("Urgent") == "Medium"
        assert validate_urgency("") == "Medium"


class TestInboxAssistant:
    """Integration tests for InboxAssistant system."""

    def test_assistant_initialization(self):
        assistant = InboxAssistant()
        assert assistant.pipeline is not None
        assert assistant.session_service is not None
        assert assistant.memory_service is not None
        assert assistant.runner is not None

    def test_sample_messages_coverage(self):
        assert len(SAMPLE_MESSAGES) >= 10

        urgency_levels = set()
        for key in MESSAGE_METADATA:
            urgency_levels.add(MESSAGE_METADATA[key].get("expected_urgency"))

        assert "High" in urgency_levels
        assert "Medium" in urgency_levels
        assert "Low" in urgency_levels


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
