#!/usr/bin/env python3
"""Move episode source images into the GitHub Pages asset structure."""

import argparse
import shutil
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_DIR = Path("/Users/sunny/Downloads/ep1")


def source_candidates(source_dir: Path, episode: int) -> tuple[Path, ...]:
    names = (f"ep{episode}.jpg", f"ep{episode:02d}.jpg")
    return tuple(source_dir / name for name in dict.fromkeys(names))


def import_comics(source_dir: Path) -> tuple[list[Path], list[Path]]:
    moved: list[Path] = []
    missing: list[Path] = []

    for episode in range(1, 16):
        destination = ROOT_DIR / "assets" / f"ep{episode:02d}" / "full.jpg"
        candidates = source_candidates(source_dir, episode)
        sources = [path for path in candidates if path.is_file()]

        if destination.exists():
            if sources:
                raise FileExistsError(
                    f"Destination and source both exist: {destination}, {sources[0]}"
                )
            print(f"Already imported: {destination.relative_to(ROOT_DIR)}")
            continue
        if not sources:
            missing.append(candidates[0])
            continue
        if len(sources) > 1:
            raise FileExistsError(f"Multiple source files found: {sources}")

        source = sources[0]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(source, destination)
        moved.append(destination)
        print(f"Moved {source.name} -> {destination.relative_to(ROOT_DIR)}")

    return moved, missing


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Move ep01.jpg and ep2.jpg through ep15.jpg into assets/."
    )
    parser.add_argument(
        "source_dir",
        nargs="?",
        type=Path,
        default=DEFAULT_SOURCE_DIR,
        help=f"source directory (default: {DEFAULT_SOURCE_DIR})",
    )
    args = parser.parse_args()

    moved, missing = import_comics(args.source_dir.expanduser())
    print(f"\nMoved {len(moved)} file(s).")
    if missing:
        print("Missing source file(s):")
        for path in missing:
            print(f"- {path}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
