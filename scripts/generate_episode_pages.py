#!/usr/bin/env python3
"""Generate the comic index and episode HTML pages from assets directories."""

import re
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
PANEL_PATTERN = re.compile(r"^(\d+)\.png$")

EPISODE_TITLES = {
    1: "起點，讓AI幫我做測試報告",
    2: "報告有了，但看完更想哭",
    3: "拯救苦命兔大作戰",
    4: "苦力怕（Codex）登場！跨 Agent 合作挑戰",
    5: "我只是叫苦命兔測一張票，牠卻寫了 200 個 E2E……",
    6: "苦命兔超努力，無效的那種",
    7: "那隻兔子只是聞到怪味道，就順手把整個房間都打掃了",
    8: "那隻兔子，自從被我罵過一次後……",
    9: "因為苦命兔，我不得不重新檢視工作流程",
    10: "失之毫里，差之千里",
    11: "辯論大賽！苦命兔 VS 苦力怕",
    12: "苦命兔的秘密小本本",
    13: "那隻兔子就像渣男",
    14: "臭兔子！你又偷偷改家規！",
    15: "吃你的狗食！",
}


def episode_title(episode: int) -> str:
    return f"第{episode:02d}話：{EPISODE_TITLES[episode]}"


def panel_paths(asset_name: str) -> list[Path]:
    directory = ROOT_DIR / "assets" / asset_name
    panels = [path for path in directory.iterdir() if PANEL_PATTERN.fullmatch(path.name)]
    return sorted(panels, key=lambda path: int(path.stem))


def render_episode(filename: str, asset_name: str, title: str) -> None:
    panels = panel_paths(asset_name)
    if panels:
        image_lines = []
        for index, panel in enumerate(panels, start=1):
            lazy = "" if index == 1 else ' loading="lazy"'
            image_lines.append(
                f'    <img class="comic-panel" src="assets/{asset_name}/{panel.name}" '
                f'alt="{title}第{index}格"{lazy}>'
            )
        content = "\n".join(image_lines)
    else:
        content = '    <p class="empty-state">圖片準備中。</p>'

    html = f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body class="comic-page">
  <header class="comic-header">
    <a href="index.html">← 回目錄</a>
    <h1>{title}</h1>
  </header>
  <main class="comic-content" aria-label="{title}漫畫內容">
{content}
  </main>
</body>
</html>
"""
    (ROOT_DIR / filename).write_text(html, encoding="utf-8")
    print(f"Created {filename}: {len(panels)} panel(s)")


def render_index() -> None:
    regular_items = "\n".join(
        f'        <li><a href="ep{episode:02d}.html">{episode_title(episode)}</a></li>'
        for episode in range(1, 16)
    )
    special_items = "\n".join(
        f'        <li><a href="special{episode:02d}.html">特別篇 {episode:02d}</a></li>'
        for episode in range(1, 4)
    )
    html = f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>苦命兔 QA 日誌</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body class="home-page">
  <main class="home-shell">
    <h1>苦命兔 QA 日誌</h1>
    <p class="subtitle">一位 QA、一隻兔子，以及兩個 AI Agent 的真實故事。</p>
    <nav aria-labelledby="episodes-title">
      <h2 id="episodes-title">目錄</h2>
      <ul class="episode-list">
{regular_items}
      </ul>
      <h2>特別篇</h2>
      <ul class="episode-list">
{special_items}
      </ul>
    </nav>
  </main>
</body>
</html>
"""
    (ROOT_DIR / "index.html").write_text(html, encoding="utf-8")
    print("Created index.html")


def main() -> None:
    for episode in range(1, 16):
        render_episode(
            f"ep{episode:02d}.html",
            f"ep{episode:02d}",
            episode_title(episode),
        )
    for episode in range(1, 4):
        render_episode(
            f"special{episode:02d}.html",
            f"special{episode:02d}",
            f"特別篇 {episode:02d}",
        )
    render_index()


if __name__ == "__main__":
    main()
