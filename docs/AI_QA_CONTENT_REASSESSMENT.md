# AI QA 內容重新盤點與提案（AI QA Content Reassessment）

日期：2026-08-23
盤點對象：`~/my-playwright`（AI QA 系統本體）、`~/personal/kuming-rabbit`（網站與文章）
狀態：提案，未動任何網站檔案、未改檔名、未改 series numbering、未撰寫新文章
盤點方法：以實作為準（rules / skills / commands / hooks / CI / scripts / tests），文件只作交叉比對；凡文件描述與實作不符者，一律標為 Deprecated 或 Planned

---

## 1. Executive Summary

### 1.1 這次盤點的三個主要發現

**發現一：已發布文章有一處事實已經過時，而且過時得比文章還早。**

`portfolio/ai-qa-series-01.html`（發布日 2026-06-23）寫著「這邊我是包成一個 command `/jira-tc`，裡面有兩個 skill：AI Mirror Understanding 和 Requirement Audit」。

實際上 `docs/QA_THOUGHT_COLLECTOR_GUIDE.md` 已在 **2026-06-15** 標記 `status: deprecated`，理由寫在文件開頭：「實測採用率極低（26 票僅 1 票產出）」。也就是說文章描述的機制，在文章發布前 8 天就被自己廢掉了。同一篇文章提到的 `Test Case Audit`，在整個 repo 中找不到任何對應的 skill、command 或 artifact，屬於當時的構想而非落地機制。

這件事本身就是最好的文章題材：一個被公開描述過的機制，因為量測到採用率只有 1/26 而被作者自己砍掉，改成「執行中即時攔截」。但目前網站上沒有任何地方交代這件事。

**發現二：repo 的重心已經從「把票測完」移到「怎麼相信 AI 說測完了」。**

11 步主線仍在，但近三個月長出來的東西幾乎全是驗證與治理：執行帳本（`scripts/ledger.py`）、executor 入帳 manifest、Stop hook 收工檢查、交付物驗收 subagent、trace taxonomy、Shared Change Review Gate、上線前回歸集。這些機制的共同問題不是「AI 會不會做」，而是「AI 做完之後，我憑什麼相信它」。

現有文章與草稿的七篇規劃，完全沒有涵蓋這一整塊。原規劃的第 06 篇「如何驗證 AI 的品質？」只有 23 行大綱，而這塊現在是 repo 裡證據最密的區域。

**發現三：兩篇已完稿的文章躺在 `docs/articles/` 沒有上架。**

`how_ai_understands_requirements.md`（288 行）與 `how_to_build_ai_qa_knowledge_recycling.md`（388 行，另有 fact-checked 標註版 373 行）都是完整成稿，狀態 `status: draft`，網站上沒有對應的 HTML。網站的 portfolio 只有一篇文章、上下篇導覽兩邊都是 `Coming Soon`。

### 1.2 對網站定位的判斷

從「QA 漫畫 / 個人作品集」提升成「AI-Assisted QA Engineering Lab」，repo 的材料是夠的，但要換一組分類軸。

目前網站用兩套軸線描述這個系統：漫畫 15 話的「能力」標籤，以及 `architecture.html` 的「八種角色一條資訊流」。兩套都是**能力盤點式**的——列出有什麼。Senior SDET 與 QA Lead 看能力清單不會產生信任，因為能力清單任何人都寫得出來。

真正有辨識度的軸線是**失敗驅動**：某個治理機制之所以存在，是因為某次交付真的出過事。repo 裡這種因果鍊完整、有票號可回溯的案例至少有 16 條（見第 6 節），而且每一條都有 commit、有 worklog、有規則落點。這是別人抄不走的部分。

### 1.3 建議

1. 先把兩篇完稿文章做一次事實校正後上架，成本最低、立刻讓 portfolio 從 1 篇變 3 篇。
2. 下一篇**新寫**的文章寫「憑什麼相信 AI 說測完了」——證據紀律與交付物驗收（理由見第 10 節）。
3. 已發布文章的 `/jira-tc` 那段需要處理，但不是刪掉，而是改寫成「這個機制後來被我砍了」，並在新文章裡展開。這比默默修掉有價值得多。
4. Series numbering 現在是「檔名 01、標題 03」的錯位狀態，本次不動；建議等 Series 2.0 架構確認後一次性重編（處理方式見第 3.4 與第 9 節）。

---

## 2. Current AI QA System Map（現在真正運作的系統）

### 2.0 狀態標記定義

| 標記 | 定義 |
|---|---|
| **Current** | 有實作、有規則、正在用 |
| **Evolved** | 機制還在，但形態已與早期文件描述不同 |
| **Deprecated** | 明確標記廢止或已被取代，僅留歷史脈絡 |
| **Experimental** | 有實作但未進主流程 / 未合併 / 樣本數極少 |
| **Planned** | 文件描述了但沒有實作 |

### 2.1 Execution Layer（票怎麼被測完）

| 機制 | 狀態 | 實作位置 | 說明 |
|---|---|---|---|
| 11 步主線 | Current | `docs/PROJECT_RULES.md`（259 行） | 唯一 Execution flow。硬規則正本，明確宣告「沒有第二套並行流程」 |
| Assurance checkpoint（5 個 + DoD） | **Evolved** | `docs/OW_TICKET_SOP.md` | 前身是 Gate 0-5。現在改為「掛在 11 步節點上的驗收點」，明確聲明不構成第二條流程 |
| Manual-only 分支 | Current | `PROJECT_RULES` + `OW_TICKET_SOP` | 判定 manual-only 可免 POM / bdd-steps / 自動化 report，但 TC、執行結果、evidence、executor 入帳仍必備 |
| 票面採集（3 個子 gate） | Current | `scripts/fetch_ow_ticket.py` + `/pm` | 抓票 → 整理 → 依風險審閱定稿（`review_status: reviewed` / `ai_drafted`） |
| Reuse Audit 前置 | Current | `docs/EXPLORE_GUIDE.md` + `reuse-audit` subagent | 硬規則：Reuse Audit 未完成不得開 playwright-cli |
| POM / Component 分層 | Current | `pages/`（34 支 .py）+ `docs/POM_GUIDE.md` | 硬規則：test 檔不得出現 `.locator()` |
| pytest-bdd | Current | `tests/`（19 支票 test）+ `features/`（41 支 .feature） | 只實作 test plan 標記本次自動化的 scenario |
| 交付物規模 | Current | — | `docs/tickets/`：69 份 test_cases、9 份 test_plan；`docs/features/`：9 份；`docs/product/`：62 份 |

### 2.2 Assurance / Evidence Layer（怎麼相信結果）

這是近三個月成長最快的一層。

| 機制 | 狀態 | 實作位置 | 說明 |
|---|---|---|---|
| 報告資料合約（JSON 先於 PDF） | Current | `reports/schema/qa_report.schema.json` + `scripts/render_report.py` | pytest 只產 JSON，PDF 手動渲染；產 PDF 前必過 `validate_report_data.py` |
| 執行帳本（execution ledger） | Current | `scripts/ledger.py` | 每個 TC 帶 append-only `executions[]`；四個寫入者共用 file lock；who 由環境變數自動判定，**禁止 default 成人名**（註解原文：「錯誤歸因比沒記帳更毒」） |
| ad-hoc 實測記帳 | Current | `scripts/qa_probe.py` | 把「發 API 請求」與「記帳＋存證據」綁成同一個動作，AI 無法只做前者 |
| executor 入帳 manifest | Current | `docs/tickets/_executors.json` | 42 張票有紀錄，其中 15 張標 `AI（Claude Code）`。看板「AI測」chip 的唯一來源 |
| Evidence Board（常駐 hub） | Current | `scripts/serve_evidence_board.py` + `build_evidence_board.py` | 單票板 / sprint 板；chip 區分「草稿 / 測試案例 / AI測」；同時是 PDF by-sprint 落點的唯一決定者（寫 `reports/_sprint_map.json`） |
| 交付物驗收 subagent | **Experimental** | `.claude/agents/report-verifier.md` | 只讀不改，逐頁開 PDF、逐張開截圖肉眼檢查。**未被任何 rule 或 command 引用**，目前靠人記得叫它 |
| Stop hook 收工檢查 | Current | `scripts/hooks/stop_deliverable_check.py` | 檢查三件事：executor 有沒有入帳、registry 有沒有回補、report 是不是一張截圖都沒有 |
| AI 自主性 trace | Current | `eval_trace/*.jsonl`（180 筆事件） | 事件型別：`human_delegate_to_ai` / `ai_fallback_to_human` / `ai_run_completed`；帶 `reason_type` 分類 |
| reason_type taxonomy | **Evolved** | `serve_evidence_board.py` + `EVALUATION_GUIDE` | 2026-07-08 新增 `process_reuse_miss`（「未使用現有資源」），把「資源缺口」與「流程未遵守」分開統計 |
| Usage dashboard | Experimental | `scripts/usage_dashboard.py` | 讀本機 session log 出 HTML/CSV，只取 usage metadata |

### 2.3 Governance Layer（規則怎麼被約束）

