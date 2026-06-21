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

PORTFOLIO_SECTIONS = [
    ("🐰 作者後記", True),
    ("🔥 真實案例", False),
    ("🛠 解決方案", False),
    ("💡 我學到什麼", False),
    ("🏷 關鍵能力", False),
]

EPISODE_PORTFOLIO_CONTENT = {
    1: {
        "🐰 作者後記": """<p>當一個 QA 做久了，很容易發現一件事：</p>
          <p>真正花時間的，往往不是測試本身。</p>
          <p>而是測試之後的整理工作。</p>
          <p>截圖、整理步驟、彙整結果、撰寫報告……</p>
          <p>這些工作雖然重要，但總讓我覺得有點重複。</p>
          <p>於是某一天，我開始想：</p>
          <p>如果 AI 能夠理解我的測試結果，是不是有機會幫我完成這些事情？</p>
          <p>這就是苦命兔的起點。</p>""",
        "🔥 真實案例": """<h3>當時遇到的問題</h3>
          <h4>測試報告整理成本高</h4>
          <p>每完成一張票，通常都需要：</p>
          <ul>
            <li>整理測試範圍</li>
            <li>截圖留存證據</li>
            <li>記錄測試結果</li>
            <li>撰寫測試報告</li>
            <li>整理風險與觀察</li>
          </ul>
          <p>這些工作雖然必要，但會消耗大量時間。</p>
          <p>而這些時間，原本可以用在更有價值的事情上：</p>
          <ul>
            <li>理解需求</li>
            <li>探索風險</li>
            <li>設計測試策略</li>
          </ul>""",
        "🛠 解決方案": """<h3>我嘗試的解法</h3>
          <p>我開始嘗試讓 AI 協助產生測試報告。</p>
          <p>最初的想法其實很單純：</p>
          <div class="workflow-flow" aria-label="測試報告產生流程">
            <span>輸入一張票</span><span aria-hidden="true">↓</span>
            <span>執行測試</span><span aria-hidden="true">↓</span>
            <span>AI 產出測試報告</span>
          </div>
          <p>如果可行的話，理論上就能大幅降低報告整理成本。</p>
          <p>於是，苦命兔正式上工。</p>
          <h3>結果</h3>
          <p>第一版真的成功產出了測試報告。</p>
          <p>那一刻其實滿震撼的。</p>
          <p>因為原本覺得有點科幻的事情，竟然真的發生了。</p>
          <p>不過我很快發現：</p>
          <p>能產出報告，不代表能產出「好的報告」。</p>
          <p>而這也成為第二話的開始。</p>""",
        "💡 我學到什麼": """<p>當時的我以為：</p>
          <p>只要把工作交給 AI，AI 就會幫我完成。</p>
          <p>後來才發現：</p>
          <p>真正困難的不是產生結果。</p>
          <p>而是讓 AI 理解脈絡。</p>
          <p>而這個問題，正是後面整個苦命兔系列不斷在面對的核心課題。</p>""",
    }
}


def episode_title(episode: int) -> str:
    return f"第{episode:02d}話：{EPISODE_TITLES[episode]}"


def panel_paths(asset_name: str) -> list[Path]:
    directory = ROOT_DIR / "assets" / asset_name
    panels = [path for path in directory.iterdir() if PANEL_PATTERN.fullmatch(path.name)]
    return sorted(panels, key=lambda path: int(path.stem))


def render_navigation(episode: int) -> str:
    previous = (
        f'<a class="nav-link nav-previous" href="ep{episode - 1:02d}.html">'
        f'← 第{episode - 1:02d}話</a>'
        if episode > 1
        else '<span class="nav-placeholder" aria-hidden="true"></span>'
    )
    following = (
        f'<a class="nav-link nav-next" href="ep{episode + 1:02d}.html">'
        f'第{episode + 1:02d}話 →</a>'
        if episode < 15
        else '<span class="nav-placeholder" aria-hidden="true"></span>'
    )
    return f"""    <nav class="episode-nav" aria-label="漫畫話數導覽">
      {previous}
      <a class="nav-link nav-index" href="index.html">回目錄</a>
      {following}
    </nav>"""


def render_portfolio_framework(episode: int) -> str:
    cards = []
    episode_content = EPISODE_PORTFOLIO_CONTENT.get(episode, {})
    for title, expanded in PORTFOLIO_SECTIONS:
        open_attribute = " open" if expanded else ""
        card_content = episode_content.get(title, "<p>（待補內容）</p>")
        cards.append(
            f"""      <details class="portfolio-card"{open_attribute}>
        <summary>{title}</summary>
        <div class="portfolio-card-content">
          {card_content}
        </div>
      </details>"""
        )
    return """    <section class="portfolio-content" aria-label="AI QA Portfolio 內容">
      <h2>AI QA Portfolio</h2>
{}
    </section>""".format("\n".join(cards))


def render_episode(
    filename: str,
    asset_name: str,
    title: str,
    progress: str | None = None,
    episode_number: int | None = None,
) -> None:
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

    progress_html = f'\n    <p class="episode-progress">{progress}</p>' if progress else ""
    navigation_html = (
        f"\n{render_navigation(episode_number)}" if episode_number is not None else ""
    )
    portfolio_html = (
        f"\n{render_portfolio_framework(episode_number)}"
        if episode_number is not None
        else ""
    )
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
    <h1>{title}</h1>{progress_html}
  </header>
  <main class="comic-content" aria-label="{title}漫畫內容">
{content}{navigation_html}{portfolio_html}
  </main>
</body>
</html>
"""
    (ROOT_DIR / filename).write_text(html, encoding="utf-8")
    print(f"Created {filename}: {len(panels)} panel(s)")


def render_index() -> None:
    regular_items = "\n".join(
        f"""        <li>
          <a href="ep{episode:02d}.html">
            <span class="episode-title">{episode_title(episode)}</span>
            <span class="episode-capability"><strong>能力：</strong>（待補）</span>
          </a>
        </li>"""
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
    <a class="about-link" href="about.html">關於這個 AI QA Portfolio</a>
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


def render_about() -> None:
    html = """<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>關於｜苦命兔 QA 日誌</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body class="home-page">
  <main class="home-shell about-shell">
    <a class="about-back-link" href="index.html">← 回目錄</a>
    <h1>苦命兔 QA 日誌</h1>
    <p>這是一個記錄 QA 與 AI Agent 協作演化過程的作品集。</p>
    <p>內容包含：</p>
    <ul>
      <li>漫畫</li>
      <li>真實案例</li>
      <li>AI QA 方法論</li>
      <li>工作流程演化</li>
      <li>Agent 治理實驗</li>
    </ul>
  </main>
</body>
</html>
"""
    (ROOT_DIR / "about.html").write_text(html, encoding="utf-8")
    print("Created about.html")


def main() -> None:
    for episode in range(1, 16):
        render_episode(
            f"ep{episode:02d}.html",
            f"ep{episode:02d}",
            episode_title(episode),
            f"第 {episode} / 15 話",
            episode,
        )
    for episode in range(1, 4):
        render_episode(
            f"special{episode:02d}.html",
            f"special{episode:02d}",
            f"特別篇 {episode:02d}",
        )
    render_index()
    render_about()


if __name__ == "__main__":
    main()
