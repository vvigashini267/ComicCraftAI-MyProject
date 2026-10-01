from dataclasses import dataclass
from pathlib import Path
from typing import Callable
from uuid import uuid4

from app.config import settings
from app.exporters import save_pdf
from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.layout_builder import build_comic_layout
from app.schemas import ComicPanel, PromptRequest
from app.services.image_generator import generate_image


@dataclass
class ComicResult:
    title: str
    panels: list[ComicPanel]
    pdf_filename: str
    pdf_path: Path


def build_comic(
    request: PromptRequest,
    on_progress: Callable[[str], None] | None = None,
) -> ComicResult:
    """Run the full outline -> story -> images -> PDF pipeline."""

    def progress(message: str) -> None:
        if on_progress:
            on_progress(message)

    progress("Generating story outline...")
    outline = generate_outline(request)

    progress("Writing the story...")
    story = generate_story(request, outline)

    story_panels = sorted(story.panels, key=lambda p: p.panel_number)
    story_panels = story_panels[: settings.MAX_PANELS]

    if not story_panels:
        raise RuntimeError("The AI did not return any panels. Please try again.")

    progress("Generating comic images...")
    image_paths = []

    for panel in story_panels:
        filename = f"panel_{panel.panel_number}_{uuid4().hex[:8]}.png"
        image_paths.append(generate_image(panel.image_prompt, filename))

    progress("Building comic layout...")
    comic_panels = build_comic_layout(story_panels, image_paths)

    progress("Creating PDF...")
    pdf_filename = f"comic_{uuid4().hex[:10]}.pdf"
    pdf_path = save_pdf(story.title, comic_panels, pdf_filename)

    return ComicResult(
        title=story.title,
        panels=comic_panels,
        pdf_filename=pdf_filename,
        pdf_path=pdf_path,
    )
