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
