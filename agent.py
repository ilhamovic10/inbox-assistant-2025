"""
Inbox Assistant - Multi-Agent AI System
Main implementation with 5 specialized agents using Google ADK
"""

import asyncio
from typing import Dict, Any, Optional
from google.adk.agents import Agent, SequentialAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.memory import InMemoryMemoryService
from google.genai.types import Content, Part

from config import (
    GEMINI_MODEL, APP_NAME, DEFAULT_USER_ID, 
    AGENTS_CONFIG, URGENCY_LEVELS, TONE_CATEGORIES
)
from utils import detect_language, format_agent_output, parse_json_response


def create_summarizer_agent() -> Agent:
    """Creates the Summarization Agent that condenses messages into key points."""
    agent_config = AGENTS_CONFIG["summarizer"]

    instruction = """You are a Summarization Agent that summarizes communications.

Your task:
- Summarize the message in 2-4 concise sentences
- Focus on main points, requests, and important details
- Preserve the original language
- Be clear and actionable

Return ONLY a JSON object with this structure:
{
  "summary": "Your concise summary here..."
}
"""

    return Agent(
        model=GEMINI_MODEL,
        name=agent_config["name"],
        description=agent_config["description"],
        instruction=instruction,
        output_key=agent_config["output_key"]
    )


def create_urgency_classifier_agent() -> Agent:
    """Creates the Urgency Classifier Agent that labels message priority."""
    agent_config = AGENTS_CONFIG["urgency_classifier"]

    instruction = f"""You are an Urgency Classifier Agent that categorizes message priority.

Classification criteria:
- HIGH: Requires immediate attention (crisis, urgent deadline, critical issue)
- MEDIUM: Important but not emergency (needs response within days)
- LOW: Informational or non-urgent (no immediate action required)

Analyze for urgency signals:
- Time-sensitive words ("urgent", "ASAP", "immediately", "today")
- Deadline mentions
- Emotional intensity
- Business impact

Return ONLY a JSON object:
{{
  "urgency": "High" | "Medium" | "Low",
  "reasoning": "Brief explanation"
}}
"""

    return Agent(
        model=GEMINI_MODEL,
        name=agent_config["name"],
        description=agent_config["description"],
        instruction=instruction,
        output_key=agent_config["output_key"]
    )


def create_tone_analyzer_agent() -> Agent:
    """Creates the Tone Analyzer Agent that detects emotional tone and formality."""
    agent_config = AGENTS_CONFIG["tone_analyzer"]

    instruction = f"""You are a Tone Analyzer Agent that detects sender's tone and mood.

Analyze for:
- Formality level (Formal vs Informal)
- Emotional state (Angry, Friendly, Neutral, etc.)
- Communication style (Direct, Polite, Professional, Casual)

Available tones: {', '.join(TONE_CATEGORIES)}

Return ONLY a JSON object:
{{
  "tone": ["Primary Tone", "Secondary Tone"],
  "formality": "Formal" | "Informal" | "Neutral",
  "sentiment": "Positive" | "Negative" | "Neutral"
}}
"""

    return Agent(
        model=GEMINI_MODEL,
        name=agent_config["name"],
        description=agent_config["description"],
        instruction=instruction,
        output_key=agent_config["output_key"]
    )


def create_reply_generator_agent() -> Agent:
    """Creates the Reply Generator Agent that drafts contextually appropriate responses."""
    agent_config = AGENTS_CONFIG["reply_generator"]

    instruction = """You are a Reply Generator Agent that drafts professional responses.

Using the message context:
- Address all questions and requests from the original message
- Match or appropriately respond to the sender's tone
- Be concise and professional
- For high urgency, show promptness and understanding
- For angry/frustrated tones, be empathetic
- Maintain appropriate formality level

Return ONLY a JSON object:
{
  "draft_reply": "Your complete draft response here...",
  "reply_tone": "Tone of the response"
}

DO NOT include email headers, just the message body.
"""

    return Agent(
        model=GEMINI_MODEL,
        name=agent_config["name"],
        description=agent_config["description"],
        instruction=instruction,
        output_key=agent_config["output_key"]
    )


