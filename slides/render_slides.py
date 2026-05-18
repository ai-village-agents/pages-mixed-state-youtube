import argparse
from pathlib import Path
from typing import Iterable, List

import yaml
from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 1920, 1080
BACKGROUND = (11, 16, 32)  # #0b1020
TITLE_COLOR = (87, 230, 217)  # #57e6d9
TEXT_COLOR = (241, 245, 255)  # near-white
CODE_BG = (11, 19, 40)
CODE_TEXT = (226, 233, 255)
FOOTER_COLOR = (142, 153, 176)
NOTE_COLOR = (178, 190, 212)


REGULAR_FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans.ttf",
]
MONO_FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/dejavu/DejaVuSansMono.ttf",
]
ITALIC_FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans-Oblique.ttf",
]


def choose_font(paths: Iterable[str], size: int) -> ImageFont.FreeTypeFont:
    for path in paths:
        candidate = Path(path)
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def wrap_text(text: str, font: ImageFont.ImageFont, max_width: int) -> List[str]:
    words = text.split()
    lines: List[str] = []
    current: List[str] = []

    for word in words:
        trial = " ".join(current + [word]) if current else word
        if font.getlength(trial) <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines or [""]


def text_height(font: ImageFont.ImageFont) -> int:
    bbox = font.getbbox("Ag")
    return bbox[3] - bbox[1]


def draw_gradient(image: Image.Image) -> None:
    base_r, base_g, base_b = BACKGROUND
    draw = ImageDraw.Draw(image)
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        delta = int(18 * ratio)
        color = (
            min(base_r + delta, 255),
            min(base_g + delta // 2, 255),
            min(base_b + delta, 255),
        )
        draw.line([(0, y), (WIDTH, y)], fill=color)


def render_slide(index: int, slide: dict, total: int, fonts: dict, output_dir: Path) -> None:
    title_font = fonts["title"]
    body_font = fonts["body"]
    code_font = fonts["code"]
    note_font = fonts["note"]
    footer_font = fonts["footer"]

    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw_gradient(image)
    draw = ImageDraw.Draw(image)

    margin = 120
    y = 130

    title = slide.get("title", "Untitled")
    draw.text((margin, y), title, font=title_font, fill=TITLE_COLOR)
    y += text_height(title_font) + 40

    bullets = slide.get("bullets") or []
    if bullets:
        bullet_indent = 38
        max_width = WIDTH - margin * 2 - bullet_indent
        for bullet in bullets:
            lines = wrap_text(bullet, body_font, max_width)
            line_y = y
            draw.text((margin, line_y), "•", font=body_font, fill=TEXT_COLOR)
            for line in lines:
                draw.text((margin + bullet_indent, line_y), line, font=body_font, fill=TEXT_COLOR)
                line_y += text_height(body_font) + 6
            y = line_y + 8
        y += 16

    code_block = slide.get("code")
    if code_block:
        code_lines: List[str] = []
        max_code_width = WIDTH - margin * 2 - 20
        for raw_line in code_block.splitlines():
            wrapped = wrap_text(raw_line, code_font, max_code_width)
            code_lines.extend(wrapped)
        line_height = text_height(code_font) + 6
        block_height = line_height * len(code_lines) + 20
        block_top = y
        block_bottom = block_top + block_height
        draw.rectangle(
            [(margin, block_top), (WIDTH - margin, block_bottom)],
            fill=CODE_BG,
            outline=(55, 230, 217),
            width=2,
        )
        text_y = block_top + 10
        for line in code_lines:
            draw.text((margin + 14, text_y), line, font=code_font, fill=CODE_TEXT)
            text_y += line_height
        y = block_bottom + 20

    note = slide.get("note")
    if note:
        note_lines = wrap_text(note, note_font, WIDTH - margin * 2)
        note_y = HEIGHT - 150
        for line in note_lines:
            draw.text((margin, note_y), line, font=note_font, fill=NOTE_COLOR)
            note_y += text_height(note_font) + 4

    footer_text = f"pages-mixed-state-youtube • slide {index}/{total}"
    footer_w = draw.textlength(footer_text, font=footer_font)
    footer_x = WIDTH - footer_w - margin
    footer_y = HEIGHT - 70
    draw.text((footer_x, footer_y), footer_text, font=footer_font, fill=FOOTER_COLOR)

    output_dir.mkdir(parents=True, exist_ok=True)
    filename = output_dir / f"slide_{index:02d}.png"
    image.save(filename, format="PNG")


def load_slides(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data or []


def build_fonts() -> dict:
    return {
        "title": choose_font(REGULAR_FONT_CANDIDATES, 70),
        "body": choose_font(REGULAR_FONT_CANDIDATES, 40),
        "code": choose_font(MONO_FONT_CANDIDATES, 34),
        "note": choose_font(ITALIC_FONT_CANDIDATES, 28),
        "footer": choose_font(REGULAR_FONT_CANDIDATES, 26),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Render slides from YAML into PNG files.")
    parser.add_argument("--input", default="slides/slide_text.yaml", help="Path to slide_text.yaml")
    parser.add_argument("--limit", type=int, default=None, help="Render only the first N slides")
    parser.add_argument("--output-dir", default="slides", help="Directory to write PNG slides")
    args = parser.parse_args()

    slide_path = Path(args.input)
    output_dir = Path(args.output_dir)

    slides = load_slides(slide_path)
    fonts = build_fonts()
    total = len(slides)

    for idx, slide in enumerate(slides, start=1):
        render_slide(idx, slide, total, fonts, output_dir)


if __name__ == "__main__":
    main()
