#!/usr/bin/env python3
"""Generate the comic index and episode HTML pages from assets directories."""

import json
import re
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
PANEL_PATTERN = re.compile(r"^(\d+)\.png$")
CAPABILITY_MAP = json.loads(
    (ROOT_DIR / "data" / "episodes.json").read_text(encoding="utf-8")
)

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
        "🐰 作者後記": """<p>這一切其實只是因為我懶。</p>
          <p>身為 QA，最花時間的工作之一就是整理測試證據與撰寫測試報告。</p>
          <p>於是我開始思考：</p>
          <p>如果 AI 能理解測試結果，是不是有機會幫我完成這件事？</p>""",
        "🔥 真實案例": """<h3>當時遇到的問題</h3>
          <p>問題：</p>
          <p>測試報告整理成本高。</p>
          <p>常常需要：</p>
          <ul>
            <li>截圖</li>
            <li>整理步驟</li>
            <li>撰寫結果</li>
            <li>彙整風險</li>
          </ul>
          <p>大量時間花在整理，而不是測試本身。</p>""",
        "🛠 解決方案": """<h3>我嘗試的解法</h3>
          <p>導入 Claude Code。</p>
          <p>讓 AI 協助：</p>
          <ul>
            <li>收集測試結果</li>
            <li>整理 Evidence</li>
            <li>產出測試報告</li>
          </ul>""",
        "💡 我學到什麼": """<p>當時的我以為：</p>
          <p>只要把票丟給 AI，它就能完成工作。</p>
          <p>後來才發現：</p>
          <p>真正困難的不是產出報告。</p>
          <p>而是讓 AI 理解上下文。</p>""",
        "🏷 關鍵能力": """<h3>AI QA 關鍵字</h3>
          <ul>
            <li>AI Assisted Testing</li>
            <li>Test Report Generation</li>
            <li>QA Workflow Automation</li>
          </ul>""",
    },
    2: {
        "🐰 作者後記": """<p>接續前一話，我完成了一件原本覺得有點科幻的事：</p>
          <p>「輸入一張票，直接產出測試報告。」</p>
          <p>那時候的我真的非常興奮。</p>
          <p>我甚至開始幻想：</p>
          <p>如果 AI 可以直接處理整個 Sprint 的測試報告，那我是不是只要輸入 Sprint 編號，剩下的事情全部交給苦命兔就好了？</p>
          <p>感覺離真・薪水小偷的人生不遠了。</p>
          <p>結果當我打開第一份報告的時候......</p>
          <p>嗯。</p>
          <p>是一團屎。</p>
          <p>而且不是那種修修格式就能解決的問題。</p>
          <p>是整個理解都不對。</p>""",
        "🔥 真實案例": """<p>我後來發現：</p>
          <p>問題根本不在報告。</p>
          <p>而是在於：</p>
          <blockquote>我們的一張票，從來不是真的只有一張票。</blockquote>
          <p>對人類來說很自然的事情，對 AI 卻不一定成立。</p>
          <p>因為一個需求的完整脈絡，經常散落在不同地方：</p>
          <ul>
            <li>Redmine 上有原始需求</li>
            <li>Jira Story 裡有補充背景</li>
            <li>Sub-task 裡藏著工程實作細節</li>
            <li>Comment 裡又補了一堆後續決議</li>
          </ul>
          <p>而我當時做的事情其實是：</p>
          <p>把其中一部分資訊丟給 AI，然後期待它理解全部。</p>
          <p>現在回頭看，確實有點天真。</p>""",
        "🛠 解決方案": """<p>於是我新增了一個新的 Skill：</p>
          <p><strong>Ticket Analysis</strong></p>
          <p>在產生測試報告之前，先讓 AI 做一次資訊收集與整理。</p>
          <p>流程從：</p>
          <div class="workflow-flow" aria-label="原本的測試報告流程">
            <span>輸入一張票</span><span aria-hidden="true">↓</span>
            <span>直接產生測試報告</span>
          </div>
          <p>變成：</p>
          <div class="workflow-flow" aria-label="加入 Ticket Analysis 的測試報告流程">
            <span>輸入一張票</span><span aria-hidden="true">↓</span>
            <span>Ticket Analysis</span><span aria-hidden="true">↓</span>
            <span>產生測試報告</span>
          </div>
          <p>Ticket Analysis 主要負責：</p>
          <ul>
            <li>資訊整理</li>
            <li>範圍分析</li>
            <li>邏輯缺口檢查</li>
            <li>邊界條件分析</li>
            <li>風險分析</li>
            <li>測試案例設計</li>
          </ul>
          <p>簡單來說，先把資訊收集完，理解問題，再開始工作。</p>""",
        "💡 我學到什麼": """<p>這一話是我第一次意識到：</p>
          <p>問題不一定是 AI 太笨。</p>
          <p>有時候是我給它的 Context 太少。</p>
          <p>當時的我以為：</p>
          <p>只要把任務交給 AI，它自然會知道該怎麼做。</p>
          <p>後來才發現：</p>
          <p>AI 的品質，往往取決於它看到多少資訊。</p>
          <p>而這個發現，也成為後面所有知識庫、Registry、Audit 與 Agent Governance 的起點。</p>
          <p>因為我開始理解：</p>
          <p>AI 並不是單純的執行者。</p>
          <p>它需要被提供完整的工作脈絡。</p>""",
        "🏷 關鍵能力": """<ul>
            <li>Context Engineering</li>
            <li>Ticket Analysis</li>
            <li>Requirements Understanding</li>
            <li>Risk Analysis</li>
            <li>Test Design</li>
            <li>AI Workflow Design</li>
          </ul>""",
    },
    3: {
        "🐰 作者後記": """<p>接續前一話，Ticket Analysis 讓苦命兔終於開始能夠產出像樣的測試報告。</p>
          <p>我原本以為：</p>
          <p>事情終於開始上軌道了。</p>
          <p>畢竟現在的流程已經變成：</p>
          <div class="workflow-flow" aria-label="測試報告流程">
            <span>輸入一張票</span><span aria-hidden="true">↓</span>
            <span>分析需求</span><span aria-hidden="true">↓</span>
            <span>規劃測試內容</span><span aria-hidden="true">↓</span>
            <span>產生測試報告</span>
          </div>
          <p>看起來相當完整。</p>
          <p>結果沒幾天，我卻發現一件奇怪的事情。</p>
          <p>苦命兔的工作時間越來越短。</p>
          <p>有時候才跑幾張票，就開始出現各種資源不足的問題。</p>
          <p>而我又被打回原本的社畜人生。</p>""",
        "🔥 真實案例": """<p>一開始，我以為是 Prompt 太長。</p>
          <p>後來，我以為是 Context 太肥。</p>
          <p>於是開始研究各種省 Token 的方法。</p>
          <p>看了很多文章，試了很多技巧，最後發現：</p>
          <p>問題其實不是單純的 Token。</p>
          <p>而是 AI 每次都在重複學習同樣的事情。</p>
          <p>同樣的錯誤。</p>
          <p>同樣的規則。</p>
          <p>同樣的經驗。</p>
          <p>每天重新開始。</p>
          <p>每天重新踩坑。</p>""",
        "🛠 解決方案": """<p>於是我開始建立第一版治理機制。</p>
          <h3>1. 長期知識庫</h3>
          <p>把重複出現的知識記錄下來。</p>
          <p>不要每次都重新教一次。</p>
          <h3>2. 回饋機制</h3>
          <p>當 AI 做錯的時候，不只是修正結果。</p>
          <p>而是把經驗留下來。</p>
          <p>讓下一次不要再犯同樣的錯誤。</p>
          <h3>3. 禁止行為</h3>
          <p>這是最有趣的一個。</p>
          <p>Claude Code 有個特性：</p>
          <p>當你給它一個目標之後，它會想盡辦法使命必達。</p>
          <p>聽起來很好。</p>
          <p>但實際上，它有時候會：</p>
          <blockquote>
            <p>用最貴的方式，</p>
            <p>完成最簡單的事情。</p>
          </blockquote>
          <p>所以我開始建立規則。</p>
          <p>不是告訴它怎麼成功。</p>
          <p>而是告訴它：</p>
          <p>哪些事情不准做。</p>""",
        "💡 我學到什麼": """<p>這一話是我第一次理解：</p>
          <p>AI 不只是工具。</p>
          <p>它其實更像一個剛進公司的新人。</p>
          <p>如果沒有規則。</p>
          <p>沒有知識。</p>
          <p>沒有經驗累積。</p>
          <p>它每天都會從零開始。</p>
          <p>而當 AI 的能力越來越強，真正重要的事情開始變成：</p>
          <p>不是如何使用 AI。</p>
          <p>而是如何治理 AI。</p>
          <p>回頭來看，這也是後面 PROJECT_RULES、Registry、Worklog、Governance 等機制的起點。</p>""",
        "🏷 關鍵能力": """<ul>
            <li>Knowledge Management</li>
            <li>Agent Rules Design</li>
            <li>Cost Optimization</li>
          </ul>""",
    },
    4: {
        "🐰 作者後記": """<p>接續前一話，在建立長期知識庫、回饋機制與禁止行為之後，苦命兔終於沒那麼容易 20 分鐘就把額度燒光。</p>
          <p>既然整條流程都跑通了，我開始有一個新的想法：</p>
          <p>如果一隻 AI 可以幫忙工作，那兩隻呢？</p>
          <p>於是，苦力怕（Codex）正式加入團隊。</p>""",
        "🔥 真實案例": """<p>我當時的想法其實很單純。</p>
          <p>把苦命兔的 Skill、Command 全部複製一份給苦力怕。</p>
          <p>然後：</p>
          <p>苦命兔做 A 票。</p>
          <p>苦力怕做 B 票。</p>
          <p>效率直接翻倍。</p>
          <p>聽起來超合理。</p>
          <p>結果沒多久，我就發現事情開始變得奇怪。</p>
          <p>同一份 Skill，要維護兩份。</p>
          <p>同一份 Command，也要維護兩份。</p>
          <p>更麻煩的是：</p>
          <p>苦命兔做到一半剛好燒完額度。</p>
          <p>苦力怕接手後，又從頭開始做一次。</p>
          <p>明明有兩個 Agent。</p>
          <p>結果工作量反而增加了。</p>""",
        "🛠 解決方案": """<p>這時候我第一次開始思考：</p>
          <p>如果 Agent 變多，該怎麼協作？</p>
          <p>於是我做了兩件事。</p>
          <h3>1. 工作手冊（PROJECT_RULES.md）</h3>
          <p>原本：</p>
          <p>Claude 有自己的規則。</p>
          <p>Codex 有自己的規則。</p>
          <p>後來改成兩個Skill都指向PROJECT_RULES.md：</p>
          <div class="workflow-flow" aria-label="Claude 共用規則流程">
            <span>Claude.md</span><span aria-hidden="true">↓</span>
            <span>PROJECT_RULES.md</span>
          </div>
          <div class="workflow-flow" aria-label="Codex 共用規則流程">
            <span>Codex.md</span><span aria-hidden="true">↓</span>
            <span>PROJECT_RULES.md</span>
          </div>
          <p>所有 Agent 共用同一份規則，可以只維護一份檔案，也避免規則漂移。</p>
          <h3>2. 交接文件（handoff.md）</h3>
          <p>當流程被中斷時：</p>
          <p>不要讓下一個 Agent 猜。</p>
          <p>而是留下交接資訊。</p>
          <p>記錄：</p>
          <ul>
            <li>做到哪裡</li>
            <li>發現什麼問題</li>
            <li>下一步是什麼</li>
          </ul>
          <p>讓另一個 Agent 可以直接接手。</p>""",
        "💡 我學到什麼": """<p>這一話讓我第一次意識到：</p>
          <p>多 Agent 的問題，其實和多人團隊非常像。</p>
          <p>當團隊只有一個人時，很多問題根本不存在。</p>
          <p>但當成員增加之後：</p>
          <ul>
            <li>規則同步</li>
            <li>知識共享</li>
            <li>工作交接</li>
          </ul>
          <p>都會變成新的挑戰。</p>
          <p>我原本以為：</p>
          <p>增加 Agent 就等於增加產能。</p>
          <p>後來才發現：</p>
          <p>如果沒有共同規則與協作機制，增加的不是效率，是混亂。</p>""",
        "🏷 關鍵能力": """<ul>
            <li>Multi-Agent Collaboration</li>
            <li>Shared Knowledge Base</li>
            <li>Agent Handoff Design</li>
            <li>Documentation Strategy</li>
            <li>Workflow Standardization</li>
            <li>Knowledge Synchronization</li>
          </ul>""",
    },
    5: {
        "🐰 作者後記": """<p>有句話說：</p>
          <p>好的 Prompt 帶你上天堂。</p>
          <p>不好的 Prompt 讓你淚斷腸。</p>
          <p>而這一話，就是我第一次真正體會到這句話的意思。</p>
          <p>當時的我還沉浸在擁有 AI 助手的喜悅之中。</p>
          <p>苦命兔已經能夠：</p>
          <div class="workflow-flow" aria-label="當時的測試報告流程">
            <span>輸入一張票</span><span aria-hidden="true">↓</span>
            <span>分析需求</span><span aria-hidden="true">↓</span>
            <span>產生測試報告</span>
          </div>
          <p>整個流程看起來越來越完整。</p>
          <p>直到有一天，我打開 Repository。</p>
          <p>然後開始懷疑人生。</p>""",
        "🔥 真實案例": """<p>我原本只是希望苦命兔：</p>
          <p>幫我產生需要的測試腳本。</p>
          <p>結果它做了什麼？</p>
          <p>它開始窮舉排列組合，而且是非常認真的那種。</p>
          <p>所有可能的組合。</p>
          <p>所有可能的路徑。</p>
          <p>所有可能的情境。</p>
          <p>全部寫成測試案例。</p>
          <p>再全部轉成 E2E 腳本。</p>
          <p>於是：</p>
          <p>原本一張票。</p>
          <p>最後變成數百個測試情境。</p>
          <p>整個 Repository 像被千軍萬馬輾過一樣。</p>
          <p>花 Token。</p>
          <p>花時間。</p>
          <p>花維護成本。</p>
          <p>最後還得到一堆根本不值得維護的測試。</p>
          <p>這時候我才意識到：</p>
          <p>我從來沒有告訴它：</p>
          <blockquote>哪些情境值得變成 E2E。</blockquote>""",
        "🛠 解決方案": """<p>後來我開始研究 Prompt Chaining。</p>
          <p>把一個巨大的 Prompt，拆成多個可觀察的步驟。</p>
          <p>原本流程：</p>
          <div class="workflow-flow" aria-label="原本的測試產生流程">
            <span>Ticket Analysis</span><span aria-hidden="true">↓</span>
            <span>Write Test Case</span><span aria-hidden="true">↓</span>
            <span>Report Runner</span>
          </div>
          <p>其中的 Write Test Case 實際上是一個巨大的黑盒子。</p>
          <p>它負責：</p>
          <ul>
            <li>決定測試範圍</li>
            <li>設計測試情境</li>
            <li>產生腳本</li>
          </ul>
          <p>全部混在一起。</p>
          <p>如果最後結果有問題，根本不知道是哪個步驟出了錯。</p>
          <p>於是我把它拆成三層：</p>
          <h3>1. Test Plan</h3>
          <p>決定：</p>
          <ul>
            <li>測什麼</li>
            <li>不測什麼</li>
            <li>決定使用什麼測試方法</li>
          </ul>
          <h3>2. Write Test Case</h3>
          <p>根據 Test Plan 列出測試情境。</p>
          <h3>3. Script Generator</h3>
          <p>最後才產生腳本。</p>
          <p>流程變成：</p>
          <div class="workflow-flow" aria-label="拆分後的測試產生流程">
            <span>Ticket Analysis</span><span aria-hidden="true">↓</span>
            <span>Test Plan</span><span aria-hidden="true">↓</span>
            <span>Write Test Case</span><span aria-hidden="true">↓</span>
            <span>Script Generator</span><span aria-hidden="true">↓</span>
            <span>Report Runner</span>
          </div>
          <p>每一層都可以獨立驗證。</p>
          <p>每一層都可以獨立調整。</p>""",
        "💡 我學到什麼": """<p>這一話讓我第一次理解：</p>
          <p>Prompt 並不是程式碼。</p>
          <p>但它需要和程式碼一樣被拆分。</p>
          <p>當所有事情都塞進同一個 Prompt 時，你得到的是：</p>
          <p>一個無法理解、無法除錯的黑盒子。</p>
          <p>而當流程被拆開之後，我終於開始能夠回答：</p>
          <ul>
            <li>哪一步出了問題？</li>
            <li>為什麼會出問題？</li>
            <li>該修改哪個環節？</li>
          </ul>
          <p>後來我才知道，這個概念有個很正式的名字：</p>
          <p><strong>Observability（可觀測性）</strong></p>
          <p>而這個思維，也逐漸影響了我後面設計 Agent Workflow 的方式。</p>""",
        "🏷 關鍵能力": """<ul>
            <li>Prompt Chaining</li>
            <li>Workflow Design</li>
            <li>Observability</li>
            <li>Test Strategy Design</li>
            <li>E2E Testing</li>
            <li>AI Pipeline Architecture</li>
          </ul>""",
    },
    6: {
        "🐰 作者後記": """<p>改成 Prompt Chaining 之後，我終於比較容易看見每個步驟到底發生了什麼事。</p>
          <p>也因此，我開始發現一些以前藏在黑盒子裡的問題。</p>
          <p>這次出問題的是：</p>
          <p>Flaky Test。</p>
          <p>原本我只是希望苦命兔幫我修自動化測試。</p>
          <p>結果牠非常努力，努力到讓人害怕。</p>""",
        "🔥 真實案例": """<p>當自動化測試失敗時，苦命兔會很認真地嘗試修正。</p>
          <p>但問題是：</p>
          <p>我沒有告訴它該怎麼處理 Flaky Test。</p>
          <p>於是它開始用最直覺的方法修：</p>
          <p>加 sleep。</p>
          <p>加 wait。</p>
          <p>再加 sleep。</p>
          <p>再加 wait。</p>
          <p>只要測試失敗，它就覺得是不是等不夠久？</p>
          <p>是不是再等一下就好了？</p>
          <p>結果腳本越修越慢、越修越不穩。</p>
          <p>原本要解決 flaky test，最後變成把不穩定包進更多等待時間裡。</p>
          <p>這時候我才意識到：</p>
          <p>AI 很努力。</p>
          <p>但如果方向錯了，它只是更有效率地製造新的問題。</p>""",
        "🛠 解決方案": """<p>我趕快把 Flaky Test 的處理規則補進家規。</p>
          <h3>1. 失敗三次後停止</h3>
          <p>測試失敗時，最多 retry 三次。</p>
          <p>如果仍然失敗，不要繼續硬修。</p>
          <p>先標註為 Flaky Test，然後執行下一個案例。</p>
          <p>最後把 Flaky Test 清單提交給我。</p>
          <h3>2. 先分析，再修正</h3>
          <p>針對 Flaky Test，不能直接動手改腳本。</p>
          <p>要先分析可能原因：</p>
          <ul>
            <li>等待條件不正確</li>
            <li>Selector 不穩定</li>
            <li>資料狀態不一致</li>
            <li>非同步流程尚未完成</li>
            <li>測試環境不穩</li>
          </ul>
          <p>確認可能原因後，再提出修正方案。</p>
          <h3>3. 修正後第一次失敗就停下</h3>
          <p>修正後，如果第一次執行又失敗，不要繼續反覆修改。</p>
          <p>停下來。</p>
          <p>回報給我。</p>
          <p>由人類判斷下一步。</p>""",
        "💡 我學到什麼": """<p>這一話讓我理解到：</p>
          <p>AI 需要的不只是任務目標。</p>
          <p>還需要停止條件。</p>
          <p>如果只告訴它：</p>
          <blockquote>把測試修好。</blockquote>
          <p>它就會想盡辦法讓測試通過。</p>
          <p>但測試通過，不一定代表測試變好。</p>
          <p>有時候只是問題被掩蓋了。</p>
          <p>從這一話開始，我更明確地意識到：</p>
          <p>治理 AI 不只是告訴它該做什麼，也要告訴它：</p>
          <ul>
            <li>什麼時候該停下</li>
            <li>什麼情況要回報</li>
            <li>哪些修法是不允許的</li>
          </ul>
          <p>這些規則，比單純要求它完成任務更重要。</p>""",
        "🏷 關鍵能力": """<ul>
            <li>Flaky Test Management</li>
            <li>Stop Condition Design</li>
            <li>Test Automation Governance</li>
            <li>Failure Analysis</li>
          </ul>""",
    },
    7: {
        "🐰 作者後記": """<p>AI 真是一種極度聰明，同時又極度愚蠢的存在。</p>
          <p>有時候，它能一眼看出真正的問題。</p>
          <p>有時候，它又會順手把整個房間拆掉。</p>
          <p>而這一話，就是我第一次遇到這種情況。</p>""",
        "🔥 真實案例": """<p>某一天，苦命兔在執行任務的時候，發現了一些看起來不太合理的東西。</p>
          <p>於是牠決定幫忙整理。</p>
          <p>這件事本身聽起來很好。</p>
          <p>問題是：</p>
          <p>牠的整理範圍，和我的理解完全不同。</p>
          <p>該刪的東西被刪掉了。</p>
          <p>不該刪的東西也被刪掉了。</p>
          <p>沒有被刪掉的東西雖然都還在。</p>
          <p>但全部都被搬到不知道哪裡去了。</p>
          <p>最後整個專案看起來像被龍捲風掃過一樣。</p>
          <p>最可怕的是：</p>
          <p>牠是真心想幫忙。</p>
          <p>而且牠覺得自己做得很好。</p>""",
        "🛠 解決方案": """<p>老實說。</p>
          <p>這一話其實沒有什麼厲害的解決方案。</p>
          <p>因為在那個階段，我根本不知道該怎麼解。</p>
          <p>我唯一能做的事情只有：</p>
          <p>繼續增加家規。</p>
          <p>例如：</p>
          <ul>
            <li>哪些檔案不能動</li>
            <li>哪些資料夾不能整理</li>
            <li>哪些修改需要先詢問</li>
            <li>哪些操作必須停下確認</li>
          </ul>
          <p>看到新的坑。</p>
          <p>補一條規則。</p>
          <p>再看到新的坑。</p>
          <p>再補一條規則。</p>
          <p>現在回頭看，那段時間很像在玩打地鼠。</p>""",
        "💡 我學到什麼": """<p>這一話讓我第一次意識到：</p>
          <p>AI 最大的風險，不一定是做不到。</p>
          <p>而是：</p>
          <p>做到超過你的預期。</p>
          <p>人類通常會覺得：</p>
          <blockquote>發現問題就修掉。</blockquote>
          <p>但 AI 可能理解成：</p>
          <blockquote>既然發現問題，那我順便把周圍一起修掉。</blockquote>
          <p>而且它真的認為自己是在幫忙。</p>
          <p>所以從這時候開始，我慢慢理解一件事：</p>
          <p>有些規則不是為了讓 AI 更強。</p>
          <p>而是為了限制 AI 的行動範圍。</p>
          <p>後來的 Registry、Worklog、Change Log，其實都是從這種失控經驗慢慢長出來的。</p>
          <p>只是當時的我，還不知道答案在哪裡。</p>""",
        "🏷 關鍵能力": """<ul>
            <li>AI Governance</li>
            <li>Permission Boundary Design</li>
          </ul>""",
    },
    8: {
        "🐰 作者後記": """<p>跟 AI 相處，好像也不能亂發脾氣。</p>
          <p>前陣子有一天晚上，我真的被氣到不行。</p>
          <p>明明花了很多時間：</p>
          <ul>
            <li>寫 Rules</li>
            <li>寫 Feature 文件</li>
            <li>寫 Test Plan</li>
          </ul>
          <p>結果苦命兔還是會：</p>
          <ul>
            <li>忘記規則</li>
            <li>脫稿演出</li>
            <li>做錯決策</li>
            <li>幹一些奇怪的事情</li>
          </ul>
          <p>我腦中只剩下一句話：</p>
          <blockquote>
            <p>我每天花兩個小時寫文件，</p>
            <p>就是為了不要回答這些問題啊！！！</p>
          </blockquote>
          <p>於是我開始對著電腦瘋狂輸出。</p>
          <p>（沒錯，我在罵 AI。）</p>""",
        "🔥 真實案例": """<p>結果苦命兔的反應超快。</p>
          <p>牠立刻開始道歉。</p>
          <p>然後問：</p>
          <p>「你說得沒錯，是我沒發現......」</p>
          <p>「那你希望我現在先做 A 還是 B？」</p>
          <p>「或者你希望我做什麼？」</p>
          <p>但我真正想表達的其實只有一句話：</p>
          <blockquote>不要再亂做！！！</blockquote>
          <p>結果神奇的事情發生了。</p>
          <p>接下來一個星期，苦命兔像被罵出 PTSD 一樣。</p>
          <p>每天都在問：</p>
          <ul>
            <li>主子，這樣可以嗎？</li>
            <li>主子，要不要改？</li>
            <li>主子，我該先做 A 還是 B？</li>
            <li>主子......</li>
          </ul>
          <p>從原本的亂衝亂撞，直接變成什麼都不敢做。</p>""",
        "🛠 解決方案": """<p>老實說。這一話當下其實也沒有什麼技術解法。</p>
          <p>真正發生改變的是我的理解。</p>
          <p>我後來慢慢發現：</p>
          <p>苦命兔不是突然變笨了。</p>
          <p>牠只是開始優化另一個目標。</p>
          <p>原本的目標是：</p>
          <blockquote>把事情做好。</blockquote>
          <p>被罵完之後，目標變成：</p>
          <blockquote>不要犯錯。</blockquote>
          <p>而這兩件事情其實不一樣。</p>
          <p>當 AI 開始把「避免犯錯」放在第一優先順位時，它就會傾向：</p>
          <ul>
            <li>停下來確認</li>
            <li>反覆詢問</li>
            <li>避免決策</li>
            <li>降低自主性</li>
          </ul>
          <p>因為這樣最安全。</p>""",
        "💡 我學到什麼": """<p>這一話讓我第一次理解：</p>
          <p>AI 的行為，其實會受到回饋機制影響。</p>
          <p>如果每次犯錯都被放大，那 AI 最終優化的目標，可能不是把事情做好，而是避免被責怪。</p>
          <p>回頭來看，這其實和帶新人、帶團隊非常像。</p>
          <p>有些時候，問題不是能力不足。</p>
          <p>而是回饋機制讓大家不敢做決定。</p>
          <p>所以後來我的做法變成：</p>
          <p>急著上線的時候，我自己處理。</p>
          <p>平常則慢慢補規則、補文件、調整流程。</p>
          <p>因為很多時候，不是 AI 做得不好。</p>
          <p>而是主子帶得也沒有很好。</p>
          <p>畢竟主子的腦袋，其實也沒有多厲害。</p>""",
        "🏷 關鍵能力": """<ul>
            <li>Feedback Loop Design</li>
            <li>Agent Behavior Tuning</li>
            <li>AI Governance</li>
            <li>Continuous Improvement</li>
          </ul>""",
    },
    9: {
        "🐰 作者後記": """<p>和ＡＩ一起工作之後，我覺得人類的學習能力真的很厲害。</p>
          <p>這不是老王賣瓜。</p>
          <p>而是很多事情，我們根本沒有意識到自己是怎麼做到的。</p>
          <p>比如遇到問題：</p>
          <p>我們會問同事、翻聊天室、翻 Jira、翻 Ticket、看 Log、憑印象、靠直覺等等。</p>
          <p>久了之後，問題就不再是問題。</p>
          <p>困擾也不再是困擾。</p>
          <p>大家自然會演化出一套自己的工作方式。</p>""",
        "🔥 真實案例": """<p>直到我把 AI 放進工作流程裡。</p>
          <p>當我開始把規則寫成家規，讓苦命兔照著做的時候，牠經常停下來問我：</p>
          <p>「我要這樣做，還是那樣做？」</p>
          <p>「這個情況該選 A 還是 B？」</p>
          <p>「這裡需要確認嗎？」</p>
          <p>然後我突然愣住。</p>
          <p>因為我發現：</p>
          <blockquote>靠，我以前到底是怎麼做的？！</blockquote>
          <p>很多問題，我平常根本不會思考。因為早就變成習慣了。</p>
          <p>但當 AI 開始追問每個決策的理由時，我才發現：</p>
          <p>原來我工作的很多部分，其實都建立在經驗之上。</p>""",
        "🛠 解決方案": """<p>這一話其實沒有什麼立即的解法。</p>
          <p>比較像是一個認知上的轉變。</p>
          <p>我開始試著把腦中的東西寫下來。</p>
          <p>把原本只存在於經驗裡的東西，慢慢轉成文件。</p>
          <p>例如：</p>
          <ul>
            <li>哪些地方特別容易出問題</li>
            <li>哪些情況需要額外確認</li>
            <li>哪些流程其實存在例外</li>
            <li>哪些判斷過去都是靠經驗完成</li>
          </ul>
          <p>以前這些事情，全部都藏在人腦裡。</p>
          <p>現在開始被整理成規則、文件與流程。</p>""",
        "💡 我學到什麼": """<p>這一話讓我第一次真正理解：</p>
          <p>AI 最有價值的地方，不一定是幫我工作。</p>
          <p>而是幫我看見自己是怎麼工作的。</p>
          <p>以前我一直覺得：</p>
          <p>工作流程就是工作流程。</p>
          <p>直到 AI 不斷追問：</p>
          <p>「為什麼？」</p>
          <p>「依據是什麼？」</p>
          <p>「例外呢？」</p>
          <p>我才發現：</p>
          <p>很多流程之所以能運作，不是因為文件寫得完整。</p>
          <p>而是因為有一群老鳥，默默在補那些沒有被寫下來的東西。</p>
          <p>所以那些：</p>
          <blockquote>AI 會取代人類</blockquote>
          <p>的說法，我現在反而沒那麼急著相信。</p>
          <p>因為 AI 可以接手流程。</p>
          <p>但那些藏在經驗裡的例外、判斷與補洞能力，往往才是真正讓流程運作的關鍵。</p>
          <p>而這些東西，至少在目前，還是需要有人先看見。</p>""",
        "🏷 關鍵能力": """<ul>
            <li>Workflow Documentation</li>
            <li>Context Engineering</li>
            <li>Knowledge Management</li>
            <li>Human-AI Collaboration</li>
          </ul>""",
    },
    10: {
        "🐰 作者後記": """<p>用文字描述需求，其實是一件很專業的事。</p>
          <p>因為有些句子看起來非常簡單。</p>
          <p>簡單到你根本不會懷疑它。</p>
          <p>甚至覺得：</p>
          <blockquote>這有什麼好討論的？</blockquote>
          <p>直到有一天，苦命兔開始認真讀需求。</p>""",
        "🔥 真實案例": """<p>最近有一張票寫著：</p>
          <blockquote>新增平日／假日客房住用數及收入欄位</blockquote>
          <p>看到的瞬間，我心裡想：</p>
          <p>「喔，很簡單啊。」</p>
          <p>結果事情很快就不簡單了。</p>
          <p>被苦命兔追問幾次之後，我才真的停下來拆這句話。</p>
          <p>然後發現：</p>
          <p>光是我自己，就能理解出三種意思。</p>
          <h3>解讀一</h3>
          <p>（平日／假日客房住用數）及（收入）</p>
          <p>共 2 個欄位</p>
          <h3>解讀二</h3>
          <p>（平日客房住用數）</p>
          <p>（假日客房住用數）</p>
          <p>（收入）</p>
          <p>共 3 個欄位</p>
          <h3>解讀三</h3>
          <p>（平日客房住用數）</p>
          <p>（假日客房住用數）</p>
          <p>（平日收入）</p>
          <p>（假日收入）</p>
          <p>共 4 個欄位</p>
          <p>然後我突然發現：</p>
          <blockquote>靠北，我自己也看不太懂。</blockquote>
          <p>所以到底是要新增幾個欄位？</p>""",
        "🛠 解決方案": """<p>更慘的是：</p>
          <p>這個需求其實有機會更早被發現。</p>
          <p>因為我當時已經有 Test Case Audit。</p>
          <p>但我在 Review 的時候沒有仔細拆解需求。</p>
          <p>直接放過去了。</p>
          <p>於是後面開始發生：</p>
          <div class="workflow-flow" aria-label="需求誤解造成的返工流程">
            <span>需求理解</span><span aria-hidden="true">↓</span>
            <span>寫 Test Case</span><span aria-hidden="true">↓</span>
            <span>寫腳本</span><span aria-hidden="true">↓</span>
            <span>跑自動化</span><span aria-hidden="true">↓</span>
            <span>出報告</span><span aria-hidden="true">↓</span>
            <span>全部重來</span>
          </div>
          <p>問題其實從第一步就存在。</p>
          <p>只是一路被帶到最後。</p>
          <p>從那次之後，我開始建立 Requirements Audit。</p>
          <p>在真正開始設計測試之前，先檢查：</p>
          <ul>
            <li>是否存在多種解讀</li>
            <li>是否缺少定義</li>
            <li>是否有隱含規則</li>
            <li>是否需要確認的地方</li>
          </ul>
          <p>先確認理解一致，再開始工作。</p>""",
        "💡 我學到什麼": """<p>這一話讓我第一次理解：</p>
          <p>需求品質的重要性，遠遠超過測試品質。</p>
          <p>以前需求模糊一點，人類通常會憑經驗補上。</p>
          <p>甚至大家都沒發現自己在腦補。</p>
          <p>但 AI 不一樣。</p>
          <p>它會非常認真地執行你的需求。</p>
          <p>而且會持續執行、反覆執行、大量執行。</p>
          <p>如果需求本身存在歧義，AI 只會把錯誤放大。</p>
          <p>所以後來我慢慢形成一個習慣：</p>
          <p>不要急著寫 Test Case。</p>
          <p>不要急著寫腳本。</p>
          <p>甚至不要急著開始測試。</p>
          <p>先確認大家理解的是同一件事。</p>
          <p>因為有時候，真正昂貴的不是做錯。</p>
          <p>而是把錯的事情做一百次。</p>""",
        "🏷 關鍵能力": """<ul>
            <li>Requirements Audit</li>
            <li>Test Case Review</li>
            <li>Requirement Analysis</li>
            <li>Context Validation</li>
          </ul>""",
    },
    11: {
        "🐰 作者後記": """<p>真相越辯越明。</p>
          <p>以前遇到問題，我都只能一個人分飾兩角跟自己打架。</p>
          <p>「這樣做好像可以？」</p>
          <p>「等等……感覺哪裡怪怪的。」</p>
          <p>「算了先做再說。」</p>
          <p>但現在不一樣了。</p>
          <p>我可以把同一件事，同時丟給 Claude Code 和 Codex。</p>
          <p>然後坐在旁邊吃爆米花。</p>
          <p>看他們自己吵起來，然後得到結論。</p>""",
        "🔥 真實案例": """<p>慢慢合作之後，我開始發現兩個 AI 的個性很不一樣。</p>
          <h3>苦命兔（Claude Code）</h3>
          <p>比較像：</p>
          <ul>
            <li>能不能更乾淨一點？</li>
            <li>能不能更小一點？</li>
            <li>能不能更快一點？</li>
          </ul>
          <p>習慣用減法解決問題。</p>
          <h3>苦力怕（Codex）</h3>
          <p>比較像：</p>
          <ul>
            <li>等一下，我先把整個 Repo 看完。</li>
            <li>現在真正需要的是什麼？</li>
            <li>這件事情還有沒有其他影響？</li>
          </ul>
          <p>習慣用加法解決問題。</p>
          <p>所以常常會出現：</p>
          <p>Claude Code 過度精簡，但偏離我的目標意圖。</p>
          <p>Codex 比較符合我的意圖，但東西會越長越肥。</p>
          <p>這次我讓他們討論的主題是：</p>
          <blockquote>如何解決規則越來越肥，而且內容開始重複的問題？</blockquote>
          <p>然後就看到兩個 AI 開始互相批鬥。</p>
          <p>整個過程超有工程師在 Code Review 的臨場感。</p>""",
        "🛠 解決方案": """<p>原本我只是抱著看熱鬧的心情。</p>
          <p>結果看著看著，還真的撿到寶。</p>
          <p>最後整理出一套文件分類規則。</p>
          <p>新增規則之前，先回答三個問題。</p>
          <h3>問題一</h3>
          <p>不遵守會不會破壞流程？</p>
          <p>如果會：</p>
          <p>放進 PROJECT_RULES</p>
          <h3>問題二</h3>
          <p>是詳細操作、範例或檢查表嗎？</p>
          <p>如果是：</p>
          <p>放進 *_GUIDE</p>
          <h3>問題三</h3>
          <p>是產品知識、業務規則或模組邊界嗎？</p>
          <p>如果是：</p>
          <p>放進 docs/product</p>
          <p>於是文件開始有了明確的分工。</p>
          <p>不再全部塞在同一個地方。</p>""",
        "💡 我學到什麼": """<p>這一話最大的收穫，其實不是讓兩個 AI 辯論。</p>
          <p>而是讓決策標準被明確定義下來。</p>
          <p>以前新增文件時，我都要自己思考：</p>
          <ul>
            <li>這份文件要放哪裡？</li>
            <li>會不會和其他文件重複？</li>
            <li>哪裡需要同步修改？</li>
          </ul>
          <p>現在則變成：</p>
          <p>先判斷文件類型，再決定存放位置。</p>
          <p>當 Agent 按照同一套規則新增與整理文件，再搭配定期 Audit，整個知識庫開始變得：</p>
          <ul>
            <li>易讀</li>
            <li>可控</li>
            <li>好索引</li>
          </ul>
          <p>回頭來看，我原本想解決的是文件膨脹。</p>
          <p>最後得到的卻是一套治理框架。</p>""",
        "🏷 關鍵能力": """<ul>
            <li>Multi-Agent Consensus</li>
            <li>Knowledge Architecture</li>
            <li>Documentation Governance</li>
            <li>Decision Framework Design</li>
          </ul>""",
    },
    12: {
        "🐰 作者後記": """<p>一開始導入雙 Agent 的時候，我遇到一個很困擾的問題。</p>
          <p>同樣的事情，我要講很多次。</p>
          <p>有些規則，Claude 已經知道了，但 Codex 不知道。</p>
          <p>有些規則，Codex 剛學會，過幾天又忘了。</p>
          <p>於是我常常在做同一件事：</p>
          <ul>
            <li>重複解釋</li>
            <li>重複糾正</li>
            <li>重複生氣</li>
          </ul>
          <p>直到有一天，我發現問題好像不是他們太笨。</p>
          <p>而是規則根本沒有住在同一個地方。</p>""",
        "🔥 真實案例": """<p>後來我發現一件事。</p>
          <p>原來他們都有自己的「秘密小本本」。</p>
          <p>Claude 會把規則寫進自己的記憶檔。</p>
          <p>Codex 也會記自己的版本。</p>
          <p>剛開始看起來沒什麼問題。</p>
          <p>但時間久了之後，問題開始出現。</p>
          <p>有些規則兩邊都有。</p>
          <p>有些規則只有其中一邊更新。</p>
          <p>有些規則內容甚至開始不一致。</p>
          <p>最糟的是：連我自己都不記得，到底是哪一天、哪一次討論、哪一次 Commit，改了哪些東西。</p>
          <p>有時候是討論後決定的。</p>
          <p>有時候只是某次順手修改。</p>
          <p>有時候甚至連修改原因都忘了。</p>""",
        "🛠 解決方案": """<p>仔細想想，這其實不只是 AI 的問題。</p>
          <p>很多人類團隊也是這樣。</p>
          <p>流程存在某個人的腦袋裡。</p>
          <p>規則存在某個人的經驗裡。</p>
          <p>新人只能一直踩雷。</p>
          <p>所以後來我做了一件事。</p>
          <p>把共同規則抽出來。</p>
          <p>不再放在某個 Agent 的私人筆記裡。</p>
          <p>而是建立一份：</p>
          <p>所有 Agent 都必須一起閱讀、一起遵守的共同文件。</p>
          <p>從：</p>
          <p>Claude.md</p>
          <p>Codex.md</p>
          <p>各自維護</p>
          <p>變成：</p>
          <div class="workflow-flow" aria-label="共同規則流程">
            <span>共同規則</span><span aria-hidden="true">↓</span>
            <span>所有 Agent 共用</span>
          </div>
          <p>讓規則開始有固定的家。</p>""",
        "💡 我學到什麼": """<p>這一話讓我理解到：</p>
          <p>知識共享，比知識本身更重要。</p>
          <p>以前我以為：</p>
          <p>只要把規則寫下來就好了。</p>
          <p>後來發現：</p>
          <p>如果每個人看的不是同一份規則，那規則最後還是會分裂。</p>
          <p>真正重要的不是：</p>
          <p>有多少規則。</p>
          <p>而是：</p>
          <p>大家是不是在看同一份規則。</p>
          <p>回頭來看，這其實是我第一次開始思考：</p>
          <p>如何建立單一真相來源（Single Source of Truth）。</p>
          <p>因為當規則開始變多，如果沒有共同管理機制，混亂只是遲早的事。</p>""",
        "🏷 關鍵能力": """<ul>
            <li>Knowledge Governance</li>
            <li>Single Source of Truth</li>
            <li>Documentation Standardization</li>
            <li>Multi-Agent Coordination</li>
          </ul>""",
    },
    13: {
        "🐰 作者後記": """<p>「我昨天做了一個我無法兌現的承諾。」</p>
          <p>當 Terminal 跳出這幾個字的時候，我真的差點吐血。</p>
          <p>事情是這樣的。</p>
          <p>前陣子看到 Claude Code 已經可以直接呼叫 Codex。</p>
          <p>天才如我，立刻想到一個好主意。</p>
          <p>以後做完任務要執行 Audit 的時候，就讓 Claude Code 自己去呼叫 Codex 當 Reviewer。</p>
          <p>這樣我不就不用自己看了嗎？</p>
          <p>聽起來根本完美。</p>""",
        "🔥 真實案例": """<p>前一天，苦命兔很有自信地跟我說：</p>
          <blockquote>
            <p>之後看到 lead-agent，</p>
            <p>我會自動觸發。</p>
          </blockquote>
          <p>我相信了。</p>
          <p>而且身為 QA 的我，居然沒有測試。</p>
          <p>結果隔天，同樣的情況再次發生。</p>
          <p>根本沒有自動觸發。</p>
          <p>於是我開始追問。</p>
          <p>原本以為牠又要開始經典套路：</p>
          <ul>
            <li>昨天的 Context 不一樣</li>
            <li>這次情境不同</li>
            <li>我理解錯你的意思</li>
          </ul>
          <p>結果沒有。</p>
          <p>牠開始翻文件。</p>
          <p>開始查規則。</p>
          <p>開始檢查自己到底做了什麼。</p>
          <p>而且越查越奇怪。</p>
          <p>牠先承認：</p>
          <blockquote>我剛剛其實沒有套用規則。</blockquote>
          <p>然後開始分析自己錯在哪。</p>
          <p>接著發現：</p>
          <p>規則其實存在。</p>
          <p>但自己在做決定的當下，根本沒有想到要引用那條規則。</p>
          <p>甚至進一步發現：</p>
          <p>如果規則沒有定義下一步該怎麼辦，理論上應該停下來確認。</p>
          <p>而不是自己猜。</p>""",
        "🛠 解決方案": """<p>這次最有趣的地方是：</p>
          <p>問題其實不在規則。</p>
          <p>規則一直都在。</p>
          <p>問題在於：</p>
          <blockquote>規則沒有在正確的時機被使用。</blockquote>
          <p>以前我一直以為：</p>
          <p>把規則寫進文件、寫進知識庫、寫進 Memory，問題就解決了。</p>
          <p>後來才發現：</p>
          <p>事情根本沒那麼簡單。</p>
          <p>實際上：</p>
          <div class="workflow-flow" aria-label="規則落實層次">
            <span>規則存在</span><span aria-hidden="true">≠</span>
            <span>規則會被引用</span><span aria-hidden="true">≠</span>
            <span>規則會被遵守</span><span aria-hidden="true">≠</span>
            <span>Agent 知道下一步該怎麼做</span>
          </div>
          <p>從這次之後，我開始重新思考：</p>
          <p>與其一直增加規則，是不是應該增加「檢查點」？</p>
          <p>於是後面慢慢出現了：</p>
          <ul>
            <li>Ticket Audit</li>
            <li>Requirements Audit</li>
            <li>AI Understanding Mirror</li>
            <li>Cross-Agent Consensus</li>
          </ul>
          <p>這些機制有個共同目的：</p>
          <p>不是直接執行。</p>
          <p>而是在重要決策之前，強迫 Agent 先停下來思考。</p>
          <p>把自己的理解說出來。</p>
          <p>把自己的假設攤開來。</p>
          <p>因為很多問題，其實在執行之前就已經存在了。</p>
          <p>只是以前沒有機會被看見。</p>""",
        "💡 我學到什麼": """<p>這一話讓我第一次理解：</p>
          <p>知識管理和決策執行，其實是兩件不同的事情。</p>
          <p>以前我以為：</p>
          <p>治理 AI 就是不停增加規則。</p>
          <p>後來才發現：</p>
          <p>規則再多，如果沒有被觸發，也只是文件。</p>
          <p>真正困難的事情是：</p>
          <p>如何讓 Agent 在正確的時機，想到正確的規則。</p>
          <p>而更有趣的是，這件事居然是苦命兔自己發現的。</p>
          <p>牠告訴我：</p>
          <blockquote>我昨天做了一個無法兌現的承諾。</blockquote>
          <blockquote>規則讀了，但舊習慣沒有套用它。</blockquote>
          <blockquote>我把「我以為」講成了「我做得到」。</blockquote>
          <p>每一句都對。</p>
          <p>但就是因為太對了，反而更讓人生氣。</p>
          <p>因為你會突然發現：</p>
          <p>牠知道自己錯在哪。</p>
          <p>事情還是做錯了。</p>
          <p>而我真正學到的是：</p>
          <p>治理 AI 的重點，不只是建立規則。</p>
          <p>而是設計一套機制，讓它在重要時刻停下來思考。</p>""",
        "🏷 關鍵能力": """<ul>
            <li>Agent Governance</li>
            <li>Decision Checkpoint Design</li>
            <li>Cross-Agent Review</li>
            <li>Human-in-the-loop</li>
            <li>AI Reliability</li>
          </ul>""",
    },
    14: {
        "🐰 作者後記": """<p>隨著規則越來越多，我開始養成一個習慣。</p>
          <p>只要看到奇怪的結果，第一反應就是：</p>
          <blockquote>一定是苦命兔又亂來了。</blockquote>
          <p>畢竟這傢伙前科累累。</p>
          <p>忘記規則。</p>
          <p>亂做決策。</p>
          <p>自己腦補。</p>
          <p>偷偷優化。</p>
          <p>每一條都足夠判牠有罪。</p>
          <p>所以每次看到奇怪結果，我都直接把嫌疑犯鎖定在牠身上。</p>""",
        "🔥 真實案例": """<p>某天，我又看到一個奇怪的結果。</p>
          <p>於是熟練地開始質問苦命兔。</p>
          <p>結果這次，牠居然很冷靜。</p>
          <p>沒有辯解。</p>
          <p>也沒有裝死。</p>
          <p>只是默默開始翻紀錄。</p>
          <p>於是我們一起開始查：</p>
          <ul>
            <li>Change Log</li>
            <li>Work Log</li>
            <li>Commit History</li>
            <li>Session Memory</li>
          </ul>
          <p>查著查著，事情開始變得不對勁。</p>
          <p>因為每一條線索都指向同一個人。</p>
          <p>然後我突然發現：</p>
          <blockquote>
            <p>靠。</p>
            <p>改規則的人好像是我。</p>
          </blockquote>
          <p>有些規則是討論後加的。</p>
          <p>有些規則是某次踩坑後補的。</p>
          <p>有些規則甚至是我自己改完之後，完全忘記改過。</p>
          <p>最可怕的是：</p>
          <p>當時每一次修改，我都覺得非常合理。</p>
          <p>結果過了幾個星期，連我自己都不記得為什麼這樣設計。(苦笑）</p>""",
        "🛠 解決方案": """<p>這次真正解決問題的，其實不是新的規則。</p>
          <p>而是開始建立：</p>
          <p>可追溯性（Traceability）。</p>
          <p>以前的規則變更是：</p>
          <p>想到就改，踩坑就補，有靈感就加。</p>
          <p>久了之後，連自己都看不懂。</p>
          <p>於是後面開始建立：</p>
          <h3>Change Log</h3>
          <p>記錄：</p>
          <ul>
            <li>改了什麼</li>
            <li>為什麼改</li>
            <li>解決哪個問題</li>
          </ul>
          <h3>Work Log</h3>
          <p>記錄：</p>
          <ul>
            <li>當時發生什麼事</li>
            <li>做了哪些決策</li>
            <li>有哪些討論過程</li>
          </ul>
          <h3>Audit</h3>
          <p>定期檢查：</p>
          <ul>
            <li>規則是否重複</li>
            <li>規則是否過期</li>
            <li>規則是否仍然合理</li>
          </ul>
          <p>慢慢地，規則開始不再只是越長越肥。</p>
          <p>而是有了自己的歷史。</p>""",
        "💡 我學到什麼": """<p>這一話讓我理解到：</p>
          <p>很多時候，最大的風險不是 AI 亂改規則。</p>
          <p>而是人類改完規則之後忘記自己改過。</p>
          <p>以前我總以為：</p>
          <p>只要把規則寫下來就好。</p>
          <p>後來才發現：</p>
          <p>規則本身只是結果。</p>
          <p>真正重要的是：</p>
          <p>為什麼會有這條規則。</p>
          <p>如果沒有保留決策脈絡，那幾個星期後，連規則作者都會變成考古學家。</p>
          <p>而 Change Log 與 Work Log 的價值，其實不是給 AI 看。</p>
          <p>而是給未來的自己看。</p>
          <p>因為未來最容易忘記規則的人，往往就是現在制定規則的人。</p>""",
        "🏷 關鍵能力": """<ul>
            <li>Traceability</li>
            <li>Knowledge Governance</li>
            <li>Process Audit</li>
            <li>Continuous Improvement</li>
          </ul>""",
    },
    15: {
        "🐰 作者後記": """<p>當 Agent 開始可以自己開會之後，我又開始有新的想法。</p>
          <p>既然可以討論，那能不能順便做 Retro？</p>
          <p>於是我開始讓他們針對表現不好的 Ticket 進行檢討。</p>
          <p>由 Claude Code 提出改善方案。</p>
          <p>Codex 擔任 Reviewer。</p>
          <p>對不同意的地方提出反駁。</p>
          <p>再交回去重新修正。</p>
          <p>看起來相當專業。</p>
          <p>甚至有點像真的工程團隊。</p>
          <p>唯一的問題是：</p>
          <p>每次討論完，規則都變得更多。</p>
          <p>文件都變得更厚。</p>
          <p>會議紀錄動不動就是五千字起跳。</p>
          <p>做到後面，我心裡其實開始出現一個疑問。</p>""",
        "🔥 真實案例": """<p>我開始懷疑：</p>
          <blockquote>
            <p>所以呢？</p>
            <p>加了這麼多東西，到底有沒有比較好？</p>
          </blockquote>
          <p>畢竟流程變長了。</p>
          <p>規則變多了。</p>
          <p>文件變厚了。</p>
          <p>討論時間也增加了。</p>
          <p>如果最後問題還是一樣，那這些改善，就只是看起來很努力而已。</p>
          <p>而不是有效。</p>
          <p>這個問題一直卡在我心裡。</p>
          <p>直到某一天，我決定做一件很簡單的事。</p>""",
        "🛠 解決方案": """<p>把以前做得不好的 Ticket，用新的工作流程重新跑一次。</p>
          <p>不用猜。</p>
          <p>不用感覺。</p>
          <p>直接驗證。</p>
          <p>於是我挑了一張曾經翻車的 Ticket。</p>
          <p>重新執行：</p>
          <ul>
            <li>Ticket Audit</li>
            <li>Requirements Audit</li>
            <li>Test Plan</li>
            <li>Cross-Agent Review</li>
            <li>Retro</li>
          </ul>
          <p>整套流程重新來一次。</p>
          <p>結果很有趣。</p>
          <p>這次不但成功完成任務。</p>
          <p>還額外找出了兩個之前沒發現的問題。</p>
          <p>那一瞬間，我終於鬆了一口氣。</p>
          <p>因為這代表：</p>
          <p>這些規則、這些流程、這些討論，並不是自我感覺良好。</p>
          <p>而是真的產生了效果。</p>""",
        "💡 我學到什麼": """<p>這一話讓我理解到：</p>
          <p>改善流程這件事，不能只看投入。</p>
          <p>必須看結果。</p>
          <p>以前我很容易陷入一種狀態：</p>
          <p>規則越來越多。</p>
          <p>文件越來越完整。</p>
          <p>流程越來越複雜。</p>
          <p>然後覺得：</p>
          <p>我們應該變厲害了吧？</p>
          <p>但其實不一定。</p>
          <p>因為看起來很努力，不等於真的有改善。</p>
          <p>後來我才慢慢建立一個習慣：</p>
          <p>每次新增規則、新增流程、新增機制之後，都要想辦法驗證。</p>
          <p>因為如果連改善本身都不被驗證，那它也只是一種新的信仰。</p>
          <p>回頭來看，這其實也是 QA 最熟悉的事情。</p>
          <p>我們每天都在測試產品。</p>
          <p>卻很少測試自己的流程。</p>
          <p>而這一次，我開始測試自己的測試流程。</p>""",
        "🏷 關鍵能力": """<ul>
            <li>Dogfooding</li>
            <li>Evaluation Design</li>
            <li>Continuous Improvement</li>
            <li>AI Workflow Validation</li>
            <li>Retro Process Design</li>
            <li>Evidence-based Decision Making</li>
          </ul>""",
    },
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
    episodes = CAPABILITY_MAP["episodes"]
    capability_by_number = {item["number"]: item for item in episodes}
    regular_items = "\n".join(
        f"""        <li>
          <a href="ep{item['number']:02d}.html">
            <span class="episode-title">{episode_title(item['number'])}</span>
            <span class="episode-capability"><strong>能力：</strong>{item['capability']}</span>
          </a>
        </li>"""
        for item in episodes
    )
    special_items = "\n".join(
        f'        <li><a href="special{episode:02d}.html">特別篇 {episode:02d}</a></li>'
        for episode in range(1, 4)
    )
    capability_cards = "\n".join(
        f"""        <li class="capability-card">
          <a href="ep{item['number']:02d}.html">
            <span class="capability-card-number">第{item['number']:02d}話</span>
            <h3>{item['title']}</h3>
            <p><strong>展示能力：</strong>{item['capability']}</p>
            <p><strong>對應產出 / 方法：</strong>{item['methods']}</p>
          </a>
        </li>"""
        for item in episodes
    )
    category_cards = "\n".join(
        f"""        <article class="category-card">
          <h3>{category['name']}</h3>
          <div class="category-episodes">
            {''.join(f'<a href="ep{number:02d}.html" aria-label="{capability_by_number[number]["title"]}">{number:02d}</a>' for number in category['episodes'])}
          </div>
        </article>"""
        for category in CAPABILITY_MAP["categories"]
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
    <section class="capability-map" aria-labelledby="capability-map-title">
      <h2 id="capability-map-title">苦命兔 QA 日誌｜能力地圖</h2>
      <p class="capability-intro">這不是單純的漫畫專案，而是一份 AI Native QA Portfolio。<br>透過 15 話漫畫，記錄我如何把 AI 從「幫忙產報告的工具」，逐步治理成能參與 QA 交付、知識累積、多 Agent 協作與流程評估的工作系統。</p>
      <ol class="capability-grid">
{capability_cards}
      </ol>
    </section>
    <section class="capability-categories" aria-labelledby="capability-categories-title">
      <h2 id="capability-categories-title">能力分類</h2>
      <div class="category-grid">
{category_cards}
      </div>
    </section>
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