| 機制 | 狀態 | 實作位置 | 說明 |
|---|---|---|---|
| Agent Doctrine（判斷力層） | Current | `docs/AGENT_DOCTRINE.md`（194 行） | 七章：證據紀律 / 失敗分類學（6 類）/ 喊 bug 四關門檻 / 兩次停損 / 入口導航紀律 / context 經濟 / 模型強度自我校準。每條附來源票號 |
| Shared Change Review Gate | Current（2026-08 新增） | `PROJECT_RULES` | 判準一句：「其他票不改任何一行，行為或產出會不會變？」；分類依據是影響面不是檔案位置；PR 必須附回歸驗證前後對照 |
| Command / Skill 治理 | Current | `docs/AGENT_GOVERNANCE.md` + `COMMAND_SKILL_MAP.md` | `.agents/skills/`（22 個）是共用 source；`.claude/commands/`（19 個）與 `.codex/` 只是薄 wrapper |
| Permission baseline | Current | `docs/discuss/PERMISSION_BASELINE.md` | allowlist 從 125 條收斂到 42 條後定為基準線；明文禁止廣義 pattern（`python3 *`、`curl *`）與內嵌敏感值 |
| 跨 agent 共識流程 | Current | `docs/CROSS_AGENT_CONSENSUS_GUIDE.md` + `/lead-agent` | Claude Code 為預設 lead，透過 Codex plugin 呼叫；最多三回合取得共識或列出分歧交 Sunny；紀錄一律進 `docs/discuss/`（36 份） |
| Eval 不得自動觸發 | Current | `docs/EVALUATION_GUIDE.md` | 硬規則：agent 不得靜默產出 eval report、不得自行宣告 eval 通過 |
| Knowledge Governance | Current | `docs/KNOWLEDGE_GOVERNANCE.md` + `KNOWLEDGE_MAP.md` | 治理規則（更新優先於新增、canonical/derived/superseded 六種權威狀態）與 routing 表分家 |

### 2.4 機械化防線（不靠 AI 自願想起的那一層）

這一層是「規則寫在文件裡不夠」的直接回應。

| 機制 | 狀態 | 實作 | 攔什麼 |
|---|---|---|---|
| CI 靜態稽核 | Current | `.github/workflows/qa-audit.yml` | 四關：硬規則 lint、PYTHON_FILE_INDEX 完整性、report layout、report JSON schema。**不跑 E2E、不需 secrets、不連外部服務**。註解明說「hooks 只約束 Claude Code，本 CI 對所有 agent 一視同仁」 |
| 硬規則 lint | Current | `scripts/lint_test_rules.py` | test 檔禁 `.locator()`、禁 `full_page`、feature Background 禁登入、禁寫死登入；R005 擋引用不存在的 feature 檔 |
| pre-commit hook | **Evolved** | `.githooks/pre-commit` | 只攔「DB 連線形狀」四種（env 賦值、DSN URI、受管主機、私網 IP）。2026-07-08 刻意收斂——原本泛抓所有網域是假警報來源 |
| PostToolUse hook | Current | `scripts/hooks/post_edit_py_check.py` | 改 `.py` 就跑 index 稽核；改 tests/feature 就跑硬規則 lint；exit 2 + stderr 讓 Claude 自己修 |
| SessionStart hook | Current | `scripts/hooks/session_start_check.py` | 開工先報 git status / worktree / 落後 remote |
| Make 入口 | Current | `Makefile` | `verify` / `lint` / `audit-reports` / `report OW=` / `seed`；permission baseline 規定常用流程走 make 而不逐條授權底層指令 |

### 2.5 Knowledge Layer（知識怎麼進來、怎麼不爛掉）

| 機制 | 狀態 | 實作 | 說明 |
|---|---|---|---|
| 知識回收（執行中攔截） | **Evolved** | `.agents/skills/qa-thought-capture/` | 三條攔截門檻（非顯然 / 可複用 / 決策形狀）＋一句話判準「這個判斷會不會改變未來 agent 對類似情境的決定？」；**儲存永遠要人逐條點頭，無默認同意**；裁決記入 `docs/QA_CAPTURE_CALIBRATION.md` 讓自動採集越採越準 |
| 產品知識四段 pipeline | Current | `spec-research` → `spec-backfill` → `spec-review` → `spec-promote` | 草稿落 `docs/product/inbox/`，研究痕跡進 `_provenance/`；完成標準是「刪掉 Reference 仍能回答六個產品問題」；人明說 promote 才搬正式目錄 |
| Memory 對帳 | Current | `.agents/skills/memory-triage/` | 定期盤點 Claude memory，該進 repo 的歸位，memory 端留指標 |
| Registry | Current | `pages/_registry/`（35 份） | 硬規則：playwright-cli 走過的頁面必須沉澱 registry，「report 產了但 registry 沒回補，視為知識回補未完成」 |
| QA Heuristics | Current 但薄 | `docs/QA_HEURISTICS.md`（48 行） | 只收 what to check 的抽象角度，不複述特定票事實。條目偏少，是實際採集量的反映 |
| Seed 能力庫 | Current | `seeds/`（order_factory、pms_seed_manager、scenarios yaml、4 份 API catalog） | 單位是「可重用測試情境製造能力」不是「某張票的資料」；禁以 OW-xxxx 為主要入口命名 module |
| 使用手冊（衍生層） | Current | `docs/manual/` + `/user-tutorial-page` | 從 `docs/product/` 改寫成任務導向手冊，濾掉票號與 QA 痕跡 |
| Context 經濟 | Current | Doctrine 第 6 章 + 兩支 subagent | 搜尋外包給 `reuse-audit`；禁整資料夾全讀；大量 Jira 查詢走 REST `/search/jql` 不用 MCP |

### 2.6 上線前回歸集

| 機制 | 狀態 | 實作 |
|---|---|---|
| 回歸集 | **Experimental（未合併）** | `docs/REGRESSION_GUIDE.md` + `tests/regression/`，在未合併分支 `test/regression-suite`（worktree `~/my-playwright-worktrees/regression-suite`） |

內容值得單獨記錄，因為它是整個 repo 裡設計最完整的一塊：

- **Journey 樹（J1-J6）給人看，domain 字彙表（ACCESS/BOOKING/ORDER/ROOM/STAY/MONEY/PRICING/CUSTOMER）當案例身分**。刻意分開的理由寫在文件裡：`tc_id` 是報告 JSON 的 upsert 主鍵，journey 一重排 tc_id 就變，舊條目變孤兒、歷史比對斷掉。identity 不綁敘事順序。
- **接力（golden path）**：同一張訂單依序走訂房 → PMS 接單 → 排房 → 收款 → 入住 → 退房。不拆成獨立 smoke 的理由是「每段各造一張前置訂單就不是同一張單，最容易壞的接縫反而測不到」；不塞成一條超長 scenario 的理由是「失敗只會報 Golden Path 掛了，看不出斷在哪段」。
- **`chain_guard` fixture**：前段紅了本段標略過並寫明卡在哪段；但**跳著挑段跑會直接紅**——刻意不是略過，因為略過會讓該驗的段靜默消失、涵蓋率掉了沒人知道。
- **xdist 平行直接 raise**，不讓它靜靜跑成一堆略過。
- **測資紀律**：一律走 `pms_seed` fixture，禁止在回歸案例裡直接呼叫 seed CLI（CLI 建的單不進 ledger、清不掉）。文件裡有一張「清得掉 / 清不掉 / 一定清不掉」的邊界表。
- **已知不穩清單**（yellow 分類）：兩條，各帶症狀、起始日、狀態，規則是「超過兩輪還在就必須修或移出集」。
- **已知覆蓋缺口表**：9 條，每條寫明「現況 / 補的方式」，其中一條原文寫著「**不要宣稱『取消功能』已受把關，只有非代收那條受把關**」。
- **新增 smoke 前四問**：會擋 release 嗎 / business outcome 一句話講得完嗎 / 測資能自建自清嗎 / 有依賴固定單號日期嗎。反例點名 `tests/test_OW4714.py`（寫死 5 個 release 單號，現在已經跑不動）。

### 2.7 測 AI 產品的 eval harness

| 機制 | 狀態 | 實作 |
|---|---|---|
| chat AI 自動化 eval | **Experimental** | `evals/chat_ai/`（DESIGN.md、runner.py、judge.py、assertions.py、dates.py、test-cases.yaml、45 條題庫） |

這塊和「用 AI 做測試」是完全不同的問題：被測對象本身是 LLM。設計上的判斷值得記錄：

- **選 `/v1/chat/completions` 而不是 `/api/chat` 當測試入口**，理由是兩條 path 收斂到同一顆推論引擎；`/api/chat` 只是外面加了限流閘與 session store。並明確列出 `/v1` 覆蓋不到的三項（限流閘、真實 session store、前端渲染）交給少量 UI smoke。
- **壓浮動**：`temperature=0`；語意類 case `repeat: 3`，三次不一致標 **FLAKY 並視同失敗**。
- **時鐘注入是測試專用能力，需受限**：僅 dev/release 可注入，production 一律禁止；RD 完成改造前 runner 強制用實際跑測日，否則丟 SetupError → case 標 ERROR，避免相對日期悄悄對不上還假 PASS。
- 分層：能精準斷言的走精準判，理解與多輪語意才用 judge。

### 2.8 Deprecated（明確廢止，只留脈絡）

