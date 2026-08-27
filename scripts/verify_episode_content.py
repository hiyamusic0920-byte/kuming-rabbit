#!/usr/bin/env python3
"""漫畫頁的 content-preservation 驗證。

重產 episode 頁之前先 snapshot，重產之後 compare。欄位分兩級，判定不一樣：

一、Immutable story content —— 漫畫本體。變動就是 FAIL。
  title          <h1> 文字
  progress       第 N / 15 話（話數順序）
  image_count    漫畫格數
  image_src      每一格的檔案路徑與順序
  story_text     作者後記 / 真實案例 / 解決方案 / 我學到什麼 / 關鍵能力 的純文字
  prev_next      上一話 / 下一話 的連結（結構順序）

二、Reviewable accessibility / navigation metadata —— 可以改，但要有人看過。
  image_alt      每一格的替代文字
  description    meta description
  related        往技術內容的連結

  這一級變動回報成 REVIEW，不是 FAIL：改善 alt 不等於「漫畫本體被破壞」。
  但它也不能無聲通過——alt 是讀螢幕的人唯一能拿到的畫面資訊，改了要有人確認
  新的描述真的在講那一格。

離開碼：0 = 全部相符或只有 REVIEW；1 = 有 FAIL。
加 --strict 時 REVIEW 也算失敗（重產外殼的例行檢查用這個）。

用法：
  python3 scripts/verify_episode_content.py snapshot before.json
  python3 scripts/verify_episode_content.py compare before.json [--strict]
"""

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [f"ep{n:02d}.html" for n in range(1, 16)] + [
    f"special{n:02d}.html" for n in range(1, 4)
]


class Extract(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.h1: list[str] = []
        self.in_h1 = False
        self.panels: list[tuple[str, str]] = []
        self.progress: list[str] = []
        self.in_progress = False
        self.story: list[str] = []
        self.story_depth = 0
        self.prev_next: list[tuple[str, str]] = []
        self._nav_href: str | None = None
        self._nav_text: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "")
        if tag == "h1":
            self.in_h1 = True
        elif tag == "img" and "comic-panel" in cls:
            self.panels.append((a.get("src", ""), a.get("alt", "")))
        elif tag == "p" and "episode-progress" in cls:
            self.in_progress = True
        elif tag == "div" and "portfolio-card-content" in cls:
            self.story_depth = 1
        elif self.story_depth:
            self.story_depth += 1
        elif tag == "a" and ("nav-previous" in cls or "nav-next" in cls):
            self._nav_href = a.get("href", "")
            self._nav_text = []

    def handle_endtag(self, tag):
        if tag == "h1":
            self.in_h1 = False
        elif tag == "p" and self.in_progress:
            self.in_progress = False
        elif self.story_depth:
            self.story_depth -= 1
        elif tag == "a" and self._nav_href is not None:
            self.prev_next.append((self._nav_href, "".join(self._nav_text).strip()))
            self._nav_href = None

    def handle_data(self, data):
        if self.in_h1:
            self.h1.append(data)
        if self.in_progress:
            self.progress.append(data)
        if self.story_depth:
            self.story.append(data)
        if self._nav_href is not None:
            self._nav_text.append(data)


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def snapshot_page(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    p = Extract()
    p.feed(raw)
    desc = re.search(r'<meta name="description" content="([^"]*)"', raw)
    return {
        "description": desc.group(1) if desc else "",
        # 一定要轉成 list：JSON 讀回來的是 list，tuple 跟 list 比會每頁都誤報
        "related": [list(t) for t in
                    re.findall(r'<li><a href="([^"]+)">([^<]*)<span>', raw)],
        "title": norm("".join(p.h1)),
        "progress": norm("".join(p.progress)),
        "image_count": len(p.panels),
        "image_src": [src for src, _ in p.panels],
        "image_alt": [alt for _, alt in p.panels],
        "story_text": norm("".join(p.story)),
        "prev_next": [[h, norm(t)] for h, t in p.prev_next],
    }


def snapshot() -> dict:
    return {rel: snapshot_page(ROOT / rel) for rel in PAGES if (ROOT / rel).exists()}


# 一級：漫畫本體，變了就是 FAIL
IMMUTABLE = ["title", "progress", "image_count", "image_src", "story_text", "prev_next"]
# 二級：無障礙 / 導覽 metadata，變了要人工 review
REVIEWABLE = ["image_alt", "description", "related"]


def compare(before: dict, strict: bool = False) -> int:
    after = snapshot()
    failures = 0
    reviews = 0
    for rel in PAGES:
        if rel not in before:
            print(f"NEW      {rel} （沒有 before 基準，跳過比對）")
            continue
        if rel not in after:
            print(f"MISSING  {rel} 重產後不存在")
            failures += 1
            continue
        broken = [f for f in IMMUTABLE
                  if before[rel].get(f) != after[rel].get(f)]
        changed = [f for f in REVIEWABLE
                   if f in before[rel] and before[rel].get(f) != after[rel].get(f)]
        if changed:
            reviews += 1
            print(f"REVIEW   {rel}: {', '.join(changed)} 有變動，需要人工確認")
            for f in changed:
                b, a = before[rel].get(f), after[rel].get(f)
                if f == "image_alt" and isinstance(b, list) and isinstance(a, list):
                    for i, (bb, aa) in enumerate(zip(b, a), start=1):
                        if bb != aa:
                            print(f"           第 {i} 格 alt：")
                            print(f"             before: {bb}")
                            print(f"             after : {aa}")
                    if len(b) != len(a):
                        print(f"           alt 數量 {len(b)} -> {len(a)}")
                else:
                    print(f"           before: {b}")
                    print(f"           after : {a}")
        if broken:
            failures += 1
            print(f"CHANGED  {rel}: {', '.join(broken)}")
            for f in broken:
                b, a = before[rel][f], after[rel][f]
                if f == "story_text":
                    # 只印差異開頭，整段太長
                    for i in range(min(len(str(b)), len(str(a)))):
                        if str(b)[i] != str(a)[i]:
                            print(f"           {f} 從第 {i} 字開始不同")
                            print(f"           before: …{str(b)[max(0,i-30):i+50]}")
                            print(f"           after : …{str(a)[max(0,i-30):i+50]}")
                            break
                    else:
                        print(f"           {f} 長度不同 {len(str(b))} -> {len(str(a))}")
                else:
                    print(f"           before: {b}")
                    print(f"           after : {a}")
        if not broken and not changed:
            print(f"OK       {rel}  {after[rel]['image_count']} 格")
    print(f"\n{len(after)} 頁：{failures} 頁漫畫本體有變動（FAIL）、"
          f"{reviews} 頁 alt/metadata 有變動（需人工 review）")
    if reviews and not failures:
        print("漫畫本體完好。alt / metadata 的變動請逐格確認新的描述是否符合畫面。")
    return 1 if (failures or (strict and reviews)) else 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "snapshot"
    args = [a for a in sys.argv[2:] if not a.startswith("--")]
    target = Path(args[0]) if args else Path("episode-snapshot.json")
    if mode == "snapshot":
        target.write_text(json.dumps(snapshot(), ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"snapshot -> {target} ({len(snapshot())} pages)")
    elif mode == "compare":
        raise SystemExit(compare(json.loads(target.read_text(encoding="utf-8")),
                                 strict="--strict" in sys.argv))
    else:
        raise SystemExit("usage: verify_episode_content.py [snapshot|compare] <file>")
