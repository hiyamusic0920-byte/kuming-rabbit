# Core 06 Evidence Pack — 《規則寫下來之後，AI 還是會違規》

日期：2026-08-23
角色：Senior SDET Evidence Editor + Technical Fact Checker
用途：確認這篇文章的故事是否成立、哪些 claim 有 evidence、哪些必須誠實揭露
原則：**implementation 優先於文件。**只有文件寫著、沒有 usage evidence 的，不得升級成「實際運作」

本輪沒有寫文章、沒有改 repo、沒有補 hook / artifact / CI / lint baseline。所有數字都是本輪實跑量出來的，指令列在第 7 節。

---

## 1. Core Question Verdict

### 1.1 原 hypothesis

> 我原本以為，把規則清楚寫給 AI 看，它就會照做。後來才發現 prose rule 本身不是 control。真正的問題是：哪些規則可以被機械化檢查？哪些只能靠紀律？哪些甚至因為沒有留下 artifact，根本無法被 enforce？

### 1.2 Verdict：**成立，而且比原文更硬。**但要改一個地方

repo 支持這個 framing，證據是一個我本輪才算出來的數字：

**`PROJECT_RULES.md` 的「強制規則」表有 12 條。其中只有 2 條有 blocking 的機械檢查。**

| 強制規則表的 12 條 | 有機械檢查？ |
|---|---|
| test plan 必須在 test case 前 | ❌ 純紀律 |
| feature 必須在 explore 前 | ❌ 純紀律 |
| explore 必須先讀 POM、tests、registry | ❌ **無 artifact，結構上不可查** |
| 只有 selector gap 才開 playwright-cli | ❌ 純紀律 |
| 開 playwright-cli 必須帶登入狀態 | ❌ 有設定檔但無檢查 |
| POM 必須在 bdd-steps 前 | ❌ 純紀律 |
| POM 後必須檢查 registry | ⚠️ Stop hook 只提醒，不阻擋 |
| **test 檔不能出現 `.locator()`** | ✅ lint R001 + PostToolUse + CI |
| **Background 不寫登入和旅館切換** | ✅ lint R002 + CI |
| 旅館切換用 `Sidebar(page, hotel_id)` | ❌ 純紀律 |
| 同一問題超過 2 次必須停損 | ❌ 純紀律 |
| 共用變更先過 Shared Change Review Gate | ❌ 純紀律（OW-4945 就是漏判） |

**2 / 12 blocking、1 / 12 提醒、9 / 12 純紀律。**

這個比例比 hypothesis 講的更有力。原本的 framing 隱含「有些能機械化、有些不能」，實際分布是**絕大多數不能**——而且能機械化的那兩條，都是「一行字串出現在檔案裡」這種最淺的形狀。

### 1.3 要改的地方：把第三問提到最前面，並改寫成因果而非並列

原 framing 把三個問題並列：哪些可以機械檢查／哪些靠紀律／哪些沒 artifact。實際上第三個是前兩個的**成因**，不是第三種類別。

修正後的 core question：

> **一條規則要具備什麼條件，才可能被機械化執行？**
>
> 答案不是「看它重不重要」，而是「它做完之後有沒有留下可以被檢查的狀態」。留下了，才輪得到談驗證與阻擋；沒留下，這條規則不管寫得多硬，都只能停在紀律。

順序因此是：`rule → inspectable state → validation → enforcement`。文章的每一段都對應鍊上的一節，失敗的案例則對應「鍊在哪一節斷掉」。

**不要用的 framing**：「AI 不聽話所以要管它」。repo evidence 不支持這個版本——那 9 條純紀律規則不是因為 AI 特別叛逆才失效，而是它們的完成狀態本來就不落檔（例如「同一問題不超過 2 次」，沒有任何檔案會記錄嘗試次數）。這是設計問題，不是服從問題。

---

## 2. Recommended Story Spine

只列骨架，不寫正文。三幕，每幕一個 failure → mechanism → learning。

```
[前提]  規則早就寫好了：PROJECT_RULES 12 條強制規則，2026-05-22 就在
        3 個 agent（Claude / Codex / Gemini）都被要求讀
        ——然後違規照樣發生

第一幕  鍊斷在最後一節：規則有、狀態有、就是沒人擋
  Failure    OW-4696：AI 實測完沒入帳 → 看板誤判成「沒 AI 測過」
             OW-3712 / OW-4017：走過的頁面沒回補 registry → 下張票重新探索同一頁
  Mechanism  2026-07-07 一天之內：lint + 三個 hook + CI 一起進 repo
             Stop hook 在收工點檢查「有新報告 JSON 但 executor 沒入帳」
  Learning   能用程式驗證的，就不要靠模型自律
             （這句是 2026-07-07 盤點的原文，不是我事後總結的）

第二幕  鍊斷在第二節：沒有可檢查的狀態，規則就只能是宣示
  Failure    OW-3666：Reuse Audit 被跳過，直接開 raw Playwright spike
             6 個驗證區只完成 2 個就卡死
  診斷       這條規則有 guide、有硬規則、有專屬 subagent，
             但它的產出是「回覆裡的一張表格」，沒有落檔
             → 沒有 artifact → 沒有東西可查 → 不可能加 gate
  Mechanism  當時能做的只有新增一個 trace 分類（process_reuse_miss）
             讓違規事後可見。那份紀錄自己寫著「強制 gate 仍需另案設計」
  Learning   可強制性的前提是可稽核性；可稽核性的前提是留下可檢查的狀態

第三幕  兩種失敗方向：太鬆會漏，太緊會被無視
  太鬆      lint 上線時 grandfathered 88 行既有違規（62 個 signature）
            所以硬規則只對新 code 生效——這是刻意的棘輪，不是漏洞
            實測結果：7/07 之後新增的 test 檔，違規數全部是 0
  太緊      pre-commit 原本泛抓所有網域，假警報一堆 → 一個月後刻意收斂
            到只抓四種「DB 連線形狀」
  現場       本輪跑 PostToolUse hook：exit 2，但吐出 143 筆全是假的 missing
            原因是 index 稽核用 rglob 掃檔案系統，把一個未進版控的
            agent worktree 一起掃了。CI 綠燈，因為 CI 的 checkout 沒有那個目錄
  Learning   enforcement 的失效有兩種形狀：擋不住，和擋太多以致沒人看

[收尾]  文件與工程控制是兩件事。
        判斷力層（AGENT_DOCTRINE）比 lint / CI / hooks 晚 6 天出生——
        先把能自動檢查的抽走，剩下的才寫成給人和 AI 讀的準則。
        機械化管得住形狀，管不住證據力。（→ 接 Core 04）
```

