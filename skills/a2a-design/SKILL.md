---
name: a2a-design
description: Design workflow for adding Agent2Agent protocol support to Hermes Agent.
version: 1.0.0
author: Sherlock Shi
license: MIT
metadata:
  hermes:
    tags: [A2A, Protocol, Adapter, Hermes]
    requires_toolsets: [terminal]
---
# A2A Design Skill

## When to Use

Use this skill when discussing or implementing Agent2Agent support for Hermes.

## Procedure

1. Decide whether the work is A2A Server, A2A Client, or shared protocol models.
2. Start from AgentCard and task/session mapping before streaming.
3. Reuse ACP adapter patterns for:
   - session manager;
   - event bridge;
   - permission bridge;
   - cancellation.
4. Reuse Gateway patterns for:
   - authorization;
   - session routing;
   - platform-safe delivery concepts.
5. Do not expose raw reasoning, memory, prompts, credentials, local paths, or full internal tool implementation details.
6. Draft the minimal protocol surface.
7. Write test cases for task lifecycle before implementing transport.

## MVP Order

1. AgentCard generator.
2. Task/context/session manager.
3. `message:send` non-streaming.
4. `message:stream` SSE.
5. `tasks/{id}:cancel`.
6. Auth and permission hardening.
7. Docs and examples.

## Output Format

```text
A2A operation:
Hermes modules touched:
Data mapping:
State transitions:
Security constraints:
Tests:
Open questions:
```
