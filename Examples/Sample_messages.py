"""
Sample messages for testing the Inbox Assistant
"""

SAMPLE_MESSAGES = {
    "urgent_technical": """
    URGENT: Production Database Down

    The main production database went offline 15 minutes ago. All customer 
    transactions are failing. This is impacting revenue and we're getting 
    hundreds of support tickets. Need immediate action from the DevOps team.

    Please escalate to VP Engineering if not resolved in 30 minutes.
    """,

    "medium_request": """
    Hi John,

    Hope you're doing well. I wanted to check if you could review the Q3 
    report by end of this week? It's for the board meeting next Tuesday, 
    so we need to finalize it soon.

    Let me know if you need any additional information.

    Best regards,
    Emily
    """,

    "low_informational": """
    FYI - Office Hours Update

    Just a heads up that our office hours will be changing next month to 
    9 AM - 6 PM instead of 8 AM - 5 PM. This affects parking access codes 
    which will be sent separately.

    No action needed from you.
    """,

    "angry_customer": """
    Subject: UNACCEPTABLE SERVICE!!!

    I have been waiting for THREE WEEKS for a response to my support ticket 
    #45678. This is absolutely unacceptable! I paid for premium support and 
    I'm getting NOTHING. I want a full refund and I'm going to post about 
    this terrible experience on social media.

    Fix this NOW or I'm canceling my subscription.
    """,

    "friendly_casual": """
    Hey! 😊

    Just wanted to say thanks for helping out with the presentation yesterday. 
    You totally saved me! The client loved it and we got the deal!!!

    Coffee's on me next time - let me know when you're free!

    Cheers,
    Mike
    """,

    "formal_business": """
    Dear Dr. Patterson,

    I am writing to request your participation as a keynote speaker at our 
    Annual Healthcare Innovation Summit on March 15-17, 2026. Your research 
    on AI in diagnostics would be invaluable to our audience of 500+ 
    healthcare professionals.

    We would be honored to offer an honorarium of $5,000 plus travel expenses.
    Would you be available for a brief call next week to discuss details?

    Respectfully yours,
    Dr. Jennifer Morrison
    Conference Chair
    """,

    "multilingual_spanish": """
    Hola María,

    Espero que estés bien. Quería recordarte sobre la reunión del proyecto 
    mañana a las 10 AM. Por favor, prepara el informe de progreso y trae 
    las actualizaciones del equipo.

    Nos vemos mañana!

    Saludos,
    Carlos
    """,

    "meeting_request": """
    Hi Sarah,

    Can we schedule a 30-minute sync this week to discuss the new marketing 
    campaign? I'd like to go over the budget allocation and timeline. 
    Thursday or Friday afternoon works best for me.

    Also, please bring the analytics from the last campaign so we can compare.

    Thanks!
    Alex
    """,

    "multiple_tasks": """
    Team Update - Action Items

    Following our standup:

    1. Jake - please deploy the hotfix to staging by EOD today
    2. Lisa - review and approve the PR #234 for the authentication update
    3. Tom - update the API documentation with the new endpoints
    4. Everyone - submit your time logs by Friday for payroll processing

    Let me know if there are any blockers.

    Thanks,
    Project Manager
    """,

    "appreciative_positive": """
    Hi Team,

    I just wanted to take a moment to thank everyone for the incredible work 
    on the product launch. We exceeded our targets by 150% and the client 
    feedback has been overwhelmingly positive.

    I'm genuinely impressed by the dedication and quality everyone brought 
    to this project. Well done!

    Warm regards,
    Sandra
    VP of Product
    """
}


MESSAGE_METADATA = {
    "urgent_technical": {
        "expected_urgency": "High",
        "expected_tone": ["Urgent", "Direct", "Professional"],
        "language": "en",
        "should_have_actions": True
    },
    "medium_request": {
        "expected_urgency": "Medium",
        "expected_tone": ["Polite", "Formal", "Friendly"],
        "language": "en",
        "should_have_actions": True
    },
    "low_informational": {
        "expected_urgency": "Low",
        "expected_tone": ["Neutral", "Informational"],
        "language": "en",
        "should_have_actions": False
    },
    "angry_customer": {
        "expected_urgency": "High",
        "expected_tone": ["Angry", "Direct", "Urgent"],
        "language": "en",
        "should_have_actions": True
    },
    "friendly_casual": {
        "expected_urgency": "Low",
        "expected_tone": ["Friendly", "Casual", "Appreciative"],
        "language": "en",
        "should_have_actions": False
    },
    "formal_business": {
        "expected_urgency": "Medium",
        "expected_tone": ["Formal", "Polite", "Professional"],
        "language": "en",
        "should_have_actions": True
    },
    "multilingual_spanish": {
        "expected_urgency": "Medium",
        "expected_tone": ["Friendly", "Professional"],
        "language": "es",
        "should_have_actions": True
    },
    "meeting_request": {
        "expected_urgency": "Medium",
        "expected_tone": ["Polite", "Professional"],
        "language": "en",
        "should_have_actions": True
    },
    "multiple_tasks": {
        "expected_urgency": "Medium",
        "expected_tone": ["Direct", "Professional"],
        "language": "en",
        "should_have_actions": True
    },
    "appreciative_positive": {
        "expected_urgency": "Low",
        "expected_tone": ["Appreciative", "Positive", "Professional"],
        "language": "en",
        "should_have_actions": False
    }
}


def get_sample_message(key: str) -> str:
    return SAMPLE_MESSAGES.get(key, "").strip()


def get_all_samples() -> dict:
    return SAMPLE_MESSAGES


def get_metadata(key: str) -> dict:
    return MESSAGE_METADATA.get(key, {})
