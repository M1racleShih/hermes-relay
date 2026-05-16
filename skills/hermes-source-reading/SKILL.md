---
name: hermes-source-reading
description: Structured workflow for reading Hermes Agent source code and producing notes, diagrams, and verification steps.
version: 1.0.0
author: Sherlock Shi
license: MIT
metadata:
  hermes:
    tags: [Hermes, Source, Learning, Architecture]
    requires_toolsets: [terminal]
---
# Hermes Source Reading

## When to Use

Use this skill whenever the task is to understand a Hermes source file, subsystem, or contribution path.

## Procedure

1. Identify the layer: entrypoint, agent core, tools, gateway, ACP, provider, state, skills, plugin, packaging.
2. Locate the smallest relevant file set. Do not read the entire repository.
3. Extract:
   - entry points;
   - key classes/functions;
   - data structures;
   - call chain;
   - invariants;
   - tests;
   - likely regression risks.
4. Create or update a note in `notes/source/`.
5. If the topic is a flow or state machine, embed the Mermaid diagram in the same `notes/source/` note. If the diagram captures a design choice rather than source truth, put it in the relevant `notes/design/` note.
6. Add a journal entry in `journal/`.
7. Propose one verification command or test.

## Output Format

```text
目标：
相关源码：
调用链：
关键不变量：
风险：
验证方式：
下一步 commit：
```

## Pitfalls

- Do not linearly summarize huge files.
- Do not confuse user-facing behavior with implementation extension points.
- Do not recommend modifying `run_agent.py` until the adapter/tool/prompt/plugin alternatives are ruled out.