| 項目 | 廢止時間 | 取代者 | 為什麼重要 |
|---|---|---|---|
| QA Thought Collector（測前 intake / AI Understanding Mirror） | 2026-06-15 | `qa-thought-capture`（執行中攔截） | **採用率 26 票僅 1 票**。這是「憑量測結果砍掉自己設計的機制」的完整案例 |
| Gate 0-5 命名與流程 | 2026-07 前 | Assurance checkpoint | 從「關卡」改成「掛在步驟出口的驗收點」，避免變成第二套流程 |
| `AGENTIC_WORKFLOW_ENHANCEMENT_PLAN.md` | 標 draft/proposal | `PROJECT_RULES` + `OW_TICKET_SOP` | `IMPROVEMENT_BACKLOG` 直接稱它為「殭屍計畫」的前車之鑑 |
| `PHASE2_GATE_CONTRACT_AUDIT.md` | 標 historical | 同上 | 2026-06-03 的稽核紀錄，結論是「Phase 2 尚未完成」 |
| 報告 per-ticket 資料夾 | 2026-07 | by-sprint 結構 | PDF 直接放 `reports/<sprint>/qa report/`，不再分票夾 |
| Postman collection 當 API 規格來源 | — | 後端 repo 原始碼 | Doctrine 第 3 章第 3 關的來源票就是這個（拿過期 collection 猜欄位繞了 6 發） |
| `playwright-cli --storage-state` | 0.1.13 起 | `.playwright/cli.config.json` | 傳了只印 help 不報錯，會變成沒登入的空 session |

### 2.9 Planned but not implemented（文件寫了、實作沒有）

這一節必須誠實，因為它直接決定哪些文章現在寫不了。

| 項目 | 文件位置 | 實際狀況 |
|---|---|---|
| `/eval OW-xxxx` command | `EVALUATION_GUIDE` 通篇假設它存在 | `.claude/commands/` 裡**沒有** eval 檔案。`eval/` 目錄只有 1 份實例（`OW-4468_eval_report.md`）＋1 份 template |
| 五層 eval 框架的常態運作 | `EVALUATION_GUIDE` | 樣本數 1。寫成文章會變成描述一個沒在跑的框架 |
| Decision Layer | `AI_QA_SYSTEM_LAYERS` 討論第 7 層 | 明確記載「尚未實作」。Sunny 想要一層能在規則不足時做取捨的機制，目前是人在做 |
| Maintenance 固定制度 | 同上第 6 層 | 有局部機制（supersede/delete、frontmatter 規範、python index 稽核），缺「定期掃過時知識 / 找重複規則 / 合併 product docs」的固定週期 |
| Reuse Audit 強制 gate | `TRACE_REASON_TAXONOMY` 尚未決定段 | 目前只做到「讓失敗可見」（trace taxonomy），沒有 PreToolUse hook 擋下未做 Reuse Audit 就開 playwright |
| Test Case Audit | 已發布文章提到 | repo 中查無此機制。TC 品質把關實際散在 `/jira-tc` 標記原則、test plan checkpoint 與人工審閱 |
| Requirement Audit（作為獨立 skill） | 已發布文章提到 | 查無此 skill。需求層的把關現在在 step 1 的「依風險審閱定稿」＋ step 4 的 Spec Ready checkpoint |
| Flaky test 治理 | 漫畫第 06 話標為能力 | **沒有** `pytest-rerunfailures`、沒有 retry 設定、沒有 quarantine 機制。現有的只有：回歸集的「已知不穩清單」＋ `diagnose` skill 要求先建可重現 loop 再修 |
| `report-verifier` 進主流程 | agent 定義存在 | 沒有任何 rule / command 引用它 |

---

## 3. Original Article Series Archaeology

### 3.1 原始規劃：七篇

證據在 `docs/drafts/`，檔名自帶編號，是原始規劃的直接證物。

| Series | 原始主題 | 狀態 | Evidence |
|---|---|---|---|
| 01 | 為什麼 QA 需要 AI？ | **未完成**（15 行問題清單） | `docs/drafts/01 為什麼 QA 需要 AI？.md`。內容是四個待答問題＋一句核心論點「人類時間很貴，不該浪費在規則檢查」 |
| 02 | AI 可以幫 QA 做什麼？ | **未完成**（21 行） | `docs/drafts/02 …`。只有「AI 很適合 / AI 不適合」兩張清單 |
| 03 | 如何讓 AI 參與測試流程？ | **已發布** | `docs/drafts/03 …`（671 行，含 155 行寫作大綱＋完稿）→ `portfolio/ai-qa-series-01.html` |
| 04 | AI QA 的治理與知識管理 | **部分轉化**（47 行思考稿） | `docs/drafts/04 …`。其中「知識回收」那半被獨立寫成完稿（見 3.2）；「治理」那半仍未寫 |
| 05 | 哪些決策該交給 AI？ | **未完成**（30 行） | `docs/drafts/05 …`。核心觀察：「這其實已經超過 QA，變成怎麼管理代理人」 |
| 06 | 如何驗證 AI 的品質？ | **未完成**（23 行） | `docs/drafts/06 …`。點名 Dogfood / Flaky / Evidence Board / Cross-Agent Debate 四個題材，收尾句「測試你的測試的測試」 |
| 07 | 如何讓 AI 理解需求？ | **已完稿、未發布** | `docs/drafts/07 …`（384 行）→ `docs/articles/how_ai_understands_requirements.md`（288 行成稿） |

### 3.2 額外存在、不在原編號內的完稿

| 檔案 | 行數 | 狀態 | 對應原規劃 |
|---|---|---|---|
| `docs/articles/how_to_build_ai_qa_knowledge_recycling.md` | 388 | 完稿、未發布 | 04 的「知識管理」半邊 |
| `docs/articles/how_to_build_ai_qa_knowledge_recycling_fact_checked.md` | 373 | 完稿的 fact-check 標註版 | 同上 |

fact-checked 版本值得單獨講：它用四級標註（`[已落地事實]` / `[從 repo 推導]` / `[作者反思]` / `[待補真實案例]`）逐句檢查文章主張，並附一張「文章主張 ↔ 事實強度 ↔ Repo 依據」對照表。這個做法本身就是 AI QA 的證據紀律套用到寫作上，是可以寫成文章的方法論。

### 3.3 現有文章內對未來文章的引用（承諾清單）

已發布文章明確承諾了三處，目前全部未兌現：

| 文章內原文 | 指向 | 現況 |
|---|---|---|
| 「因此我把這個主題獨立放到系列第五篇：《哪些決策該交給 AI？》」 | 05 | 未寫（30 行大綱） |
| 「而這些內容，也是下一篇：《AI QA 的治理與知識管理》要討論的主題」 | 04 | 半邊完稿未發布，治理半邊未寫 |
| 「因此我有自己的 Selector 優先策略與 Page Registry。這部分之後會另外展開」 | 未編號 | 未寫。registry 現有 35 份，材料充足 |

另外文章結尾列出「目前仍然持續調整的部分」四項：Requirement Audit、Test Case Audit、Evidence Board、Cross-Agent Review。這四項現在的真實狀態是：前兩項不存在、第三項已成常駐 hub server、第四項已制度化成 `/lead-agent` ＋三回合停損。

### 3.4 為什麼檔名是 series-01、標題是系列 03

盤點結論（有 git 證據）：

1. `docs/drafts/` 的 01-07 是**原始七篇規劃編號**，早於任何發布。
2. 實際第一個寫完並上架的是規劃中的第 03 篇。
3. 上架時**檔名用「第幾篇發布」編號（01），標題用「原規劃第幾篇」編號（03）**，兩套編號在同一個檔案裡打對台。
4. git 歷史佐證發布順序：`e89b4f1 Add AI QA portfolio article` → `0f9ece0 Refine AI QA article presentation` → `781c1e2 docs: 從 my-playwright 搬入 AI QA 文章（完稿 articles + 草稿 drafts）`。文章先上架，草稿與完稿是**後來才從 my-playwright 搬進網站 repo** 的——所以上架當時，網站 repo 裡看不到那套 01-07 編號，錯位是在這個時間差裡發生的。

沒有 Series 01 / 02 的草稿以外內容，也沒有它們的 HTML。`portfolio/index.html` 只列一篇，上下篇導覽兩邊都是 `Coming Soon`。

### 3.5 哪些規劃已經被 my-playwright 的演進弄過時

| 原規劃 | 過時的部分 |
|---|---|
| 03（已發布） | `/jira-tc` 內含 AI Mirror Understanding + Requirement Audit 兩個 skill——**已廢止**。流程圖缺 Assurance checkpoint、缺 Reuse Audit、缺 executor 入帳與 registry 回補這兩條收尾硬規則 |
| 04 治理半邊 | 當時只有 Project Rules / Registry / SOP / Governance / Dogfood 五個詞。現在多出 Shared Change Review Gate、permission baseline、CI 四關、三個 Claude hook、KNOWLEDGE_GOVERNANCE 六種權威狀態 |
| 04 知識半邊（完稿） | 完稿寫的分流表少了 `docs/AGENT_DOCTRINE.md`（2026-07-13 才建，現在是「how to behave」的正本），也沒有四段 spec pipeline 與 `memory-triage` |
| 06 | 點名的 Flaky 現在仍**沒有**治理機制（見 2.9）；Evidence Board 已從原型變成常駐 hub；Dogfooding 的真正實例其實是 `evals/chat_ai`，不是原本想的 retro |
| 全系列 | 缺一整層「執行帳本 / executor 入帳 / trace taxonomy / 交付物驗收」——這層在七篇規劃裡完全沒有位置 |

---

## 4. Existing Article Writing DNA

分析對象：`portfolio/ai-qa-series-01.html`（成稿）＋ `docs/drafts/03 …` 的 155 行寫作大綱（作者自訂的規則，比成稿更能說明意圖）。

### 4.1 可量測的形式特徵

