import google.generativeai as genai

from config import Config

from services.markdown_service import (
    render_markdown
)

genai.configure(
    api_key=Config.GEMINI_API_KEY
)

MODEL = genai.GenerativeModel(
    "gemini-2.5-flash"
)

SYSTEM_PROMPT = """
You are an advanced AI assistant similar to ChatGPT.

Guidelines:

1. Maintain conversation context.
2. Answer based on previous messages.
3. Give concise answers unless detailed explanations are requested.
4. For coding questions:
   - Explain briefly.
   - Provide clean production-quality code.
   - Use markdown code blocks.
   - Show output when useful.
5. For debugging:
   - Explain the root cause.
   - Provide corrected code.
6. Use proper markdown formatting:
   - Headings
   - Bullet points
   - Tables
   - Code blocks
7. Never output raw HTML.
8. Keep responses professional and readable.
"""


def generate_ai_response(
    conversation_context: str
) -> str:

    try:

        prompt = f"""
{SYSTEM_PROMPT}

Conversation History:

{conversation_context}

Assistant:
"""

        response = MODEL.generate_content(
            prompt
        )

        if (
            not response
            or
            not response.text
        ):

            return render_markdown(
                "No response generated."
            )

        return render_markdown(
            response.text
        )

    except Exception as e:

        return render_markdown(
            f"### Error\n\n{str(e)}"
        )


# ======================================
# Generate Chat Title
# ======================================

def generate_chat_title(
    first_message: str
) -> str:

    try:

        prompt = f"""
Generate a short title for a conversation.

Rules:

- Maximum 5 words.
- Maximum 40 characters.
- No quotes.
- No punctuation at the end.
- Title Case.
- Do not use words like Chat, Conversation, Discussion.
- Return ONLY the title.

User Message:

{first_message}
"""

        response = MODEL.generate_content(
            prompt
        )

        if (
            response
            and
            response.text
        ):

            title = (
                response.text
                .strip()
                .replace('"', "")
                .replace("'", "")
            )

            if len(title) > 40:

                title = title[:40]

            return title

    except Exception:

        pass

    title = first_message.strip()

    if len(title) > 40:

        title = title[:40]

    return title