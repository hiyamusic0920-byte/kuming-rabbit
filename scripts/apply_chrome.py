#!/usr/bin/env python3
"""把 site_chrome.py 的 header / footer / 導覽 JS 注入各頁的標記區塊。

為什麼要這樣做：這個站沒有 build step，也沒有 include。要嘛 26 頁各自手改
（改一次 nav 要動 26 個檔，一定漂移），要嘛留標記讓腳本重寫。選後者。

用法：python3 scripts/apply_chrome.py [--check]
      --check 只檢查有沒有頁面的 chrome 跟單一來源不一致，不寫檔（CI 用）。
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import site_chrome as chrome  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

# 每一頁的 active nav key 與相對深度。epNN / specialNN 由 generator 自己處理。
PAGES = {
    "index.html": ("", 0),
    "ai-qa.html": ("ai-qa", 0),
    "architecture.html": ("ai-qa", 0),
    "case-studies.html": ("case-studies", 0),
    "lessons.html": ("lessons", 0),
    "diary.html": ("diary", 0),
    "about.html": ("about", 0),
    "portfolio/index.html": ("", 1),
    "portfolio/ai-qa-series-01.html": ("", 1),
    "portfolio/core06-rules-enforcement.html": ("ai-qa", 1),
}

BLOCK = re.compile(
    r"(<!-- CHROME:(HEADER|FOOTER|NAVJS) -->)(.*?)(<!-- /CHROME:\2 -->)",
    re.DOTALL,
)


def build(kind: str, active: str, depth: int) -> str:
    if kind == "HEADER":
        return chrome.header(active, depth)
    if kind == "FOOTER":
        return chrome.footer(depth)
    return chrome.nav_js()


def main() -> int:
    check_only = "--check" in sys.argv
    drift, written, missing = [], [], []

    for rel, (active, depth) in PAGES.items():
        path = ROOT / rel
        if not path.exists():
            missing.append(rel)
            continue
        src = path.read_text(encoding="utf-8")
        found = set()

        def replace(m: re.Match) -> str:
            kind = m.group(2)
            found.add(kind)
            body = build(kind, active, depth)
            if m.group(3).strip() != body.strip():
                drift.append(f"{rel}:{kind}")
            return f"{m.group(1)}\n{body}\n{m.group(4)}"

        out = BLOCK.sub(replace, src)
        for kind in ("HEADER", "FOOTER", "NAVJS"):
            if kind not in found:
                missing.append(f"{rel}: 缺少 CHROME:{kind} 標記")
        if out != src and not check_only:
            path.write_text(out, encoding="utf-8")
            written.append(rel)

    for item in missing:
        print(f"MISSING  {item}")
    for item in drift:
        print(f"{'DRIFT   ' if check_only else 'UPDATED '} {item}")
    if not check_only:
        print(f"{len(written)} file(s) rewritten: {', '.join(written) or '—'}")
    return 1 if (missing or (check_only and drift)) else 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