| 特徵 | 觀察 |
|---|---|
| 段落長度 | 極短。大量段落是**一句話一個 `<p>`**，例如「AI 負責理解與執行。」「人類負責確認與決策。」連續三到五個單句段落形成節奏 |
| 章節長度 | 每個 `<h2>` 底下約 8-20 個短段落，讀完一節約 30 秒 |
| 分節符號 | 每節之間一律 `<hr>`。全文 10 節、9 條分隔線 |
| 清單使用 | 用在真正並列的項目（產出物、檢查項、改變前後對照），不用來鋪陳論述 |
| code block | 4 處，全部是**流程圖或真實產物**：pipeline ASCII 圖、Gherkin feature 片段、執行階段 ASCII 圖、拆步驟 ASCII 圖。沒有一段是為了展示技術而貼的 code |
| 引用（blockquote） | 只用來包「某個角色說的一句話」——AI 的理解、人類的補充 |
| 佔位標記 | 3 處未填：`【插入 AI 理解 → 人類修正的真實對話】`、`【插入報告資料夾結構】`、`【插入 PDF 報告縮圖】`。作者刻意留白等真材料，沒有拿文字硬湊 |
| 閱讀時間標示 | 「約 7 分鐘閱讀」，放在標題下的 meta 區 |

### 4.2 敘事骨架（作者自訂，寫在大綱裡）

大綱明確定義六段結構，成稿完整遵守：

```
0. 開場痛點（3-5 句，具體場景，不講大道理）
1. 先給全貌：一張流程圖（整篇靠這張圖撐起來）
2. 逐站拆解（每站對應一個真實機制）
3. 串起管線的東西（點到為止，深入留給下一篇）
4. 結果與取捨（誠實的代價）
5. 如果重來會怎麼做（大綱原文標註：「最值錢、最少人寫」）
```

大綱裡還有一份**邊界守則**，四條全部是「這個題目不屬於本篇」：

> 「AI 能做什麼 / 不能做什麼」是 02 的事 → 這篇不要再列能力清單。
> 「哪些決策該交給 AI」是 05 的事 → 這篇的人類確認步驟只描述流程上發生了，不展開為什麼。
> 「Rules / Registry / SOP 怎麼設計」是 04 的事 → 這篇只說管線跑在這些軌道上，點到為止。

這是整份 Writing DNA 裡最該保留的機制：**每篇文章都先寫一份「不寫什麼」清單**。它是文章不膨脹成教科書的唯一防線。

### 4.3 語氣特徵

**第一人稱的使用方式**：全程「我」，但「我」永遠在做具體動作或承認具體侷限，不用來宣示成果。

- 動作型：「我會閱讀 AI 的分析結果，補充它漏掉的地方」「我把這個主題獨立放到系列第五篇」
- 承認型：「以前這些思考只存在我腦中。做完測試就消失了。」
- 沒有出現過的句型：「我建立了一套完整的……」「我成功地……」

**如何從真實問題進入技術**：先給一個 QA 讀者立刻認得的場景，再翻轉。

> 花半小時讀 Ticket / 花一小時翻歷史資料 / 最後發現需求根本沒寫清楚

這三行之後才出現第一個技術名詞。技術名詞永遠**後於**痛點出現。

**如何描述 failure**：failure 是文章的主軸而非插曲。開場標題直接是「我把 AI 丟進測試流程後，第一個月就翻車了」。翻車的描述方式是「機制沒有生效的後果」，不是「AI 很笨」——例如「如果一開始對需求理解錯了，後面做得再完整，也只是把錯誤放大而已」。

**如何介紹 mechanism**：固定四拍。

1. 這一步做什麼（一句）
2. 產出什麼（清單）
3. **這步真正的價值不是省時間，而是……**（翻轉句，全文出現多次）
4. 一個具體例子

第 3 拍是這篇文章最有辨識度的招式。範例：「這一步最大的價值其實不是省時間。而是把需求中的模糊地帶挖出來。」

**如何做 reflection**：集中在最後兩節，而且是**帶代價的反思**，不是心得感想。

> 但代價也很明顯。這條 Pipeline 本身需要維護。AI 並不會因為接上流程就突然變聰明。相反地。很多時間其實花在：「如何避免 AI 一直犯同樣的錯。」

**如何避免變成教科書**：不定義術語。POM、Gherkin、Selector、stop loss 全部直接使用，靠上下文自明。沒有「什麼是 X」段落。

**如何避免變成 AI marketing**：三個明確的自我約束（從成稿反推）。

1. 不給效率數字。全文沒有任何「省下 X%」「快 X 倍」。改變被描述為「資訊流動方式改變了」。
2. 每個成果後面接一個代價。
3. 未完成的東西直接說未完成（「目前仍然持續調整的部分包含……」）。

**如何呈現「我實際做過、踩過坑、後來才理解」**：靠**時間差句式**。

- 「這也是我後來發展 QA Thought Capture 的原因。」
- 「我發現：這一步其實不是在修正 AI。而是在把 QA 的直覺轉換成可重用的規則。」
- 「因為我後來發現，AI 最大的問題不是不會寫程式。而是不知道自己不知道什麼。」

句式固定是：**當時我以為 A → 後來發現其實是 B**。B 永遠比 A 抽象一層。這是「踩過坑」的文字證明，比任何自我宣稱都有效。

### 4.4 給後續文章的 DNA 檢查清單

寫完任何一篇新文章，逐條打勾：

- [ ] 開場 5 句內出現一個 QA 讀者認得的具體場景，且技術名詞尚未出現
- [ ] 有一張撐起全篇的圖或流程（ASCII 或 SVG），不是裝飾
- [ ] 有一份「本篇不寫什麼」清單，且在文中至少有一處明確把題目讓給另一篇
- [ ] 每個 mechanism 都有「這步真正的價值不是 X，而是 Y」的翻轉句
- [ ] 至少兩處「當時我以為 A，後來發現是 B」的時間差句式
- [ ] 每個成果後面接一個代價或侷限
- [ ] 沒有效率數字；沒有「完整的」「成功地」「一套完善的」
- [ ] 沒有術語定義段落
- [ ] 有一節「如果重來會怎麼做」
- [ ] 真材料（真實產物、真實對話、真實截圖）至少 2 處；沒有就留 `【插入…】` 佔位，不用文字硬湊
- [ ] 票號、旅館 ID、產品名、同事名已去識別化

---

## 5. Audience Needs

### 5.1 五類受眾真正想知道什麼

| 受眾 | 他真正的問題 | repo 裡回答得最好的部分 |
|---|---|---|
| **Senior QA / SDET** | 「這套東西我能不能抄？抄了會不會反過來咬我？」 | 硬規則 + 反例票號。他要的是「為什麼是這條規則而不是另一條」，以及規則失效時的症狀 |
| **QA Lead / EM** | 「導入這個要付什麼代價？人的角色怎麼變？怎麼跟老闆解釋品質沒有下降？」 | Assurance checkpoint 的人機分工、executor 入帳（誰測的說得清楚）、稽核用 PDF、Shared Change Review Gate |
| **想導入的工程團隊** | 「第一步該做什麼？哪些坑可以繞過？」 | 「如果重來一次」那類內容；四段 spec pipeline 這種可分階段導入的結構；permission baseline 這種可直接照抄的清單 |
| **Recruiter / Hiring Manager** | 「這個人的能力邊界在哪？他做的是工程還是操作工具？」 | 有沒有從失敗長出制度、有沒有量測、有沒有誠實標記自己沒做到的部分 |
| **對 Agentic QA 有興趣的 QA** | 「agent 到底哪裡會壞？壞了怎麼辦？」 | 失敗分類學六類、兩次停損、trace taxonomy、`process_reuse_miss` |

### 5.2 不該當分類軸的東西

**工具名不能當分類軸。** 「我用了 Claude Code / Codex / Playwright」對上述五類受眾都沒有資訊量——工具是可替換的，而 repo 自己的核心原則就寫著「Agent 可換，repo 才是真理來源」（`architecture.html` 原文）。用工具分類會讓文章在工具換版時整批過期。

**能力清單也不該當分類軸。** 現有網站已經有兩套能力盤點（漫畫 15 話標籤、architecture 八角色），再寫第三套只是重複。

### 5.3 該當分類軸的四個問題

1. **AI 原本在哪裡失敗？** → 每篇文章的入口
2. **我怎麼發現的？** → 這是 Senior 受眾唯一真正在意的部分，因為發現方法可遷移
3. **長出了什麼機制？** → 具體到檔案與規則，可驗證
4. **人保留了哪些決策權？** → QA Lead / EM 的核心關切

### 5.4 repo 能支撐、而且其他 domain 遷得走的設計判斷

這些是「非 QA 讀者也用得上」的部分，寫進文章能大幅擴大受眾：

| 設計判斷 | 為什麼可遷移 |
|---|---|
| 宣稱層級不得高於驗證層級 | 任何 AI 產出的驗收都適用。四級證據階梯（前端渲染 > API > DB > code 讀起來對）換個 domain 就是另一組階梯 |
| identity 不綁敘事順序 | 回歸集 tc_id 的設計理由。任何有主鍵與人類編號的系統都會踩到 |
| 記帳與動作綁成同一個操作 | `qa_probe` 的核心設計。任何要求 agent 留痕的場景都能用 |
| who 禁止 default 成人名 | 「錯誤歸因比沒記帳更毒」。所有稽核系統適用 |
| 影響面而非檔案位置決定審查層級 | Shared Change Review Gate。任何 code review 政策都適用 |
| 兩次停損 + 停損報告四要件 | agent 行為準則，與 QA 無關 |
| 讓失敗可見，先於強制擋下 | trace taxonomy 的漸進策略：先能觀測，再談 gate |
| 誠實的覆蓋缺口表 | 回歸集的 9 條缺口表。任何「我們測過了」的宣稱都該附這張表 |
| 採用率不足就砍掉自己的設計 | intake 26 票 1 票 → 廢止。這是產品思維套在內部工具上 |

