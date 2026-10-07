import json

from google import genai

from app.config import settings
from app.schemas import OutlineResponse


def _get_client():
    if not settings.GEMINI_API_KEY:
        raise RuntimeError(
            "Gemini API is not configured. Please add GEMINI_API_KEY to your .env file."
        )

    return genai.Client(api_key=settings.GEMINI_API_KEY)


def _generate(prompt: str) -> str:
    client = _get_client()

    response = client.models.generate_content(
        model=settings.GEMINI_OUTLINE_MODEL,
        contents=prompt,
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return response.text


def generate_outline(user_request):
    prompt = f"""
Create a 5-panel comic story outline.

Story idea:
{user_request.prompt}

Main character:
{user_request.character_name}

Setting:
{user_request.setting}

Tone:
{user_request.tone}

Art style:
{user_request.art_style}

Create exactly 5 panels.

Return ONLY valid JSON in this format:

{{
    "title": "Comic title",
    "panels": [
        {{
            "panel_number": 1,
            "scene": "Description of the scene",
            "action": "What happens in this panel"
        }},
        {{
            "panel_number": 2,
            "scene": "Description of the scene",
            "action": "What happens in this panel"
        }},
        {{
            "panel_number": 3,
            "scene": "Description of the scene",
            "action": "What happens in this panel"
        }},
        {{
            "panel_number": 4,
            "scene": "Description of the scene",
            "action": "What happens in this panel"
        }},
        {{
            "panel_number": 5,
            "scene": "Description of the scene",
            "action": "What happens in this panel"
        }}
    ]
}}
"""

    result = _generate(prompt)

    try:
        data = json.loads(result)
    except json.JSONDecodeError:
        start = result.find("{")
        end = result.rfind("}")

        if start == -1 or end == -1:
            raise RuntimeError("Gemini did not return valid JSON.")

        data = json.loads(result[start:end + 1])

    return OutlineResponse(**data)
