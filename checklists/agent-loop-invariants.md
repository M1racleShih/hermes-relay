# Agent Loop Invariants

Use this when reading or changing `run_agent.py` or adapter code that calls `AIAgent`.

- [ ] System prompt remains stable unless explicitly rebuilt.
- [ ] Internal messages remain OpenAI-style dicts.
- [ ] Role alternation is preserved: user -> assistant -> user, except tool result blocks.
- [ ] Assistant tool calls are followed by matching tool result messages.
- [ ] Parallel tool results are reinserted in original tool call order.
- [ ] Interactive tools force sequential behavior where needed.
- [ ] Raw model reasoning is not exposed unintentionally.
- [ ] Interrupt does not inject partial response into history.
- [ ] Fallback changes provider/client/model consistently.
- [ ] Compression flushes memory first.
- [ ] Compression protects recent messages and tool pairs.
- [ ] Session persistence happens once per completed turn.
- [ ] Errors are sanitized and model/user appropriate.