第三幕的「現場」那段是本輪新查到的，也是全篇最有說服力的一段：**這不是三個月前的歷史，是我現在跑一次就會發生的事。**

---

## 3. Candidate Failure Ranking

| 候選 | 判定 | Evidence strength | Narrative value | Audience value | 理由 |
|---|---|---|---|---|---|
| **A. Reuse Audit 被跳過（OW-3666）** | **Keep — 全篇核心** | 強 | 最高 | 高 | 唯一能把整條鍊斷在第二節講完的案例。有 ticket、有 trace 事件、有討論紀錄自承無法強制、有 guide 原文證明產出不落檔 |
| **B. `.locator()` + lint baseline** | **Keep — 第三幕上半** | **最強（可重跑驗證）** | 中高 | 高 | 88 行 / 62 signature 的豁免，加上「7/07 後新檔違規全 0」的實測，是全篇唯一能證明機制真的改變行為的數據 |
| **C. pre-commit 假警報收斂** | **Keep，但降為第三幕下半的引子** | 中 | 中 | 中高 | 故事完整（6/04 建立 → 7/08 收斂，兩個 commit 都在），但假警報造成的具體損害沒有留下紀錄。真正的主角換成本輪現場抓到的 143 筆假 missing——那個有實跑輸出 |
| **D. CI 四關** | **Keep，但改成「移出 agent context」的論證** | 強 | 中 | 高 | 60 次 run、59 成功、**1 次失敗**，那次失敗的內容剛好構成一個完整微故事（見下） |
| **E. 三個 hook** | **部分 Keep — 只留 Stop hook 與 PostToolUse，且不平鋪介紹** | Stop 強 / PostToolUse 強（含現場故障）/ SessionStart 弱 | 中 | 中 | SessionStart 沒有對應的「規則被違反」故事，它解的是並行事故，屬於 Core 05 或不寫 |
| **新增 F. CI 唯一那次失敗** | **Keep — 第一幕或第三幕的收尾** | 強 | **最高（密度最高的一則）** | 高 | 見下方說明 |

### 3.1 新增候選 F 的完整內容（本輪查到）

60 次 CI run 裡只有 1 次失敗：

- 時間：2026-08-10
- 分支：`chore/stop-hook-screenshot-check`（PR #85）
- 該 PR 在做什麼：**新增 Stop hook 的「整份報告零截圖」提醒**（來源是 OW-4929）
- 失敗在第 2 關：`PYTHON_FILE_INDEX 完整性稽核`
- 第 1 關（硬規則 lint）通過，第 3、4 關 skipped（fail-fast）
- 後續：修好後 merge 進 main（commit `9161d18`）

也就是說：**一個「新增檢查」的變更，被一個既有檢查擋下來，理由是忘記更新索引。**

這一則的價值在於它同時證明三件事，而且不需要任何論述：CI 真的會擋、它擋的對象包含作者自己、被擋的正好是在加強管控的那次改動。全篇如果只能留一則實例，留這個。

### 3.2 Drop 的候選

- **SessionStart hook**：只當 supporting 一句。它是好機制，但它解的是「開在錯的分支 / 本地 commit 被甩飛」，屬於並行協作事故，不是規則違反。放進來會讓第三幕失焦。
- **Makefile 五個入口**：純 supporting，最多一句。它解的是 permission prompt 噪音，主題屬 Core 07 或 Lab Note。
- **permission baseline（125 → 42）**：已定為 Lab Note，不進本篇。

---

## 4. Evidence Maturity Table

四級判定，不用 Yes/No，寫實際限定條件。

