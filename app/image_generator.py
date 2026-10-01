
from pathlib import Path
from PIL import Image, ImageDraw

from app.config import settings


def generate_image(prompt: str, output_path=None, *args, **kwargs):
    """Generate a placeholder comic illustration.

    This keeps the comic pipeline working when no image API is configured.
    It does not generate AI artwork.
    """
    settings.PANELS_DIR.mkdir(parents=True, exist_ok=True)

    if output_path is None:
        output_path = (
            settings.PANELS_DIR
            / f"panel_{abs(hash(prompt)) % 1000000}.png"
        )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    image = Image.new(
        "RGB",
        (settings.IMAGE_WIDTH, settings.IMAGE_HEIGHT),
        "#f4e8d0",
    )
    draw = ImageDraw.Draw(image)

    draw.rectangle(
        (20, 20, settings.IMAGE_WIDTH - 20, settings.IMAGE_HEIGHT - 20),
        outline="#333333",
        width=5,
    )

    draw.text(
        (40, 40),
        "ComicCraft - Comic Panel",
        fill="#222222",
    )

    max_chars = 45
    words = prompt.split()
    lines = []
    current_line = ""

    for word in words:
        candidate = (
            f"{current_line} {word}".strip()
        )
        if len(candidate) > max_chars:
            if current_line:
                lines.append(current_line)
            current_line = word
        else:
            current_line = candidate

    if current_line:
        lines.append(current_line)

    y = 100
    for line in lines[:12]:
        draw.text((40, y), line, fill="#222222")
        y += 30

    image.save(output_path)
    return str(output_path)
