## type: article status: draft domain: AI QA topics: [AI QA, knowledge recycling, fact-checked, qa-thought-capture, knowledge system] created: 2026-06-24

## AI 摘要

- 主題：`how_to_build_ai_qa_knowledge_recycling.md` 的 fact-checked 標註版。
- 用途：區分文章內容哪些是 my-playwright 已落地事實、哪些是從 repo 推導出的概念、哪些是作者反思或仍需補案例。
- 主要來源：`docs/PROJECT_RULES.md`、`.agents/skills/qa-thought-capture/SKILL.md`、`docs/QA_HEURISTICS.md`、`docs/discuss/AI_MANAGEMENT_DISCUSSION_20260615_QA_THOUGHT_CAPTURE_REBUILD.md`、`docs/discuss/AI_ADOPTION_THIRD_MONTH_KNOWLEDGE.md`、`docs/discuss/QA_AI_ADOPTION_20260616_FOURTH_MONTH_REVIEW.md`。
- 使用方式：先用本版檢查事實強度，再回到正式文章版調整語氣與案例。
- 發表提醒：公開版仍需移除真實 ticket、產品名、旅館 ID、同事名與內部系統資訊。

---

# 如何建立 AI QA 的知識回收機制？（fact-checked 標註版）

## 標註規則

- **[已落地事實]**：repo 內已有明確文件、規則、skill 或討論紀錄支撐。
- **[從 repo 推導]**：不是 repo 原文，但可由既有規則與 artifact 合理推導。
- **[作者反思]**：Sunny 的經驗化、文章化表述，方向符合 repo，但不是硬規則。
- **[待補真實案例]**：文章要更有說服力，最好補一個去識別化實例。

## 事實來源對照

| 文章主張                                                | 事實強度        | Repo 依據                                                                  |
| --------------------------------------------------- | ----------- | ------------------------------------------------------------------------ |
| 知識要回收到持久落點，不能只留在聊天裡                                 | 已落地事實       | `docs/PROJECT_RULES.md` 知識放置規則；第三個月回顧「AI 不會可靠記得昨天，但 repo 會」              |
| 測試執行中可複用 QA 判斷要用 `qa-thought-capture` 攔截            | 已落地事實       | `.agents/skills/qa-thought-capture/SKILL.md`、`docs/PROJECT_RULES.md`     |
| 儲存前必須經 Sunny 確認，不自動寫入 repo                          | 已落地事實       | `.agents/skills/qa-thought-capture/SKILL.md` 採集與儲存流程                     |
| 分流到 memory / heuristics / product / seed / registry | 已落地事實       | `.agents/skills/qa-thought-capture/SKILL.md` 分流表；`docs/PROJECT_RULES.md` |
| memory 和 heuristics 要避免雙寫                           | 已落地事實       | `docs/QA_HEURISTICS.md`；6/15 討論紀錄的 Codex 審計與 final consensus             |
| 規則需要 supersede/delete，不只 append                     | 已落地事實       | `.agents/skills/qa-thought-capture/SKILL.md`；6/15 討論紀錄                   |
| 知識會腐爛、context rot 會干擾 AI                            | 從 repo 推導   | repo 有「文件越來越多、導航跟不上」、「修剪避免門檻膨脹失準」等證據，但 `context rot` 是文章化命名              |
| 健康知識庫應允許變小                                          | 作者反思        | 可由 supersede/delete 推導，但 repo 沒有這句原則                                     |
| 負面樣本能攔 AI 重犯舊錯                                      | 從 repo 推導   | `qa-thought-capture` 校準用 `❌ 拒` / `➕ 補` 蒸餾例示；文章把它抽象成「負面樣本」                |
| 「我像在不停教同一堂課」                                        | 作者反思 / 待補案例 | 符合第三個月回顧的「不要每次從零開始」，但需要補真實去識別化故事                                         |

---

## 文章標註稿

上一篇我寫「如何讓 AI 理解需求」，核心是：不要讓 AI 一拿到 ticket 就開始寫測試，先讓它把自己的理解、假設和不確定攤開來，讓人可以校正。  
**[從 repo 推導]** 這個說法延續前一篇文章；repo 事實支撐是 `PROJECT_RULES` 中票面採集、功能知識文件、test plan 前置於 test case 的流程。

