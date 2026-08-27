# AI QA 內容架構評審（Architecture Review, Round 2）

日期：2026-08-23
角色：Repo-aware Technical Editor + Senior SDET Content Architect
前一輪：`docs/AI_QA_CONTENT_REASSESSMENT.md`（不覆蓋、不取代，本文件只做 challenge 與架構決定）
本輪範圍：架構評審。沒有寫文章、沒有改網站、沒有改檔名、沒有改 numbering、沒有改 my-playwright 任何一行實作

驗證方法：所有成熟度判定都用**可重跑的量測**得出，不採信文件自述。量測指令與原始數字列在第 10 節附錄。

---

## 1. Executive Verdict

### 1.1 仍然成立的判斷

| 上一輪判斷 | 本輪驗證結果 |
|---|---|
| 已發布文章的 `/jira-tc` 那段（AI Mirror + Requirement Audit）已廢止 | ✅ 成立。`QA_THOUGHT_COLLECTOR_GUIDE.md` 標 deprecated 2026-06-15，早於文章發布 8 天 |
| repo 重心已從「把票測完」移到「怎麼相信 AI 說測完了」 | ✅ 成立，而且比我上一輪講的更硬。機制誕生時間線是三段式而非兩段式（見第 2 節） |
| 兩篇完稿躺著未上架 | ✅ 成立 |
| flaky / eval / CI-CD 三條紅線 | ✅ 全部成立，且 eval 比我上一輪寫的更弱 |
| `report-verifier` 沒被任何規則引用 | ✅ 成立。全 repo 除了它自己的定義檔，只出現在一份 2026-07-07 討論紀錄裡。**零規則引用、零命令引用** |

### 1.2 要推翻的判斷（我上一輪錯了或講太滿）

**推翻一：「先 observe failure，再 enforce」不是這個 repo 的通用 pattern。**

我上一輪在 S07 寫了「讓失敗可見要先於強制擋下（trace taxonomy 的漸進策略）」，並暗示它是一條設計原則。實際查證：這條策略**只有一個案例**（2026-07-08 的 `process_reuse_miss`），而且那份討論紀錄自己就寫著「Trace taxonomy 只能讓失敗可見，不能單獨強制 Reuse Audit；強制 gate 仍需另案設計」。n=1，而且是「做不到強制才退而求其次做觀測」，不是「刻意先觀測再強制」。把它抽成核心原則是過度概括。

真正反覆出現的 pattern 是另一條，證據更強（見第 2.3 節）。

**推翻二：「傳統自動化沒有 provenance 問題，因為執行者只有 CI」——這句過度絕對，收回。**

repo evidence 支持的是使用者提出的版本：provenance 不是 AI 才有的問題，但被 AI 放大。放大的具體機制在 `scripts/ledger.py` 的註解裡寫得很清楚：**同一份證據檔有四個異質寫入者**（pytest 的 conftest、`qa_probe` 的 ad-hoc API 實測、evidence board server 的人工標記、以及人直接標），沒有鎖會互相覆蓋。傳統 CI 的證據只有一個寫入者、一條路徑；這裡的執行者會自己換工具（curl / playwright-cli / pytest），而且人與 AI 混在同一份帳上。放大的是**歸屬**與**寫入競爭**，不是 traceability 本身。

**推翻三：「先把 `report-verifier` 接進 checkpoint，S04 就能寫成閉環」——這個推理方向是錯的。**

上一輪我把它列成「投入產出比最高的一項實作」，理由是文章比較好寫。這是為文章改系統，順序顛倒。本輪重新從 QA 需求評估，結論是**應該接，但不該無條件強制**，理由與代價列在第 8 節，且與文章無關。

**推翻四：S04 的中心不該是 Evidence Board 或 `report-verifier`。**

接受 review。實測數字支持這個修正：9 份報告、279 個步驟，`actual` 欄的罐頭字（「如預期」）比例是 **0%**——即使 `conftest` 的預設 fallback 至今仍是「如預期」。也就是說「證據等級紀律」這件事**已經被實際遵守**（Observed），而 `report-verifier` 這個工具**還沒被接上**（未 Integrated）。文章要寫已經在運作的那個，不是寫還沒接上的工具。

**推翻五：10 + 2 篇單一 Series 的架構不成立。**

理由不是篇數太多，而是**成熟度混在一起**。同一條 Series 裡混著「CI 每次 push 都在跑」與「只有 1 份實例的框架」，讀者無法分辨哪些是這套系統真的在跑的、哪些是實驗。單一 Series 的隱含承諾是「這些是同一套系統的連續章節」，而 repo 現實不是。

### 1.3 最大的架構改變

**從「一條 10 篇 Series」改成「7 篇 Core Series + 一個 Lab Notes 區（內含 Retrospective 與 Field Note 兩種標籤）」。**

Core Series 的收錄門檻是**成熟度**，不是題材好壞：只有達到「Integrated 且有實際使用證據」的機制才能當一篇 Core 文章的主軸。達不到的題材不是刪掉，而是移到 Lab Notes 並在文章開頭明說它的成熟度。

這個門檻直接產生四個移動：回歸集移出 Core、chat AI eval 移出 Core、採用率 1/26 移出 Core、AI 自主性量測整篇不寫。

---

## 2. System Evolution Thesis

### 2.1 命題

> 一開始是在 engineering「怎麼讓 AI 做 QA」，後來變成 engineering「怎麼觀察、限制、驗證 AI 做 QA」。

### 2.2 驗證：成立，但是三段不是兩段

用「機制首次進 repo 的 commit 日期」排出時間線（這是最不會騙人的證據，因為它是 git 而不是文件自述）：

```
2026-05-22  PROJECT_RULES.md              ← 規則以 prose 形式存在
2026-05-29  validate_report_data.py       ← 第一個機械化 gate（產 PDF 前必驗 schema）
2026-06-07  build_evidence_board.py       ← 證據集中
2026-06-17  audit_python_index.py         ← 程式入口稽核
2026-06-25  docs/tickets/_executors.json  ← 「誰測的」開始入帳
────────────────────────────────────────── 以上：把執行產物變成可檢查的東西
2026-07-07  lint_test_rules.py + lint_baseline.json
2026-07-07  .github/workflows/qa-audit.yml
2026-07-07  hooks（SessionStart / PostToolUse / Stop）
2026-07-07  .claude/agents/（reuse-audit、report-verifier）
2026-07-07  PERMISSION_BASELINE（allowlist 125 → 42）
2026-07-13  AGENT_DOCTRINE.md             ← 不能機械化的部分才蒸餾成判斷準則
2026-07-17  ledger.py + qa_probe.py       ← 執行本身開始留帳
────────────────────────────────────────── 以上：把「規則靠自律」換成「規則靠機械」
2026-08-18  Shared Change Review Gate（含 OW-4945 事後判例）
2026-08-19  上線前回歸集（未合併分支，8/19 建、8/20-21 實跑兩輪）
────────────────────────────────────────── 以上：治理開始有判例，把關對象從單票變成一版
```

三段可以命名為：**產物可檢查（5-6 月）→ 規則可強制（7 月）→ 治理可援引判例、把關從單票變成整版（8 月）**。

命題成立。但要修正一個關鍵前提。

### 2.3 修正：不是「AI 做 QA」被解決了，所以才轉向 assurance

這個修正很重要，否則整個 series 的敘事會變成一個假的成功故事。

實測數字：

| 指標 | 數字 | 意思 |
|---|---|---|
| `_executors.json` 入帳票數 | 42 | 有記錄執行者的票 |
| 其中 AI 執行 | **15（36%）** | 六成四的票仍然是人測的 |
| `eval_trace` 的 `human_manual_test` 事件 | 36 | 人工測試是常態不是例外 |
| 回歸集兩輪實跑的 executor 欄 | **Sunny Hsieh（人）** | 這套自動化回歸集是人在跑 |
| `ai_run_completed` vs `ai_fallback_to_human`（全期） | 24 vs 18 | 交給 AI 的執行，接近四成最後回到人手上 |

所以正確的敘事不是「執行解決了，於是往上走做治理」，而是：

> **執行始終沒有被完全交出去。工程重心之所以移到 assurance，正是因為執行不可靠——不可靠的東西唯一能管的方式，是讓它可觀測、可歸屬、有邊界。**

這個版本比命題原文更難聽，但它是 repo 支持的版本，而且對 Senior 讀者更有說服力：沒有人相信「我把 QA 交給 AI 就沒事了」，但每個人都相信「我沒辦法完全信它，所以我做了這些」。

### 2.4 反覆出現的真 pattern（可以抽成核心原則）

