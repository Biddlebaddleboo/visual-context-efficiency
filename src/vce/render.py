from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .fonts import resolve_font

PATCH_SIZE = 32


@dataclass(frozen=True)
class RenderConfig:
    font_id: str = "jetbrains-mono"
    font_size_px: int = 14
    line_gap_px: int = 1
    margin_px: int = 1
    min_patch_columns: int = 3
    max_patch_columns: int = 80
    max_aspect_ratio: float | None = 2.0
    patch_token_multiplier: float = 1.2


@dataclass(frozen=True)
class RenderResult:
    path: str
    width: int
    height: int
    patch_columns: int
    patch_rows: int
    patches: int
    estimated_image_tokens: float
    image_sha256: str
    font_sha256: str
    line_height_px: int
    line_count: int
    config: dict


def _text_width(font: ImageFont.FreeTypeFont, text: str) -> int:
    return math.ceil(font.getlength(text))


def _wrap_paragraph(font: ImageFont.FreeTypeFont, paragraph: str, max_width: int) -> list[str]:
    words = paragraph.split()
    if not words:
        return [""]
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if _text_width(font, candidate) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def wrap_text(font: ImageFont.FreeTypeFont, text: str, max_width: int) -> list[str]:
    lines: list[str] = []
    paragraphs = text.split("\n")
    for i, paragraph in enumerate(paragraphs):
        lines.extend(_wrap_paragraph(font, paragraph, max_width))
        if i != len(paragraphs) - 1 and paragraph == "":
            lines.append("")
    return lines or [""]


def _line_height(font: ImageFont.FreeTypeFont) -> int:
    # A stable representative box that includes ascenders and descenders.
    box = font.getbbox("Agjpqy|", anchor="lt")
    return max(1, math.ceil(box[3] - box[1]))


def _layout(font: ImageFont.FreeTypeFont, text: str, cfg: RenderConfig) -> tuple[list[str], int, int, int]:
    line_height = _line_height(font)
    candidates: list[tuple[int, float, int, list[str], int, int]] = []
    fallback: list[tuple[int, float, int, list[str], int, int]] = []

    for target_cols in range(cfg.min_patch_columns, cfg.max_patch_columns + 1):
        max_text_width = max(1, target_cols * PATCH_SIZE - 2 * cfg.margin_px)
        lines = wrap_text(font, text, max_text_width)
        width = max((_text_width(font, line) for line in lines), default=1) + 2 * cfg.margin_px
        height = (
            2 * cfg.margin_px
            + len(lines) * line_height
            + max(0, len(lines) - 1) * cfg.line_gap_px
        )
        cols = math.ceil(width / PATCH_SIZE)
        rows = math.ceil(height / PATCH_SIZE)
        patches = cols * rows
        ratio = max(width / max(height, 1), height / max(width, 1))
        square_penalty = abs(math.log(max(width, 1) / max(height, 1)))
        item = (patches, square_penalty, width * height, lines, width, height)
        fallback.append(item)
        if cfg.max_aspect_ratio is None or ratio <= cfg.max_aspect_ratio:
            candidates.append(item)

    pool = candidates or fallback
    patches, _, _, lines, width, height = min(pool, key=lambda x: (x[0], x[1], x[2]))
    return lines, width, height, line_height


def render_instruction(text: str, output: Path, cfg: RenderConfig) -> RenderResult:
    font_path, font_meta = resolve_font(cfg.font_id)
    font = ImageFont.truetype(str(font_path), cfg.font_size_px)
    lines, width, height, line_height = _layout(font, text, cfg)

    image = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(image)
    y = cfg.margin_px
    for line in lines:
        draw.text((cfg.margin_px, y), line, font=font, fill=0, anchor="lt")
        y += line_height + cfg.line_gap_px

    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, format="PNG", optimize=True)
    data = output.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    cols = math.ceil(width / PATCH_SIZE)
    rows = math.ceil(height / PATCH_SIZE)
    patches = cols * rows

    return RenderResult(
        path=str(output),
        width=width,
        height=height,
        patch_columns=cols,
        patch_rows=rows,
        patches=patches,
        estimated_image_tokens=patches * cfg.patch_token_multiplier,
        image_sha256=digest,
        font_sha256=font_meta["sha256"],
        line_height_px=line_height,
        line_count=len(lines),
        config=asdict(cfg),
    )
