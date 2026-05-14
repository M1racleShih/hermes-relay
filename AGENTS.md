# Project Instructions for AI/Hermes

本仓库用于学习 Hermes Agent 源码并逐步实现 A2A 支持。

当你协助本仓库工作时，请遵守：

1. 先检查 `LEARNING_PLAN.md`、`SOURCE_MAP.md`、`ROADMAP_A2A.md`，不要直接跳到实现。
2. 任何源码分析都必须落到具体文件、函数、调用链和不变量。
3. 遇到流程性内容，优先用 Mermaid 图表达。
4. 不要建议线性精读整个 `run_agent.py`；应该按任务切片阅读。
5. 每次学习会话都要更新 `journal/`，并尽量新增或完善一份 `notes/source/` 或 `notes/design/` 文档。
6. 如果讨论 A2A，实现优先级是：AgentCard -> task/session mapping -> non-stream message send -> streaming -> cancellation -> auth/permission -> advanced artifacts。
7. 对远程协议入口保持安全保守：不要暴露 prompt、memory、raw reasoning、credentials、完整内部工具表。
8. 如果需要修改 Hermes 上游源码，先提出 PR 分解和测试计划，不要一次性大改。

推荐输出格式：

```text
目标：
相关源码：
调用链：
关键不变量：
风险：
验证方式：
下一步 commit：
```
