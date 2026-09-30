from pathlib import Path

from fpdf import FPDF
from PIL import Image

from app.config import settings
from app.schemas import ComicPanel

# The built-in PDF fonts only support Latin-1. Gemini often returns curly
# quotes, long dashes, etc., which would otherwise crash the export.
_REPLACEMENTS = {
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2013": "-",
    "\u2014": "-",
    "\u2026": "...",
    "\u2022": "-",
    "\u00a0": " ",
}

IMAGE_BOX_WIDTH = 180.0
IMAGE_BOX_HEIGHT = 110.0


def _pdf_safe(text: object) -> str:
    value = str(text or "")

    for old, new in _REPLACEMENTS.items():
        value = value.replace(old, new)

    return value.encode("latin-1", "replace").decode("latin-1")


def _add_image(pdf: FPDF, image_path: Path) -> None:
    """Place the image at the cursor, keeping its aspect ratio."""

    with Image.open(image_path) as img:
        width_px, height_px = img.size

    scale = min(IMAGE_BOX_WIDTH / width_px, IMAGE_BOX_HEIGHT / height_px)
    width = width_px * scale
    height = height_px * scale

    x = (pdf.w - width) / 2
    y = pdf.get_y()

    pdf.image(str(image_path), x=x, y=y, w=width, h=height)
    pdf.set_y(y + height + 4)


def _add_section(pdf: FPDF, heading: str, body: str) -> None:
    if not body:
        return

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, heading, new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, _pdf_safe(body), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)


def save_pdf(
    title: str,
    panels: list[ComicPanel],
    filename: str,
) -> Path:
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in panels:
        pdf.add_page()

        pdf.set_font("Helvetica", "B", 18)
        pdf.multi_cell(
            0, 10, _pdf_safe(title[:100]), new_x="LMARGIN", new_y="NEXT"
        )

        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(
            0, 8, f"Panel {panel.panel_number}", new_x="LMARGIN", new_y="NEXT"
        )
        pdf.ln(2)

        image_path = Path(panel.image_path)

        if image_path.exists():
            _add_image(pdf, image_path)

        if panel.caption:
            pdf.set_font("Helvetica", "BI", 12)
            pdf.multi_cell(
                0, 7, _pdf_safe(panel.caption), new_x="LMARGIN", new_y="NEXT"
            )
            pdf.ln(2)

        _add_section(pdf, "Scene", panel.scene_description)
        _add_section(pdf, "Narration", panel.narration)
        _add_section(pdf, "Dialogue", panel.dialogue)

    # Never let a caller-supplied name escape the exports folder.
    output_path = settings.EXPORTS_DIR / Path(filename).name
    pdf.output(str(output_path))

    return output_path