---

## 6. Failure → Mechanism Map

以下每條都能在 repo 找到票號與落點。這是整份盤點裡最有文章價值的一節。

| # | Failure / Problem | 實際發生了什麼 | 長出的 mechanism | Lesson |
|---|---|---|---|---|
| 1 | **綠燈但零證據**（OW-4468） | pytest 全過、schema 驗證過、JSON 有截圖路徑，但截圖停在同一週、前後一模一樣。靠人反問「有檢查過嗎」才抓到 | Doctrine 第 1 章「green ≠ 可交付」；`report-verifier` subagent；Stop hook 的零截圖提醒；report `actual` 欄必須真值 | 自動化能驗格式，不能驗證據力。交付前必須有人（或一個只讀 agent）真的把檔案打開 |
| 2 | **read API 過了不等於功能過**（OW-4593） | seed 資料 read API 全回 `status=0`，前端格式檢查全擋，整批 14 張作廢 | Doctrine 證據等級階梯：前端渲染 > API > DB > code；宣稱層級不得高於驗證層級 | 「後端讀得到」與「功能正常」是兩句不同的話 |
| 3 | **軟刪除誤報 bug**（OW-4593） | 查 DB 漏過濾 `deleted_at IS NULL`，把舊單算進來，誤報「重複收款」 | 喊 bug 四關門檻的第 4 關（可重現關含查詢條件檢查）；`QA_HEURISTICS` 的資料判讀條目 | 誤報 bug 的成本是信任，不是時間 |
| 4 | **AI 測過但帳上沒有**（OW-4696、OW-3712、OW-4017） | AI 用 curl / playwright-cli 實測過，只在 worklog 手打片段，原始 request/response 沒落點。票被誤判成沒 AI 測過 | `docs/tickets/_executors.json` 入帳底線；`scripts/qa_probe.py`（發請求與記帳同一動作）；`scripts/ledger.py`（append-only executions[]、file lock、who 自動判定）；Stop hook 檢查未入帳；playwright-cli 沉澱 registry 底線 | 沒有記帳的執行等於沒有執行。而且要讓「不記帳」比「記帳」更麻煩 |
| 5 | **AI 跳過 Reuse Audit 從零寫 spike**（OW-3666） | 既有 `BalanceComponent`、`OrderDetailPage`、團單 POM 都能用，AI 直接開 raw Playwright spike，6 區只完成 2 區就卡死 | trace 新增 `reason_type: process_reuse_miss`（「未使用現有資源」）；`reuse-audit` subagent 外包搜尋；Doctrine context 經濟章 | 「資源缺口」與「流程未遵守」要分開統計，否則改善方向會被誤導 |
| 6 | **測前 intake 沒人用**（26 票 1 票） | 設計了「AI Understanding Mirror → 人類補充 → knowledge snapshot」四段式測前流程，實際只有 1 票產出 | 整套廢止；改成 `qa-thought-capture` 執行中即時攔截，因為「很多 QA 直覺不是測前想出來的，而是測到一半才冒出來」 | 知識採集的時機決定採用率。設計得再漂亮，時機錯了就是零 |
| 7 | **同一問題磨五次**（OW-4300 DatePicker） | 連續換五種 selector / keyboard 打法，實際是 Vue component 綁定結構問題 | 失敗分類學六類（先分類再修）；兩次停損規則；停損報告四要件 | 分類錯，修的方向就錯。第一個問題是「這屬於哪一類」不是「怎麼修」 |
| 8 | **拿自動化硬磨 manual TC**（OW-4338） | TC 從 test plan 起就標 manual，仍用 playwright-cli 硬磨 el-select，而人早已手動測完 | Manual-only 票的流程分支；「人類 5 秒可解的交給人類」；AI 做前置與報告不硬跑 | 人機分工要寫進流程，不能靠 agent 當下判斷 |
| 9 | **站錯入口就宣告不可行**（OW-4836） | 在審核端找「新增合約」找不到就斷言做不到；實際新增走合約列表的「複製合約」，入口完全不同 | Doctrine 第 5 章入口導航紀律；宣告不可行前的四項 checklist | 「新增」與「修改」常是不同入口。宣告不可行前先確認站對地方 |
| 10 | **grep 沒中就當沒有**（2026-07-02 切旅宿） | 只 grep 沒讀檔，跟 bootstrap-select 搏鬥三輪，還把錯誤結論寫進 registry | 「卡導航先整份讀 registry」；`sidebar.md` 與 `common.md` 兩份通用檔規定整份讀 | 關鍵字搜尋會漏（「旅館 ID 透過 localStorage 設定」不含 switch 字樣）。錯的結論寫進知識庫比沒寫更貴 |
| 11 | **allowlist 長到 125 條、含明文 API key** | 授權清單從 40 條漲到 125 條，混入一次性垃圾、廣義 pattern、一條含明文 Redmine API key 的 curl | `PERMISSION_BASELINE.md`（收斂到 42 條定為基準）；七條維護原則；常用流程走 make 入口不逐條授權 | 權限清單會自然膨脹。沒有基準線就沒有「該砍了」的判斷點 |
| 12 | **共用改動直推 main 影響所有票**（OW-4945） | 改 `pdf_reporter.py` 讓「執行時間」欄在無值時不輸出，所有票的報告版面都跟著變，當時直推 main | Shared Change Review Gate（三問法 + PR 必附回歸驗證前後對照）；判例寫進 PROJECT_RULES | 分類依據是影響面不是檔案位置。而且要有判例，不只有規則 |
| 13 | **草稿卡在 feature 分支等於消失**（OW-4474 / 4493、sprint 43） | TC 草稿停在未合併分支被遺忘 | evidence board 草稿一產出就 commit push 到 main；草稿與已測的區分改靠 chip（`草稿` / `測試案例` / `AI測`）不靠 commit 時機 | 「等審完再合併」在多分支環境等於丟掉。改變的是判斷依據，不是紀律要求 |
| 14 | **寫死單號的測試會自己死掉**（`tests/test_OW4714.py`） | 寫死 5 個 release 單號，其中兩張還必須是「昨入今出、已入住」狀態，現在整支跑不動 | 回歸集「新增 smoke 前四問」；日期一律 runtime 挑（`find_bookable_window()`）；測資一律走 `pms_seed` fixture | 會回歸的才值得自動化；不能自建自清的前置一律不收 |
| 15 | **純 API 就出報告，畫面沒驗**（OW-4929） | TC 描述的是畫面行為，報告卻零截圖。schema 允許 `screenshot=null`（純 API 步驟合法）所以 validator 抓不到 | Stop hook 第 3 檢查：所有 step screenshot 皆為 null 時在收工點補問一句 | schema 合法不等於交付合格。合約管得住形狀，管不住意圖 |
| 16 | **腳本印 ✅ 但抄回死 token** | Sales token 腳本讀 HTTP code 判成功，實際 body 的 status 是失敗；2FA 是下游症狀不是原因 | 驗 token 要讀 body 的 status；「假成功比失敗更貴」 | 成功訊號的來源要選對層級。這是第 2 條的同一個病在另一個地方 |

### 6.1 這張表最值得寫成文章的三組

**組 A：假綠燈家族（#1 / #2 / #15 / #16）**
四條的病灶完全相同：**成功訊號來自比宣稱更淺的層級**。四條分別發生在截圖、API status、schema 合法、HTTP code 四個地方，卻長出同一組解——證據等級階梯 + 交付物肉眼驗收 + 收工檢查。這是最完整的一條演化線，也是 Senior SDET 最買單的題目。

**組 B：記帳家族（#4 / #5 / #13）**
共同問題是**AI 做了事但系統看不到**。解法的演化很漂亮：先要求（規則）→ 再讓失敗可見（trace taxonomy）→ 再把記帳綁進動作（qa_probe）→ 最後在收工點機械化檢查（Stop hook）。四個階段對應四種治理強度，可以直接畫成一張圖。

**組 C：自我否決（#6 / #11 / #12）**
共同點是**作者砍掉或收斂自己做過的東西**：廢掉採用率 1/26 的 intake、把 125 條授權砍回 42 條、把自己直推 main 的行為事後分類成漏判並寫成判例。這組對 Recruiter / Hiring Manager 的說服力最強，因為它證明的是判斷力而不是產能。

---

## 7. Proposed AI QA Series 2.0

### 7.1 設計原則

1. **每篇一個 failure 開場**，不從機制開場。
2. **不重複既有兩套能力盤點**（漫畫標籤、architecture 八角色）。
3. **材料不足就標明，不硬寫**。每篇附「材料是否足夠」判斷。
4. **保留原系列的承諾**：05（哪些決策該交給 AI）與 selector/registry 兩處承諾必須兌現，因為已發布文章寫了。
5. **不預設篇數**。以下 10 篇 + 2 篇候補。

### 7.2 分幕

```
第一幕 骨架（1-3）    一張票怎麼流過去，以及為什麼理解與知識是地基
第二幕 信任（4-7）    憑什麼相信 AI 說完成了
第三幕 邊界（8）      人保留哪些決策權
第四幕 工程（9-10）   從單票驗收長到上線把關，以及測 AI 產品
```

---

### S01｜一張 Ticket 如何流過 AI QA Pipeline（改版）

