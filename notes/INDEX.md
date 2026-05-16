# Notes Index

知识图谱导航。

## 源码笔记

| 笔记 | 覆盖源码模块 | Phase | 关联 |
|---|---|---|---|
| `00-repo-map.md` | 全局架构、入口、核心层 | 0 | 前置：无。延伸：01, 01a, 02, 03, 05, 06 |
| `01-tool-runtime.md` | registry + model_tools + toolsets 概览 | 0→1 | 前置：00。延伸：01a |
| `01a-registry-dispatch-deep.md` | ToolEntry, ToolRegistry, discover, register, dispatch, get_definitions, handle_function_call, toolsets 解析 | 1 | 前置：01。延伸：下一步→approval + terminal_tool |
| `02-prompt-assembly.md` | prompt 层 | 1 | 前置：01 |
| `03-agent-loop.md` | agent loop | 2 | 前置：01 |
| `05-gateway-internals.md` | gateway | 3 | 前置：03 |
| `06-acp-adapter.md` | ACP adapter | 4 | 前置：01a。A2A 直接参考 |

## 设计笔记

| 笔记 | 主题 | 关联 |
|---|---|---|
| `a2a-hermes-mapping.md` | A2A 与 Hermes 映射 | 前置：01a, 06 |

## 当前进度

- **Phase 0**：✅ 完成（repo map + 概览笔记）
- **Phase 1**：🔄 进行中（切片 1-1 完成，下一步：approval + terminal_tool）
- **Phase 2-9**：待开始