但校正之後呢？

如果我今天花了十分鐘糾正 AI，告訴它某個欄位不能這樣解讀、某種狀態不能這樣測、某個 UI 行為以前踩過坑，但這些校正只留在當下那段對話裡，那下一個 session 重新開始時，它很可能又犯一模一樣的錯。  
**[作者反思 + 從 repo 推導]** repo 明確記錄「同一個 selector、同一個 UI 陷阱、同一個 seed 規則，如果只留在聊天裡，下次很可能又被重做」。但這段是文章化敘事，最好補一個去識別化案例。

那一刻的感覺很像在不停地教同一堂課。  
**[作者反思 / 待補真實案例]** 建議補一個具體情境，例如「同一類 selector 探索重做」或「同一類 seed 規則被重問」。

我後來才意識到，問題不是 AI 學不會，而是我沒有一個讓它「記得住、又不會堆爛」的機制。  
**[從 repo 推導]** repo 已落地「寫回 repo、分流落點、supersede/delete、校準 log」。但「記得住、又不會堆爛」是文章化總結。

所以這篇接著上一篇，只回答一件事：

> 怎麼讓一次校正不蒸發，而是沉澱成下次 AI 就懂的知識？

**[已落地事實]** `qa-thought-capture` 的目的明確寫著「餵未來接手的 agent」，攔到並寫進複用層後，下一個 agent 可繼承。

而且更重要的是，怎麼讓這些知識不要越堆越爛。  
**[從 repo 推導]** `qa-thought-capture` 已有 supersede/delete 與校準中的「修剪」；第四個月回顧也記錄文件變多後導航成本上升。

## 沒被回收的校正，就是白費

一開始我以為，教 AI 就是在對話裡糾正它。它誤解需求，我補充脈絡；它測錯方向，我告訴它真正風險；它選錯 selector，我貼一段正確做法。  
**[作者反思]** 這是經驗化開場，不是 repo 硬規則。

這樣當下看起來有效，因為 AI 會立刻修正。但過幾天、換一個 session、換一個 agent，問題又回來了。  
**[從 repo 推導]** 第三個月回顧明確提到多 agent、多 thread、多模型的痛點是知識不共享；不是模型不夠聰明，而是知識沒有共享。

因為那次校正沒有流回任何持久的地方。  
**[已落地事實]** `PROJECT_RULES` 規定商業規則、測資、UI selector、本票紀錄、AI 管理決策要分別放入固定位置。

後來我把這件事重新看成一個迴圈：

```text
AI 出錯 / 誤解
  ↓
人類校正
  ↓
沉澱成一條可重用的知識
  ↓
回流到 AI 下次會讀到的脈絡
  ↓
下次 AI 不再從零開始
  ↺
定期修剪，避免知識越堆越爛
```

**[從 repo 推導]** 這張圖是文章化模型。底層事實是：`qa-thought-capture` 有採集候選、確認關卡、落地、校準與修剪；`PROJECT_RULES` 規定知識回補與固定落點。

很多人做到第二步就停了：AI 錯了，人類改它。但真正讓 AI QA 系統變強的，是第三步之後。  
**[作者反思]** 符合 repo 方向，但屬於文章觀點。

重點不是「教 AI」。重點是設計一個讓校正能流回去、而且越用越清楚的迴圈。  
**[從 repo 推導]** `qa-thought-capture` 的校準段落明確說「會學習的是 repo 檔案，不是模型本身」。這句是本篇最應該保留的核心。

## 為什麼預設情況下，知識會蒸發

AI 很會在一段對話裡學你的偏好。你糾正它幾次，它會在同一個 session 裡調整語氣、修正策略、避開剛剛踩過的坑。這很容易讓人誤以為它真的學會了。  
**[作者反思]** 這是使用 AI 的一般經驗，不是 my-playwright repo 專屬事實。

但多數時候，它學到的是當下 context，不是長期知識。  
**[已落地事實]** `.agents/skills/qa-thought-capture/SKILL.md` 明確寫：「會『學習』的是 repo 檔案，不是模型本身。」