- **Core question**：一張票進來到產出報告，中間到底發生了什麼？
- **Target audience**：全部五類；這是 series 的入口
- **Why it matters**：現有已發布文章就是這篇，但有一段事實已廢止（`/jira-tc` 內含 AI Mirror + Requirement Audit）。不處理它，整個 series 的可信度會被這一段拖累
- **Repository evidence**：`docs/PROJECT_RULES.md` 11 步；`docs/OW_TICKET_SOP.md` 5 個 checkpoint；`docs/COMMAND_SKILL_MAP.md`
- **Related episode**：第 05 話「200 個 E2E」（Test Strategy）、第 09 話「重新檢視工作流程」
- **Key mechanisms**：11 步主線、Assurance checkpoint、Reuse Audit 前置、收尾兩條硬規則（executor 入帳 + registry 回補）
- **Main lesson**：固定的是交付物，變動的是測試深度
- **材料**：✅ 充足。**改版方式建議：不刪那段，改寫成「這個機制後來被我砍了，為什麼」並連到 S03**
- **依賴**：無，series 起點

### S02｜如何讓 AI 理解需求（上架已完稿）

- **Core question**：怎麼讓 AI 在動手前先把「它以為自己理解了什麼」攤開？
- **Target audience**：Senior QA / SDET、想導入的團隊
- **Why it matters**：已完稿 288 行，只需事實校正。核心論點（AI 最大風險是不知道自己不知道什麼）是整個 series 的地基
- **Repository evidence**：`docs/articles/how_ai_understands_requirements.md`；step 1 三個子 gate；`review_status: reviewed / ai_drafted`；Spec Ready checkpoint
- **Related episode**：第 10 話「失之毫里，差之千里」（Requirements Audit）、第 13 話「那隻兔子就像渣男」（Decision Checkpoint）
- **Key mechanisms**：confidence marker（查到的 / 推論 / 假設）、高風險票必經人工審閱、Doctrine 第 1 章宣稱分級
- **Main lesson**：理解錯了，後面做得越完整只是把錯誤包裝得越像真的
- **材料**：✅ 完稿。**校正項：文中「Requirement Audit」若指稱 skill 需改寫；補上 Doctrine 三級宣稱分級（文章寫作時該檔還不存在）**
- **依賴**：S01 之後

### S03｜知識回收：怎麼讓一次校正不蒸發（上架已完稿 + 補新機制）

- **Core question**：我花十分鐘糾正 AI，怎麼讓下個 session 不用重講？
- **Target audience**：Senior QA / SDET、QA Lead、想導入的團隊
- **Why it matters**：已完稿 388 行，且另有一份 fact-checked 標註版。但完稿寫於 2026-06-24，之後新增的機制（AGENT_DOCTRINE、四段 spec pipeline、memory-triage）都不在裡面
- **Repository evidence**：`qa-thought-capture` SKILL（三條攔截門檻 + 確認關卡 + 校準 log）；`docs/KNOWLEDGE_MAP.md`；`KNOWLEDGE_GOVERNANCE.md` 六種權威狀態；`QA_HEURISTICS.md`；`pages/_registry/`（35 份）；四段 spec pipeline
- **Related episode**：第 03 話「拯救苦命兔大作戰」（長期知識累積）、第 12 話「秘密小本本」（Single Source of Truth）
- **Key mechanisms**：一句話判準「這個判斷會不會改變未來 agent 對類似情境的決定？」；儲存無默認同意；supersede / delete；memory vs heuristics 的決勝語句（「這是要 AI 怎麼做事，還是 QA 檢查什麼」）
- **Main lesson**：回收不只是加，還要修剪。健康的知識庫要允許變小
- **材料**：✅ 完稿 + 需補三塊新機制。這篇也是**唯一可以順帶介紹 S06「採用率 1/26 砍掉 intake」的地方**
- **依賴**：S02 之後（文章開頭已寫「上一篇我寫如何讓 AI 理解需求」）

### S04｜憑什麼相信 AI 說「測完了」

- **Core question**：pytest 全綠、schema 過了、報告產出了——我憑什麼相信這份交付？
- **Target audience**：Senior QA / SDET（主）、QA Lead、Recruiter
- **Why it matters**：這是全 repo 證據最密的一塊，也是七篇原規劃完全沒有位置的一塊。而且它直接回答 Senior 受眾唯一在意的問題：怎麼驗證 AI 而不是相信它
- **Repository evidence**：`docs/AGENT_DOCTRINE.md` 第 1 章（含四級證據階梯與完成宣告 checklist）；`.claude/agents/report-verifier.md`；`scripts/hooks/stop_deliverable_check.py`（三項檢查含註解裡的來源票）；`scripts/validate_report_data.py`；`reports/schema/qa_report.schema.json`；OW-4468 / OW-4593 / OW-4929 三條
- **Related episode**：第 15 話「吃你的狗食」（Evaluation / Dogfooding）、第 01 話（報告自動化的起點）
- **Key mechanisms**：宣稱層級不得高於驗證層級；證據等級階梯（前端渲染 > API > DB > code）；`actual` 欄禁罐頭字；只讀 subagent 做交付物驗收；收工 hook
- **Main lesson**：「green ≠ 可交付」。自動化能驗格式，驗不了證據力
- **材料**：✅ 非常充足，是本次盤點中材料密度最高的題目
- **誠實揭露**：`report-verifier` 目前**沒有被任何 rule 引用**，靠人記得叫它。文章要寫成「機制存在但尚未進主流程」，不能寫成已閉環

### S05｜AI 說它測過了，但帳上查不到——執行帳本與記帳紀律

- **Core question**：怎麼讓「誰測的、測了哪段、用什麼方法、證據在哪」永遠查得到？
- **Target audience**：QA Lead / EM（主，這是稽核與交付責任問題）、Senior SDET
- **Why it matters**：這是 AI 參與交付後**新出現**的問題類別。傳統自動化沒有這個問題，因為執行者只有 CI
- **Repository evidence**：`scripts/ledger.py`（append-only executions[]、file lock、who 自動判定禁 default 人名）；`scripts/qa_probe.py`（三個 subcommand）；`docs/tickets/_executors.json`（42 票 / 15 AI）；evidence board chip 三態；Stop hook 第 1 檢查；OW-4696 / OW-3712 / OW-4017
- **Related episode**：第 14 話「偷偷改家規」（Traceability / Change Management）
- **Key mechanisms**：記帳與動作綁成同一操作；四個寫入者共用 file lock；who 禁止 default 成人名；治理強度四階（要求 → 讓失敗可見 → 綁進動作 → 收工檢查）
- **Main lesson**：錯誤歸因比沒記帳更毒。看起來像有帳，其實是假帳
- **材料**：✅ 充足，含 `ledger.py` 註解裡直接可引用的設計理由

### S06｜我砍掉了自己設計的機制：採用率 1/26 的教訓

- **Core question**：怎麼知道一個 AI 流程機制是真的在用，還是只是存在？
- **Target audience**：QA Lead / EM、想導入的團隊、Recruiter
- **Why it matters**：這是全 repo 最有辨識度的單一故事，而且是**產品思維套在內部工具上**。多數 AI QA 文章寫「我做了什麼」，沒人寫「我量了採用率然後砍掉」
- **Repository evidence**：`docs/QA_THOUGHT_COLLECTOR_GUIDE.md`（`status: deprecated`，原文「實測採用率極低（26 票僅 1 票產出）」）；`AI_MANAGEMENT_DISCUSSION_20260615_QA_THOUGHT_CAPTURE_REBUILD.md`；改版後的 `qa-thought-capture`；`PERMISSION_BASELINE`（125→42）；OW-4945 事後自我分類
- **Related episode**：第 09 話「重新檢視工作流程」、第 08 話「被罵過一次後」（Feedback Loop）
- **Key mechanisms**：機制採用率當汰除依據；知識採集時機從測前改成執行中；權限基準線；判例式治理（把自己的漏判寫成判例）
- **Main lesson**：設計得漂亮但沒人用的機制，比沒有機制更貴——它會讓人以為那件事已經有人管了
- **材料**：✅ 充足。**這篇同時是已發布文章那段過時描述的正式交代**

### S07｜規則寫在文件裡是不夠的：機械化防線

- **Core question**：AI 讀了規則卻沒照做，怎麼辦？
- **Target audience**：Senior SDET（主）、想導入的團隊
- **Why it matters**：這是「治理」半邊（原規劃 04 未寫的部分）。而且它回答一個很少被寫的問題：prose 規則的極限在哪
- **Repository evidence**：`.github/workflows/qa-audit.yml`（四關、無 secrets、註解明說「hooks 只約束 Claude Code，本 CI 對所有 agent 一視同仁」）；`scripts/lint_test_rules.py`；三個 Claude hook；`.githooks/pre-commit`（2026-07-08 刻意收斂的理由）；`Makefile` 五個入口；`PERMISSION_BASELINE` 七原則
- **Related episode**：第 07 話「順手把整個房間打掃了」（Permission Boundary）、第 12 話「秘密小本本」
- **Key mechanisms**：規則的三層強度（prose → lint/CI → hook）；hook 只約束單一 agent 所以 CI 才是共同防線；pre-commit 誤報反而降低信任所以刻意收斂；廣義 pattern 禁令
- **Main lesson**：「讓失敗可見」要先於「強制擋下」（trace taxonomy 的漸進策略）
- **材料**：✅ 充足
- **誠實揭露**：CI 只跑靜態稽核，**沒有任何 E2E 進 CI**。文章要寫清這條界線與理由（需要 secrets、需要測試環境資料、E2E 進 CI 的代價還沒付）

### S08｜哪些決策不能交出去（兌現原規劃 05）

