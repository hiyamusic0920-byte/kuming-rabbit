# 🐰 苦命兔 Kuming Rabbit — AI QA Lab

一個 QA 把兩個 AI agent 放進真實測試流程的實驗紀錄。包含跑得起來的部分，也包含翻車的部分。

線上：https://hiyamusic0920-byte.github.io/kuming-rabbit/

主角：主子（QA）、苦命兔（Claude Code）、苦力怕（Codex）。

---

## 網站結構

| 頁面 | 內容 |
| --- | --- |
| `index.html` | 首頁。AI QA Lab 入口，七個區段。 |
| `ai-qa.html` | Overview / Workflow / Architecture / Governance / Knowledge・Evaluation。 |
| `case-studies.html` | 三個有實際紀錄的案例。Problem → Approach → Evidence → Learning。 |
| `lessons.html` | Things AI Got Wrong 完整版。Failure → Mechanism → Learning。 |
| `diary.html` | 18 話索引（正篇 15 + 特別篇 3），可按能力面向篩選。 |
| `about.html` | 關於我、關於這個網站、這個網站怎麼做的。 |
| `architecture.html` | 漫畫設定與真實系統的對照表。 |
| `ep01`–`ep15`, `special01`–`special03` | 漫畫本體。由腳本產生。 |
| `portfolio/` | 早期的技術長文，走長文版面。 |

Episode 的網址不會變動（`ep01.html` 這種形式保留），舊連結不會壞。

---

## 技術

靜態 HTML + 一份 `styles.css`，放在 GitHub Pages。沒有框架，沒有 build step。

### 共用版面只有一份來源

沒有 build step 也就沒有 include，所以 header / footer / 導覽 JS 由腳本注入頁面裡的標記區塊：

```
<!-- CHROME:HEADER -->  ...  <!-- /CHROME:HEADER -->
```

改導覽只要改 `scripts/site_chrome.py`，然後：

```bash
python3 scripts/apply_chrome.py          # 寫回各頁
python3 scripts/apply_chrome.py --check  # 只檢查有沒有頁面跑掉（不寫檔）
```

### 漫畫頁由腳本產生，本體有保護

18 頁漫畫由 `scripts/generate_episode_pages.py` 從 `assets/` 目錄產生，不手改。
重產之前一定要先 snapshot、之後一定要比對：

```bash
python3 scripts/verify_episode_content.py snapshot validation/episode-snapshot-before.json
python3 scripts/generate_episode_pages.py
python3 scripts/verify_episode_content.py compare validation/episode-snapshot-before.json --strict
```

比對欄位分兩級，判定不一樣。

**一、Immutable story content —— 漫畫本體。變動就是 FAIL。**

| 欄位 | 內容 |
| --- | --- |
| `title` | 話數標題 |
| `progress` | 第 N / 15 話（話數順序） |
| `image_count` | 格數 |
| `image_src` | 每一格的檔案路徑與順序 |
| `story_text` | 作者後記 / 真實案例 / 解決方案 / 我學到什麼 / 關鍵能力 |
| `prev_next` | 上一話 / 下一話（結構順序） |

**二、Reviewable accessibility / navigation metadata —— 可以改，但要有人看過。**

| 欄位 | 內容 |
| --- | --- |
| `image_alt` | 每一格的替代文字 |
| `description` | meta description |
| `related` | 往技術內容的連結 |

第二級變動回報成 `REVIEW` 而不是 `FAIL`，離開碼是 0。理由：**改善 alt 不等於漫畫本體被破壞。**
目前 124 個 alt 還是「第 N 格」這種位置描述，這是已知的無障礙債，未來一定要改；
如果 alt 被歸進第一級，任何改善都會被驗證擋下來。

但它也不會無聲通過——alt 是讀螢幕的人唯一能拿到的畫面資訊，改了會逐格印出前後對照，
要有人確認新的描述真的在講那一格。重產外殼的例行檢查請加 `--strict`，
這時候 `REVIEW` 也算失敗，確保只有「刻意改 alt」的那一次才會看到它。

外殼（header / footer / 版面 wrapper）不在比對範圍，隨便改。

> 這支驗證不是裝飾。它抓到過一次真的：特別篇 03 的圖檔命名是 `full-N.jpg`，
> 而 generator 當時只認 `NN.png`——照舊重跑會把那四張圖換成「圖片準備中」。

### 其他腳本

| 腳本 | 用途 |
| --- | --- |
| `scripts/site_chrome.py` | header / footer / meta 的單一來源 |
| `scripts/apply_chrome.py` | 把 chrome 注入各頁 |
| `scripts/generate_episode_pages.py` | 產生 18 頁漫畫與 `diary.html` |
| `scripts/verify_episode_content.py` | 漫畫本體 content-preservation 驗證 |
| `scripts/make_thumbs.py` | 首頁縮圖（480×360 WebP） |
| `scripts/import_comics.py`, `split_*.py` | 匯入與切格 |

`data/episodes.json` 是話數、能力分類、以及每一話往技術內容的出口連結的來源。

---

## 作者

Sunny · QA Engineer / AI Native QA Explorer
