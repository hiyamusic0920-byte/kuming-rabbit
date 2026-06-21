#!/usr/bin/env python3
"""Crop special episode panels using measured frame coordinates."""

from pathlib import Path

from PIL import Image


ROOT_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT_DIR / "assets"
SHEET_GAP = 16

# Pillow boxes are (left, top, right, bottom); right and bottom are exclusive.
SPECIAL_CROPS: dict[str, list[tuple[int, int, int, int]]] = {
    "special01": [
        (14, 43, 763, 379), (772, 43, 1523, 379),
        (14, 388, 763, 688), (772, 388, 1523, 688),
        (14, 697, 763, 1010), (772, 697, 1523, 1010),
    ],
    "special02": [
        (10, 8, 536, 552), (542, 8, 1140, 552), (1146, 8, 1642, 552),
        (10, 560, 536, 1038), (542, 560, 1030, 1038),
        (1038, 560, 1642, 1038),
    ],
}

SPECIAL_ROWS = {
    "special01": [[1, 2], [3, 4], [5, 6]],
    "special02": [[1, 2, 3], [4, 5, 6]],
}


def create_contact_sheet(
    panels: list[Image.Image], rows: list[list[int]]
) -> Image.Image:
    row_widths = [
        sum(panels[index - 1].width for index in row) + SHEET_GAP * (len(row) - 1)
        for row in rows
    ]
    row_heights = [max(panels[index - 1].height for index in row) for row in rows]
    sheet = Image.new(
        "RGB",
        (max(row_widths), sum(row_heights) + SHEET_GAP * (len(rows) - 1)),
        "black",
    )
    y = 0
    for row, row_width, row_height in zip(rows, row_widths, row_heights):
        x = (sheet.width - row_width) // 2
        for index in row:
            panel = panels[index - 1]
            sheet.paste(panel, (x, y + (row_height - panel.height) // 2))
            x += panel.width + SHEET_GAP
        y += row_height + SHEET_GAP
    return sheet


def split_special(name: str) -> None:
    directory = ASSETS_DIR / name
    source_path = directory / "full.jpg"
    if not source_path.is_file():
        raise FileNotFoundError(f"Source image not found: {source_path}")

    panels = []
    with Image.open(source_path) as source:
        for panel_number, crop_box in enumerate(SPECIAL_CROPS[name], start=1):
            panel = source.crop(crop_box)
            panel.save(directory / f"{panel_number:02d}.png", "PNG")
            panels.append(panel)
    create_contact_sheet(panels, SPECIAL_ROWS[name]).save(
        directory / "contact_sheet.png", "PNG"
    )
    print(f"{name}: {len(panels)} panels")


def main() -> None:
    for name in SPECIAL_CROPS:
        split_special(name)


if __name__ == "__main__":
    main()