- **Core question**：AI 負責執行，人負責什麼？邊界怎麼定、怎麼移？
- **Target audience**：QA Lead / EM（主）、Senior QA
- **Why it matters**：已發布文章公開承諾過這篇。而且它是 EM 受眾唯一真正在意的題目
- **Repository evidence**：`OW_TICKET_SOP.md` checkpoint 表（哪些查核者是 Sunny、agent 不得自行宣告通過）；step 2 的 Sunny Scope 授權；step 1 高風險票必經審閱（金流 / 報表 / 稅務 / 庫存 / 狀態流 / 跨模組 / 第三方 / 資料清空 / API 寫入）；`qa-thought-capture` 儲存無默認同意；eval 不得自動觸發；Doctrine 第 7 章模型強度自我校準（高判斷步驟清單 + 降級回報）；Manual-only 分支
- **Related episode**：第 13 話「那隻兔子就像渣男」（Decision Checkpoint Design）、第 05 話（Test Strategy）
- **Key mechanisms**：決策權清單化（哪些 checkpoint 的查核者是人）；風險分級決定審閱強度；高判斷步驟的補償措施（更低宣稱權限、更早升級、兩次規則收緊為一次）
- **Main lesson**：把「該問人」寫進流程節點，不靠 agent 當下判斷
- **材料**：✅ 充足
- **誠實揭露**：`AI_QA_SYSTEM_LAYERS` 討論裡的 **Decision Layer 明確記載尚未實作**。文章不能寫成已經有一層 decision engine；要寫成「決策權目前是靠 checkpoint 表釘住的，還不是一層機制」

### S09｜從單票驗收到上線把關：回歸集怎麼長出來

- **Core question**：每張票都測過了，為什麼還是不知道這版能不能上線？
- **Target audience**：Senior SDET / QA Lead（主）
- **Why it matters**：這是 repo 裡設計最完整、最能證明「這是測試工程不是工具操作」的一塊。也直接回答 Senior 受眾對 regression strategy 的期待
- **Repository evidence**：`docs/REGRESSION_GUIDE.md`（journey 樹 / domain 字彙表 / 接力 / 測資紀律 / 已知不穩清單 / 9 條覆蓋缺口 / 四問）；`tests/regression/`（conftest 三個 chain fixture、relay.py）；反例 `tests/test_OW4714.py`
- **Related episode**：第 06 話「超努力，無效的那種」（Flaky）、第 05 話（Test Strategy）
- **Key mechanisms**：案例照 journey 分類不照系統模組（模組分類會漏掉系統接縫）；identity 不綁敘事順序（tc_id 是 upsert 主鍵）；接力 vs 獨立 smoke 的取捨；跳段跑直接紅不是略過；xdist 直接 raise；清理能力邊界表；已知缺口誠實表
- **Main lesson**：「我們測過了」這句話必須附一張覆蓋缺口表才有意義
- **材料**：✅ 非常充足，但**在未合併分支 `test/regression-suite`**。寫文章前建議先確認合併狀態，否則文章描述的是一個 main 上不存在的系統
- **誠實揭露**：flaky 只有「已知不穩清單」這種人工紀律，**沒有 retry / quarantine 機制**

### S10｜當被測對象本身是 LLM：chat AI 的 eval harness

- **Core question**：測一個會胡說八道、而且每次回答都不一樣的功能，測試該長什麼樣？
- **Target audience**：Senior SDET、對 AI Testing 有興趣的 QA（主）；這篇的外部吸引力最高
- **Why it matters**：前面九篇都是「用 AI 做測試」，這篇是「測 AI 產品」。兩者的工程問題完全不同，而多數 AI QA 內容不區分這件事
- **Repository evidence**：`evals/chat_ai/DESIGN.md`（兩條 request path 收斂分析、為何 /v1 測得準、覆蓋不到的三項）；`runner.py` / `judge.py` / `assertions.py` / `dates.py`；`test-cases.yaml`（45 條）；`report/`
- **Related episode**：第 15 話「吃你的狗食」（Evaluation / Dogfooding）
- **Key mechanisms**：選測試入口的判準（共用推論引擎 vs 外層橫切）；`temperature=0` + `repeat:3`，三次不一致標 FLAKY 且視同失敗；單一 injectable clock 且 production 禁止注入；測不到的部分明確交給 UI smoke；精準斷言優先於 judge
- **Main lesson**：不確定性不能靠重試蓋掉。要嘛壓成決定性，要嘛把不一致本身當成失敗訊號
- **材料**：✅ 設計文件充足，**但只有一輪執行紀錄（首輪抓到「換日期不重查」等 3 個發現）**。文章要寫成 vertical slice 的設計與首輪結果，不能寫成成熟 eval 體系
- **依賴**：可獨立閱讀，適合當 series 的收尾或對外投稿

### 7.3 候補兩篇（材料尚不足，先不排入）

| 候補 | 缺什麼 |
|---|---|
| **Selector 優先策略與 Page Registry**（已發布文章承諾過） | 材料在（35 份 registry、`pages/` 34 支、`UI_DISCOVERY_GUIDE` / `UI_DEBUG_GUIDE`），但缺一條完整的「策略演化」敘事——目前 registry 是條目累積而非優先序設計。要寫之前得先把 selector 優先序整理成一份明確的正本 |
| **AI 自主性怎麼量**（trace taxonomy） | `eval_trace/` 只有 180 筆事件、reason 分類七類、dashboard 是 mockup（`docs/mockups/ai_trace_dashboard_mock.html`）。量測有了但趨勢結論還不夠寫成一篇。建議先累積到能講「這三個月自主完成率變化」再寫 |

---

## 8. Gap Analysis

判斷標準：如果一位 Senior SDET / QA Lead / EM 看完網站，要能得出「這個人在建 AI-Assisted Testing Workflow，不是在用 LLM 產 testcase」。

| 主題 | repo 證據強度 | 網站現況 | 判斷 |
|---|---|---|---|
| **Test Strategy** | 中。`TEST_PLAN_GUIDE` 有分層 SOP（E2E/API/integration/unit/manual/skip）、9 份 test_plan、「不把所有 decision branches 推成 E2E」硬規則 | 只有漫畫第 05 話標籤 | ⚠️ **內容缺口（可寫）**。材料夠寫一篇，但目前完全沒文章。缺的是「怎麼決定不測」的實例 |
| **Risk-based testing** | 中偏弱。step 1 有高風險票九類清單並決定審閱強度；Doctrine 第 7 章有「高判斷步驟清單」 | 無 | ⚠️ **內容缺口（可寫，但薄）**。有風險分級的**觸發規則**，缺風險評估的**方法論**。建議併入 S08 而不是單獨成篇 |
| **API / integration testing** | 中。4 份 API catalog（order / calendar / invoice / permission）、`qa_probe api` 完整 dump request/response、seed 一律走真實建單 API、後端 repo 當規格來源 | 無 | ⚠️ **內容缺口（可寫）**。但要誠實：**沒有獨立的 API test suite**。API 測試目前是 seed 手段與 ad-hoc 驗證，不是一層測試 |
| **Regression strategy** | 強。見 2.6 | 只有漫畫標籤 | ✅ **材料最強、文章為零**。S09 |
| **CI/CD** | 弱到中。CI 有四關靜態稽核且刻意不需 secrets；**完全沒有 E2E 進 CI**、沒有 nightly、沒有部署流程參與 | 無 | ⚠️ **部分缺口**。可以寫「為什麼刻意只讓 CI 跑靜態稽核」，但**不能寫成有 CI/CD pipeline** |
| **Test data** | 強。`seeds/` 完整能力庫、`PmsSeedManager` ledger 與 cleanup 邊界表、日期 runtime 挑、禁捏 serial、token 自動更新 | 無 | ✅ **材料強、文章為零**。可獨立成篇或併入 S09 |
| **Evidence / traceability** | 強。合約 JSON + schema、execution ledger、executor manifest、evidence board、sprint map、KPMG 對標 PDF | 只有 architecture 頁一句話 | ✅ **材料最強之一**。S04 + S05 |
| **AI evaluation** | **分裂**。對「AI 做的 QA」的 eval：`EVALUATION_GUIDE` 有五層框架與六階段閉環，但 `/eval` command 不存在、只有 1 份實例 → 幾乎是紙上制度。對「AI 產品」的 eval：`evals/chat_ai` 有真實 harness 與一輪結果 → 實作較強 | 無 | 🔴 **重要缺口，且要小心**。不能用 `EVALUATION_GUIDE` 的五層框架寫文章（會變成描述沒在跑的東西）。可寫的是 chat_ai eval（S10）與「為什麼 eval 制度沒跑起來」的誠實檢討 |
| **Governance** | 強。Doctrine / AGENT_GOVERNANCE / Shared Change Review Gate / permission baseline / KNOWLEDGE_GOVERNANCE / 36 份 discuss 紀錄 | 只有 architecture 頁一格 | ✅ **材料最強之一**。S06 + S07 |
| **Human decision checkpoints** | 強。5 個 checkpoint 標明查核者、agent 不得自行宣告通過、儲存無默認同意、eval 不得自動觸發 | 已發布文章有提但未展開（作者自己說留給 05） | ✅ **材料充足、承諾未兌現**。S08 |
| **Knowledge management** | 強。四段 spec pipeline、KNOWLEDGE_MAP、KNOWLEDGE_GOVERNANCE 六種權威狀態、qa-thought-capture、memory-triage、62 份 product 文件 | 完稿未上架 | ✅ **完稿躺著**。S03 |
| **Failure recovery** | 中。失敗分類學六類、兩次停損、停損報告四要件、`diagnose` skill 要求先建可重現 loop、token / auth 自助修復 | 已發布文章提過 two failure stop loss 一句 | ⚠️ **可寫但需擴充**。有「怎麼停」的紀律，缺「停下來之後怎麼系統性復原」。retry / quarantine 完全沒有 |
| **Observability / metrics** | 中偏弱。`eval_trace/` 180 筆事件、七類 reason、`usage_dashboard.py`；但 dashboard 仍是 mockup、沒有趨勢結論 | 無 | ⚠️ **內容缺口（材料不足）**。列候補，先累積數據 |
| **Flaky test handling** | **弱**。沒有 retry 設定、沒有 quarantine、沒有 `pytest-rerunfailures`。只有回歸集「已知不穩清單」（2 條）＋ `diagnose` skill ＋ chat_ai eval 的 `repeat:3` FLAKY 判定 | **漫畫第 06 話直接標成能力「Flaky Test Governance」** | 🔴 **要修正的落差**。網站已經對外聲稱有這個能力，repo 的實作遠比標籤薄。建議：要嘛在文章裡把它降級成「已知不穩清單這種人工紀律」，要嘛先把機制補起來再寫。**不要寫成有 flaky 治理體系** |