| Mechanism | Implemented | Integrated | Enforced | Observed / Adopted | Evidence |
|---|---|---|---|---|---|
| **hard rule / PROJECT_RULES 強制規則表** | ✅ 12 條，2026-05-22 起 | ✅ 所有 agent 入口都指向它 | **Partial — 2 / 12 blocking、1 / 12 提醒、9 / 12 純紀律** | ⚠️ 違規有紀錄（OW-4696 / 3712 / 4017 / 3666） | 第 1.2 節逐條對照 |
| **lint（`lint_test_rules.py`）** | ✅ R001-R004 | ✅ 被 PostToolUse hook 與 CI 兩處呼叫 | ✅ blocking，exit 1 | ✅ 本輪實跑：對新違規檔輸出 2 筆 R001/R003 並 exit 1 | 第 7 節 Asset 2 |
| **lint baseline** | ✅ 單一 JSON | ✅ lint 預設吃 baseline | **New code only** — 88 行 / 62 signature 豁免 | ✅ 有效：7/07 後新增的 test 檔 `.locator()` 數全為 0 | 第 7 節 Asset 3 |
| **PostToolUse hook** | ✅ | ✅ 寫在 `.claude/settings.json` matcher `Edit\|Write` | ✅ exit 2 + stderr 回饋 | ⚠️ **目前在本機是壞的**：每次改 .py 都吐 143 筆假 missing | 第 7 節 Asset 5 |
| **Stop hook** | ✅ 3 項檢查 | ✅ 寫在 settings | **提醒不阻擋**（exit 2 + stderr，明文「不做無法回頭的阻擋」） | ⚠️ 間接：有專屬單元測試 `tests/test_stop_deliverable_check.py`，但無「實際攔下某票」的紀錄 | hook docstring；PR #85 |
| **SessionStart hook** | ✅ | ✅ | ❌ 永遠 exit 0（設計上不阻擋開工） | ✅ 本 session 的開場輸出即為證據 | 本對話 |
| **pre-commit** | ✅ | ⚠️ 需本機 `core.hooksPath` 指向 `.githooks`（未驗證是否已設） | ✅ blocking，但 `--no-verify` 可繞 | ⚠️ 無攔截紀錄；有「因假警報而收斂」的 commit 紀錄 | 2026-06-04 建立、2026-07-08 收斂 |
| **CI（`qa-audit.yml`）** | ✅ 4 關 | ✅ push + pull_request 都觸發 | ✅ blocking，fail-fast | ✅ **60 run / 59 success / 1 failure**，涵蓋 2026-08-05 ~ 08-19 | 第 7 節 Asset 4 |
| **Make 入口** | ✅ 5 個 | ⚠️ 被 permission baseline 引用為「常用流程走 make」 | ❌ 不是 gate | ⚠️ 無使用計數 | `Makefile` |
| **Reuse Audit（規則層）** | ✅ 硬規則 + `EXPLORE_GUIDE` 輸出格式 | ✅ PROJECT_RULES step 6 明文「未完成不得開 playwright-cli」 | ❌ **No artifact — 結構上不可查** | ⚠️ 只觀測到違規：`process_reuse_miss` 3 筆 | 第 7 節 Asset 6 |
| **`reuse-audit` subagent** | ✅ 定義完整、只讀 | ⚠️ 只被 `AGENT_DOCTRINE` 第 6 章以「如 `reuse-audit`」提及，**PROJECT_RULES step 6 沒有指名它** | ❌ | ❌ 無使用痕跡（無輸出落檔，無法計數） | grep 全 repo 僅 2 筆引用，其中 1 筆在討論紀錄 |
| **report schema 驗證** | ✅ | ✅ `render_report.py` 內建 + CI 第 4 關 | ✅ blocking | ✅ 9 份報告都過 | 對照組，本篇只當一句 |

### 4.1 這張表對文章的三個約束

1. **只有 lint、CI、report schema 三者到達「blocking + 有實跑證據」。** 文章講 enforcement 的正面案例只能舉這三個。
2. **兩個 hook 是提醒不是阻擋，而且是刻意的。** Stop hook 的 docstring 明寫「不做無法回頭的阻擋」。文章不得把 hook 說成 gate。
3. **`reuse-audit` subagent 連 Integrated 都不算。** 它甚至沒有被主規則指名，只在 doctrine 裡被舉例。這一點比我上一輪寫的更弱，要更新。

---

## 5. Artifact 是 enforcement 前提 — 專題驗證

這是本輪最值得驗的新發現，分三題回答。

### 5.1 哪些規則有 machine-checkable artifact

| 規則 | Artifact | 誰檢查 | 檢查形態 |
|---|---|---|---|
| test 檔不得出現 `.locator()` | `tests/*.py` 檔案內容 | lint R001 → PostToolUse + CI | blocking |
| feature Background 不得寫登入 | `features/*.feature` 內容 | lint R002 → CI | blocking |
| 截圖統一 viewport | `tests/*.py` 內容 | lint R003 | blocking |
| 不得寫死登入 | `tests/*.py` 內容 | lint R004 | blocking |
| 報告資料合約 | `reports/data/*.json` | `validate_report_data.py` + CI | blocking |
| 報告產物落點 | `reports/` 目錄結構 | `audit_report_layout.py` + CI | blocking |
| Python 入口索引同步 | `docs/PYTHON_FILE_INDEX.md` vs 檔案系統 | `audit_python_index.py` + CI + hook | blocking（CI）／提醒（hook） |
| executor 入帳 | `docs/tickets/_executors.json` + git diff | Stop hook | 提醒 |
| registry 回補 | `pages/_registry/` 的 git diff | Stop hook | 提醒 |
| 報告有畫面證據 | report JSON 的 `step.screenshot` | Stop hook | 提醒 |
| DB 連線資訊不得進版控 | `git diff --cached` | pre-commit | blocking（可 `--no-verify` 繞） |

**共同形狀**：能被檢查的規則，違規全部表現為「**某個檔案裡出現/缺少某個東西**」。`git diff` 也算一種 artifact——它是「這次改了什麼」的可檢查狀態，Stop hook 的三項檢查全靠它。

### 5.2 哪些規則沒有 artifact，因此只能靠自律或人事後回頭看

| 規則 | 為什麼沒有 artifact |
|---|---|
| **Reuse Audit 必須先做** | 產出是回覆裡的 markdown 表格。`EXPLORE_GUIDE` 的「輸出格式」段只規定表格長什麼樣，**沒有規定寫到哪個檔**。整份 guide 唯一的回寫規則是「偵查發現的 selector 知識寫進 `pages/_registry/`」——那是副產物，不是 audit 本身 |
| test plan 必須在 test case 前 | 兩份檔案都存在，但「誰先寫」不留狀態。git 時間戳可推但沒人檢查，且同一 commit 就看不出 |
| feature 必須在 explore 前 | 同上，且 explore 完全不落檔 |
| 只有 selector gap 才開 playwright-cli | 「有沒有 gap」是判斷，不是狀態 |
| 同一問題超過 2 次必須停損 | 嘗試次數不落任何檔 |
| 旅館切換用 `Sidebar` | 可以 lint（grep localStorage 寫法）但目前沒做 |
| 共用變更先過 Review Gate | 「影響面會不會變」是判斷。OW-4945 證明它會被自己的手滑繞過 |

### 5.3 能不能抽成通則

候選命題：

> Enforceability depends on auditability; auditability depends on leaving inspectable state.

