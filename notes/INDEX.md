# Notes Index

知识图谱导航。

## 源码笔记

| 笔记 | 覆盖源码模块 | Phase | 关联 |
|---|---|---|---|
| `00-architecture-overview.md` | 全局架构、入口、核心层、运行形态、一条请求的完整旅程 | 0 | 前置：无。延伸：所有笔记 |
| `00-source-file-index.md` | 全部关键源码文件索引（按模块分类，精确到行号） | 0 | 前置：无。与所有笔记交叉引用 |
| `01-tool-system-full-chain.md` | registry + model_tools + toolsets + approval 全链路 | 1 | 前置：00。延伸：02 |
| `02-prompt-assembly.md` | prompt builder、skills、memory snapshot、context files | 2 | 前置：01 |
| `03-agent-turn-lifecycle.md` | agent loop | 3 | 前置：01, 02 |
| `05-gateway-internals.md` | gateway | 4 | 前置：03 |
| `06-acp-adapter.md` | ACP adapter | 5 | 前置：03。A2A 直接参考 |

## 设计笔记

| 笔记 | 主题 | 关联 |
|---|---|---|
| `a2a-hermes-mapping.md` | A2A 与 Hermes 映射 | 前置：03, 06 |

## 笔记模板（v3）

每个笔记必须包含：
1. **核心结论**（先说结论，2-4 句）
2. **推荐阅读路径**（按什么顺序读源码最有效）
3. **重难点清单**（★-★★★ 难度标记）
4. **设计意图**（Why，推荐但不强制）
5. 详细分析（调用链、数据结构、不变量；必要时用 Mermaid、ASCII、表格或文字结构辅助说明）

## 参考仓库（Claude Code 源码剖析方法论）

| 仓库 | Stars | 特色 | 推荐用途 |
|---|---|---|---|
| [liuup/claude-code-analysis](https://github.com/liuup/claude-code-analysis) | 2.5k | 18章 + 7篇组件详解，从总览到函数级拆解 | 整体组织方式参考 |
| [anneheartrecord/claude-code-docs](https://github.com/anneheartrecord/claude-code-docs) | — | 13篇，中英双语，每篇聚焦一个核心机制 | 按需查阅 |
| [alchaincyf/claude-code-source-analysis-orange-book](https://github.com/alchaincyf/claude-code-source-analysis-orange-book) | — | 80页 PDF，强调设计决策背后的原因 | 方法论参考 |
| [ghboke/claude-code-reverse](https://github.com/ghboke/claude-code-reverse) | — | 启动流程分析最详细 | 入口分析参考 |

## 当前进度

- **Phase 0**：✅ 完成（repo map + 代码证据索引 + 架构总览）
- **Phase 1**：✅ 完成（Tool System 全链路，已补图文说明）
- **Phase 2**：✅ 完成（Prompt Assembly，已按源码修正 skills 缓存描述）
- **Phase 3-6**：下一里程碑，目标是 core development readiness（AIAgent loop、state/memory、Gateway、ACP）
- **Phase 7-8**：A2A design readiness（provider/runtime policy + protocol mapping）
- **Phase 9-10**：A2A 毕业设计（spike + MVP PR design）
