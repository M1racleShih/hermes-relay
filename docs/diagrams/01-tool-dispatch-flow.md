# Tool Dispatch Flow

```mermaid
sequenceDiagram
    participant ModelTools as model_tools.py
    participant Registry as tools/registry.py
    participant Tool as tools/*.py
    participant Toolsets as toolsets.py
    participant Agent as AIAgent
    participant Model as LLM

    ModelTools->>Registry: discover_builtin_tools()
    Registry->>Tool: import module with top-level registry.register()
    Tool->>Registry: registry.register(name, toolset, schema, handler, check_fn)
    Agent->>ModelTools: get_tool_definitions(enabled/disabled toolsets)
    ModelTools->>Toolsets: resolve / validate toolsets
    ModelTools->>Registry: get_definitions(resolved tool names)
    Registry-->>ModelTools: available tool schemas
    ModelTools-->>Agent: filtered tool schemas
    Agent->>Model: API call with tool schemas
    Model-->>Agent: tool_calls
    Agent->>Agent: route agent-level tools when applicable
    Agent->>ModelTools: handle_function_call(name, args, context)
    ModelTools->>Registry: dispatch(name, args)
    Registry->>Tool: handler(args, **kwargs)
    Tool-->>Registry: result string / JSON
    Registry-->>ModelTools: tool result
    ModelTools-->>Agent: normalized tool result
    Agent->>Model: continue with tool result
```

关键不变量：

- 新 tool 的 `registry.register()` 必须在模块 top-level；
- 只注册不够，还要能被 toolset 解析/暴露；内置 tool 通常归属一个 `Toolset`，插件也可以注册 toolset；
- `AIAgent` 不直接向 registry 要 tool schema，也不直接对普通 registry tool 做 dispatch；中间层是 `model_tools.py`；
- `todo`、`memory`、`session_search`、`delegate_task` 等 agent-level tool 会在 `run_agent.py` 内部先被截获处理；
- `check_fn` 出错视为 unavailable；
- tool handler 应返回字符串，通常是 JSON 字符串；
- 异常必须包装成模型可读的 JSON error，而不是炸出 agent loop。