**判定：前半 strongly supported，後半 supported but with a scope limit。**

- **前半（可強制 ← 可稽核）**：11 條有檢查的規則，100% 都有一個可檢查的 artifact；7 條沒檢查的規則，100% 都沒有。相關性在這個 repo 內是完全的，沒有反例。
- **後半的限制**：`inspectable state` 不等於「要為每條規則造一個檔案」。反例思考——「同一問題不超過 2 次」如果為它造一個嘗試計數檔，成本高於價值，而且會鼓勵造假。所以正確的說法是**條件式而非規範式**：

> **有 inspectable state，這條規則才有可能被機械強制；沒有，它就只能停在紀律——這是設計選擇的結果，不是紀律不夠。**
> 推論：如果一條規則重要到不能只靠紀律，那麼要改的是「讓它的完成留下狀態」，而不是「把規則寫得更大聲」。

這個版本沒有把 n=1 抽成 universal law，而且它給出一個可操作的判斷：想強制某條規則，先問它做完之後留下了什麼。Reuse Audit 就是那個「重要到不該只靠紀律，但目前不留狀態」的例子——所以正解方向是讓它落檔，而不是再加一句更硬的規則。

**必須限制語氣的地方**：這條通則的證據全部來自單一 repo、單一團隊、三個月。文章可以寫「我在自己的 repo 裡看到的是」，不能寫「軟體工程的規律是」。

---

## 6. Transferable Principles（逐條判定）

| # | Principle | 判定 | Repo evidence |
|---|---|---|---|
| **A** | **Prose is not enforcement.** | **Strongly supported** | 12 條強制規則只有 2 條 blocking；4 條違規反例（OW-4696 / 3712 / 4017 / 3666）全部發生在規則寫好之後；2026-07-07 盤點原文「最大缺口是規則靠 AI 自律、缺機械化強制」，以及那句對照——「規則遵循率取決於每個 agent 記得 409 行規則／改善後取決於 lint hook CI 有沒有跑，後者是確定的」 |
| **B** | **A rule cannot be mechanically enforced if completion leaves no inspectable state.** | **Strongly supported（本篇最有價值的一條）** | 第 5 節：11 條有檢查的全有 artifact、7 條沒檢查的全沒有，零反例。Reuse Audit 是完整案例：有硬規則 + guide + subagent，但產出不落檔，所以當時只能加 trace 分類而不是 gate，且該紀錄自承「強制 gate 仍需另案設計」 |
| **C** | **Legacy debt can be frozen with a ratchet instead of requiring instant cleanup.** | **Supported，但要補一個誠實的後半** | 正面：baseline 豁免 88 行 / 62 signature；實測 7/07 之後新增的 test 檔 `.locator()` 全為 0，棘輪確實擋住了新債。**反面：baseline 只有一次 commit（2026-07-07），六週來沒有縮減過一條**——債被凍住了，但沒人在還。文章要兩面都寫，否則就是把 ratchet 講成免費 |
| **D** | **Over-enforcement creates false positives and destroys trust.** | **Partially supported（歷史證據弱、現場證據強）** | 歷史：pre-commit 從泛抓網域收斂到四種 DB 連線形狀（2026-06-04 → 07-08），commit message 明寫「消除公開網域/loopback 假警報」，但假警報造成的實際損害沒有留下紀錄。**現場：本輪跑 PostToolUse hook，exit 2 但 143 / 144 筆是假的**——這是可重跑的直接證據，比歷史那條強得多 |
| **E** | **Agent-specific hooks and shared CI solve different scopes.** | **Strongly supported** | CI 的 yml 註解原文：「hooks 只約束 Claude Code；本 CI 對所有 agent 的 PR 一視同仁把關」。這在三 agent（Claude / Codex / Gemini）共用 repo 的前提下是硬事實，不是設計偏好。60 次 run 中 21 次由 pull_request 觸發，證明它真的在 PR 層把關 |

### 6.1 建議新增的第六條

| # | Principle | 判定 | Evidence |
|---|---|---|---|
| **F** | **同一個檢查，掃「工作目錄」與掃「進版控的內容」會給出不同答案；而人會相信綠的那個。** | **Strongly supported（本輪新發現）** | `audit_python_index.py` 用 `REPO_ROOT.rglob("*.py")` 掃檔案系統。本機有一個未進版控的 agent worktree，於是本機報 143 筆 missing；CI 的 checkout 沒有那個目錄，所以 CI 全綠。**同一支腳本、同一天、兩個相反結論。** 而實際被信任的是 CI 那個 |

這一條的可攜性很高：任何在本機與 CI 都跑同一支 linter 的團隊都會撞到，而且撞到的時候通常是本機紅、CI 綠 → 大家選擇忽略本機。

### 6.2 建議不要當 principle 的

- **「先讓失敗可見，再強制」**：n=1（`process_reuse_miss`），而且那份紀錄自己說做不到強制。上一輪已判定不得抽成原則，本輪維持。可以當「當時只能做到這樣」的敘述，不能當設計方法。

---

## 7. Evidence Assets

六項必要真材料，全部已取得或已定位。

### Asset 1 — 規則寫了但仍被跳過（OW-3666）

- **Source**：`docs/discuss/AI_MANAGEMENT_DISCUSSION_20260708_TRACE_REASON_TAXONOMY.md`；`eval_trace/OW-3666.jsonl` 的 `ai_fallback_to_human` 事件（`reason_type: process_reuse_miss`）
- **內容**：事件 metadata 原文 `"root_cause": "未執行 PROJECT_RULES 第6步 Reuse Audit 就直接開 playwright-cli spike，違反『explore 先讀 POM/tests/registry』"`；`reason` 欄記載 6 個驗證區只完成 2 個、balance dialog 在 headless 有 render race、試 4 次達停損
- **Why it matters**：這是全篇唯一一則「規則、工具、文件全都到位，違規照樣發生」的完整紀錄，而且違規原因被寫進了結構化欄位而不只是抱怨
- **Supports claim**：Principle A、B；第二幕主線
- **去識別化**：**需要**。ticket 編號可保留（OW-xxxx 已是外部無意義的內部編號，且現有文章慣例保留），但 metadata 裡的旅宿名稱、hotel id、頁面路徑要抹掉
- **建議呈現**：JSON snippet，只留 `event` / `reason_type` / `root_cause` 三個欄位，其餘用 `…` 省略。這比一段散文有力得多

