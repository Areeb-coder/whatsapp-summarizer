import os
from google.genai import Client


def summarize_chat(messages):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "❌ Gemini API key not found. Please set GEMINI_API_KEY."

    # Initialize client at runtime (NOT at import time)
    client = Client(api_key=api_key)

    if not messages:
        return "No valid messages found in the chat."

    text = " ".join(
        m["message"]
        for m in messages
        if isinstance(m, dict) and m.get("message")
    )

    # Safety cap
    text = text[:12000]

    prompt = (
        "Summarize the following WhatsApp group chat.\n"
        "Focus on main topics, announcements, and overall tone.\n\n"
        f"{text}"
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text
