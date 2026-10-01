from app.config import settings
from app.gemini_common import generate_structured
from app.schemas import OutlineResponse, PromptRequest, StoryResponse


def generate_story(
    request: PromptRequest,
    outline: OutlineResponse,
) -> StoryResponse:
    outline_text = "\n".join(
        f"Panel {panel.panel_number}: "
        f"Scene: {panel.scene} | Action: {panel.action}"
        for panel in outline.panels
    )

    prompt = f"""
You are the detailed story writer for ComicCraft.

Create the complete {settings.MAX_PANELS}-panel comic story using the outline below.

Original user request:
{request.prompt}

Character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Comic title:
{outline.title}

Outline:
{outline_text}

Requirements:
- Create exactly {settings.MAX_PANELS} panels.
- Preserve the same character and story continuity.
- Give every panel a detailed scene description.
- Give every panel a short caption.
- Give every panel narration suitable for a comic.
- Give dialogue only when it naturally fits the scene.
- Create a detailed image-generation prompt for every panel.
- The image prompt must describe characters, environment, action,
  lighting, composition, and requested art style.
- Do not change the main character's identity between panels.
"""

    return generate_structured(
        settings.GEMINI_STORY_MODEL,
        prompt,
        StoryResponse,
    )