### Asset 2 — lint 實際退回 violation 的輸出

- **Source**：本輪實跑。在 repo 內建一支含兩個違規的臨時 test 檔，跑 `python3 scripts/lint_test_rules.py --paths <該檔>`，跑完立即刪除（`git status` 已確認無殘留）
- **實際輸出**：

```
新違規 2 筆（不在 baseline，必須修正）：

  R001 — tests/ 不得出現 .locator()（selector 封裝在 Page Object）
    tests/_tmp_lint_probe.py:2  total = page.locator("#foo .bar").inner_text()

  R003 — tests/ 不得出現 full_page=True（截圖統一 viewport）
    tests/_tmp_lint_probe.py:3  page.screenshot(path="x.png", full_page=True)

exit=1
```

- **Why it matters**：這是全篇唯一能讓讀者看見「規則變成程式之後長什麼樣」的東西。而且輸出裡直接印出規則原文，證明 lint 與 PROJECT_RULES 是同一套字
- **Supports claim**：lint 到達 Enforced；Principle A 的正面例
- **去識別化**：不需要（示範檔內容是我造的假 selector）
- **建議呈現**：code block，原樣貼。**不要美化排版**——原樣的 exit=1 才是重點

### Asset 3 — lint baseline 的 legacy debt

- **Source**：`scripts/lint_baseline.json`；`python3 scripts/lint_test_rules.py --no-baseline --json`
- **數字（本輪實測）**：
  - 實際違規**行數 88**：R001 82、R002 5、R004 1
  - baseline **unique signature 62**：R001 56、R002 5、R004 1
  - 差異原因：signature 是 `(rule, file, 該行內容)`，同檔同內容的多行只算一條
  - 集中度：`tests/test_name_sort.py` 48 行、`tests/test_OW4396.py` 15 行、`test_OW3916.py` 9、`test_OW4196.py` 9
  - baseline 的 commit 歷史：**只有一次**（2026-07-07 建立），至今未縮減
- **棘輪有效性（本輪實測）**：所有含 `.locator()` 的 test 檔，建檔日期都是 2026-05-22 / 05-28；2026-07-30 之後新增的 test 檔，違規數全部 0
- **Why it matters**：這是全篇唯一能證明「機制真的改變了行為」的數據，同時也是唯一能證明「機制沒有解決舊債」的數據。兩件事同一份材料
- **Supports claim**：Principle C 兩面
- **去識別化**：不需要（檔名與 selector 都是內部 UI 元素，無敏感資訊）；但 `baseline` 節錄要避免貼出完整 selector 清單，選 3 行示意即可
- **建議呈現**：一張小 table（88 / 62 / 各規則分佈）＋一句 baseline commit 次數。**不要貼整份 JSON**

### Asset 4 — CI run 的實際結果

- **Source**：`gh run list --limit 60`；`gh run view 31378477834`
- **數字**：60 次 run（2026-08-05 ~ 08-19）、59 success、**1 failure**；觸發來源 push 39 / pull_request 21；耗時 11-23 秒
- **那次失敗的完整內容**：

```
2026-08-10  PR #85  chore/stop-hook-screenshot-check
displayTitle: chore(hooks): 收工提醒整份報告零截圖的票

success  硬規則 lint（tests 禁 .locator()/full_page、feature Background 禁登入、禁寫死登入）
failure  PYTHON_FILE_INDEX 完整性稽核
skipped  報告產物 layout 稽核
skipped  已提交的 report JSON schema 驗證（無則跳過）
→ 修好後 merge 進 main（9161d18）
```

- **Why it matters**：一個「新增檢查」的變更被既有檢查擋下，理由是忘記更新索引。同時證明 CI 會擋、擋自己人、以及 fail-fast
- **Supports claim**：CI 到達 Enforced 且 Observed；Principle E
- **去識別化**：不需要（PR 標題與分支名無敏感資訊）
- **建議呈現**：四關的 success/failure/skipped 清單，原樣貼。這是全篇密度最高的一則
- **限制**：**無法取得該次失敗的 log 內文**（run log 已過期）。文章只能說「失敗在第 2 關」，不能描述錯誤訊息細節

### Asset 5 — hook 實際觸發輸出（含現場故障）

- **Source**：本輪實跑 `echo '{"tool_input":{"file_path":"tests/_tmp_lint_probe.py"}}' | python3 scripts/hooks/post_edit_py_check.py`
- **實際行為**：`exit=2`，stderr 同時包含兩段——
  1. **有效訊號**：lint 的 2 筆新違規（與 Asset 2 相同內容）
  2. **噪音**：`python index audit: 287 file(s), 144 missing, 0 stale` 加上 144 行 `[missing] …`，其中 **143 行來自未進版控的 `.claude/worktrees/agent-…/`**，只有 1 行（我的臨時檔）是真的
- **根因（本輪確認）**：`audit_python_index.py` 第 19 行 `for path in REPO_ROOT.rglob("*.py")` —— 掃檔案系統而非 git 追蹤清單，因此把本機殘留的 agent worktree 一起算進來。CI 的 checkout 沒有該目錄，所以 CI 這一關是綠的
- **Why it matters**：這是「enforcement 擋太多以致訊號被淹掉」的**現場證據**，不是三個月前的歷史。而且它同時是 Principle F 的證據
- **Supports claim**：Principle D、F；PostToolUse hook 的成熟度限定條件
- **去識別化**：**需要**。143 行路徑會暴露完整專案結構與檔名，只節錄前 3 行 + `… 共 143 筆` 即可
- **建議呈現**：截短的 stderr code block，把有效訊號與噪音用註解標出來。**不要順手把它修掉再寫文章**——現在這個狀態就是這篇文章的論點

