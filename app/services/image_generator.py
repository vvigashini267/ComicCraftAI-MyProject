from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def get_font(size):
    try:
        return ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            size
        )
    except Exception:
        return ImageFont.load_default()


def get_panel_number(filename):
    try:
        name = Path(filename).stem
        number = name.split("_")[-1]
        return int(number)
    except Exception:
        return 1


def draw_background(draw, width, height, night=False):
    if night:
        sky = (25, 35, 80)
        ground = (45, 90, 55)
    else:
        sky = (120, 190, 245)
        ground = (100, 190, 100)

    draw.rectangle(
        (0, 0, width, height),
        fill=sky
    )

    draw.rectangle(
        (0, 500, width, height),
        fill=ground
    )


def draw_sun(draw):
    draw.ellipse(
        (620, 50, 710, 140),
        fill=(255, 220, 40)
    )


def draw_moon(draw):
    draw.ellipse(
        (620, 50, 700, 130),
        fill=(245, 245, 220)
    )


def draw_tree(draw, x, y):
    draw.rectangle(
        (x, y, x + 35, y + 180),
        fill=(110, 70, 40)
    )

    draw.ellipse(
        (x - 50, y - 80, x + 90, y + 50),
        fill=(40, 130, 55)
    )

    draw.ellipse(
        (x - 25, y - 120, x + 110, y + 20),
        fill=(30, 110, 45)
    )


def draw_forest(draw):
    for x in [50, 180, 550, 680]:
        draw_tree(draw, x, 350)


def draw_house(draw):
    draw.rectangle(
        (250, 330, 520, 550),
        fill=(220, 170, 100),
        outline=(80, 50, 30),
        width=5
    )

    draw.polygon(
        [
            (220, 330),
            (385, 200),
            (550, 330)
        ],
        fill=(150, 50, 50),
        outline=(80, 30, 30)
    )

    draw.rectangle(
        (350, 420, 420, 550),
        fill=(90, 55, 35)
    )

    draw.rectangle(
        (285, 370, 340, 430),
        fill=(120, 200, 240),
        outline=(50, 50, 50),
        width=3
    )

    draw.rectangle(
        (430, 370, 485, 430),
        fill=(120, 200, 240),
        outline=(50, 50, 50),
        width=3
    )


def draw_library(draw):
    draw.rectangle(
        (170, 250, 600, 560),
        fill=(190, 145, 90),
        outline=(70, 40, 20),
        width=6
    )

    draw.polygon(
        [
            (140, 250),
            (385, 100),
            (630, 250)
        ],
        fill=(120, 70, 40),
        outline=(60, 30, 20)
    )

    for x in [200, 300, 400, 500]:
        draw.rectangle(
            (x, 290, x + 60, 520),
            fill=(80, 45, 30),
            outline=(40, 20, 10),
            width=3
        )

        for y in [310, 370, 430]:
            draw.rectangle(
                (x + 10, y, x + 50, y + 35),
                fill=(220, 80 + (x % 100), 70)
            )

    draw.rectangle(
        (340, 430, 430, 560),
        fill=(70, 45, 30)
    )


def draw_castle(draw):
    draw.rectangle(
        (230, 250, 540, 560),
        fill=(180, 180, 190),
        outline=(60, 60, 70),
        width=5
    )

    for x in [210, 330, 450]:
        draw.rectangle(
            (x, 170, x + 70, 300),
            fill=(160, 160, 175),
            outline=(60, 60, 70),
            width=5
        )

        draw.polygon(
            [
                (x, 170),
                (x + 35, 110),
                (x + 70, 170)
            ],
            fill=(120, 70, 150)
        )

    draw.rectangle(
        (345, 410, 425, 560),
        fill=(70, 50, 40)
    )


def draw_throne(draw):
    # Throne
    draw.rectangle(
        (300, 300, 470, 560),
        fill=(210, 160, 40),
        outline=(100, 60, 20),
        width=5
    )

    draw.rectangle(
        (270, 250, 500, 340),
        fill=(220, 170, 50),
        outline=(100, 60, 20),
        width=5
    )

    draw.ellipse(
        (335, 290, 435, 390),
        fill=(160, 30, 40)
    )

    # Pillars
    for x in [100, 620]:
        draw.rectangle(
            (x, 150, x + 50, 560),
            fill=(230, 190, 70)
        )

        draw.ellipse(
            (x - 10, 130, x + 60, 180),
            fill=(245, 210, 100)
        )


