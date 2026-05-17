# Notes Index

知识图谱导航。

## 源码笔记

| 笔记 | 覆盖源码模块 | Phase | 关联 |
|---|---|---|---|
| `00-repo-map.md` | 全局架构、入口、核心层、运行形态、一条请求的完整旅程 | 0 | 前置：无。延伸：所有笔记 |
| `00-code-evidence-index.md` | 全部关键源码文件索引（按模块分类，精确到行号） | 0 | 前置：无。与所有笔记交叉引用 |
| `01-tool-runtime.md` | registry + model_tools + toolsets 概览 | 0→1 | 前置：00。延伸：01a |
| `01a-registry-dispatch-deep.md` | ToolEntry, ToolRegistry, discover, register, dispatch, get_definitions, handle_function_call, toolsets 解析 | 1 | 前置：01。延伸：01b |
| `01b-approval-and-e2e.md` | 危险命令审批链（hardline/dangerous/yolo/session），check_fn 探测，web_search 端到端追踪 | 1 | 前置：01a。延伸：Phase 2（prompt assembly） |
| `02-prompt-assembly.md` | prompt 层 | 1 | 前置：01 |
| `03-agent-loop.md` | agent loop | 2 | 前置：01 |
| `05-gateway-internals.md` | gateway | 3 | 前置：03 |
| `06-acp-adapter.md` | ACP adapter | 4 | 前置：01a。A2A 直接参考 |

## 设计笔记

| 笔记 | 主题 | 关联 |
|---|---|---|
| `a2a-hermes-mapping.md` | A2A 与 Hermes 映射 | 前置：01a, 06 |

## 笔记模板（v3）

每个笔记必须包含：
1. **核心结论**（先说结论，2-4 句）
2. **推荐阅读路径**（按什么顺序读源码最有效）
3. **重难点清单**（★-★★★ 难度标记）
4. **设计意图**（Why，推荐但不强制）
5. 详细分析（调用链、数据结构、不变量、Mermaid 图）

## 参考仓库（Claude Code 源码剖析方法论）

| 仓库 | Stars | 特色 | 推荐用途 |
|---|---|---|---|
| [liuup/claude-code-analysis](https://github.com/liuup/claude-code-analysis) | 2.5k | 18章 + 7篇组件详解，从总览到函数级拆解 | 整体组织方式参考 |
| [anneheartrecord/claude-code-docs](https://github.com/anneheartrecord/claude-code-docs) | — | 13篇，中英双语，每篇聚焦一个核心机制 | 按需查阅 |
| [alchaincyf/claude-code-source-analysis-orange-book](https://github.com/alchaincyf/claude-code-source-analysis-orange-book) | — | 80页 PDF，强调设计决策背后的原因 | 方法论参考 |
| [ghboke/claude-code-reverse](https://github.com/ghboke/claude-code-reverse) | — | 启动流程分析最详细 | 入口分析参考 |

## 当前进度

- **Phase 0**：✅ 完成（repo map + 代码证据索引 + 架构总览 v2）
- **Phase 1**：✅ 核心目标达成（切片 1-1、1-2 完成，笔记已补全结论/路径/重难点）
- **Phase 2-9**：待开始