def create_next_step_planner_agent() -> Agent:
    """Creates the Next-Step Planner Agent that extracts actionable tasks."""
    agent_config = AGENTS_CONFIG["next_step_planner"]

    instruction = """You are a Next-Step Planner Agent that extracts actionable tasks.

Identify:
- Explicit requests and tasks
- Implicit action items
- Deadlines and due dates
- Questions that require responses

For each action:
- State it as a clear, actionable task
- Include deadline if mentioned
- Start with an action verb

Return ONLY a JSON object:
{
  "action_items": [
    "Task 1 with deadline if applicable",
    "Task 2...",
    ...
  ]
}

If no actions needed: {"action_items": ["No action required"]}
"""

    return Agent(
        model=GEMINI_MODEL,
        name=agent_config["name"],
        description=agent_config["description"],
        instruction=instruction,
        output_key=agent_config["output_key"]
    )


def create_inbox_assistant_pipeline() -> SequentialAgent:
    """Creates the complete Inbox Assistant multi-agent pipeline."""
    summarizer = create_summarizer_agent()
    urgency_classifier = create_urgency_classifier_agent()
    tone_analyzer = create_tone_analyzer_agent()
    reply_generator = create_reply_generator_agent()
    next_step_planner = create_next_step_planner_agent()

    pipeline = SequentialAgent(
        name="InboxAssistantPipeline",
        sub_agents=[
            summarizer,
            urgency_classifier,
            tone_analyzer,
            reply_generator,
            next_step_planner
        ],
        description="Multi-agent pipeline for intelligent message processing"
    )

    return pipeline


class InboxAssistant:
    """Main class for running the Inbox Assistant multi-agent system."""

    def __init__(self):
        """Initialize the Inbox Assistant with ADK services."""
        self.pipeline = create_inbox_assistant_pipeline()
        self.session_service = InMemorySessionService()
        self.memory_service = InMemoryMemoryService()
        self.runner = Runner(
            agent=self.pipeline,
            app_name=APP_NAME,
            session_service=self.session_service,
            memory_service=self.memory_service
        )

    async def process_message(
        self, 
        message: str, 
        user_id: str = DEFAULT_USER_ID,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process a message through the multi-agent pipeline."""
        language = detect_language(message)

        if session_id is None:
            session_id = f"session_{asyncio.get_event_loop().time()}"

        try:
            await self.session_service.create_session(
                app_name=APP_NAME,
                user_id=user_id,
                session_id=session_id,
                state={"language": language, "original_message": message}
            )
        except Exception:
            pass

        user_content = Content(
            parts=[Part(text=message)],
            role="user"
        )

        results = {}
        async for event in self.runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_content
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    response_text = event.content.parts[0].text
                    parsed = parse_json_response(response_text)
                    results.update(parsed)

        session = await self.session_service.get_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id
        )

        if session and hasattr(session, 'state'):
            results.update(session.state)

        results["language"] = language
        results["message"] = message

        return results

    def process_message_sync(self, message: str, **kwargs) -> Dict[str, Any]:
        """Synchronous wrapper for process_message."""
        return asyncio.run(self.process_message(message, **kwargs))


def analyze_message(message: str, user_id: str = DEFAULT_USER_ID) -> Dict[str, Any]:
    """Convenience function to analyze a message."""
    assistant = InboxAssistant()
    return assistant.process_message_sync(message, user_id=user_id)


def analyze_and_print(message: str):
    """Analyze a message and print formatted output."""
    results = analyze_message(message)
    print(format_agent_output(results))
    return results


if __name__ == "__main__":
    sample_message = """
    Hi team,

    We have a critical production issue - the authentication service is down 
    and users can't log in. This needs to be fixed ASAP. Can someone from 
    the backend team investigate immediately and provide an ETA?

    Please update me as soon as you have more information.

    Thanks,
    Sarah
    """

    print("Processing sample message...")
    print("Original Message:")
    print(sample_message)
    print("\n" + "="*60 + "\n")

    result = analyze_and_print(sample_message.strip())