不是「先觀測再強制」。是這條，而且有一句 repo 原文可以直接引用（`AI_MANAGEMENT_DISCUSSION_20260707_HARNESS_ENGINEERING_AUDIT.md`）：

> **能用程式驗證的，就不要靠模型自律。prose 規則只有在被機械化 gate（lint / hook / CI / schema 驗證）背書時才真正可靠。**

同一份文件還有一句把代價講得更精準的：

> 目前的規則遵循率取決於「每個 agent 每次都讀懂並記得 409 行規則」；改善後取決於「lint / hook / CI 有沒有跑」——後者是確定的。

完整的 pattern 有四拍，而且四拍都能在時間線上指出對應物：

```
1. prose 規則寫下來                          （5/22 PROJECT_RULES）
2. 出現具體反例事故                          （OW-4696 測了沒入帳、OW-3712/4017 registry 沒回補）
3. 把「能用程式驗證的部分」機械化              （7/07 lint + hook + CI）
4. 剩下不能機械化的部分，蒸餾成判斷準則        （7/13 AGENT_DOCTRINE）
```

第 4 拍的順序是這條 pattern 最有價值的部分，而且是時間線證明的、不是我推論的：**AGENT_DOCTRINE 比 lint/CI/hooks 晚 6 天出生**。也就是「判斷力層」不是起點而是殘差——先把能自動檢查的抽走，剩下的才寫成給人和 AI 讀的準則。這解釋了為什麼 doctrine 全篇是「判準 + 正反例 + checklist」而不是原則宣示：它處理的本來就是機械檢查不了的那些。

第 3 拍還有一個誠實的附帶條件必須寫進文章，否則就是造假：**機械化不等於溯及既往**。`lint_baseline.json` grandfathered 了 **62 條既有違規**（R001 佔 56 條），也就是「test 檔不能出現 `.locator()`」這條硬規則，**只對新寫的 code 生效**。這是 ratchet（棘輪）設計，正確且務實，但不能寫成「規則從此不可能違反」。

---

## 3. Evidence Maturity Model

四級定義（依 review 採用）：

| 級 | 定義 | 判定方式 |
|---|---|---|
| **1 Implemented** | 程式 / skill / rule / artifact 存在 | 檔案存在 |
| **2 Integrated** | 被主 workflow 引用，不靠人記得手動叫 | 在 PROJECT_RULES / SOP / command 中被指名 |
| **3 Enforced** | 不遵守會被 hook / lint / CI / gate 擋住 | 有可執行的檢查，且該檢查真的在跑 |
| **4 Observed / Adopted** | 實際 ticket / execution 有使用證據 | artifact 數量、事件計數、報告內容 |

判定原則：**任一級不成立就不得往上宣稱**。這是把 doctrine 的「宣稱層級不得高於驗證層級」套用到自己的內容盤點上。

### 3.1 主要機制逐項判定

| 機制 | 1 Impl | 2 Integ | 3 Enforced | 4 Observed | 到頂級數 | 證據 |
|---|---|---|---|---|---|---|
| **CI 靜態稽核（4 關）** | ✅ | ✅ | ✅ | ✅ | **4** | `gh run list`：8 筆最近執行全 success，11-23 秒，push 與 pull_request 都觸發 |
| **executor 入帳 manifest** | ✅ | ✅ | ✅ | ✅ | **4** | Stop hook 檢查未入帳；`_executors.json` 42 票 / 15 AI |
| **report schema 驗證** | ✅ | ✅ | ✅ | ✅ | **4** | `render_report.py` 內建驗證；CI 第 4 關驗已提交 JSON |
| **`actual` 欄真值紀律** | ✅ | ✅ | ⚠️ 部分 | ✅ | **4（但 3 弱）** | 279 步驟罐頭字 **0%**；但 `conftest` 預設 fallback 仍是「如預期」，沒有任何 gate 擋罐頭字 |
| **hooks（3 個）** | ✅ | ✅ | ✅ | ✅ | **4** | 本 session 的 SessionStart 輸出即為證據 |
| **Assurance checkpoint（人工關卡）** | ✅ | ✅ | ❌ 機械不可能 | ✅ | **4（3 永不成立）** | `eval_trace`：`human_report_review` 6、`human_delegate_to_ai` 27；`review_status` 欄位 |
| **qa-thought-capture** | ✅ | ✅ | ❌（設計上不該強制） | ⚠️ 量少 | **4（量薄）** | 校準 log 只有 2 批（OW-4834、OW-4836）；`QA_HEURISTICS` 48 行、約 5 條；`knowledge_captured` 39 筆 |
| **知識 pipeline（4 段）** | ✅ | ✅ | ❌ | ⚠️ n=1 | **4（n=1）** | 完整走完一輪（《專案設定》發布、inbox 清空）；目前 inbox 有 `orders.md` 在途 |
| **Reuse Audit** | ✅ | ✅ 硬規則 | ❌ **無 artifact 可查** | ⚠️ 只觀測到違規 | **2** | PROJECT_RULES 寫「未完成不得開 playwright-cli」，但產出只是對話裡的表格，沒有落檔；`process_reuse_miss` 3 筆記錄的全是違規 |
| **execution ledger（`ledger.py`）** | ✅ | ⚠️ 部分 | ❌ | ⚠️ 2 票 | **2** | 9 份報告只有 **2 份**（OW-4745、OW-4929）的 TC 帶 `executions[]` |
| **`qa_probe`** | ✅ | ⚠️ | ❌ | ⚠️ 2 票 | **2** | 64 份 API dump，集中在 2 張票 |
| **回歸集** | ✅ | ❌ 未合併 | ⚠️ 僅分支內 | ✅ 2 輪 | **1（main）/ 4（分支內）** | 分支領先 main 12 個 commit；REG-20260820（6 TC 全 PASS）、REG-20260821（8 TC 全 PASS）；R005 lint 只存在於該分支 |
| **chat AI eval harness** | ✅ | ❌ | ❌ | ⚠️ 1 輪 | **1** | 45 條題庫、DESIGN v0.2；首輪抓到 3 個發現 |
| **`report-verifier`** | ✅ | ❌ **零引用** | ❌ | ❌ 無痕跡 | **1** | 全 repo 除定義檔外，只出現在一份討論紀錄 |
| **AI workflow eval（五層框架）** | ⚠️ 只有 guide | ❌ 無 `/eval` command | ❌ | ❌ 1 份實例 | **0.5** | `eval/` 只有 `OW-4468_eval_report.md` + template |
| **flaky 治理** | ❌ | ❌ | ❌ | ⚠️ 間接 | **0** | 無 retry / 無 quarantine / 無 `pytest-rerunfailures`；只有回歸集 2 條「已知不穩清單」與 chat eval 的 `repeat:3` |

### 3.2 這張表對內容架構的四個直接後果

1. **能當 Core 文章主軸的只有到頂級數 4 的機制。** 那是：CI/hooks/lint、executor 入帳、schema 驗證、actual 紀律、人工 checkpoint、qa-thought-capture、知識 pipeline。剛好對應 7 篇 Core。
2. **級數 2 的機制只能當「這個問題我還沒解完」的誠實段落**，不能當主軸。ledger / qa_probe / Reuse Audit 都在這一格。
3. **級數 1 的機制不進 Core，進 Lab Notes 並標成 Experimental。** 回歸集、chat eval、report-verifier。
4. **級數 0 的題材完全不寫。** flaky、AI workflow eval 的五層框架、AI 自主性趨勢。

### 3.3 兩個必須寫進文章的成熟度細節（否則就是包裝）

**細節一：Reuse Audit 是「有硬規則但不可稽核」的教科書案例。**

規則寫得很硬（「Reuse Audit 未完成不得開 playwright-cli」），但它的產出只是對話裡的一張表，沒有落成檔案。沒有 artifact 就沒有東西可以檢查，所以這條規則**永遠停在級數 2**。OW-3666 的違規被抓到，不是因為有 gate，而是因為事後有人回頭看。這也直接解釋了為什麼當時只能新增一個 trace 分類（讓它可見）而不是加一個 hook（擋下來）——那份討論紀錄自己就寫了「強制 gate 仍需另案設計」。

這一項是 Core 06 最好的素材，因為它把「可強制性的前置條件是可稽核性，可稽核性的前置條件是有 artifact」整條說完了。

**細節二：人工 checkpoint 的級數 3 永遠不成立，而這是設計而非缺陷。**

你不可能用 hook 強制一個人做判斷。這裡唯一的「強制」是社會性的加上結構性的：規則寫「agent 不得自行宣告通過」，而 artifact 上有一個必須由人填的欄位（`review_status: reviewed / ai_drafted`）。文章要把這件事講成 authority design 的固有性質，而不是假裝有 gate。

---

## 4. Proposed Content Architecture

