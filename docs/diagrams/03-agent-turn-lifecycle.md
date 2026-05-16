# Agent Turn Lifecycle

```mermaid
flowchart TD
    Start[run_conversation] --> UserMsg[Append user message]
    UserMsg --> Prompt[Build/reuse system prompt]
    Prompt --> Compress{Preflight compression needed?}
    Compress -- yes --> Flush[Flush memory]
    Flush --> Summarize[Summarize middle turns]
    Summarize --> Ephemeral[Inject current-turn context]
    Compress -- no --> Ephemeral
    Ephemeral --> BuildAPI[Build and sanitize API messages]
    BuildAPI --> Call[Interruptible API call; streaming preferred when available]
    Call --> Parse[Parse / normalize provider response]
    Parse --> HasTools{tool_calls?}
    HasTools -- yes --> AppendAssistant[Append assistant tool-call message]
    AppendAssistant --> Execute[Execute tools sequential/concurrent]
    Execute --> AppendTool[Append tool results]
    AppendTool --> Ephemeral
    HasTools -- no --> Transform[Transform final response / callbacks]
    Transform --> Persist[Persist session + usage]
    Persist --> Background[Memory sync / background review]
    Background --> Return[Return final response]
```

切片阅读 `run_agent.py` 时围绕这张图找代码，不要全文线性阅读。