session 結束、context 被壓縮、換一個 agent 或換一條 thread 之後，這些校正就可能消失。留下來的通常只有人的記憶，以及一段很難被下一個 agent 自動讀到的聊天紀錄。  
**[從 repo 推導]** repo 有多 agent 接手必須讀 repo 狀態、不能依賴前一段對話記憶的規則；這段把它轉成文章語言。

這就是第一個問題：人的記憶不是系統。

第二個問題是：prompt 也不是知識庫。  
**[作者反思 + 從 repo 推導]** 這句不在 repo 原文，但與「知識要寫回 repo、agent 入口只是薄指標、共同 source of truth」一致。若 04 也要寫 governance，這句建議在本篇主打，04 只引用。

把所有規則塞進 prompt，看起來很直覺。今天多踩一個坑，就在 prompt 裡加一句；明天多發現一個限制，就再加一段。短期有效，但長期會變成另一種失控。  
**[從 repo 推導]** `AGENT_GOVERNANCE` 與 `PROJECT_RULES` 的方向是把 rules / skills / guides 分層，不把所有東西塞進單一入口；這段沒有逐字來源。

prompt 會越來越長，重點越來越模糊，互相矛盾的規則越來越多。AI 不是沒有讀到，而是讀到太多，抓不到哪一條才是現在最重要的。  
**[從 repo 推導 / 待補案例]** 第四個月回顧有「文件越寫越多，反而開始找不到」和 AI 摘要 / frontmatter 的解法；若要更硬，補一個 skill 或 guide 過長造成誤讀的例子。

所以我後來把「記得住」拆成兩件事：

1. 知識要有持久的家。
2. 知識要能被下次工作流程讀到。

**[已落地事實]** `PROJECT_RULES` 有知識放置規則；`qa-thought-capture` 分流表寫明「下一個 agent 怎麼拿到」。

## 知識需要一條回家的路

在 my-playwright 裡，我沒有把所有知識都塞到同一個檔案。因為 QA 知識不是同一種東西。  
**[已落地事實]** `PROJECT_RULES` 的知識放置規則明確拆分 product / seeds / registry / worklog / discuss / eval。

有些是產品規則，有些是測試資料，有些是 UI selector，有些是通用 QA 直覺，有些只是 agent 做事時要遵守的行為偏好。它們如果混在一起，短期好像方便，長期一定會爛。  
**[已落地事實 + 作者反思]** 前半是 `qa-thought-capture` 分流表；「長期一定會爛」是文章化判斷。

所以我把知識分成幾個持久落點：

| 校正出來的知識 | 應該回到哪裡 | 標註 |
|---|---|---|
| AI 該怎麼做事的行為規則 | memory | 已落地事實 |
| QA 該檢查什麼的通用直覺 | `docs/QA_HEURISTICS.md` | 已落地事實 |
| 特定產品或商業規則 | `docs/product/` | 已落地事實 |
| 測試資料、API 欄位、seed helper | `seeds/` | 已落地事實 |
| UI selector、等待條件、頁面互動陷阱 | `pages/_registry/` | 已落地事實 |

這篇不展開這些檔案各自怎麼設計。那是另一篇「AI QA 的治理與知識管理」要講的靜態架構。  
**[作者規劃]** 這是系列邊界設計，不是 repo 事實。

這裡真正重要的是動態迴圈：當一次校正發生時，它有沒有一條路徑可以流進正確的家。  
**[已落地事實]** `qa-thought-capture` 的採集與儲存流程就是這條路徑：自動採集 / `/capture` → 確認關卡 → 寫檔與校準。

## 把一次校正變成一條規則

知識回收的最小單位，不是一整份文件，而是一條可以被下次引用的規則。  
**[從 repo 推導]** `qa-thought-capture` 規定「一行規則」候選，`QA_HEURISTICS.md` 也採一條一行。這句是對格式的抽象。

一條好的回收規則要夠小、夠明確、夠可判斷。  
**[從 repo 推導]** 來自攔截門檻：非顯然、可複用、決策形狀。