### 4.1 三個方案

**方案一：原 10 + 2 篇單一 Series（上一輪提案）**

- 優點：讀者只要記一條線；編號簡單
- 致命問題：把 CI（級數 4、每次 push 都在跑）和 chat eval（級數 1、跑過一輪）放進同一條 Series，等於用編排暗示它們成熟度相同。這是最容易被 Senior 讀者當場抓到的問題，一旦被抓到，整站的可信度一起掉

**方案二：review 提的 4 Track（Workflow / Quality Engineering / AI Product Evaluation / Lab Retrospectives）**

- 優點：成熟度不再混雜；每個 Track 有清楚的提問
- 問題：**過度分類**。以現在的材料，Track B（Quality Engineering）只有回歸集一篇可寫，而它還沒合併；Track C（AI Product Evaluation）只有 chat eval 一篇，而它只跑過一輪。為兩篇未成熟的文章各開一個 Track，讀者看到的是兩個幾乎空的分頁——那比不分類更傷

**方案三（採用）：7 篇 Core Series + 一個 Lab Notes 區，Lab Notes 內用兩種標籤**

```
AI-Assisted QA Engineering Lab
│
├── Core Series（7 篇，成熟度門檻：Integrated 且有使用證據）
│     01  一張 Ticket 如何流過 AI QA          orientation
│     02  AI 不知道自己不知道什麼              understanding / uncertainty
│     03  怎麼讓一次 QA 判斷留下來             knowledge lifecycle
│     04  憑什麼相信 AI 說「測完了」            truth / verification
│     05  AI 說它做過，但系統怎麼證明？         provenance / attribution
│     06  規則寫下來之後，AI 還是會違規          enforcement design
│     07  哪些決策我始終沒有交給 AI             authority design
│
└── Lab Notes（單篇獨立，開頭必標成熟度）
      [Retrospective]  26 張票只有 1 份產出：我砍掉自己設計的流程
      [Retrospective]  allowlist 從 125 條砍回 42 條
      [Retrospective]  我自己漏判了一次共用變更（OW-4945）
      [Field Note]     測 AI 產品：chat AI 的 eval harness（Experimental，一輪）
      [Field Note]     上線前回歸集的設計取捨（未合併，WIP）
```

### 4.2 為什麼選方案三

1. **成熟度隔離做到了，但只用兩層導覽。** 讀者的心智模型只需要「主線」與「單篇筆記」，不需要記四個 Track 名稱。
2. **Lab Notes 是一個可以誠實放未成熟內容的地方。** 「Field Note」這個標籤本身就在告訴讀者：這是進行中的東西，不是結論。這比在文章內文道歉有效得多。
3. **Retrospective 與 Field Note 分開標籤但不分開導覽**，解決了方案二的空分頁問題，也解決了把「技術設計文」和「失敗檢討」硬塞進同一個 Track 名稱下的語意混亂。
4. **未來要升級成 Track 很容易。** 當回歸集合併、跑滿一季，或 chat eval 跑到第三輪，把那些 Field Note 抽出來變成 Track B / C 是加法不是重構。現在先不建。

### 4.3 導覽怎麼保持簡單

- Portfolio 首頁兩個清單：Core Series（有編號、有閱讀順序）、Lab Notes（時間逆序、每篇一行標籤）。
- Core Series 每篇有上一篇／下一篇；Lab Notes 沒有前後篇，只有「相關 Core 篇」一條連結。
- 每篇 Lab Note 開頭一行成熟度標示，例如：`成熟度：Experimental — 已實作，未合併主線，實跑 2 輪`。這一行是格式要求，不是可選。

### 4.4 相對於原提案的變動總表

| 原提案 | 決定 |
|---|---|
| S01 Pipeline | **Keep** → Core 01 |
| S02 理解需求 | **Keep** → Core 02 |
| S03 知識回收 | **Keep + 大幅瘦身** → Core 03 |
| S04 憑什麼相信 | **Keep + 換中心** → Core 04（中心從工具改成 verification level） |
| S05 執行帳本 | **Keep + 改框架** → Core 05（從 ledger 說明書改成 provenance 設計；且必須誠實標 ledger 只覆蓋 2 票） |
| S06 我砍掉自己的機制 | **Move** → Lab Notes [Retrospective] |
| S07 機械化防線 | **Keep + 升權重** → Core 06（本輪判定它是成熟度最高的一篇） |
| S08 哪些決策不交出去 | **Keep** → Core 07 |
| S09 回歸集 | **Move + Delay** → Lab Notes [Field Note]，合併後才考慮升 Core |
| S10 chat AI eval | **Move** → Lab Notes [Field Note] |
| 候補：Selector 策略 | **Delay**（維持候補，前置是先把 selector 優先序整理成正本） |
| 候補：AI 自主性量測 | **Drop（本輪不寫）** 理由見第 7 節 |

---

## 5. Article-by-Article Challenge

每篇固定六欄：Core design question（讀者要理解什麼）／Why reader cares／Failure evidence／Transferable principle（拿掉 my-playwright 還成立的）／Supporting implementation（只能點到，不得主導敘事）／Current evidence gap（必須在文章裡誠實揭露的）／本篇不寫什麼。

---

### Core 01 — 一張 Ticket 如何流過 AI QA｜Keep（改版）

**定位**：orientation / system map。全站的地圖，不是機制展示。

- **Core design question**：一個 ticket-driven 的 QA 流程，哪些站可以交給 AI、哪些站的產出必須固定下來？
- **Why reader cares**：讀者需要一張圖才能理解後面六篇在講哪一段。沒有這張圖，Core 04 和 Core 06 讀起來會像兩篇不相關的文章。
- **Failure evidence**：開場沿用現有的「第一個月就翻車」；補一句已發布文章沒有的——當時流程圖裡有兩個機制後來被我自己砍了。
- **Transferable principle**：**固定的是交付物，變動的是深度。** 流程的穩定性不該建立在「每一步都做同樣多的事」，而該建立在「每一步都產出同一種可接手的東西」。這條原則跟 QA 無關，任何多階段人機協作流程都適用。
- **Supporting implementation**（點到即止）：11 步的步驟名、5 個 checkpoint 的掛載位置、`docs/features/` → `docs/tickets/` → `features/` → `pages/` → `reports/` 的產物鏈。
- **Current evidence gap**：**必須說明 36% 這個數字**——42 張入帳的票裡只有 15 張是 AI 執行的。流程圖不等於流程都由 AI 走完。不寫這個數字，整站的可信度從第一篇就開始欠債。
- **本篇不寫什麼**：不列 AI 能力清單；不展開任何單一機制（每個都有專篇）；不寫 Assurance checkpoint 的 pass condition 細節；不寫 registry / seeds 的內部設計。

---

### Core 02 — AI 不知道自己不知道什麼｜Keep

**已完稿 288 行，本篇是事實校正而非重寫。**

- **Core design question**：怎麼在 AI 動手之前，讓它的「理解」與「不確定」變成可以被人檢查的東西？
- **Why reader cares**：這是導入 AI 到任何專業流程的第一個真問題。讀者關心的不是 prompt 技巧，是「我怎麼知道它誤解了」。
- **Failure evidence**：中文連接詞歧義那個例子（「外匯收入與裝修及設備支出項目」到底切在哪）是全站最好的具體例子之一，保留。補 repo 側證據：step 1 的高風險票九類清單（金流 / 報表 / 稅務 / 庫存 / 狀態流 / 跨模組 / 第三方 / 資料清空保留 / API 寫入）決定審閱強度，`review_status` 只有 `reviewed` 與 `ai_drafted` 兩種值——風險決定的是「要不要人簽」，不是「AI 要不要更努力」。
- **Transferable principle**：**要求 AI 先輸出「它以為的」，並把假設與推論分級標示；風險等級決定人審的強度，不是 AI 努力的程度。** 三級宣稱（親眼驗證／推論／假設）可以直接搬到任何 AI 輔助專業工作。
- **Supporting implementation**：`/pm` 產 `docs/features/OW-xxxx.md`、`review_status` 欄、Spec Ready checkpoint、`scripts/fetch_ow_ticket.py` 全量抓取。
- **Current evidence gap**：**文中若出現 "Requirement Audit" 作為 skill 名稱必須改寫**——repo 裡沒有這個 skill。需求層的把關實際散在 step 1 的審閱定稿與 step 4 的 Spec Ready。另外完稿寫於 2026-06-24，比 `AGENT_DOCTRINE`（7/13）早，三級宣稱分級要補進去。
- **本篇不寫什麼**：不介紹任何 skill 的操作步驟（review 已明確要求避免寫成 skill 介紹）；不展開知識落點（那是 03）；不展開「誰有權簽」（那是 07）。

