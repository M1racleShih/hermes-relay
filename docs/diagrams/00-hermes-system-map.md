# Hermes System Map

```mermaid
flowchart TB
    subgraph Entrypoints
        CLI[CLI / TUI]
        Gateway[Messaging Gateway]
        APIServer[API Server Adapter]
        ACP[ACP Adapter]
        Cron[Cron Scheduler]
        Batch[Batch Runner]
    end

    subgraph Core
        Agent[AIAgent]
        Prompt[Prompt Builder / Context Files]
        Runtime[Provider Runtime]
        ToolDefs[model_tools.py Tool Definitions]
        Dispatch[model_tools.py + registry dispatch]
        State[SessionDB]
        Memory[Memory Manager]
    end

    subgraph Backends
        Providers[LLM Providers]
        Tools[Tools]
        Env[Terminal Environments]
        Plugins[Plugins]
        Skills[Skills]
    end

    CLI --> Agent
    Gateway --> Agent
    APIServer --> Gateway
    ACP --> Agent
    Cron --> Agent
    Batch --> Agent

    Agent --> Prompt
    Agent --> Runtime
    Agent --> ToolDefs
    Agent --> Dispatch
    Agent --> State
    Agent --> Memory

    Runtime --> Providers
    ToolDefs --> Tools
    Dispatch --> Tools
    Tools --> Env
    Prompt --> Skills
    Agent --> Plugins
```

这张图是顶层定位图。更细的工具、prompt、turn lifecycle、Gateway、ACP、A2A 映射分别看后续图。
