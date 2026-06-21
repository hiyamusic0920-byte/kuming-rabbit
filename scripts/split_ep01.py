#!/usr/bin/env python3
"""Crop episode 01 panels using measured black-frame coordinates."""

from pathlib import Path

from PIL import Image

ROOT_DIR = Path(__file__).resolve().parents[1]
EPISODE_DIR = ROOT_DIR / "assets" / "ep01"
SOURCE_IMAGE = EPISODE_DIR / "full.jpg"
CONTACT_SHEET = EPISODE_DIR / "contact_sheet.png"

# Pillow crop boxes use (left, top, right, bottom); right and bottom are exclusive.
# These coordinates follow each panel's outer black frame in full.jpg (2008x1346).
PANEL_CROPS = {
    1: (14, 21, 812, 554),
    2: (823, 21, 2000, 554),
    3: (15, 566, 978, 946),
    4: (989, 566, 2000, 946),
    5: (16, 955, 928, 1339),
    6: (940, 956, 2000, 1339),
}

SHEET_GAP = 16


def create_contact_sheet(panels: list[Image.Image]) -> Image.Image:
    rows = [panels[index : index + 2] for index in range(0, 6, 2)]
    column_widths = [
        max(row[column].width for row in rows) for column in range(2)
    ]
    row_heights = [max(panel.height for panel in row) for row in rows]
    sheet_width = sum(column_widths) + SHEET_GAP
    sheet_height = sum(row_heights) + SHEET_GAP * 2
    sheet = Image.new("RGB", (sheet_width, sheet_height), "black")

    y = 0
    for row, row_height in zip(rows, row_heights):
        x = 0
        for column, panel in enumerate(row):
            offset_x = (column_widths[column] - panel.width) // 2
            offset_y = (row_height - panel.height) // 2
            sheet.paste(panel, (x + offset_x, y + offset_y))
            x += column_widths[column] + SHEET_GAP
        y += row_height + SHEET_GAP

    return sheet


def split_image() -> None:
    if not SOURCE_IMAGE.is_file():
        raise FileNotFoundError(f"Source image not found: {SOURCE_IMAGE}")

    with Image.open(SOURCE_IMAGE) as image:
        panels = []
        for panel_number, crop_box in PANEL_CROPS.items():
            output_path = EPISODE_DIR / f"{panel_number:02d}.png"
            panel = image.crop(crop_box)
            panel.save(output_path, "PNG")
            panels.append(panel)
            print(f"Created {output_path.relative_to(ROOT_DIR)} from {crop_box}")

        contact_sheet = create_contact_sheet(panels)
        contact_sheet.save(CONTACT_SHEET, "PNG")
        print(f"Created {CONTACT_SHEET.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    split_image()