例如，不好的寫法是：

```text
測試時要注意資料。
```

比較好的寫法是：

```text
驗金額加總或計數前，先確認資料來源是否包含軟刪除或舊資料，避免把不應計入的資料算進結果。
```

**[已落地事實 + 去識別化改寫]** `docs/QA_HEURISTICS.md` 內已有類似條目：「驗任何金額均攤 / 加總 / 計數前，先確認有沒有軟刪除或舊資料被算進去」。文章版已去掉真實來源票細節。

後來我把 `qa-thought-capture` 設計成一個執行中的攔截器，就是為了抓這種句子。  
**[已落地事實]** 6/15 討論紀錄與 skill 皆明確說新版是「執行中 QA 直覺攔截器」。

當測試過程中出現一個非顯然、可複用、會影響未來決策的 QA 判斷時，先把它標成候選。  
**[已落地事實]** 完全對應 skill 的三條攔截門檻與一句話判準。

但它不會自動寫進 repo。真正儲存前，還是要經過人類確認。  
**[已落地事實]** skill 明確規定儲存永遠要 Sunny 明確點頭，沒有默認同意，不會自動寫檔。

因為如果讓 AI 自己決定什麼知識值得永久保存，它很快就會把 repo 寫滿看似有道理、其實沒有通過 QA 判斷的句子。  
**[從 repo 推導]** 這是對「確認關卡」設計理由的文章化說法；repo 原文沒有這句，但方向一致。

我也越來越重視穩定的 ID 或穩定的錨點。  
**[部分已落地 / 部分推導]** memory 的 `feedback_*` 是硬事實；`QA_HEURISTICS.md` 用分類作為錨點。文章中的「slug ID」概念需要避免寫得像所有落點都已全面實作 slug。

所以一條可維護的知識，最好有穩定位置。  
**[已落地事實]** 分流規則與 upsert 規則支持這點；product / registry / seed 都要求 upsert 到對應檔的對應段落。

## 知識會爛掉：回收不只是加，還要修剪

大家談 AI knowledge base，通常都在講怎麼加知識、怎麼寫文件、怎麼做 RAG、怎麼讓 AI 讀更多資料。但用久了會發現，知識不是越多越好。  
**[作者反思]** 這是對外文章的切入角度，不是 repo 事實。

知識會爛掉。  
**[從 repo 推導]** repo 有 supersede/delete、校準修剪、文件導航成本上升等事實；「爛掉」是文章化命名。

有些規則是過時的；有些規則是重複的；有些規則太細；有些規則太長。  
**[從 repo 推導]** 6/15 討論明確指出 memory / heuristics 邊界會 drift、已有 seed 與 memory 重複、缺 supersede/delete 會讓錯誤規則殘留。太長則可由第四個月「文件越來越多，導航跟不上」支撐。

這就是 context rot。  
**[作者命名]** repo 沒有把這套問題命名為 context rot；若要公開，可以保留，但建議寫成「我把它稱為 context rot」。

當知識堆久了，問題不再是「AI 沒有資料」，而是「AI 被太多品質不一的資料干擾」。  
**[從 repo 推導]** 可由修剪、AI 摘要 / frontmatter、MOC / 橫向連結等設計推導。

所以知識回收不能只有新增。它還要有修剪。  
**[已落地事實]** skill 有 supersede/delete；校準迴路有「修剪」。

> 一個健康的知識庫，會變小的次數應該跟變大的次數差不多。

**[作者反思]** 這句很有力，但不是 repo 既有原則。若要強 fact-based，可改成：「至少，它要允許變小。」

這也是為什麼 `qa-thought-capture` 不只要能 append，還要能 supersede 和 delete。  
**[已落地事實]** 6/15 Codex 審計指出只 append 會讓錯誤規則長期殘留，final consensus 採納 supersede/delete；skill 已落地。

當一條規則被新事實取代時，不應該在旁邊再加一條補充說明。  
**[已落地事實]** skill 明確要求取代時改寫成新規則，不只 append，避免後續 agent 同時讀到新舊兩版。

## 不只記正確做法，也要記錯誤樣本

