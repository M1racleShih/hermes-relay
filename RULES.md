# Learning Rules

## 1. 每次学习必须留下 Git 痕迹

禁止“看了一下午源码但没有 commit”。每次至少提交一种产物：笔记、图、脚本、测试、设计草案。

推荐 commit 粒度：

```text
docs(tools): map registry discovery flow
docs(agent): record message alternation invariants
test(a2a): draft task state transition cases
chore(journal): add session log for acp adapter reading
```

## 2. 先画图，再深挖

流程性或状态性内容必须先画 Mermaid：

- tool dispatch flow；
- prompt layer assembly；
- agent turn lifecycle；
- session lineage；
- gateway message flow；
- ACP/A2A event bridge；
- A2A task state machine。

## 3. 源码阅读不要逐行主义

按切片阅读：

```text
入口 -> 数据结构 -> 关键函数 -> 状态变化 -> 错误处理 -> 测试 -> 风险
```

只有以下情况才逐行精读：

- 你准备改这段代码；
- 这里维护关键不变量；
- 这里涉及安全、并发、持久化、跨平台；
- 测试失败指向这里。

## 4. 所有设计必须写 trade-off

每个 ADR 至少包含：

- Context；
- Decision；
- Alternatives；
- Consequences；
- Test plan；
- Open questions。

## 5. 不要复制 runtime logic

新增 adapter 或协议层时，优先复用：

- provider runtime resolver；
- tool registry；
- session storage；
- approval callback；
- prompt builder；
- AIAgent main loop。

复制逻辑通常意味着后续维护成本翻倍。

## 6. A2A 安全默认保守

A2A 是远程协议入口，默认策略：

- 默认关闭；
- 默认 localhost 或 token protected；
- 不泄露 memory、prompt、tool internals、credentials；
- 不暴露 raw reasoning；
- destructive action 仍走 Hermes approval；
- task/context 必须按 client identity 隔离。

## 7. 每阶段结束前必须做回顾

模板：

```text
我现在能解释什么？
我还不能解释什么？
我能改哪里？
我不敢改哪里？为什么？
如果现在做 A2A，会卡在哪里？
下一阶段要降低哪个风险？
```
