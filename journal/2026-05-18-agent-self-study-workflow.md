# Session Log: agent-self-study-workflow

Date: 2026-05-18
Branch:
Hermes commit/version: local source at `$HERMES_SRC`

## Goal

把学习仓库的协作规则统一成“agent 自学”语境：保留切片化、源码取证、验证和接续点，但去掉机械化的图表要求，让文档更像人和 agent 协作学习 Hermes 源码的 workflow。

## Source touched

- `README.md`
- `AGENTS.md`
- `LEARNING_PLAN.md`
- `RULES.md`
- `notes/INDEX.md`
- `templates/source-reading-note.md`
- `templates/session-log.md`
- `scripts/doctor.py`

## What I learned

原有规则已经能约束 agent 不泛读、不乱改上游源码，但“无人值守”和“必须 Mermaid”会把学习过程推向机械执行。更合适的表达是：agent 自学每次只推进一个小切片，重要结论必须回到源码证据；可视化只在它能提升理解时使用，并且必须配文字解释。

## Call chain / invariants

- README 说明项目初衷和 agent 自学入口。
- AGENTS 给 agent 执行边界：先读计划和地图，按切片学习，默认不改 Hermes 上游源码。
- LEARNING_PLAN 定义阶段顺序，A2A 是毕业设计，不是每个切片的实现目标。
- RULES 约束学习产物、设计取舍和 A2A 安全默认值。
- notes/INDEX 作为学习资产导航，必须指向真实存在的笔记。

关键不变量：

- 每次 agent 自学必须产出可复盘材料，而不是只给口头总结。
- 源码分析必须落到文件、函数、调用链、不变量和验证动作。
- 图不是任务本身；图服务理解，文字负责解释。
- A2A 相关远程入口默认安全保守。

## Verification

Command/test/script:

```bash
python3 scripts/doctor.py
rg -n "无人值守|Mermaid 图|必须.*Mermaid|先画图|01-tool-system-overview|01a-registry-internals|01b-approval" .
```

Result:

- `scripts/doctor.py` 通过：正式文档使用 agent 自学术语，`notes/INDEX.md` 中的笔记引用都能解析到真实文件。
- `rg` 未发现正式文档中仍使用“无人值守”或旧的 `01/01a/01b` 笔记索引；剩余 Mermaid 提及都是参考或说明，不再是强制图表章节。

## Questions

- 下一次真实 agent 自学切片跑完后，应根据实际输出手感再调整模板，而不是继续抽象优化规则。

## Next commit

```bash
git add .
git commit -m "docs: standardize agent self-study workflow"
```
