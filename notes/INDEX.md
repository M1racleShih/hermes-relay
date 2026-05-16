# Notes Index

知识图谱导航。记录笔记覆盖的源码模块、笔记之间的关联关系、当前学习进度。

## 源码笔记

| 笔记 | 覆盖源码模块 | Phase | 关联 |
|---|---|---|---|
| `00-repo-map.md` | 全局架构、入口、核心层 | 0 | 前置：无。延伸：01, 02, 03, 05, 06 |
| `01-tool-runtime.md` | `tools/registry.py`, `model_tools.py`, `toolsets.py` | 1 | 前置：00。延伸：03（agent loop 如何调用 tool） |
| `02-prompt-assembly.md` | `prompt_builder.py`, `prompt_caching.py`, `skill_commands.py` | 2 | 前置：00。延伸：03（agent turn 中的 prompt 使用） |
| `03-agent-loop.md` | `run_agent.py`, `model_tools.py`, `context_compressor.py` | 3 | 前置：01, 02。延伸：05（gateway 如何调用 agent） |
| `05-gateway-internals.md` | `gateway/run.py`, `gateway/platforms/base.py`, `gateway/session.py` | 5 | 前置：03。延伸：06（ACP 类似 adapter 模式） |
| `06-acp-adapter.md` | `acp_adapter/server.py`, `session.py`, `events.py`, `permissions.py` | 6 | 前置：03, 05。延伸：`a2a-hermes-mapping.md` |
| `diagram-source-alignment.md` | 跨模块审计 | 跨 Phase | 引用：00, 01, 02, 03, 05, 06 |

## 设计笔记

| 笔记 | 主题 | Phase | 关联 |
|---|---|---|---|
| `a2a-hermes-mapping.md` | A2A 协议对象到 Hermes 的映射设计 | 8 | 前置：06（ACP 参考实现）。延伸：ROADMAP_A2A.md |
| `learning-plan-review.md` | 学习路线评审与加速建议 | 跨 Phase | 引用：LEARNING_PLAN.md |

## 进度

| Phase | 状态 | 笔记 |
|---|---|---|
| 0 仓库定位 | 已完成 | `00-repo-map.md` |
| 1 Tool System | 有初始笔记 | `01-tool-runtime.md` |
| 2 Prompt Assembly | 有初始笔记 | `02-prompt-assembly.md` |
| 3 Agent Turn | 有初始笔记 | `03-agent-loop.md` |
| 4 SessionDB/Memory | 空缺 | — |
| 5 Gateway | 有初始笔记 | `05-gateway-internals.md` |
| 6 ACP Adapter | 有初始笔记 | `06-acp-adapter.md` |
| 7 Provider Runtime | 空缺 | — |
| 8 A2A Mapping | 有初始设计笔记 | `a2a-hermes-mapping.md` |
| 9 A2A Spike | 未开始 | — |
