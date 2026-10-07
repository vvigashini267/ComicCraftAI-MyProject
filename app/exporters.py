from pathlib import Path
from typing import List

from PIL import Image


def clean_pdf_text(text: str) -> str:
    """
    Make text safe for PDF if needed.
    """
    replacements = {
        "—": "-",
        "–": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "…": "...",
        "\u00a0": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text.encode(
        "latin-1",
        "ignore",
    ).decode("latin-1")


def save_pdf(
    image_paths: List[Path],
    pdf_path: Path,
) -> Path:
    """
    Create a PDF containing all comic panel images.
    Each panel becomes one PDF page.
    """

    pdf_path = Path(pdf_path)

    pdf_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not image_paths:
        raise ValueError(
            "No comic images were provided."
        )

    images = []

    for image_path in image_paths:

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(
                f"Comic image not found: {image_path}"
            )

        image = Image.open(
            image_path
        ).convert("RGB")

        images.append(image)

    first_image = images[0]

    remaining_images = images[1:]

    first_image.save(
        pdf_path,
        "PDF",
        resolution=100.0,
        save_all=True,
        append_images=remaining_images,
    )

    return pdf_path