### Asset 6 — Reuse Audit 缺 artifact 的證據

- **Source**：`docs/EXPLORE_GUIDE.md` §輸出格式（約 79-105 行）與 §回寫規則
- **關鍵事實**：輸出格式定義了三張 markdown 表（已知可複用 / 需重驗 / 需新探）與 browser 偵查範圍表，但**通篇沒有指定寫入檔案路徑**；唯一的落檔規則是「偵查發現的 selector 知識寫回 `pages/_registry/`」。另外 `ls docs/tickets/` 沒有任何 reuse audit artifact
- **對照**：`PROJECT_RULES.md` step 6 寫「Reuse Audit 未完成不得開 playwright-cli」——一條有前置條件的硬規則，而那個前置條件沒有可觀測的完成狀態
- **Why it matters**：這是 Principle B 的核心證據，也是全篇最像 senior engineering judgment 的一段
- **去識別化**：不需要
- **建議呈現**：並排對照 —— 左邊是 PROJECT_RULES 那句硬規則，右邊是 EXPLORE_GUIDE 的輸出格式（表格骨架，沒有檔案路徑）。**視覺上讓讀者自己看出「這裡少了一個檔名」**，比用文字解釋有力

### 7.1 補充素材（非必要，有則更好）

| 素材 | 狀態 |
|---|---|
| 2026-07-07 盤點的兩句原文（「能用程式驗證的就不要靠模型自律」／「取決於 lint hook CI 有沒有跑」） | ✅ 已定位，直接引用 |
| 機制誕生時間線（validate 5/29 → 板 6/07 → 索引 6/17 → 入帳 6/25 → 7/07 五件齊發 → doctrine 7/13 → ledger 7/17） | ✅ 全部由 `git log --diff-filter=A` 取得 |
| pre-commit 兩個 commit（6/04 建立、7/08 收斂） | ✅ 有 commit message，無假警報損害紀錄 |
| Stop hook 有專屬單元測試 | ✅ `tests/test_stop_deliverable_check.py` 存在 |

---

## 8. Main Diagram Recommendation

三個方案，選一個。

### Option A — Rule Enforcement Ladder（規則強制階梯）

```
        Prose rule                    12 條強制規則都在這一層起跑
             │
             ▼
     Inspectable state                ← 鍊最常斷在這裡（7 / 12 過不去）
             │
             ▼
        Validator                     lint R001-R004、schema、layout、index
             │
             ▼
   Blocking enforcement               CI 4 關、lint exit 1
```

- 優點：一張圖同時是文章結構；「7/12 卡在第二層」這個數字可以直接標在圖上
- 缺點：階梯圖容易被讀成「越上面越好」，而 repo evidence 顯示有些規則刻意停在紀律層是合理的

### Option B — 同一條規則的 before / after

拿 `.locator()` 那條規則畫兩張：7/07 之前（只有文件，56 個違規 signature 進來）與之後（lint 擋新的、baseline 凍舊的、新檔違規 0）。

- 優點：最具體，數據最硬
- 缺點：只講了成功的那條，講不出 Reuse Audit 那條為什麼失敗——而後者才是文章的核心發現

### Option C — Enforcement coverage map（12 條規則 × 有無 artifact × 有無檢查）

一張 12 列的表格化圖，三欄：規則 / 完成後留下什麼狀態 / 誰檢查。空白格自己說話。

- 優點：直接展示 2 / 12 這個核心事實，而且把「為什麼沒檢查」（第二欄空白）同時呈現
- 缺點：是表不是圖，視覺衝擊較弱

### 推薦：**Option A，並把 Option C 的數字標在第二層上。**

理由：Option A 的四層剛好對應第 1.3 節修正後的 core question（`rule → inspectable state → validation → enforcement`），也對應三幕結構——第一幕鍊斷在第 4 層、第二幕斷在第 2 層、第三幕講第 3、4 層的兩種失效。整篇只需要這一張圖就撐得起來，符合現有 Writing DNA「整篇就靠這張圖」。

Option A 的缺點用一行圖說解掉：在圖旁註明「停在紀律層不一定是缺陷；問題是你有沒有意識到它停在那裡」。Option C 降級成文章中段的一張表，不當主圖。

**不要做的**：架構大全圖、八角色資訊流、hooks / CI / lint 的工具關係圖。那些是 supporting，畫了會把文章變成工具導覽。

---

## 9. Claim Calibration

逐條校準。左邊是容易寫出口的句子，右邊是 evidence 實際支持的上限。

