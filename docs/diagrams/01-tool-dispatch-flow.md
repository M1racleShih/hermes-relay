# Tool Dispatch Flow

```mermaid
sequenceDiagram
    participant Import as model_tools import
    participant Registry as tools/registry.py
    participant Tool as tools/*.py
    participant Agent as AIAgent
    participant Model as LLM

    Import->>Registry: discover_builtin_tools()
    Registry->>Tool: import module with top-level registry.register()
    Tool->>Registry: registry.register(name, schema, handler, check_fn)
    Agent->>Registry: get_definitions(enabled tools/toolsets)
    Registry-->>Agent: available tool schemas
    Agent->>Model: API call with tool schemas
    Model-->>Agent: tool_calls
    Agent->>Registry: dispatch(name, args)
    Registry->>Tool: handler(args)
    Tool-->>Registry: result string / JSON
    Registry-->>Agent: tool result
    Agent->>Model: continue with tool result
```

关键不变量：

- 新 tool 的 `registry.register()` 必须在模块 top-level；
- 只注册不够，还要加入 `toolsets.py`；
- `check_fn` 出错视为 unavailable；
- tool handler 应返回字符串，通常是 JSON 字符串；
- 异常必须包装成模型可读的 JSON error，而不是炸出 agent loop。
