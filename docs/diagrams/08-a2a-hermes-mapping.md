# A2A to Hermes Mapping

这是目标设计图，不是当前 upstream Hermes-agent 已存在的真实模块图。目前源码里没有 `a2a_adapter/`；实现前需要先完成 AgentCard、task/session mapping、non-stream message send，再推进 streaming/cancel/auth/artifacts。

```mermaid
stateDiagram-v2
    [*] --> submitted: POST /message:send or stream
    submitted --> working: AIAgent starts
    working --> auth_required: approval needed / future
    auth_required --> working: credential or approval received
    working --> completed: final response
    working --> failed: exception / sanitized error
    working --> canceled: cancel task / interrupt
    submitted --> canceled: cancel before start
    completed --> [*]
    failed --> [*]
    canceled --> [*]
```

```mermaid
flowchart TB
    A2AMsg[A2A Message Parts] --> Normalize[Normalize supported parts]
    Normalize --> UserText[Hermes user_message]
    UserText --> Agent[AIAgent.run_conversation]
    Agent --> Final[final_response]
    Agent --> Progress[callbacks]
    Progress --> Status[TaskStatusUpdateEvent]
    Final --> Artifact[TaskArtifactUpdateEvent / Message]
```