| ❌ 不能說 | ✅ 只能說 |
|---|---|
| 「AI 不能違反這條規則」 | 「新寫入的 test 檔如果出現 `.locator()`，PostToolUse hook 會 exit 2 把它退回；PR 進 repo 時 CI 會再擋一次。既有的 88 行違規在 baseline 豁免名單裡，不受影響」 |
| 「Reuse Audit 是 gate」 | 「流程上它被定義成 gate（未完成不得開 playwright-cli），但它的完成沒有留下可檢查的狀態，所以 enforcement 尚未成立。目前只有事後可見的 trace 分類」 |
| 「CI 保證所有 agent 遵守規則」 | 「CI 對**進入 repository 的變更**提供三個 agent 共用的靜態檢查。它不驗證 session 中的行為——沒有 commit 的探索、沒有落檔的判斷，CI 看不到」 |
| 「我把規則機械化了」 | 「12 條強制規則裡，2 條有 blocking 檢查、1 條有收工提醒、9 條仍靠紀律」 |
| 「hooks 擋下了違規」 | 「PostToolUse hook 對 lint 違規回 exit 2，讓 Claude 讀 stderr 自行修正；Stop hook 的 docstring 明寫『不做無法回頭的阻擋』，它是提醒。而且 hook 只約束 Claude Code」 |
| 「lint 讓 test 檔不再有 selector」 | 「2026-07-30 之後新增的 test 檔，`.locator()` 出現次數為 0；2026-05 建立的四支檔案仍有 82 行 R001 違規，被凍在 baseline 裡，六週沒有縮減」 |
| 「pre-commit 保護了機密」 | 「pre-commit 會擋四種 DB 連線形狀，可用 `--no-verify` 繞過。目前沒有它實際攔下機密的紀錄，只有它因為假警報而被收斂的紀錄」 |
| 「這套機制讓 AI 照規則做事」 | 「它讓一部分規則的遵循從『記得 409 行文件』變成『lint / CI 有沒有跑』。剩下那部分沒有變」 |
| 「index 稽核確保程式索引同步」 | 「CI 上它是有效的 gate（唯一一次 CI 失敗就是它擋下的）。在本機它目前會對每次 .py 編輯回報 143 筆假 missing，因為它掃檔案系統而不是 git 追蹤清單」 |
| 「先讓失敗可見，再逐步強制」 | 「Reuse Audit 那次，因為做不到強制，所以退一步先讓它事後可見。這是單一案例的處置，不是我的通用策略」 |

---

## 10. Honest Limitations（文章必須主動揭露）

依 review 要求的六項，加上本輪新增的三項。

1. **lint baseline 有 legacy violations，而且沒在還。** 88 行 / 62 signature；baseline 自 2026-07-07 建立後只有一次 commit，六週未縮減。硬規則實質上只約束新 code。
2. **CI 不跑 E2E。** 四關全是靜態稽核，不需要 secrets、不連外部服務。刻意不放的理由（需要測試環境資料與可用房況、維護代價未付）可以寫，但不得寫成有 CI/CD pipeline。
3. **Reuse Audit 目前不可 enforce。** 而且它連 `reuse-audit` subagent 都不是被主規則指名的——那個 subagent 只在 `AGENT_DOCTRINE` 第 6 章被當例子提到，且無任何使用痕跡。
4. **hooks 只約束 Claude Code。** Codex 與 Gemini 完全不受 hook 約束，這是 CI 必須存在的原因，也是 hook 層永遠有缺口的原因。
5. **仍靠紀律的規則佔多數（9 / 12）。** 包含兩條相當重要的：兩次停損、共用變更審查閘。後者已經有一次實際漏判（OW-4945）。
6. **PostToolUse hook 目前在本機是壞的。** 143 / 144 筆假 missing。這是本輪跑出來的現況，不是歷史。**文章要寫它，不要先修它。**
7. **Stop hook 沒有「實際攔下某票」的紀錄。** 它有專屬單元測試證明邏輯正確，但沒有一筆 evidence 顯示它在真實票上發現過缺漏。它的成熟度是 Implemented + Integrated，Observed 只能算間接。
8. **pre-commit 的 Integrated 未經驗證。** 它需要本機把 `core.hooksPath` 指向 `.githooks` 才會生效，我本輪沒有驗證這台機器是否已設定。文章若提到它，要限定為「機制存在」。
9. **CI 唯一那次失敗的 log 已過期。** 只能說失敗在第 2 關，不能描述錯誤訊息內容。

### 10.1 其他容易讓讀者誤會成熟度的地方

- **「2026-07-07 一天之內五件齊發」聽起來像一次漂亮的重構**，實際上它是一次外部基準比對（拿 harness engineering 最佳實踐掃自己的 repo）的產出，不是從自己的痛點自然長出來的。文章要說清這個觸發來源，否則會把它寫成一個比實際更有機的演化故事。
- **60 次 CI run 只涵蓋 2026-08-05 起的兩週**（GitHub 的清單上限），不是 CI 的全部歷史。不要用「60 次」暗示總量。
- **`AGENT_DOCTRINE` 比 lint/CI 晚 6 天出生**這個順序很有力，但它是我從 git 反推的敘事，不是當時寫下的設計意圖。要標成「事後看這個順序是對的」，不是「我當時就這樣規劃」。

---

## 11. Open Evidence Gaps

還缺什麼才能開始正式寫。分成兩類。

### 11.1 阻擋性缺口（沒有就寫不了）

**無。** 六項必要材料全部已取得或已定位（第 7 節）。

### 11.2 非阻擋但會讓文章更強的缺口

| 缺口 | 現況 | 取得成本 | 若取不到怎麼寫 |
|---|---|---|---|
| Stop hook 真實攔下一次的輸出 | 只有單元測試，無真實案例 | 中——需要在一張真票的收工點觸發，且該票剛好缺入帳。不能為了取材造假 | 誠實寫「它有測試證明邏輯，但我還沒有它在真票上抓到東西的紀錄」 |
| pre-commit 假警報的當時輸出 | 只有 commit message 說「消除假警報」 | 低——可以 `git checkout` 舊版 hook 在一個安全的 diff 上重跑 | 用現在的 143 筆假 missing 取代它當主證據（更強），pre-commit 降為一句歷史 |
| `core.hooksPath` 是否已設 | 未驗證 | 極低——一條 `git config` 查詢 | 限定寫成「機制存在」 |
| CI 那次失敗的錯誤訊息 | log 已過期 | 不可取得 | 只寫「失敗在第 2 關」 |
| Reuse Audit 若落檔會長什麼樣 | 不存在 | **不要為文章造** | 寫成「正解方向是讓它落檔」，並明說我還沒做 |

### 11.3 明確不要為了寫文章而做的事

- 不修 `audit_python_index.py` 的掃描範圍（那 143 筆假 missing 是本篇第三幕的現場證據）
- 不為 Reuse Audit 造 artifact
- 不縮減 lint baseline
- 不把 `reuse-audit` subagent 接進 PROJECT_RULES step 6
- 不動 CI 範圍

