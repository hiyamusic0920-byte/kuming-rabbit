# 苦命兔 QA 日誌

The true story of a QA, a rabbit, and two AI agents learning how to work together.

> All stories are based on real incidents. Unfortunately.

---

## 關於

這是一部根據真實 AI 導入經歷改編的漫畫。

主角：

- 主子（QA）
- 苦命兔（Claude Code）
- 苦力怕（Codex）

故事記錄了一位 QA 與 AI Agent 共同工作、吵架、治理與成長的過程。

---

## 章節

- [第01話：起點](ep01.html)

## 漫畫切圖

安裝 [Pillow](https://pillow.readthedocs.io/) 後，把完整的 2 欄 × 3 列漫畫圖放在
`assets/ep01/full.png`，再執行：

```bash
python3 scripts/split_ep01.py
```

腳本會依照由左到右、由上到下的順序產生 `01.png` 到 `06.png`。