---

### Core 03 — 怎麼讓一次 QA 判斷留下來，而不是變垃圾知識｜Keep（大幅瘦身）

**已完稿 388 行 + fact-checked 標註版。本篇最大的工作是刪，不是加。**

接受 review 的警告。我上一輪把 AGENT_DOCTRINE / KNOWLEDGE_GOVERNANCE / spec pipeline / memory-triage / registry / heuristics 全列成 Key mechanisms，那會寫成一篇知識管理系統導覽。重新判定：

| 元素 | 判定 |
|---|---|
| 一句話判準（「這個判斷會不會改變未來 agent 對類似情境的決定？」） | **主軸**。全站最好的一句可攜判準 |
| 儲存無默認同意 + 逐條裁決 | **主軸**。這是知識品質的守門機制 |
| 校準 log（把裁決回寫成攔截門檻的例示） | **主軸**。這是「知識庫學習」與「模型學習」的分野，也是最少人寫的部分 |
| supersede / delete、知識可以變小 | **主軸** |
| 落點分流表（product / seeds / registry / heuristics / memory） | **supporting**。點一句，不列表 |
| 四段 spec pipeline | **supporting**，一句話帶過。它解的是產品規格重建，不是 QA 判斷回收，混進來會失焦 |
| memory-triage、AGENT_DOCTRINE、KNOWLEDGE_GOVERNANCE 六種權威狀態 | **supporting**，最多各一句 |

- **Core design question**：一次人工校正，怎麼變成下次不用重講的東西，而且不會讓知識庫越堆越爛？
- **Why reader cares**：所有導入 AI 的團隊都會撞到「我像在不停教同一堂課」。而幾乎沒有人處理第二半——教的東西堆起來之後會互相矛盾。
- **Failure evidence**：現有完稿已有敘事。補一條 repo 硬證據：校準 log 的第一批（OW-4834）精準度是 **0%**（1 條候選、1 條誤採），第二批（OW-4836）是 100%（5 條全採對）。這兩個數字比任何論述都有說服力——它證明採集門檻是被校準出來的，不是設計出來的。
- **Transferable principle**：**知識回收要有一個「拒絕」的出口，而且拒絕本身要被記錄下來當作下次的判準。** 只有 append 的知識庫一定會腐爛。
- **Supporting implementation**：`qa-thought-capture` 的三條攔截門檻、`QA_CAPTURE_CALIBRATION.md`、`KNOWLEDGE_MAP` routing。
- **Current evidence gap**：**量很薄，要說。** 校準 log 只有 2 批，`QA_HEURISTICS.md` 只有 48 行約 5 條。這套機制是對的，但採集量還不足以宣稱「知識庫已經長起來了」。
- **本篇不寫什麼**：不寫產品知識 pipeline 的四段流程；不寫 Obsidian linking；不列落點表格；不寫 memory 與 heuristics 的分流細則（一句決勝語句就夠）。

---

### Core 04 — 憑什麼相信 AI 說「測完了」｜Keep（中心換掉）

**這一篇的中心從「我做了哪些驗收工具」換成「success signal 與 claim 之間的落差」。**

- **Core design question**：一個自動化流程回報的成功訊號，是否真的足以支撐它做出的那個結論？
- **Why reader cares**：這是 Senior SDET 與 QA Lead 唯一真正共同關心的問題。它同時是「我怎麼相信 AI」和「我怎麼相信我自己的 automation」——後者讓這篇文章對還沒導入 AI 的讀者也成立。
- **Failure evidence（假綠燈家族，四條同病）**：

| 案例 | success signal 來自哪一層 | 實際 claim 需要哪一層 |
|---|---|---|
| OW-4468 | pytest PASSED + schema 過 + JSON 有截圖路徑 | 截圖內容前後有差異 |
| OW-4593 | read API 回 `status=0` | 前端渲染與格式檢查通過（實際全擋，14 張作廢） |
| OW-4929 | schema 合法（`screenshot=null` 對純 API 步驟是合法的） | TC 描述的是畫面行為，需要畫面證據 |
| Sales token 腳本 | HTTP 200 | response body 裡的 `status`（實際是失敗，抄回死 token） |

四條的病灶完全相同：**成功訊號取自比 claim 更淺的一層**。這是全站最完整的一個 failure family，而且第四條發生在完全不同的地方（一支登入腳本），證明它不是 QA 特有的疏忽而是一種系統性偏誤。

- **Transferable principle**：**宣稱層級不得高於驗證層級。** 每個領域都能列出自己的證據階梯（這裡是：前端渲染 > API 回應 > DB 狀態 > code 讀起來是對的），而規則是同一條。附帶原則：**schema 管得住形狀，管不住意圖**——OW-4929 的 `screenshot=null` 完全合法。
- **Supporting implementation**（全部降級為點到）：`validate_report_data.py`、Stop hook 的零截圖提醒、`report-verifier` subagent、`actual` 欄參數。
- **Current evidence gap（兩個都要寫）**：
  1. **`report-verifier` 未接進主流程。** 零規則引用、零命令引用。文章必須寫成「我做了一個只讀的驗收 agent，但它還沒被接進流程，所以現在仍然靠我記得叫它」。這句話比假裝閉環有價值。
  2. **`actual` 欄的紀律是靠人不是靠 gate。** 實測 279 個步驟罐頭字 0%，但 `conftest` 的預設 fallback 至今仍是「如預期」，沒有任何檢查擋罐頭字。也就是這條紀律目前的成立方式是「寫測試的人每次都傳真值」，不是「不傳就會被擋」。這正是 Core 06 的開場。
- **本篇不寫什麼**：不介紹 Evidence Board 的功能（那是 Core 05 的 supporting）；不寫 `report-verifier` 的檢查清單細節；不寫 PDF 版面與 renderer；不寫 schema 欄位表。

---

### Core 05 — AI 說它做過，但系統怎麼證明？｜Keep（框架重寫）

- **Core design question**：一件事發生過、是誰做的、用什麼方法做的、證據在哪——這四題要靠什麼結構才答得出來，而不是靠回憶？
- **與 Core 04 的分界**（明確寫在文章開頭）：
  - Core 04 問「結果是真的嗎」
  - Core 05 問「這件事到底發生過嗎、誰做的、證據在哪」
  - 一份完全正確的結果，仍然可以是無法追溯的；一份可完整追溯的紀錄，仍然可以是錯的。兩件事互不涵蓋。
- **Why reader cares**：QA Lead / EM 要對外交付與稽核。當交付物上的執行者可能是人、可能是 AI、可能是兩者接力時，「誰測的」不再是自明的。
- **Failure evidence**：OW-4696（AI 實測過，只在 worklog 手打片段，看板 AI測 chip 誤判成沒測過）、OW-3712 / OW-4017（走過的頁面沒回補 registry，下一張票重新探索同一頁）。
- **provenance 是不是 AI 特有問題——修正後的立場**（回應 review）：不是。但被 AI 放大，放大機制有三個，全部有 repo 證據：
  1. **多異質寫入者**：`ledger.py` 註解明載四個寫入者寫同一份 JSON（pytest conftest、`qa_probe`、evidence board server、人工標記），沒有鎖會互相覆蓋。傳統 CI 的證據只有一個寫入者。
  2. **執行路徑會臨時改變**：AI 會自己換工具（curl / playwright-cli / pytest），每種工具的證據落點不同。`qa_probe` 存在的理由就是把 ad-hoc 的那條路接回帳本。
  3. **歸屬會靜默出錯**：`ledger.py` 明文「who 自動判定 AI session，禁止 default 成人名」，理由寫在註解裡——「錯誤歸因比沒記帳更毒」。這是傳統 CI 不會有的問題，因為 CI 不會被誤認成人。
- **Transferable principle**：**要求留痕不如把留痕綁進動作。** `qa_probe` 的設計是「發請求」與「記帳＋存證據」是同一個指令，所以做不到只做前者。加上：**歸屬欄位不得有預設值**——寧可空著，不要 default 成一個看起來合理的人名。
- **Supporting implementation**（點到）：`ledger.py` 的 file lock 與 append-only、`_executors.json` 格式、evidence board 的三種 chip、Stop hook 第 1 檢查。
- **Current evidence gap（要寫得很清楚）**：**帳本只覆蓋了 2 張票。** 9 份報告裡只有 OW-4745 與 OW-4929 的 TC 帶 `executions[]`；`qa_probe` 的 64 份 API dump 也集中在同樣那 2 張票。`ledger.py` 是 7/17 才進 repo 的，早於它的報告沒有回填。所以正確的說法是「這個結構已經在跑，但只跑在最近的票上，舊帳沒有補」——不是「執行都有帳可查」。
- **本篇不寫什麼**：不寫 `ledger.py` 的 API 用法；不寫 JSON schema 欄位；不寫 evidence board 的 sprint map 機制；不寫 file lock 的實作方式（一句「四個寫入者需要序列化」就夠）。

