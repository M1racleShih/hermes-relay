# Hermes Core Developer Learning Repo

这是一个用于系统学习 `NousResearch/hermes-agent` 并逐步达到核心开发者水平的个人学习仓库。

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

然后按 `LEARNING_PLAN.md` 从 Phase 0 开始推进。每次学习都要求产出：

1. 一份 session log；
2. 一份源码阅读笔记或图；
3. 一个小 commit；
4. 一个可验证动作：测试、脚本、复现、最小 patch、设计草案之一。

## 仓库布局

```text
.
├── LEARNING_PLAN.md              # 主学习计划
├── SOURCE_MAP.md                  # Hermes 源码地图与阅读顺序
├── ROADMAP_A2A.md                 # 让 Hermes 支持 A2A 的实现路线
├── RULES.md                       # 学习与贡献规则
├── AGENTS.md                      # 给 Hermes/AI 助手的项目上下文
├── docs/diagrams/                 # Mermaid 架构图
├── journal/                       # 每次学习记录
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
# 阅读、画图、写笔记、做验证
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
