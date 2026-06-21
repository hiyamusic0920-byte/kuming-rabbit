#!/usr/bin/env python3
"""Crop ep02-ep15 panels using per-episode measured frame coordinates."""

from pathlib import Path

from PIL import Image


ROOT_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT_DIR / "assets"
SHEET_GAP = 16

# Pillow boxes are (left, top, right, bottom); right and bottom are exclusive.
# Coordinates were measured independently from each full.jpg black panel frames.
EPISODE_CROPS: dict[int, list[tuple[int, int, int, int]]] = {
    2: [
        (10, 10, 575, 521), (582, 10, 1006, 521), (1014, 10, 1729, 521),
        (10, 528, 509, 899), (518, 528, 1018, 899), (1026, 528, 1729, 899),
        (10, 907, 1729, 1153),
    ],
    3: [
        (6, 44, 394, 344), (401, 44, 781, 344), (789, 44, 1225, 344),
        (6, 352, 344, 745), (352, 352, 866, 745), (874, 352, 1225, 745),
    ],
    4: [
        (5, 39, 749, 363), (757, 39, 1507, 363),
        (5, 370, 749, 681), (757, 370, 1507, 681),
        (5, 688, 749, 1033), (757, 688, 1507, 1033),
    ],
    5: [
        (11, 36, 755, 390), (761, 36, 1525, 390),
        (11, 429, 755, 696), (761, 397, 1525, 696),
        (11, 703, 755, 1002), (761, 703, 1525, 1002),
    ],
    6: [
        (9, 55, 764, 464), (770, 55, 1529, 464),
        (9, 471, 764, 959), (770, 471, 1529, 959),
    ],
    7: [
        (9, 42, 559, 501), (565, 42, 1015, 501), (1021, 42, 1527, 501),
        (9, 508, 634, 989), (640, 508, 1015, 989), (1021, 508, 1527, 989),
    ],
    8: [
        (6, 40, 510, 457), (518, 40, 973, 457), (980, 40, 1529, 457),
        (6, 464, 510, 954), (518, 464, 1007, 954), (1014, 464, 1529, 954),
    ],
    9: [
        (14, 59, 766, 514), (774, 59, 1521, 514),
        (14, 521, 766, 1002), (774, 521, 1521, 1002),
    ],
    10: [
        (14, 45, 716, 494), (723, 45, 1424, 494),
        (14, 501, 716, 938), (723, 501, 1424, 938),
    ],
    11: [
        (5, 3, 1434, 482),
        (5, 489, 508, 954), (514, 489, 991, 954), (997, 489, 1434, 954),
    ],
    12: [
        (12, 50, 762, 505), (772, 50, 1522, 505),
        (12, 512, 762, 988), (772, 512, 1522, 988),
    ],
    14: [
        (8, 9, 760, 504), (770, 9, 1527, 504),
        (8, 514, 760, 1009), (770, 514, 1527, 1009),
    ],
    15: [(9, 12, 1192, 946)],
}

# Panel indexes in visual reading rows for each contact sheet.
EPISODE_ROWS: dict[int, list[list[int]]] = {
    2: [[1, 2, 3], [4, 5, 6], [7]],
    3: [[1, 2, 3], [4, 5, 6]],
    4: [[1, 2], [3, 4], [5, 6]],
    5: [[1, 2], [3, 4], [5, 6]],
    6: [[1, 2], [3, 4]],
    7: [[1, 2, 3], [4, 5, 6]],
    8: [[1, 2, 3], [4, 5, 6]],
    9: [[1, 2], [3, 4]],
    10: [[1, 2], [3, 4]],
    11: [[1], [2, 3, 4]],
    12: [[1, 2], [3, 4]],
    13: [[1, 2], [3, 4], [5, 6], [7, 8]],
    14: [[1, 2], [3, 4]],
    15: [[1]],
}

# Episode 13 spans two source images with different dimensions and coordinates.
EPISODE_13_PAGES: list[
    tuple[str, list[tuple[int, int, int, int]]]
] = [
    (
        "full-1.jpg",
        [
            (16, 51, 713, 471), (722, 51, 1423, 471),
            (16, 481, 713, 915), (722, 481, 1423, 915),
        ],
    ),
    (
        "full-2.jpg",
        [
            (11, 45, 734, 494), (744, 45, 1522, 494),
            (11, 504, 734, 979), (744, 504, 1522, 979),
        ],
    ),
]


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


def split_episode(episode: int) -> list[Path]:
    episode_dir = ASSETS_DIR / f"ep{episode:02d}"
    source_path = episode_dir / "full.jpg"
    if not source_path.is_file():
        raise FileNotFoundError(f"Source image not found: {source_path}")

    output_paths: list[Path] = []
    with Image.open(source_path) as source:
        panels = []
        for panel_number, crop_box in enumerate(EPISODE_CROPS[episode], start=1):
            left, top, right, bottom = crop_box
            if not (0 <= left < right <= source.width and 0 <= top < bottom <= source.height):
                raise ValueError(f"ep{episode:02d} panel {panel_number}: invalid {crop_box}")
            panel = source.crop(crop_box)
            output_path = episode_dir / f"{panel_number:02d}.png"
            panel.save(output_path, "PNG")
            panels.append(panel)
            output_paths.append(output_path)

        sheet_path = episode_dir / "contact_sheet.png"
        create_contact_sheet(panels, EPISODE_ROWS[episode]).save(sheet_path, "PNG")
        output_paths.append(sheet_path)

    print(f"ep{episode:02d}: {len(panels)} panels")
    return output_paths


def split_episode_13() -> list[Path]:
    episode = 13
    episode_dir = ASSETS_DIR / "ep13"
    panels: list[Image.Image] = []
    output_paths: list[Path] = []

    for source_name, crop_boxes in EPISODE_13_PAGES:
        source_path = episode_dir / source_name
        if not source_path.is_file():
            raise FileNotFoundError(f"Source image not found: {source_path}")
        with Image.open(source_path) as source:
            for crop_box in crop_boxes:
                left, top, right, bottom = crop_box
                if not (
                    0 <= left < right <= source.width
                    and 0 <= top < bottom <= source.height
                ):
                    raise ValueError(f"ep13 invalid crop in {source_name}: {crop_box}")
                panel_number = len(panels) + 1
                panel = source.crop(crop_box)
                output_path = episode_dir / f"{panel_number:02d}.png"
                panel.save(output_path, "PNG")
                panels.append(panel)
                output_paths.append(output_path)

    sheet_path = episode_dir / "contact_sheet.png"
    create_contact_sheet(panels, EPISODE_ROWS[episode]).save(sheet_path, "PNG")
    output_paths.append(sheet_path)
    print(f"ep13: {len(panels)} panels")
    return output_paths


def main() -> None:
    for episode in range(2, 16):
        if episode == 13:
            split_episode_13()
        elif episode in EPISODE_CROPS:
            split_episode(episode)


if __name__ == "__main__":
    main()