---

### Core 06 — 規則寫下來之後，AI 還是會違規｜Keep（本輪升為最成熟的一篇）

**本輪重新判定：這是七篇裡成熟度最高、且唯一「主軸機制全部到達級數 4」的一篇。**

- **Core design question**：一條規則要具備什麼條件才真的會被遵守？文件、lint、hook、CI 各自能保證什麼、不能保證什麼？
- **Why reader cares**：這篇的讀者遠超 QA。任何寫過 CONTRIBUTING.md 然後發現沒人照做的人都是讀者。
- **Failure evidence**：
  - OW-4696 / OW-3712 / OW-4017：三條純 prose 硬規則被違反（入帳、registry 回補）。
  - **Reuse Audit：有硬規則、有 guide、有 subagent，但因為沒有落檔的 artifact，永遠無法被檢查。** OW-3666 的違規只能事後發現，當時的處理是新增一個 trace 分類讓它可見，而那份討論紀錄自己就承認「強制 gate 仍需另案設計」。
  - 2026-07-07 的盤點原句：「最大缺口是規則靠 AI 自律、缺機械化強制」。
- **Transferable principle（兩條）**：
  1. **能用程式驗證的，就不要靠模型自律。** prose 規則只有被機械化 gate 背書時才可靠。
  2. **可強制性的前置條件是可稽核性，可稽核性的前置條件是有 artifact。** 沒有落檔的產出，任何規則都只能停在宣示。
  - 還有一條關於邊界的：**hook 只約束單一 agent，CI 才是多方共用的防線。** 這條在多 agent（Claude / Codex / Gemini）環境下是硬事實，CI 的 yml 註解就寫著。
- **Supporting implementation**：四關 CI、`lint_test_rules.py` R001-R004、三個 hook、`Makefile` 五個入口、pre-commit 的收斂。
- **Current evidence gap（三個，全部要寫）**：
  1. **62 條 grandfathered 違規**（R001 佔 56 條）。硬規則只對新 code 生效。這是正確的 ratchet 設計，但不能寫成「不可能違反」。
  2. **CI 只跑靜態稽核，零 E2E。** 為什麼刻意不放（需要 secrets、需要測試環境資料與可用房況、E2E 進 CI 的維護代價還沒付）——這個「刻意」值得寫，但不能寫成有 CI/CD pipeline。
  3. **R005（feature 檔必須存在）只存在於未合併的回歸集分支。** main 上沒有這條 lint。任何提到 R005 的段落都要標明分支狀態。
- **本篇不寫什麼**：不寫 hook 的 JSON payload 格式；不列 Make target 清單；不寫 permission allowlist 的 42 條明細（那是 Lab Note）；不把「先觀測再強制」寫成通用原則（n=1，見第 1.2 節）。

---

### Core 07 — 哪些決策我始終沒有交給 AI｜Keep

- **Core design question**：在一個 AI 大量參與的流程裡，哪些權力從一開始就不授權，以及這個邊界靠什麼結構維持？
- **與 Core 06 的分界**：Core 06 是「規則怎麼被強制」，Core 07 是「哪些事情本來就不由 AI 決定」。前者處理服從，後者處理授權。
- **Why reader cares**：EM 與 QA Lead 要對品質負責。他們需要知道「導入 AI 之後，責任還在誰身上」有沒有一個結構性的答案，而不是一句「當然還是人負責」。
- **Failure evidence**：OW-4338（TC 從 test plan 起就標 manual，仍用自動化硬磨，而人早就手動測完）。這條之所以重要，是因為它證明**權責邊界如果只寫在 TC 標記裡而沒有進流程分支，就會被忽略**——後來才有 manual-only 的流程分支。
- **實際存在的人工關卡**（逐項查證後保留）：

| 決策 | 人工關卡存在？ | 結構落點 |
|---|---|---|
| 測試範圍 / 必跑 TC 清單 / UI 路徑 / API 端點 | ✅ | step 2 的「Sunny Scope 授權」，SOP 表列查核者為人 |
| 高風險票定稿 | ✅ | step 1 九類風險清單 + `review_status` 欄位 |
| 知識 promote 進正式產品目錄 | ✅ | `spec-promote` 前置條件「使用者明確要求」 |
| 知識儲存（採集落地） | ✅ | 逐條 ✅/✏️/❌/➕ 裁決，無默認同意 |
| eval 執行與通過 | ✅ 規則上 | 「agent 不得自行宣告 eval 通過」——但 eval 本身幾乎沒在跑（級數 0.5） |
| manual-only 判定 | ✅ | step 2 測試策略 |
| 共用變更是否走 PR | ⚠️ 判準明確但由 agent 自判 | 三問法；OW-4945 就是自判漏了 |
| 模型能力不足時降級回報 / 提早升級 | ⚠️ 全靠自律 | doctrine 第 7 章，無任何檢查 |

- **Transferable principle**：**授權邊界要長在 artifact 的欄位上，不是長在說明文件裡。** 「高風險票要人審」這句話會被忽略；一個必須填 `reviewed` 才算完成的欄位不會。加上：**不能機械強制的關卡，至少要讓「跳過」留下痕跡。**
- **Supporting implementation**：SOP 的 checkpoint 表（查核者欄）、`review_status`、`spec-promote` 前置、doctrine 第 7 章的高判斷步驟清單。
- **Current evidence gap（兩個）**：
  1. **`Decision Layer` 不存在。** `AI_QA_SYSTEM_LAYERS` 討論明確記載尚未實作。文章不得寫成有一層 decision engine；現況是「決策權靠 checkpoint 表與 artifact 欄位釘住」。
  2. **eval 這個關卡雖然規則上要求人確認，但實際幾乎沒運作**（1 份實例）。列在表上要標明。
- **本篇不寫什麼**：不寫 Decision Layer 的設計構想（那是 Planned，寫了就是把構想當能力）；不寫 checkpoint 的 pass condition 逐條；不重複 Core 06 的強制機制。

---

### Lab Notes

**[Retrospective] 26 張票只有 1 份產出：我砍掉自己設計的流程**｜Move（原 S06）

接受 review 的重新定位。這篇真正回答的不是知識管理，是 **adoption 量測**。

- **Core design question**：一個內部流程機制，怎麼知道它是真的在用，還是只是存在？
- **Why reader cares**：這是整站對 QA Lead / EM / Recruiter 最有辨識度的一篇，因為它展示的是判斷力而不是產能。
- **Failure evidence**：`QA_THOUGHT_COLLECTOR_GUIDE.md` 的 deprecated 標註原文「實測採用率極低（26 票僅 1 票產出）」；改版後的機制把採集時機從測前改到測中，理由是「很多 QA 直覺不是測前想出來的，而是測到一半才冒出來」。
- **Transferable principle**：**設計完整但沒人用的 control，比沒有 control 更危險——團隊會誤以為那件事已經有人管了。** 這條完全不限 QA。配套的第二條：**機制的存活條件是採用率，不是設計品質；而採用率要能被量。**
- **Current evidence gap**：`26 票 1 份` 這個數字的來源是文件自述，不是我獨立重算出來的（當時的 intake artifact 已隨機制廢止，無法回頭清點）。文章要標明它是當時的自我量測結果。
- **本篇不寫什麼**：不寫替代機制的操作細節（那是 Core 03）；不把它寫成「我很有勇氣」的自我表揚。

**[Retrospective] allowlist 從 125 條砍回 42 條**

- **Core design question**：授權清單為什麼會自然膨脹，以及沒有基準線的話怎麼判斷「該砍了」？
- **Failure evidence**：125 條裡混入一次性垃圾、廣義 pattern，以及一條含明文 API key 的 curl。
- **Transferable principle**：**權限清單需要一條基準線，否則永遠只會加不會減；而膨脹的授權會偽裝成便利。**
- **Current evidence gap**：砍完之後有沒有再次膨脹，我沒有量（`settings.local.json` 未進版控，無歷史可比）。不要宣稱基準線維持住了。

**[Retrospective] 我自己漏判了一次共用變更（OW-4945）**

- **Core design question**：一條「什麼時候該走 review」的判準，為什麼寫得很清楚還是會漏判？
- **Failure evidence**：改 `pdf_reporter.py` 讓某一欄在無值時不輸出，影響所有票的報告版面，當時直推 main；事後才補回歸驗證（OW-4945 欄位消失、OW-4916 保留）並寫成判例。
- **Transferable principle**：**判準要配判例。** 抽象的三問法會被自己的手滑繞過；一條寫明「這件事當時我判錯了」的判例才會被下次讀到。
- **Current evidence gap**：這是唯一一條判例，樣本數 1。不要寫成有判例制度。