知識回收還有另一個常被忽略的面向：負面樣本。  
**[從 repo 推導]** skill 有 `❌ 拒` 代表 false positive、`➕ 補` 代表 false negative，並要求把拒絕蒸餾成負面例子；文章將其抽象成「負面樣本」。

大多數知識庫只記「應該怎麼做」。但 AI 很常重犯的，不是它完全不知道正確做法，而是它在某些情境下又走回舊路。  
**[作者反思]** 方向符合「校準」設計，但需補真實案例更有力。

正面規則教 AI 走對路。負面樣本攔 AI 走回頭路。  
**[從 repo 推導]** 可由校準 log 的正負例蒸餾推導。

例如，正面規則可以寫：

```text
狀態類驗收要走到前端 UI 呈現確認，不能只看 API 回 200。
```

**[已落地事實 + 去識別化改寫]** `docs/QA_HEURISTICS.md` 已有「狀態 / 結果類驗收要走到前端 UI 呈現去確認，不能停在 write/read API 回 200 或 status=0 就算過」。

負面樣本可以補上：

```text
不要把 write API 回 200 當成使用者看到的狀態已正確；這只能證明寫入請求成功，不能證明 UI 呈現正確。
```

**[從 repo 推導]** 這是從正面 heuristic 轉寫出的負面樣本，不是目前 repo 內已獨立存在的條目。若要寫「已落地」，需真的加到 `QA_HEURISTICS.md` 或 calibration 例示。

## 回收要有固定儀式

知識回收最難的地方不是知道要存哪，而是持續做。  
**[作者反思]** 但符合 6/15 討論中 intake 採用率低的經驗。

因為回收和修剪都屬於那種「今天不做也不會立刻死，但長期不做一定會爛」的工作。  
**[作者反思]**

在 my-playwright 裡，這個儀式通常發生在幾個時機：

- 測試過程中，出現可複用 QA 判斷時先標成採集候選。
- 工作告一段落時，用 `/capture` 或收尾檢查把候選攤開。
- 人類逐條裁決：存、改後存、拒絕、補充。
- 寫回對應落點。
- 若發現既有規則過時，直接取代或刪除。

**[已落地事實]** 這些都直接對應 `qa-thought-capture` 的採集與儲存流程、確認關卡、supersede/delete。

如果知識回收只靠「想到再記」，它一定會失敗。  
**[從 repo 推導]** 6/15 討論提到舊 intake 沒有自動觸發、採用率 1/26，支持「靠手動想到再記」不可靠。

所以我把它變成流程的一部分，而不是額外的好習慣。  
**[已落地事實]** `PROJECT_RULES` 已把 `qa-thought-capture` 寫入測試執行過程中的主規則，並把第 11 步列為最後知識回補 + worklog。

## 一條知識的生命週期

一條回收知識，不是寫下來就結束。它應該有生命週期。

```text
某次測試中發現一個非顯然判斷
  ↓
標成採集候選
  ↓
人類確認後寫入正確落點
  ↓
下次 test plan / POM / seed 設計時被讀到
  ↓
實際影響 AI 的決策
  ↓
後來產品或流程改變
  ↓
這條知識被更新、合併或刪除
```

**[從 repo 推導]** 生命週期圖是文章化模型。底層事實是分流表、test-plan 前讀 `QA_HEURISTICS.md`、POM 讀 registry、seed 設計讀 seeds、supersede/delete。

只有進沒有出，就不是知識管理，是堆積。  
**[作者反思]** 與 supersede/delete 方向一致，但不是 repo 原文。

## 建立回收機制後，實際改變了什麼

最明顯的改變，是我不用一直重新教同一件事。  
**[從 repo 推導 / 待補數據]** 第三個月回顧已有「不要每次從零開始」的方向；如果要更硬，需補具體票或前後對比。

以前 AI 常常問一些我已經回答過很多次的問題，或重新踩以前修過的 selector、seed、report 證據問題。現在它至少有機會在開始前讀到既有規則。  
**[從 repo 推導]** repo 有 Reuse Audit、registry、seed factory、report heuristic，但這句仍是經驗總結。