def draw_magic(draw):
    # Magical circles
    for radius in [60, 90, 120]:
        draw.ellipse(
            (
                385 - radius,
                350 - radius,
                385 + radius,
                350 + radius
            ),
            outline=(170, 80, 255),
            width=5
        )

    # Sparkles
    points = [
        (150, 180),
        (600, 220),
        (200, 420),
        (570, 450),
        (380, 150)
    ]

    for x, y in points:
        draw.line(
            (x - 15, y, x + 15, y),
            fill=(255, 240, 80),
            width=4
        )

        draw.line(
            (x, y - 15, x, y + 15),
            fill=(255, 240, 80),
            width=4
        )


def draw_character(draw, x, y):
    # Head
    draw.ellipse(
        (x - 35, y - 100, x + 35, y - 30),
        fill=(245, 190, 140),
        outline=(70, 50, 40),
        width=3
    )

    # Hair
    draw.pieslice(
        (x - 38, y - 110, x + 38, y - 35),
        180,
        360,
        fill=(45, 30, 20)
    )

    # Body
    draw.rectangle(
        (x - 40, y - 30, x + 40, y + 100),
        fill=(40, 90, 180),
        outline=(50, 50, 70),
        width=3
    )

    # Legs
    draw.rectangle(
        (x - 30, y + 100, x - 5, y + 180),
        fill=(40, 40, 50)
    )

    draw.rectangle(
        (x + 5, y + 100, x + 30, y + 180),
        fill=(40, 40, 50)
    )

    # Eyes
    draw.ellipse(
        (x - 20, y - 70, x - 10, y - 60),
        fill="black"
    )

    draw.ellipse(
        (x + 10, y - 70, x + 20, y - 60),
        fill="black"
    )


def draw_creature(draw):
    # Simple magical creature
    draw.ellipse(
        (290, 300, 480, 500),
        fill=(150, 80, 220),
        outline=(70, 30, 100),
        width=5
    )

    draw.ellipse(
        (330, 340, 355, 365),
        fill="white"
    )

    draw.ellipse(
        (415, 340, 440, 365),
        fill="white"
    )

    draw.ellipse(
        (340, 345, 350, 355),
        fill="black"
    )

    draw.ellipse(
        (425, 345, 435, 355),
        fill="black"
    )


def draw_panel_scene(draw, prompt, panel_number):
    text = prompt.lower()

    # Detect the scene from the Gemini image prompt
    if any(word in text for word in [
        "library",
        "book",
        "books",
        "reading"
    ]):
        draw_library(draw)

    elif any(word in text for word in [
        "throne",
        "palace",
        "imperial",
        "emperor",
        "royal"
    ]):
        draw_castle(draw)
        draw_throne(draw)

    elif any(word in text for word in [
        "village",
        "farmer",
        "house",
        "home"
    ]):
        draw_house(draw)

    elif any(word in text for word in [
        "forest",
        "woods",
        "tree",
        "jungle"
    ]):
        draw_forest(draw)

    else:
        # Different scene for each panel
        if panel_number == 1:
            draw_forest(draw)

        elif panel_number == 2:
            draw_library(draw)

        elif panel_number == 3:
            draw_magic(draw)
            draw_creature(draw)

        elif panel_number == 4:
            draw_castle(draw)

        else:
            draw_house(draw)

    # Character position changes in each panel
    positions = {
        1: (220, 420),
        2: (600, 420),
        3: (200, 420),
        4: (550, 420),
        5: (385, 400)
    }

    x, y = positions.get(
        panel_number,
        (385, 400)
    )

    draw_character(draw, x, y)


def create_comic_image(prompt, output_path, panel_number):

    width = 768
    height = 768

    image = Image.new(
        "RGB",
        (width, height),
        "white"
    )

    draw = ImageDraw.Draw(image)

    night = any(
        word in prompt.lower()
        for word in ["night", "dark", "moon", "midnight"]
    )

    draw_background(
        draw,
        width,
        height,
        night
    )

    if night:
        draw_moon(draw)
    else:
        draw_sun(draw)

    draw_panel_scene(
        draw,
        prompt,
        panel_number
    )

    # Title
    title_font = get_font(30)

    draw.text(
        (30, 25),
        f"ComicCraft AI - Panel {panel_number}",
        fill="black",
        font=title_font
    )

    # Caption
    caption_font = get_font(18)

    caption = prompt.replace(
        "\n",
        " "
    )[:95]

    draw.rectangle(
        (25, 640, 743, 735),
        fill="white",
        outline="black",
        width=3
    )

    draw.text(
        (40, 665),
        caption,
        fill="black",
        font=caption_font
    )

    # Border
    draw.rectangle(
        (5, 5, 763, 763),
        outline="black",
        width=8
    )

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    image.save(
        output_path
    )

    return output_path


def generate_image(prompt: str, filename: str):

    output_dir = Path(
        "generated"
    ) / "panels"

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = output_dir / filename

    panel_number = get_panel_number(
        filename
    )

    return create_comic_image(
        prompt,
        output_path,
        panel_number
    )
