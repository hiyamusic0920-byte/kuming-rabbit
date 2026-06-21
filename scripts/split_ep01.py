#!/usr/bin/env python3
"""Split episode 01's 2x3 source image into six panels."""

from pathlib import Path

from PIL import Image

ROOT_DIR = Path(__file__).resolve().parents[1]
EPISODE_DIR = ROOT_DIR / "assets" / "ep01"
SOURCE_IMAGE = EPISODE_DIR / "full.jpg"


def split_image() -> None:
    if not SOURCE_IMAGE.is_file():
        raise FileNotFoundError(f"Source image not found: {SOURCE_IMAGE}")

    with Image.open(SOURCE_IMAGE) as image:
        panel_number = 1
        for row in range(3):
            top = image.height * row // 3
            bottom = image.height * (row + 1) // 3
            for column in range(2):
                left = image.width * column // 2
                right = image.width * (column + 1) // 2
                output_path = EPISODE_DIR / f"{panel_number:02d}.png"
                image.crop((left, top, right, bottom)).save(output_path, "PNG")
                print(f"Created {output_path.relative_to(ROOT_DIR)}")
                panel_number += 1


if __name__ == "__main__":
    split_image()