上述每一項都可能是**工程上該做的事**，但它們的評估要走工程需求，不走內容需求。若要處理，另開一份 engineering recommendation。

---

## 12. Article Boundary — 本篇不寫什麼

七條，前五條是防止吃掉別篇，後兩條是防止變成工具導覽。

1. **不寫 evidence hierarchy / false green / 交付物驗收。** 「截圖前後一模一樣」「read API 過了不代表功能過」「actual 欄禁罐頭字」全部歸 Core 04。本篇的收尾只能點一句「機械化管得住形狀，管不住證據力」然後交棒。
2. **不寫 human decision authority。** 哪些決策不交給 AI、scope 授權、高風險票審閱、`review_status` 欄位——全部歸 Core 07。本篇碰到人工關卡時，只說「這一類規則的性質是不可機械化」，不展開誰有權。
3. **不寫 knowledge governance / 知識回收。** registry 回補只作為 Stop hook 的檢查項出現一次，不談知識分流、不談 KNOWLEDGE_MAP、不談 supersede。歸 Core 03。
4. **不寫 permission baseline（125 → 42）。** 它是授權範圍治理，不是規則強制。已定為 Lab Note。
5. **不寫回歸集、不寫 provenance / ledger / executor 帳本的設計。** executor 入帳只作為 Stop hook 的檢查項出現，不談四個寫入者、不談 file lock、不談歸屬禁預設值。歸 Core 05。
6. **不做 hook feature tour。** 三個 hook 不平鋪介紹；SessionStart 最多一句；不寫 hook 的 JSON payload、matcher 語法、settings.json 結構。
7. **不做 CI/CD 教學。** 不貼完整 yml、不解釋 GitHub Actions 語法、不列 Makefile target 清單、不寫 lint 的實作方式。

### 12.1 與其他 Core 的邊界（review 的切法驗證後保留）

| 篇 | 負責的問題 | 邊界檢查句 |
|---|---|---|
| **Core 06（本篇）** | 已經決定好的規則，怎麼讓它真的被執行 | 「這句話在講規則有沒有被遵守，還是在講結果對不對？」後者出界 |
| **Core 04** | 怎麼知道測試結果與證據真的支持那個 claim | — |
| **Core 07** | 哪些決策權根本不交給 AI | 「這句話在講服從，還是在講授權？」後者出界 |

repo reality 支持這個切法，理由是三者的失敗形狀不同、而且互不涵蓋：

- 一條被完美 enforce 的規則（lint 擋住 `.locator()`），完全不保證報告的證據力（Core 04 的 OW-4468 就是 lint 全綠的情況下發生的）
- 一條沒有 enforce 的規則（Reuse Audit），與「這件事該不該由 AI 決定」無關——它該由 AI 做，只是沒人查得到它做了沒
- 一個人工關卡（scope 授權）之所以不可機械化，原因是授權性質而非缺 artifact

**唯一需要注意的重疊**：Shared Change Review Gate 同時是「規則要被遵守」（Core 06）與「這個判斷該由誰做」（Core 07）。分法：本篇只用它當「純紀律規則」的例子（12 條裡的一條），OW-4945 那個漏判的完整故事留給 Lab Note，判斷權的設計留給 Core 07。

---

## 13. Final Go / No-Go

### Is Core 06 ready to write?

# **GO WITH GAPS**

### 為什麼是 GO

1. **六項必要材料全部到手**，其中三項（lint 退回輸出、hook 現場故障、CI 唯一失敗）是本輪實跑取得的一手材料，不是引用文件。
2. **核心論點有可重跑的量化支撐**：2 / 12 blocking、88 行 / 62 signature、7/07 後新檔違規 0、60 run / 1 fail、143 / 144 假警報。這篇文章的每一個數字讀者都能自己驗。
3. **有一條別人寫不出來的發現**：Reuse Audit 卡在「有硬規則但結構上不可稽核」，以及由它抽出的 Principle B。這是本篇的原創價值。
4. **成熟度最高**：主軸機制（lint、CI）是全 repo 唯一到達「blocking + 有實跑證據」的一組。用它當第一篇新寫的文章，可信度基準立得起來。

### 為什麼是 WITH GAPS 而不是純 GO

三個 gap 必須寫進文章而不是藏起來，否則這篇會變成它自己在批判的東西：

1. **Stop hook 沒有真實攔截紀錄。** 它在骨架第一幕裡是主要 mechanism，但 Observed 只能算間接。第一幕要據實寫成「機制到位，但我還沒有它在真票上抓到東西的證據」。
2. **PostToolUse hook 現在是壞的。** 143 筆假警報。這既是最好的第三幕材料，也是一個必須承認「我自己的 enforcement 現在正處於被無視狀態」的坦白。寫得好會是全篇最有份量的段落，寫得閃躲會毀掉整篇的可信度。
3. **baseline 六週沒還過債。** 棘輪擋住新債是成功的，但舊債完全沒動。不能只寫前半。

### 動筆前必須完成的三件事（都不涉及改 repo）

1. **確認 `core.hooksPath` 設定狀態**（一條 `git config` 查詢），決定 pre-commit 那句怎麼限定。
2. **把 Asset 1 與 Asset 5 去識別化**：OW-3666 的 metadata 抹掉旅宿名與 hotel id；143 行路徑節錄成 3 行。
3. **決定 Reuse Audit 那段的收尾姿態**。建議：明說正解是讓它落檔、明說我還沒做、不承諾時程。這比寫「未來會補上」誠實，也符合現有 Writing DNA 的「誠實的代價」段落。

### 一句話

這篇文章要建立的不是「我有很多 governance 工具」，而是：

> **寫下規則，和建立一個真的能約束行為的工程控制，是兩件完全不同的事——而我在自己的 repo 裡量過，12 條硬規則裡只有 2 條跨過了那條界線。**

這句話有數字撐著，而且數字是對自己不利的。這就是這篇可以寫的理由。
