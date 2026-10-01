
from pathlib import Path

from PIL import Image, ImageDraw
from app.config import settings


def generate_image(prompt: str, filename: str) -> str:
    """Create a placeholder comic panel and return its file path."""

    # Ensure the output directory exists
    settings.PANELS_DIR.mkdir(parents=True, exist_ok=True)

    # Use the filename supplied by pipeline.py
    output_path = settings.PANELS_DIR / Path(filename).name

    # Create a placeholder image
    width = settings.IMAGE_WIDTH
    height = settings.IMAGE_HEIGHT

    image = Image.new("RGB", (width, height), "#f4e8d0")
    draw = ImageDraw.Draw(image)

    # Draw the comic panel border
    draw.rectangle(
        (10, 10, width - 10, height - 10),
        outline="#333333",
        width=4,
    )

    draw.text((30, 30), "ComicCraft AI", fill="#222222")
    draw.text((30, 65), "Comic Panel", fill="#222222")

    # Wrap the prompt into readable lines
    words = prompt.split()
    lines = []
    current_line = ""
    max_chars = 45

    for word in words:
        candidate = f"{current_line} {word}".strip()

        if len(candidate) > max_chars and current_line:
            lines.append(current_line)
            current_line = word
        else:
            current_line = candidate

    if current_line:
        lines.append(current_line)

    y = 120
    for line in lines[:15]:
        draw.text((30, y), line, fill="#222222")
        y += 28

    # Save the image
    image.save(output_path)

    return str(output_path)