**[Field Note] 測 AI 產品：chat AI 的 eval harness**｜Move（原 S10）

- **成熟度標示（必須寫在開頭）**：Experimental — harness 已實作、45 條題庫、DESIGN v0.2、**執行樣本僅一輪**（首輪抓到 3 個發現）。
- **Core design question**：當被測對象本身會胡說八道、而且每次回答都不一樣時，測試該長什麼樣？
- **Why reader cares**：這是全站對外吸引力最高的單篇，而且它與 Core Series 回答的是不同問題（Core 是「用 AI 做 QA」，這篇是「測 AI 產品」）。
- **Transferable principle（三條，都可攜）**：
  1. **選測試入口要看「共用的是哪一段」**：兩條 request path 收斂到同一顆推論引擎，所以測外層較薄的那條也能代表；但要明確列出測不到的部分（限流閘、真實 session store、前端渲染）另外用少量 UI smoke 補。
  2. **不確定性不能靠重試蓋掉**：`temperature=0` 壓浮動；語意類 case 跑 3 次，三次不一致就標 FLAKY **並視同失敗**。
  3. **測試專用能力要有環境邊界**：時鐘注入僅 dev / release 可用、production 一律禁止；改造完成前強制用實際跑測日，否則直接 ERROR，避免相對日期悄悄對不上還假 PASS。
- **哪些結論還不能做**：不能宣稱「chat AI 的品質已被把關」；不能給通過率趨勢；不能宣稱 judge 的判準已校準（只有一輪，沒有 judge 與人工判定的一致性數據）。
- **本篇不寫什麼**：不寫 YAML schema 全貌；不寫 runner 實作；不評論 chat AI 產品本身的好壞。

**[Field Note] 上線前回歸集的設計取捨**｜Move + Delay（原 S09）

- **成熟度標示（必須寫在開頭）**：Work in progress — 在未合併分支 `test/regression-suite`（領先 main 12 個 commit），實跑 2 輪（2026-08-20 六案全 PASS、08-21 八案全 PASS），**兩輪的執行者都是人**。
- **Core design question**：每張票都測過了，為什麼還是不知道這一版能不能上線？
- **Why reader cares**：這是全 repo 設計密度最高的一塊，對 Senior SDET 的技術說服力最強。
- **值得寫的設計取捨（不是「我做了回歸集」）**：
  - **journey 給人看、domain 當身分**：`tc_id` 是報告 JSON 的 upsert 主鍵，journey 一重排 tc_id 就變，舊條目變孤兒、歷史比對斷掉 → **identity 不該綁敘事順序**（這條可攜到任何有主鍵與人類編號的系統）。
  - **接力 vs 獨立 smoke**：各段自建前置訂單就不是同一張單，最容易壞的系統接縫反而測不到；但塞成一條超長 scenario 又看不出斷在哪 → 折衷是同 module 多 scenario 共用 module-scope fixture。
  - **跳段跑直接紅、不是略過**：略過會讓該驗的段靜默消失，涵蓋率掉了沒人知道 → **靜默降級比失敗更危險**。
  - **xdist 平行直接 raise**：四段被拆到不同 worker 會各自看不到別人的訂單。
  - **測資生命週期**：一律走 `pms_seed` fixture；文件裡有一張「清得掉 / 清不掉 / 一定清不掉」的邊界表。
  - **已知覆蓋缺口表 9 條**，其中一條原文寫著「不要宣稱『取消功能』已受把關，只有非代收那條受把關」→ **「我們測過了」這句話必須附一張缺口表才有意義。**
  - **已知不穩清單**：兩條，各帶起始日與「超過兩輪還在就必須修或移出集」的處理規則。
- **Current evidence gap**：未合併；R005 lint 只在該分支；只跑兩輪且全綠（沒有「跑紅之後怎麼分類」的真實案例，只有規則）；flaky 只有人工清單沒有機制。
- **升 Core 的條件**：合併進 main + 累積至少一次真實跑紅並依 red/yellow 分類處理過。滿足才考慮升 Core 08。

---

## 6. Audience Review

問法依 review 修正：不問「他對哪個 mechanism 有興趣」，改問**「他看完之後應該對作者形成什麼 engineering judgment」**。以下每條都對應得上 repo evidence，沒有一條是為了 JD 硬造。

### Senior SDET

看完應形成的判斷：

1. **她知道什麼 verification signal 支撐什麼 claim。** 證據來源：四條假綠燈的處理方式、279 步驟罐頭字 0%、schema 合法但意圖不合格（OW-4929）。
2. **她知道規則的可強制性取決於有沒有 artifact 可查。** 證據：Reuse Audit 卡在級數 2 的原因被她自己說清楚。
3. **她知道自動化紀律要用 ratchet 導入，不是一次翻新。** 證據：62 條 grandfathered 違規，而且她主動說出來。
4. **她知道靜默降級比失敗危險。** 證據：跳段跑直接紅、xdist 直接 raise、時鐘沒對上直接 ERROR。

不該讓他形成的判斷：「她有一套成熟的 AI QA 平台」。這不是 repo 的樣子，也不是文章該傳達的。

### QA Lead

1. **她能說清楚哪些決策沒有交出去，而且能指出那些決策落在哪個欄位上。** 證據：checkpoint 查核者欄、`review_status`、`spec-promote` 前置。
2. **她知道交付物的可信度要獨立於執行者是人還是 AI。** 證據：`_executors.json` 42 票 / 15 AI、三種 chip、歸屬欄不得 default。
3. **她會把 36% 這種對自己不利的數字講出來。** 這一條對 Lead 的分量最重——她的品質報告可以被信任。

### Engineering Manager

1. **她知道導入 AI 的成本落在維護一條管線，不是省下測試時間。** 證據：現有文章已寫「很多時間其實花在如何避免 AI 一直犯同樣的錯」；沒有任何效率數字宣稱。
2. **她會量機制的採用率，並且砍掉沒人用的。** 證據：26 票 1 份 → 廢止；125 → 42。
3. **她知道文件與強制是兩件事，而且知道哪一種要花錢。** 證據：7/07 的原句「規則遵循率取決於每個 agent 記得 409 行規則 / 改善後取決於 lint hook CI 有沒有跑」。
4. **她的治理有判例，不只有原則。** 證據：OW-4945 事後自我分類。

### AI-Assisted Testing Team（想導入的團隊）

1. **他們知道第一步不是 E2E 自動化，而是需求理解與知識回收。** 證據：已完稿文章的核心論點。
2. **他們知道知識回收必須有「拒絕」的出口與校準紀錄。** 證據：校準 log 兩批（0% → 100%）。
3. **他們知道多 agent 環境下 hook 不夠、CI 才是共用防線。** 證據：CI yml 的註解與實際 run。
4. **他們拿得走可直接照抄的東西**：三級宣稱、證據階梯、兩次停損、六類失敗分類、新增 smoke 前四問、permission 七原則。

### Recruiter / Hiring Manager

1. **這個人會把 Experimental 說成 Experimental。** 證據：Lab Notes 的成熟度標示格式、Core 04 主動揭露 verifier 未接上。
2. **這個人的機制是從具體事故長出來的，每條都指得出來源。** 證據：doctrine 的教訓來源對照表、16 條 failure → mechanism。
3. **這個人會砍掉自己的作品。** 證據：兩篇 Retrospective。
4. **這個人做的是 engineering 不是工具操作。** 證據：identity 不綁敘事順序、記帳綁進動作、歸屬欄禁預設值——這三個判斷跟工具無關。

**共同的反向要求**：五類讀者都不該從網站得到「這裡有一套 production-ready 的 AI QA 平台」的印象。這不是謙虛姿態，是事實準確度問題。

---

## 7. Gaps We Must Not Hide

逐項重驗，含本輪新查到的數字。