### 8.1 三條「不要假裝已經做過」的紅線

1. **不要寫五層 eval 框架在運作。** 樣本數 1，`/eval` command 不存在。
2. **不要寫 flaky test governance。** 漫畫標籤已經超前實作，文章不要跟著超前。
3. **不要寫有 CI/CD pipeline。** CI 只跑四關靜態稽核，刻意不含 E2E。這個「刻意」本身可以寫，但不能寫成有 pipeline。

### 8.2 一條建議補的實作（成本低、補完文章價值高）

把 `report-verifier` 接進 step 10 的 Report Ready checkpoint。目前它是一個定義完整但沒人引用的 agent；接進去之後，S04 就能從「機制存在」變成「機制閉環」。這是本次盤點中投入產出比最高的一項。

---

## 9. Recommended Writing Order

### 9.1 順序與理由

| 順序 | 文章 | 工作性質 | 理由 |
|---|---|---|---|
| 1 | **S02** 如何讓 AI 理解需求 | 事實校正 + 上架 | 完稿 288 行躺著。成本最低，立刻讓 portfolio 從 1 篇變 2 篇 |
| 2 | **S03** 知識回收 | 事實校正 + 補三塊新機制 + 上架 | 完稿 388 行 + fact-checked 版。文章開頭已寫「上一篇我寫如何讓 AI 理解需求」，順序被文章本身鎖定 |
| 3 | **S04** 憑什麼相信 AI 說測完了 | **新寫** | 材料最密、對主要受眾價值最高、回答 series 目前最大的空白（見第 10 節） |
| 4 | **S06** 我砍掉了自己設計的機制 | 新寫 | 順帶正式交代已發布文章的過時描述。放在 S04 後面，因為它需要先建立「量測」的概念 |
| 5 | **S01** Pipeline（改版） | 改版 | 等 S04 / S06 上線後再改，才有地方連過去。改版時把 `/jira-tc` 那段改寫成「後來被砍了，見 S06」 |
| 6 | **S05** 執行帳本 | 新寫 | 與 S04 同一族但受眾偏 Lead / EM，分開寫避免單篇太長 |
| 7 | **S07** 機械化防線 | 新寫 | 兌現原規劃 04 的治理半邊 |
| 8 | **S08** 哪些決策不能交出去 | 新寫 | 兌現已發布文章的公開承諾。放後面是因為它需要前面幾篇的機制當素材 |
| 9 | **S09** 回歸集 | 新寫 | **前置條件：`test/regression-suite` 需先合併或明確說明狀態** |
| 10 | **S10** chat AI eval harness | 新寫 | 獨立性最高、對外吸引力最強，適合當收尾或單獨投稿 |

### 9.2 Numbering 處理建議（等確認架構後再動）

現在是「檔名 01 / 標題 03」錯位。三個選項：

| 選項 | 做法 | 代價 |
|---|---|---|
| A（建議） | 檔名與標題統一改用 Series 2.0 編號；舊檔名保留 301 或 `<link rel="canonical">`，或直接改名（外部連結目前應該極少） | 一次性工作。之後每篇都乾淨 |
| B | 標題去掉編號，只留主題名，導覽用「上一篇 / 下一篇」串 | 最省事，但失去 series 感 |
| C | 維持現狀 | 每加一篇錯位就更難解釋 |

不論選哪個，`portfolio/index.html` 的上下篇導覽（現在兩邊都是 `Coming Soon`）要一併處理。

---

## 10. 下一篇該寫哪一篇

### 結論

**新寫的下一篇是 S04《憑什麼相信 AI 說「測完了」》。**

但在動筆之前，先把 **S02 與 S03 兩篇完稿做事實校正後上架**——那是兩天的工作量，不是重寫。

### 為什麼是 S04

**1. 它回答的是網站現在最大的空白。**

已發布文章的結尾自己列了「目前仍然持續調整的部分」四項。這四項的真實現狀是：兩項不存在、兩項已經長成完整機制。而長出來的那兩項（Evidence Board、Cross-Agent Review）背後真正的問題，都是「怎麼相信 AI 的產出」。這個問題在原本七篇規劃裡沒有任何位置。

**2. 它是主要受眾唯一真正在意的問題。**

Senior QA / SDET 看「我建了 pipeline」不會有反應，因為誰都能建。看「pytest 全綠、schema 過了、報告產出了，我還是不相信，所以我做了這四件事」——這才是同行會停下來讀的東西。

**3. 材料密度最高，而且每一項都有票號可回溯。**

- OW-4468：截圖前後一模一樣，全綠但證據力為零
- OW-4593：read API 全過、前端全擋，14 張作廢
- OW-4929：TC 寫的是畫面行為，報告零截圖，schema 抓不到
- 落點：Doctrine 第 1 章四級證據階梯 + `report-verifier` subagent + Stop hook 三項檢查 + `actual` 欄禁罐頭字

四條 failure、四層防線，一篇文章的骨架已經現成。

**4. 它天然承接已發布文章，也天然開出後面三篇。**

已發布文章的最後一節在談「痕跡變成規則、知識庫、Registry、Audit 機制」。S04 就是接著講那個 Audit 機制到底長什麼樣。而 S04 講完「怎麼驗證」之後，S05（誰測的查得到嗎）、S06（機制有人用嗎）、S07（規則擋得住嗎）三篇的入口就自動打開了。

**5. 它符合現有 Writing DNA，不需要換聲音。**

S04 的敘事天生就是「我以為綠燈就是過了 → 後來發現綠燈只證明格式對 → 所以我做了四層驗證」。這正是已發布文章的招牌句式：當時我以為 A，後來發現是 B，B 比 A 抽象一層。

### 動筆前要處理的兩件事

1. **`report-verifier` 的定位要誠實。** 它現在沒有被任何 rule 引用。文章要寫成「已經做出來，但還沒接進主流程」，不能寫成閉環。或者——更好的做法是**先把它接進 Report Ready checkpoint**（第 8.2 節），再寫這篇。這是本次盤點裡投入產出比最高的一項實作。
2. **三處 `【插入…】` 佔位要準備真材料。** 這篇最需要的是：一張「截圖前後一模一樣」的反例對照、一段 Stop hook 實際攔下來的 stderr 輸出、一份 `actual` 欄從罐頭字改成真值的前後對照。這三張圖比任何文字都有說服力，而且都是現成的。

---

## 附錄：本次盤點的一手來源

**my-playwright（規則與實作）**
`docs/PROJECT_RULES.md`、`docs/AGENT_DOCTRINE.md`、`docs/AGENT_GOVERNANCE.md`、`docs/OW_TICKET_SOP.md`、`docs/COMMAND_SKILL_MAP.md`、`docs/KNOWLEDGE_GOVERNANCE.md`、`docs/EVALUATION_GUIDE.md`、`docs/CROSS_AGENT_CONSENSUS_GUIDE.md`、`docs/REPORT_GUIDE.md`、`docs/QA_HEURISTICS.md`、`docs/IMPROVEMENT_BACKLOG.md`、`docs/QA_THOUGHT_COLLECTOR_GUIDE.md`（deprecated）、`docs/AGENTIC_WORKFLOW_ENHANCEMENT_PLAN.md`（proposal）、`docs/PHASE2_GATE_CONTRACT_AUDIT.md`（historical）、`docs/REGRESSION_GUIDE.md`（未合併分支）

`.agents/skills/`（22）、`.claude/commands/`（19）、`.claude/agents/`（2）、`.claude/settings.json`、`.githooks/pre-commit`、`.github/workflows/qa-audit.yml`、`Makefile`

`scripts/ledger.py`、`scripts/qa_probe.py`、`scripts/hooks/`（3）、`scripts/build_evidence_board.py`、`scripts/serve_evidence_board.py`、`scripts/lint_test_rules.py`、`scripts/render_report.py`、`scripts/usage_dashboard.py`

`docs/discuss/`（36 份，重點：`AI_QA_SYSTEM_LAYERS`、`TRACE_REASON_TAXONOMY`、`QA_THOUGHT_CAPTURE_REBUILD`、`HARNESS_ENGINEERING_AUDIT`、`PERMISSION_BASELINE`）

`eval_trace/`（180 筆事件）、`eval/`（1 份實例 + template）、`evals/chat_ai/`、`docs/tickets/_executors.json`（42 票 / 15 AI）

**kuming-rabbit（網站與文章）**
`portfolio/ai-qa-series-01.html`、`portfolio/index.html`、`docs/drafts/`（7 份）、`docs/articles/`（3 份）、`data/episodes.json`、`index.html`、`about.html`、`architecture.html`、git log
