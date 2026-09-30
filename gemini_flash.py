from app.config import settings
from app.gemini_common import generate_structured
from app.schemas import OutlineResponse, PromptRequest


def generate_outline(request: PromptRequest) -> OutlineResponse:
    prompt = f"""
You are the story-outline generator for ComicCraft.

Create a personalized comic based on the user's request.

User story:
{request.prompt}

Character name:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Requirements:
- Create exactly {settings.MAX_PANELS} panels.
- Give the comic a clear title.
- Each panel must have a concise scene description.
- Each panel must describe the main action.
- Maintain character and story continuity from panel 1 to panel {settings.MAX_PANELS}.
- The story should have a beginning, development, and ending.
"""

    return generate_structured(
        settings.GEMINI_OUTLINE_MODEL,
        prompt,
        OutlineResponse,
    )