| 主題 | 重驗結果 | 內容處置 |
|---|---|---|
| **flaky** | 級數 **0**。無 retry、無 quarantine、無 `pytest-rerunfailures`。只有回歸集的 2 條「已知不穩清單」（人工紀律）與 chat eval 的 `repeat:3` FLAKY 判定 | **完全不寫成能力。** 漫畫第 06 話已把 Flaky Test Governance 標成能力，這是網站現存最大的名實落差。處置：不在任何文章聲稱有 flaky 治理；若 Core 06 或回歸集 Field Note 提到，一律寫成「目前只有人工清單」 |
| **AI workflow eval** | 級數 **0.5**。`EVALUATION_GUIDE` 通篇假設 `/eval` 存在，`.claude/commands/` 裡沒有；`eval/` 只有 1 份實例 + template | **不寫五層框架。** 也不要寫成「eval 制度尚在建立中」——那會讓讀者以為快好了。可寫的只有一句誠實的：對 AI 自己做的 QA 的評估，我有框架但沒跑起來 |
| **CI/CD** | CI 真的在跑（8 筆最近 run 全 success、11-23 秒、push 與 PR 都觸發），但**只有 4 關靜態稽核，零 E2E、無 nightly、不參與部署** | 可寫「為什麼刻意只放靜態稽核」，**不可寫成有 CI/CD pipeline**。另需揭露 62 條 grandfathered 與「hook 只約束單一 agent」 |
| **regression branch state** | 未合併，領先 main 12 commit，最後 commit 2026-08-21；實跑 2 輪全 PASS，**executor 都是人**；R005 lint 只在此分支 | 只能當 Field Note 並標 WIP。**不得與 main 系統混為一談。** 升 Core 的條件見第 5 節 |
| **report-verifier integration** | 級數 **1**。零規則引用、零命令引用、無使用痕跡 | Core 04 必須明說它還沒接上。**不得因為文章好寫而先接進去**（見第 8 節） |
| **API / integration test depth** | 有 4 份 API catalog、`qa_probe api` 完整 dump（64 份，2 張票）、seed 走真實建單 API、後端 repo 當規格來源；但**沒有獨立的 API test suite**、沒有 contract test、沒有 integration 層的常態回歸 | **不寫成一層測試。** 現況是「API 是造測資的手段與 ad-hoc 驗證的工具」。若要寫 API 測試主題，材料不足，列為候補 |
| **AI 自主性量測（本輪新增判定）** | `eval_trace` 180 筆，但分布極不均：2026-05 自主完成率 100%（15/15）、06 掉到 29%（6/21）、07 為 0%（0/3）、08 回到 100%（3/3）。而 `_executors.json` 有 42 張票——**trace 的覆蓋率明顯低於實際執行量** | **整篇不寫（Drop）。** 這組數字看起來像趨勢，實際反映的是「什麼時候有記 trace」而不是「AI 變強或變弱」。拿它畫趨勢圖是最容易被抓到的造假。dashboard 目前仍是 mockup |
| **知識 pipeline 採用（本輪新增）** | 完整走完一輪（《專案設定》發布、inbox 清空），目前 `orders.md` 在途。n=1~2 | 可當 Core 03 的 supporting 一句話，**不可當主軸**，也不可說「產品知識庫已由 pipeline 維護」 |
| **qa-thought-capture 採集量（本輪新增）** | 校準 log 2 批、`QA_HEURISTICS` 48 行約 5 條 | Core 03 要寫明量薄。機制對，但還沒累積成一個知識庫 |

---

## 8. Engineering Recommendation（與內容無關）

> 依 review 第八點要求，這一節與文章規劃完全脫鉤。判斷順序是先問 QA / governance 需求，不是先問文章好不好寫。若結論是不需要，就不做。

### 8.1 report-verifier 是否該接進主流程

**現在實際的 failure 是什麼**

OW-4468：pytest PASSED、schema 通過、JSON 的 `screenshot` 欄位有路徑，但截圖內容前後一模一樣，等於零證據力。被發現的方式是人反問「有檢查過嗎」。這類 failure 的共同形狀是「**檔案存在且格式正確，但內容不支撐結論**」。

**為什麼現有三道防線不夠**

| 現有防線 | 能抓什麼 | 抓不到 OW-4468 的原因 |
|---|---|---|
| `validate_report_data.py` + schema | 欄位缺漏、型別錯誤、路徑格式 | 它驗的是形狀。截圖路徑存在即通過，不看圖 |
| Stop hook | 「所有 step 的 screenshot 都是 null」 | OW-4468 每步都有截圖，只是內容相同。hook 看的是有沒有，不是有沒有差異 |
| 人工 Report Ready checkpoint | 理論上能抓 | 它是唯一能抓的，而 OW-4468 就是它漏掉的那次。人逐頁開 PDF 的成本高、且是最容易被省略的一步 |

所以 gap 是明確的：**沒有任何機制檢查「證據內容是否支撐結論」，而唯一能檢查的人工關卡成本高、容易被省略。**

**verifier 解的是哪一段**

只解一段：把「逐頁開 PDF、逐張開截圖、比對前後有無差異、確認 actual 是真值」這件高成本、低樂趣、容易省略的機械勞動，交給一個只讀 agent 先做一遍，把可疑項目挑出來給人看。它**不取代**人的 Report Ready 簽核。

**mandatory 的代價**

1. **時間成本**：每張票多一次 subagent 執行（開 PDF、開多張圖）。對截圖多的票不便宜。
2. **對純 API 票是純浪費**：沒有畫面證據的票，verifier 沒東西可看。
3. **會產生新的空轉失敗模式**：verifier 看不出差異時應該說看不出（它的定義檔已經寫了「看不出差異就明說，不放水判 PASS」），但這會製造需要人裁決的模糊回報。
4. **最重要的代價：假安全感。** 一個 AI 驗另一個 AI 的截圖，同樣會漏。如果流程上出現「verifier 判 PASS」這個訊號，人很可能因此跳過自己開 PDF——那就把 OW-4468 的病灶從「沒人看」變成「以為有人看了」。這正是 Lab Note 那篇「設計完整但沒人用的 control 比沒有 control 更危險」的同一個陷阱，只是反過來：**設計完整且被信任的 control，如果實際能力不足,危險更大。**

**結論（有條件建議，非無條件強制）**

建議做的是：把 verifier 掛在 **Report Ready checkpoint 的「人審之前」**，並且**只在符合條件時觸發**——報告含畫面證據（至少一個 step 有 screenshot）且該票要交付給業務或稽核。純 API 票不觸發。

同時要滿足三個約束，否則不要接：

1. **verifier 的輸出不得是 PASS/FAIL 結論，只能是「待人確認清單」。** 移除「verifier 判 PASS」這個訊號，就移除了假安全感的來源。
2. **人審欄位不得因為 verifier 跑過就可以省略。** `review_status` 之類的人工欄位仍然必填。
3. **要先量一次它抓不抓得到 OW-4468。** 拿 OW-4468 的舊產物當回歸案例；抓不到就不值得接。

**這件事現在該不該做**：值得做，但優先級低於「把 Reuse Audit 產出落成 artifact」。後者解的是一條**已經被違反過、且目前結構上永遠無法檢查**的硬規則（見 3.3 細節一），影響面比 verifier 大。兩件事我都不在本輪動手。

### 8.2 本輪不提出的其他實作變更

- 不建議為了寫 flaky 文章而加 retry / quarantine。加了會鼓勵掩蓋不穩，與回歸集現有的 red/yellow 人工分類紀律衝突，需要獨立評估。
- 不建議把 `/eval` command 補起來只為了讓 eval 文章可寫。eval 沒跑起來的原因需要先診斷（是不是價值不足、還是時機不對），這正是 Lab Note 那篇 adoption 教訓的適用場景。

---

## 9. Publication / New Writing Priority

### 9.1 Publication / Website Hygiene Order（低成本維護，不含新寫）

依成本與風險排序。這一段只列 editorial fix，不寫文章。

| # | 工作 | 說明 |
|---|---|---|
| 1 | **修已發布文章的事實錯誤** | `/jira-tc` 內含 AI Mirror + Requirement Audit 那段已廢止。處置建議：不刪，改寫成一句「這個機制後來被我砍掉了」並在該處留一個指向未來 Retrospective 的伏筆。另外文末「目前仍持續調整」四項需更新（前兩項不存在、後兩項已成型） |
| 2 | **補三處 `【插入…】` 佔位** | AI 理解→人類修正的真實對話、報告資料夾結構、PDF 縮圖。三者都有現成材料 |
| 3 | **fact-check 已完稿 Core 02** | 主要檢查點：Requirement Audit 名稱、補三級宣稱分級（成稿早於 doctrine） |
| 4 | **fact-check 已完稿 Core 03** | 主要工作是**刪**：把 spec pipeline / memory-triage / governance 六狀態降成各一句；補校準 log 的 0% → 100% 兩批數字；補「量還很薄」的誠實段落 |
| 5 | **上架 Core 02 / Core 03** | portfolio 從 1 篇變 3 篇 |
| 6 | **修導覽** | `portfolio/index.html` 目前上下篇兩邊都是 `Coming Soon`；建立 Core Series 與 Lab Notes 兩個清單 |
| 7 | **Numbering 一次性處理** | 現在是「檔名 01 / 標題 03」錯位。等 Core 架構確認後一次改；建議檔名與標題統一用 Core 編號，舊路徑留 canonical。**本輪不動** |
| 8 | **對齊漫畫能力標籤與實作** | 第 06 話 Flaky Test Governance 是名實落差最大的一格。最小處置：不在文章側呼應這個標籤；若要改漫畫頁文案另議 |

