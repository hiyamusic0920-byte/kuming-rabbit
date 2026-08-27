"""產生首頁精選漫畫的縮圖。

首頁只放縮圖，不放全尺寸漫畫格——單張漫畫 400~900KB，四張放進首屏會拖慢載入，
而且視覺上會把整頁語氣拉回漫畫網站。

用法：python3 scripts/make_thumbs.py
輸出：assets/thumbs/<episode>.webp（480x360，4:3 置中裁切）
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "thumbs"
SIZE = (480, 360)          # 4:3，CSS 端用 aspect-ratio 保留版位避免跳版
EPISODES = ["ep01", "ep07", "ep11", "ep15"]


def crop_4x3(im: Image.Image) -> Image.Image:
    """置中裁成 4:3。漫畫格比例差異很大（550x459 到 1429x479），統一比例才能對齊。"""
    target = SIZE[0] / SIZE[1]
    w, h = im.size
    if w / h > target:
        new_w = int(h * target)
        left = (w - new_w) // 2
        box = (left, 0, left + new_w, h)
    else:
        new_h = int(w / target)
        top = (h - new_h) // 2
        box = (0, top, w, top + new_h)
    return im.crop(box)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for ep in EPISODES:
        src = ROOT / "assets" / ep / "01.png"
        im = Image.open(src).convert("RGB")
        thumb = crop_4x3(im).resize(SIZE, Image.LANCZOS)
        dst = OUT / f"{ep}.webp"
        thumb.save(dst, "WEBP", quality=82, method=6)
        print(f"{dst.relative_to(ROOT)}  {dst.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
