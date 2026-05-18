# Project Instructions for AI/Hermes

本仓库用于借助 LLM/agent 学习 Hermes Agent 源码，并把 A2A 支持作为阶段性的毕业设计。

当你协助本仓库工作时，请遵守：

1. 先检查 `LEARNING_PLAN.md`、`SOURCE_MAP.md`、`ROADMAP_A2A.md`，不要直接跳到实现。
2. 任何源码分析都必须落到具体文件、函数、调用链和不变量。
3. 遇到流程、状态机、协议映射或调用链时，使用合适的可视化表达辅助理解；可以是 Mermaid、ASCII、表格或文字结构。图必须配文字说明，不把图当成独立知识分类；如果使用 Mermaid，参考 `https://github.com/lukilabs/beautiful-mermaid` 的清晰和可读原则。
4. 不要建议线性精读整个 `run_agent.py`；应该按任务切片阅读。
5. 每次学习会话都要更新 `journal/`，并尽量新增或完善一份 `notes/source/` 或 `notes/design/` 文档。
6. 如果讨论 A2A，实现优先级是：AgentCard -> task/session mapping -> non-stream message send -> streaming -> cancellation -> auth/permission -> advanced artifacts。
7. 对远程协议入口保持安全保守：不要暴露 prompt、memory、raw reasoning、credentials、完整内部工具表。
8. 如果需要修改 Hermes 上游源码，先提出 PR 分解和测试计划，不要一次性大改。

## Agent 自学模式

当用户要求 agent 先替他推进一个小学习切片时，按下面规则执行：

1. 每次只推进一个很小的学习切片，不要一次跨多个 phase。
2. 开始前先声明本次切片来自 `LEARNING_PLAN.md` 的哪个 phase，以及为什么选择它。
3. 优先产出给用户二次学习用的材料，而不是直接实现功能；除非用户明确要求，不要修改 Hermes 上游源码。
4. 每个切片必须落到具体源码文件、函数、调用链、不变量和风险；禁止只写概念总结。
5. 每个切片至少更新一份 `journal/`，并新增或完善一份 `notes/source/` 或 `notes/design/`。
6. 涉及复杂流程、状态机、协议映射或调用链时，自然选择合适的表达方式；如果用了图，图前后都要有文字解释。
7. 每个切片必须包含一个验证动作：可以是只读脚本、现有测试命令、fixture/日志检查、或明确的测试设计；如果没有运行测试，要说明原因。
8. 如果发现需要改上游源码，先停止在设计层，输出 PR 拆分、测试计划和风险，不要直接大改。
9. 如果发现计划文档和源码事实不一致，以源码为准，并在笔记里记录差异。
10. 如果遇到安全、认证、远程入口、prompt/memory/reasoning 暴露问题，立即保守处理并记录为风险。

Agent 自学单次切片建议上限：

- 阅读源码：3-6 个紧密相关文件；
- 新增笔记：1-2 份；
- 源码改动：默认 0；
- 总结输出：必须包含“下一次应该从哪个文件/函数继续”。

推荐 agent 自学输出自然覆盖这些信息：本次切片、阶段来源、入口问题、阅读源码、调用链、关键不变量、验证动作、发现的偏差、风险、产出文件、下一次继续点。如果使用了图或表，要在正文里解释它回答了什么问题。