### 9.2 New Content Priority（不因為「已完稿」就排前面）

排序依據：Audience value ／ Evidence density ／ Failure→Mechanism 完整度 ／ Senior SDET-QE signal ／ 是否代表 repo 現在的真正重心。

| 排名 | 篇 | Audience | Evidence | Failure完整度 | QE signal | 代表重心 | 綜合 |
|---|---|---|---|---|---|---|---|
| **1** | **Core 06** 規則寫下來之後，AI 還是會違規 | 高（跨 QA） | **最高**（CI 8 筆 run 全綠、時間線、62 條 baseline） | 高（3 反例 + Reuse Audit） | **最高** | 高 | **1** |
| **2** | **Core 04** 憑什麼相信 AI 說「測完了」 | **最高** | 高（4 條同病 + 279 步驟 0% 罐頭字） | **最高**（假綠燈家族最完整） | 高 | 高 | **2** |
| 3 | Lab Note [Retro] 26 票 1 份產出 | 高（Lead/EM/Recruiter） | 中（數字是自述） | 高 | 中 | 中 | 3 |
| 4 | Core 05 provenance | 中高（Lead/EM） | 中（帳本只覆蓋 2 票） | 高 | 高 | 高 | 4 |
| 5 | Core 07 authority | 中高 | 中（人工關卡難量化） | 中 | 中高 | 高 | 5 |
| 6 | Core 01 改版 | 中（orientation） | 高 | 低（本來就不該有） | 低 | 高 | 6 |
| 7 | Lab Note [Field] chat AI eval | 中高（對外最高） | 中（設計強、樣本 1 輪） | 低 | 高 | 低 | 7 |
| 8 | Lab Note [Field] 回歸集 | 高（SDET） | 高但在分支 | 中（規則有、真實跑紅沒有） | **最高** | 中 | 待合併 |

### 9.3 下一篇「新寫」應該是哪一篇

**結論：Core 06《規則寫下來之後，AI 還是會違規》。**

我上一輪的 hypothesis 是 Core 04，本輪推翻。四個理由：

**1. 它是唯一一篇「主軸機制全部到達級數 4」的文章。**

CI 每次 push / PR 都在跑（8 筆最近 run 全 success，11-23 秒）、三個 hook 每個 session 都在觸發（本 session 的 SessionStart 輸出就是證據）、lint 在寫入當下退回違規。Core 04 的情況相反：它最搶眼的工具（`report-verifier`）停在級數 1。

網站要從「QA 漫畫」升級成「Engineering Lab」，第一篇新文章的作用是**建立可信度基準**。用一篇每個宣稱都能被 `gh run list` 驗證的文章打頭，後面幾篇的誠實揭露才會被讀成誠實，而不是被讀成心虛。反過來，如果第一篇新文章的中心工具還沒接上流程，讀者會合理懷疑其他篇也是這樣。

**2. 它有全站最強的一句可引用原則，而且那句話是當時就寫下來的，不是事後包裝。**

> 能用程式驗證的，就不要靠模型自律。prose 規則只有在被機械化 gate 背書時才真正可靠。

配上那句代價對照——「規則遵循率取決於每個 agent 記得 409 行規則／改善後取決於 lint hook CI 有沒有跑，後者是確定的」——這一篇不需要我幫它總結論點，論點在 2026-07-07 就寫在 repo 裡了。

**3. 它的 failure evidence 有一條別人寫不出來的：Reuse Audit 卡在級數 2。**

「有硬規則、有 guide、有專屬 subagent，但因為產出沒有落檔，這條規則永遠無法被檢查」——這個發現把「可強制性 ← 可稽核性 ← artifact」整條因果講完了，而且它是我這一輪量測才得出的，不是文件裡寫好的。這是整份盤點裡最像 senior engineering judgment 的一項。

**4. 它天然承接已發布文章，也天然接到 Core 04。**

已發布文章的結尾在講「痕跡變成規則、知識庫、Registry、Audit 機制」。Core 06 就是接著回答那些規則怎麼從宣示變成擋得住的東西。而 Core 06 收尾的誠實揭露——**機械化管得住形狀，管不住證據力**（62 條 grandfathered、schema 合法但意圖不合格、`actual` 欄靠人不靠 gate）——就是 Core 04 的第一句。順序反過來寫不出這個接點。

**動筆前要處理的三件事**

1. 三個 evidence gap 必須進文章，不是附註：62 條 grandfathered（R001 佔 56）、CI 零 E2E 及其理由、R005 只在未合併分支。
2. 「先觀測再強制」不能寫成通用原則（n=1，且那份紀錄自己說不能強制）。要寫的是四拍 pattern，並強調 doctrine 比 lint/CI 晚 6 天出生這個順序。
3. 真材料準備三樣：一段 hook 實際 exit 2 退回的 stderr、一次 CI run 的四關輸出、`lint_baseline.json` 的片段（讓 62 條 grandfathered 看得見）。

**Core 04 排第二，緊接著寫。** 它的 audience value 是全站最高的，只是需要 Core 06 先把「機械化的邊界」立起來，它的「所以還需要人開檔案看」才有支點。

---

## 10. 附錄：本輪量測的可重跑指令與原始數字

所有成熟度判定都出自以下量測，不採信文件自述。在 `~/my-playwright` 執行。

| 量測 | 指令要點 | 結果 |
|---|---|---|
| report-verifier 引用數 | 全 repo grep `report-verifier`，排除自身定義檔 | 2 筆，都在同一份 2026-07-07 討論紀錄；**規則/命令 0 筆** |
| Reuse Audit 可稽核性 | grep `EXPLORE_GUIDE.md` 的產出定義 + 找 `docs/tickets/` 有無 audit artifact | 產出只是表格，**無落檔** |
| 校準 log 批次 | `docs/QA_CAPTURE_CALIBRATION.md` 進步指標表 | 2 批：OW-4834 精準度 0%、OW-4836 100% |
| lint 規則與豁免 | `lint_test_rules.py` 規則清單 + `lint_baseline.json` signature 計數 | R001-R004（main）；grandfathered **62**（R001 56 / R002 5 / R004 1）；**R005 不在 main** |
| CI 是否真在跑 | `gh run list --limit 8` | 8 筆全 success，11-23 秒，push 與 pull_request 皆觸發 |
| ledger 覆蓋率 | 掃 `reports/data/*_qa_report.json` 的 `executions[]` | 9 份中 **2 份**（OW-4745、OW-4929） |
| qa_probe 產物 | `find reports -path "*/api/*.json"` | 64 份，集中在 2 張票 |
| actual 欄紀律 | 掃全部 step 的 `actual`，比對罐頭字樣式 | 279 步驟，罐頭字 **0%**，空值 0%；但 conftest 預設 fallback 仍是「如預期」 |
| trace 事件分布 | 掃 `eval_trace/*.jsonl` | 180 筆；`knowledge_captured` 39、`human_manual_test` 36、`human_delegate_to_ai` 27、`ai_run_completed` 24、`qa_capture_decision` 21、`ai_fallback_to_human` 18、`tc_draft_created` 9、`human_report_review` 6 |
| trace reason 分布 | 同上取 `reason_type` | knowledge 39、calibration 21、spec_gap 9、environment_limit 6、**process_reuse_miss 3** |
| 自主完成率按月 | `ai_run_completed / (ai_run_completed + ai_fallback)` | 05：100%(15/15)、06：29%(6/21)、07：0%(0/3)、08：100%(3/3) → **分布過稀，不可作趨勢** |
| executor 組成 | `docs/tickets/_executors.json` | 42 票，AI 執行 **15（36%）** |
| 機制誕生時間線 | 每個檔案 `git log --diff-filter=A` 取最早 | 見第 2.2 節 |
| 回歸集狀態 | `git log main..test/regression-suite`、分支內 `reports/data/` | 領先 12 commit；REG-20260820（6 TC PASS）、REG-20260821（8 TC PASS）；executor 皆為人 |
| 知識 pipeline 採用 | `docs/product/inbox/` 內容 + git log grep promote | 完成 1 輪（《專案設定》），`orders.md` 在途 |
| eval 實例數 | `ls eval/` | 1 份實例 + 1 份 template；`.claude/commands/` 無 eval |
| flaky 機制 | grep retry / rerunfailures / quarantine；讀 `pytest.ini`、`requirements.txt` | **全部無**。僅回歸集 2 條人工清單 + chat eval `repeat:3` |