第二個改變，是 AI 的產出比較有累積感。  
**[作者反思]**

不是每次都像一個全新的外包人員從零開始，而是比較像一個會讀交接文件、會查既有資產、會延續前面決策的協作者。  
**[從 repo 推導]** `PROJECT_RULES` 規定接手 mid-ticket 要依序檢查 docs/product、test plan、feature、registry、POM、tests、reports/worklog。

第三個改變，是我比較能分辨「這是一次性修正」還是「這是值得回收的 QA 判斷」。  
**[已落地事實]** `qa-thought-capture` 攔截門檻明確排除一次性環境問題，只攔非顯然、可複用、決策形狀的判斷。

不是所有東西都值得留下來。太多一次性細節進入知識庫，未來只會造成噪音。  
**[已落地事實 + 作者反思]** skill 的「不攔」規則支持前半；「造成噪音」是文章化理由。

回收要花時間，修剪也要花時間。尤其修剪很難，因為刪除知識比新增知識更需要判斷。  
**[作者反思]** repo 有 delete 機制，但沒有衡量成本的實證。

因為 AI QA 的知識庫如果完全自動長大，很快就會變成另一個需要 QA 的東西。  
**[作者反思 + 從 repo 推導]** 很適合文章結尾，但不是已落地事實。它呼應「儲存永遠經 Sunny 確認」。

## 如果重來會怎麼做

如果回到四個月前，我會更早建立知識回收機制，而且會做得更輕。  
**[作者反思]** 這是系列主軸。

我不會一開始就設計很完整的知識架構。我會先做三件事：

1. 定義哪些校正值得回收。
2. 定義它們要流到哪幾個固定落點。
3. 定義什麼時候要修剪或取代舊規則。

**[從 repo 推導]** 這三件事分別對應 `qa-thought-capture` 攔截門檻、分流規則、supersede/delete。

很多人導入 AI QA，第一件事會想自動化更多測試。但我現在更相信，前期更重要的是建立兩個基礎機制：

第一，需求理解機制：讓 AI 在動手前先把理解攤開，讓人可以校正。

第二，知識回收機制：讓校正之後的知識流回 repo，下次不需要重講。

**[從 repo 推導 + 作者反思]** repo 事實是第 1 步功能知識文件、test plan 前置、qa-thought-capture、知識回補；「比 E2E 自動化更該先做」是作者反思。

沒有第一個機制，AI 會很有自信地把錯誤需求做完。沒有第二個機制，AI 會一直重犯你已經教過它的錯。  
**[作者反思]** 可保留，但如果要更 fact-based，建議補兩個去識別化案例。

所以我給想導入 AI QA 的人最實際的建議是：

不要只顧著教 AI。

先想好教完的東西去哪裡。

也要想好，什麼時候該刪。

**[從 repo 推導]** 這三句是文章化結論，分別對應校正、分流、supersede/delete。

---

## 需要補案例的位置

1. **開場 hook**：補一個「教過 AI，幾週後又犯同樣錯」的去識別化故事。
2. **context rot**：補一個「文件 / skill / prompt 太長導致 AI 抓錯重點」的實例；目前只有推導，沒有硬案例。
3. **負面樣本**：目前 `QA_HEURISTICS.md` 有正面 heuristic，負面樣本是文章推導。若要更硬，可以把一條 negative example 寫入 calibration 或 heuristics。
4. **成效段落**：補一個前後對比，例如「導入 registry / qa-thought-capture 後，某類 selector / seed / report 問題不再重做」。

## 建議回寫正式文章的調整

- 把「context rot」改成「我把這種現象稱為 context rot」，避免讀者以為 repo 已有這個術語。
- 把「健康知識庫會變小的次數應該跟變大的次數差不多」標成作者觀點，不要寫得像已驗證結論。
- 「stable slug ID」要收斂：memory 的 `feedback_*` 是硬事實，但不是所有落點都有 slug。正式文可改成「穩定位置或穩定 ID」。
- 如果要公開發表，保留 my-playwright 作為個人專案名可以；但不要出現真實 OW 票、產品名、旅館 ID、同事名。

