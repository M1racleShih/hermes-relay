# Hermes Core Developer Learning Repo

这是一个用于系统学习 `NousResearch/hermes-agent` 并逐步达到核心开发者水平的个人学习仓库。

这个仓库的核心用法是：让 LLM/agent 利用自己的代码理解能力、工程背景和归纳能力，帮你把 Hermes 源码拆成一个个可以学习、复盘和继续推进的小切片。A2A 支持是这个学习计划的“毕业设计”：它不是每次阅读都要提前实现的功能，而是用来验证你是否已经理解 Hermes 的入口、工具、prompt、session、gateway、ACP 和安全边界。

它不是 Hermes 源码镜像。你已经有本地 Hermes 安装和使用经验，所以这里默认你会把 Hermes 源码放在旁边，或者用环境变量指向它：

```bash
export HERMES_SRC="$HOME/code/hermes-agent"
```

建议目录结构：

```text
~/code/
├── hermes-agent/                 # 上游源码 clone
└── hermes-core-dev-learning/     # 本仓库
```

## 使用方式

第一天只做三件事：

```bash
make doctor
make new-log TITLE=repo-orientation
make open-plan
```

然后按 `LEARNING_PLAN.md` 从 Phase 0 开始推进。每次学习都要求留下可追踪证据：

1. 一份源码阅读笔记或设计笔记；
2. 一个小 commit；
3. 一个验证动作：测试、脚本、复现、最小 patch、设计草案之一。

`journal/` 是学习证据的一种，不是强制长文。如果 commit message 已经清楚记录目标、变更、验证和接续点，journal 可以省略；如果本次学习产生了未解决问题、被否定的假设、探索路径或下一次接续点，写一份短 journal。

## Agent 自学 Workflow

当你不在场，或希望 agent 先替你推进一个小学习切片时，使用 agent 自学模式。它不是机械批处理，而是一次小型源码学习会话：

1. 先读 `LEARNING_PLAN.md`、`SOURCE_MAP.md`、`ROADMAP_A2A.md`、`notes/INDEX.md` 和最近一篇 `journal/`。
2. 选一个能被源码验证的问题，通常只覆盖 3-6 个紧密相关文件。
3. 先建立模块在整体架构里的位置，再进入数据流、关键结构、调用链、错误处理和不变量。
4. 每个重要结论都落到具体文件、函数、调用链或测试，不写脱离源码的概念总结。
5. 需要可视化时自然选择表达方式：Mermaid、ASCII、表格或文字都可以。图要服务解释，不能替代解释；用了图就配文字说明它回答什么问题、揭示什么结论。Mermaid 图参考 `beautiful-mermaid` 的清晰和可读原则：`https://github.com/lukilabs/beautiful-mermaid`。
6. 至少做一个验证动作，例如 `rg` 锚点检查、只读脚本、现有测试、fixture 检查或测试设计。验证像 lint/test 一样属于 agent 的工作步骤，不作为笔记评分项；结果写在最终汇报或 commit message，不写进学习笔记正文。
7. 新增或完善一份 `notes/source/` 或 `notes/design/`；新增笔记时同步更新 `notes/INDEX.md`。需要保留探索过程或接续点时，再写短 journal。
8. 结尾留下下一次最自然的继续点。

## 仓库布局

```text
.
├── LEARNING_PLAN.md              # 主学习计划
├── SOURCE_MAP.md                  # Hermes 源码地图与阅读顺序
├── ROADMAP_A2A.md                 # 让 Hermes 支持 A2A 的实现路线
├── RULES.md                       # 学习与贡献规则
├── AGENTS.md                      # 给 Hermes/AI 助手的项目上下文
├── journal/                       # 必要时记录探索过程、疑问和接续点
├── notes/source/                  # 源码精读笔记
├── notes/design/                  # 设计草案和 ADR
├── checklists/                    # 阶段验收清单
├── templates/                     # 记录模板
├── skills/                        # 可给 Hermes 使用的学习技能
└── scripts/                       # 辅助脚本
```

## Git 学习节奏

不要把学习记录写成“大而全”的长文档后一次性提交。更好的方式是高频、小步提交：

```bash
git checkout -b phase/01-tool-system
make new-log TITLE=tool-registry-first-pass
# 阅读源码、写笔记、做验证
git add .
git commit -m "docs(tools): map registry discovery flow"
```

推荐分支命名：

```text
phase/00-orientation
phase/01-tool-system
phase/02-prompt-and-agent-loop
phase/03-session-state
phase/04-gateway-acp
phase/05-a2a-spike
phase/06-a2a-mvp
```

## 当前目标

最终目标不是“看懂很多文件”，而是能以维护者视角完成这类工作：

- 判断一个需求应该是 skill、tool、plugin、gateway adapter、ACP adapter、provider plugin，还是 agent loop 变更；
- 为一个改动建立最小设计、测试边界和回归风险说明；
- 能在不破坏 CLI/Gateway/ACP/Cron 共用核心的前提下，实现 A2A Server/Client 能力；
- 能写出符合 Hermes 贡献风格的 PR。
