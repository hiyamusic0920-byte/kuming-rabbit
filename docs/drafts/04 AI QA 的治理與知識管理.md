思考用
### 使用 AI 做測試，需要做什麼準備？

這是你的第 3 點。

我反而覺得這是你最有價值的部分。

因為大家都在講：

> 怎麼用 Claude Code

但很少人講：

> 怎麼避免 Claude Code 變白癡

這裡就能寫：

- Project Rules
- Registry
- SOP
- Governance
- Dogfood

當我校正 AI 的理解時，我會問一個問題：

> 這個判斷會不會改變未來 agent 對類似情境的決定？

如果會，它就不該只留在這次對話裡。

例如，某個產品規則會影響未來 test plan，就應該進產品知識；某個 UI 等待條件會影響未來 Playwright selector，就應該進 registry；某個測試資料準備方式會反覆用到，就應該進 seeds；某個 QA 判斷原則會跨票重用，就應該進 QA heuristics。

這也是我後來把 `qa-thought-capture` 重建成「測試執行中即時攔截器」的原因。

原本我以為，可以在測前一次問完：「這張票你想怎麼測？」但實際上，很多 QA 直覺不是測前想出來的，而是測到一半才冒出來。

所以新的做法是：只要測試過程中出現非顯然、可複用、會影響未來決策的判斷，就當下攔截，之後分流寫回 repo。

需求理解不是一次性的 prompt 技巧，而是一個會被不斷校正、回收、再利用的知識循環。

| 知識類型                  | 放置位置                                      |     |     |
| --------------------- | ----------------------------------------- | --- | --- |
| 產品規則與商業邏輯             | `docs/product/`                           |     |     |
| 單張 ticket 的功能知識       | `docs/features/`                          |     |     |
| 測試策略與測試案例             | `docs/tickets/`                           |     |     |
| UI selector、等待條件、互動陷阱 | `pages/_registry/`                        |     |     |
| 測試資料與 seed 策略         | `seeds/`                                  |     |     |
| 通用 QA 判斷              | `docs/QA_HEURISTICS.md`                   |     |     |
| agent 工作規則            | `docs/PROJECT_RULES.md`、`.agents/skills/` |     |     |