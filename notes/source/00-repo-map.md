# Hermes 系统架构总览

## 核心结论

> Hermes 不是"一个聊天机器人的 CLI 包装"，而是一个**多入口、多形态、本地优先的 Agent 平台**。
> 它有统一的执行内核（`AIAgent`）、文件化分层 memory、插件式工具注册、20+ 平台适配的 Gateway、以及 ACP 协议适配层。
> 理解 Hermes 的关键是理解"所有入口最终汇合到同一个 `run_conversation()` 循环"。

---

## 一、分层架构图

```text
┌──────────────────────────────────────────────────────────────┐
│                     入口层 (Entry Points)                     │
│  CLI(cli.py)  Gateway(gateway/run.py)  ACP(acp_adapter/)    │
│  Cron(cron/scheduler.py)  Batch(batch_runner.py)  MCP        │
└──────────────┬───────────────────┬──────────────┬────────────┘
               │                   │              │
               ▼                   ▼              ▼
┌──────────────────────────────────────────────────────────────┐
│                    编排层 (Orchestration)                      │
│  HermesCLI — CLI 交互循环 / 命令分发 / Rich UI                │
│  GatewayRunner — 多平台事件路由 / session 管理 / delivery      │
│  HermesACPAgent — ACP 协议方法 → AIAgent 调用                │
│  CronScheduler — 定时触发 → delivery → AIAgent               │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                    执行内核 (Execution Core)                   │
│  AIAgent (run_agent.py, 16k LOC)                             │
│  ┌──────────┬──────────┬───────────┬────────────────┐       │
│  │ run_conv │ _invoke  │ _compress │ _persist       │       │
│  │ ersation │ _tool    │ _context  │ _session       │       │
│  └──────────┴──────────┴───────────┴────────────────┘       │
│  IterationBudget · interrupt · fallback · streaming          │
└──────────┬──────────────┬──────────────┬────────────────────┘
           │              │              │
           ▼              ▼              ▼
┌────────────────┐ ┌─────────────┐ ┌──────────────────────────┐
│ Prompt 层      │ │ Tool 层     │ │ 持久化层                 │
│ prompt_builder │ │ model_tools │ │ hermes_state (SessionDB)  │
│ skill_commands │ │ registry    │ │ context_compressor        │
│ context files  │ │ toolsets    │ │ trajectory_compressor     │
│ SOUL.md        │ │ approval    │ │ memory_tool               │
│ .hermes.md     │ │ 73 tools    │ │ checkpoint_manager        │
└────────────────┘ └──────┬──────┘ └──────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                  后端扩展层 (Backends)                         │
│  LLM Providers · Terminal Envs · Plugins · Skills · MCP     │
│  (providers/, tools/environments/, plugins/, skills/)        │
└──────────────────────────────────────────────────────────────┘
```

---

## 二、程序入口（五种运行形态）

Hermes 有五种独立的运行形态，全部最终汇合到 `AIAgent.run_conversation()`：

### 1. CLI 交互形态

```
用户终端 → cli.py (HermesCLI) → AIAgent.run_conversation()
```

- **入口文件**：`cli.py`（13.8k LOC）
- **职责**：Rich banner、prompt_toolkit 输入、斜杠命令、skin 主题、spinner 动画
- **关键类**：`HermesCLI`，`process_command()` 分发斜杠命令
- **特点**：同步阻塞式交互，直接调用 `AIAgent`

### 2. Gateway 多平台形态

```
Telegram/Discord/Feishu/... → gateway/platforms/*.py → MessageEvent
  → gateway/run.py (GatewayRunner) → AIAgent.run_conversation()
  → gateway/delivery.py → 平台 adapter 发回响应
```

- **入口文件**：`gateway/run.py`（~1800 LOC）
- **关键类**：`GatewayRunner`，管理完整生命周期
- **平台适配器**：20+ 个，位于 `gateway/platforms/`
  - `telegram.py`, `discord.py`, `feishu.py`, `slack.py`, `whatsapp.py`
  - `matrix.py`, `signal.py`, `email.py`, `sms.py`, `api_server.py`
  - `webhook.py`, `homeassistant.py`, `wecom.py`, `weixin.py`, ...
- **Session 管理**：`gateway/session.py`（`SessionStore`、`SessionEntry`、`SessionContext`）
- **Delivery**：`gateway/delivery.py`（`DeliveryRouter`、`DeliveryTarget`）
- **特点**：异步多路复用、session key 路由、active-agent guard、hook 系统

### 3. ACP 协议形态（VS Code / JetBrains 集成）

```
IDE (ACP client) → JSON-RPC stdio → acp_adapter/server.py (HermesACPAgent)
  → worker thread 中跑 AIAgent.run_conversation()
  → asyncio.run_coroutine_threadsafe 把 callback 转为 async event
```

- **入口文件**：`acp_adapter/entry.py`（加载 .env、配置 stderr 日志、启动 ACP server）
- **核心类**：`HermesACPAgent(acp.Agent)`（`acp_adapter/server.py`, 1714 LOC）
- **Session 管理**：`acp_adapter/session.py`（`SessionManager`、`SessionState`）
- **Tool 桥接**：`acp_adapter/tools.py`（1180 LOC，MCP resource 转换、tool 池映射）
- **权限桥接**：`acp_adapter/permissions.py`（危险命令审批映射）
- **关键设计**：stdout 只给 JSON-RPC transport，日志走 stderr；AIAgent 在 worker thread 中同步运行，通过 asyncio bridge 转为异步事件

### 4. Cron 定时形态

```
CronScheduler → cron/jobs.py → _run_job_script() or _run_agent_prompt()
  → AIAgent.run_conversation() → _deliver_result() → platform delivery
```

- **入口文件**：`cron/scheduler.py`（1820 LOC）
- **任务执行**：`cron/jobs.py`（1114 LOC）
- **Delivery**：复用 Gateway 的 adapter 发送到目标平台
- **特点**：无人值守运行、prompt injection 防护、delivery target 解析

### 5. Batch 批量形态

```
batch_runner.py → 并行启动多个 AIAgent 实例 → 批量处理任务
```

- **入口文件**：`batch_runner.py`（1302 LOC）
- **特点**：并行执行、每个任务独立 session

---

## 三、一条请求的完整旅程（CLI 路径）

```text
1. 用户输入 "帮我分析一下这个 bug"
       │
2. HermesCLI.process_command() — 判断不是斜杠命令，是普通消息
       │
3. AIAgent.chat("帮我分析一下这个 bug")
       │ 薄封装
4. AIAgent.run_conversation(user_message, system_message, conversation_history)
       │
5. Prompt 组装：
   ├─ prompt_builder.build_system_prompt() 加载 SOUL.md + MEMORY.md + USER.md + .hermes.md
   ├─ skill_commands.build_skills_system_prompt() 加载 skill index
   ├─ model_tools.get_tool_definitions() 解析 enabled/disabled toolsets → registry → tool schemas
   └─ conversation_history (已有对话)
       │
6. API 调用：
   ├─ client.chat.completions.create(model, messages, tools=tool_schemas)
   ├─ 支持 streaming / non-streaming
   └─ 支持 Anthropic native / OpenAI-compatible / Codex Responses / Gemini 多种 API mode
       │
7. 响应分支：
   ├─ 普通文本 → 返回给用户
   └─ tool_calls → 进入 tool 执行循环
       │
8. Tool 执行循环（可能多轮）：
   ├─ AIAgent._invoke_tool(name, args)
   │   ├─ agent-level tools (todo/memory/session_search/delegate_task) → 直接在 agent 内部处理
   │   └─ 普通 tools → model_tools.handle_function_call(name, args)
   │       ├─ coerce_tool_args() — 类型强转
   │       ├─ pre_tool_call hook — 插件可拦截
   │       ├─ registry.dispatch(name, args) — 执行 handler
   │       ├─ post_tool_call hook
   │       └─ transform_tool_result hook
   ├─ tool result 追加到 messages
   ├─ 回到步骤 6 继续调用 API
   └─ 直到无 tool_calls 或超出 iteration budget
       │
9. 后处理：
   ├─ _persist_session() — 写入 SessionDB (SQLite + FTS5)
   ├─ _compress_context() — 上下文过长时触发压缩
   ├─ _save_trajectory() — 保存对话轨迹（可选）
   └─ memory 写入（可选）
       │
10. 最终响应返回给 HermesCLI → Rich 渲染 → 用户看到回复
```

---

## 四、核心模块速查表

### 4.1 执行内核

| 模块 | 关键文件 | LOC | 职责 | 上下游 |
|------|---------|-----|------|---------|
| **AIAgent** | `run_agent.py` | 16,083 | 核心对话循环、tool 调度、压缩、持久化、fallback | 被 CLI/Gateway/ACP/Cron/Batch 调用 |
| **Tool 编排** | `model_tools.py` | 865 | tool discovery、schema 下发、dispatch 编排、hook 链 | 被 AIAgent 调用；调用 registry |
| **Tool 注册** | `tools/registry.py` | ~500 | ToolEntry 数据结构、注册/查询/dispatch、自发现、缓存 | 被 model_tools 调用；被 73 个 tool 文件注册 |
| **Toolset** | `toolsets.py` | 866 | 平台 preset、composite toolset、resolve 展开 | 被 model_tools 调用 |
| **Tool 实现** | `tools/*.py` | 73 个文件 | 每个工具一个文件，top-level `registry.register()` | 被 registry 发现 |

### 4.2 Prompt 与 Context

| 模块 | 关键文件 | LOC | 职责 |
|------|---------|-----|------|
| **Prompt Builder** | `agent/prompt_builder.py` | 1,456 | 组装 system prompt：SOUL.md + MEMORY.md + context files + skills |
| **Skill Commands** | `agent/skill_commands.py` | — | skill index 注入 system prompt |
| **Context Compressor** | `agent/context_compressor.py` | 1,583 | 长对话压缩策略 |

### 4.3 持久化与 Memory

| 模块 | 关键文件 | LOC | 职责 |
|------|---------|-----|------|
| **SessionDB** | `hermes_state.py` | 2,966 | SQLite 存储：sessions、messages、FTS5 全文搜索 |
| **Trajectory Compressor** | `trajectory_compressor.py` | — | 对话轨迹压缩 |
| **Memory Tool** | `tools/memory_tool.py` | — | 用户可控的持久化记忆读写 |

### 4.4 Gateway 层

| 模块 | 关键文件 | 职责 |
|------|---------|------|
| **Gateway Runner** | `gateway/run.py` | 多平台事件路由、session 路由、agent 创建/复用、hook 执行 |
| **Session Store** | `gateway/session.py` | Gateway 级 session 管理（不同于 SessionDB） |
| **Delivery** | `gateway/delivery.py` | 响应发回目标平台的路由 |
| **Platform Adapters** | `gateway/platforms/*.py` | 每个聊天平台的适配器（20+） |

### 4.5 ACP 适配层

| 模块 | 关键文件 | LOC | 职责 |
|------|---------|-----|------|
| **ACP Entry** | `acp_adapter/entry.py` | 148 | CLI 入口，加载 .env，启动 ACP server |
| **ACP Server** | `acp_adapter/server.py` | 1,714 | ACP 协议方法实现、history replay、streaming event |
| **ACP Session** | `acp_adapter/session.py` | 628 | live session、cwd、cancel_event 管理 |
| **ACP Tools** | `acp_adapter/tools.py` | 1,180 | MCP resource 映射、tool 池桥接 |
| **ACP Permissions** | `acp_adapter/permissions.py` | 141 | 危险命令审批桥接 |

### 4.6 Agent 内部模块

| 模块 | 关键文件 | LOC | 职责 |
|------|---------|-----|------|
| **Auxiliary Client** | `agent/auxiliary_client.py` | 4,754 | 辅助模型调用（压缩摘要、review 等） |
| **Anthropic Adapter** | `agent/anthropic_adapter.py` | 2,079 | Anthropic native API 适配 |
| **Codex Responses** | `agent/codex_responses_adapter.py` | 1,050 | Codex Responses API 适配 |
| **Gemini Adapter** | `agent/gemini_native_adapter.py` | 971 | Gemini native API 适配 |
| **Credential Pool** | `agent/credential_pool.py` | 1,603 | 多 API key 轮换 |
| **Error Classifier** | `agent/error_classifier.py` | 1,058 | API 错误分类与 fallback 决策 |
| **Display** | `agent/display.py` | 1,011 | KawaiiSpinner、Rich 输出格式化 |

### 4.7 扩展系统

| 模块 | 位置 | 职责 |
|------|------|------|
| **Skills** | `skills/`, `optional-skills/` | 内置 + 可选 skill，YAML frontmatter + Markdown body |
| **Plugins** | `plugins/` | memory、context_engine、model-providers、kanban、image_gen 等 |
| **MCP** | `tools/mcp_tool.py`, `mcp_serve.py` | MCP tool 发现与注册 |
| **Terminal Envs** | `tools/environments/` | Docker、SSH、Modal、Daytona 等执行环境 |

---

## 五、源码规模概览

| 类别 | 文件数 | LOC | 说明 |
|------|--------|-----|------|
| 执行内核 (`run_agent.py`) | 1 | 16,083 | 单体核心，对话循环 |
| CLI (`cli.py`) | 1 | 13,809 | CLI 交互编排 |
| Agent 内部 (`agent/`) | ~25 | 37,450 | provider adapter、prompt、memory、display |
| 工具 (`tools/`) | 73+ | ~15,000 | 每个工具一个文件 |
| Gateway (`gateway/`) | 53 | ~10,000 | 20+ 平台适配器 + session + delivery |
| ACP 适配器 (`acp_adapter/`) | 9 | 4,035 | 协议适配层 |
| Cron | 3 | 2,976 | 定时调度 |
| 状态 (`hermes_state.py`) | 1 | 2,966 | SessionDB |
| **总计（Python）** | — | **815,448** | 含 tests、plugins、网站等 |

---

## 六、核心不变量

1. **所有入口最终汇合到 `AIAgent.run_conversation()`** — CLI、Gateway、ACP、Cron、Batch 共享同一个执行内核，不存在两套实现的行为差异风险
2. **Tool 注册在模块 top-level** — 73 个 tool 文件在 import 时自动注册，AST 级自发现
3. **Agent-level tools 不走 registry dispatch** — `todo`、`memory`、`session_search`、`delegate_task` 在 `AIAgent._invoke_tool()` 中直接处理
4. **`model_tools.py` 是 AIAgent 和 Tool 系统之间的唯一中介** — schema 下发、dispatch 编排、hook 链都在这里
5. **AIAgent 不直接访问 registry** — 全部通过 `model_tools.py` 中转
6. **check_fn fail-safe** — 探测异常 = tool unavailable，不炸 agent loop
7. **Tool handler 返回值必须是 JSON 字符串** — 异常在 registry.dispatch() 内包装

---

## 七、A2A 在架构中的位置

```text
                    ┌─────────────────┐
                    │  A2A Adapter    │  ← 需要新建
                    │  (a2a_adapter/) │
                    └────────┬────────┘
                             │
          与 ACP adapter 同级 │ 复用 AIAgent 核心循环
                             │
    ┌────────┬───────────────┼───────────────┬──────────┐
    │ CLI    │ Gateway       │ ACP           │ Cron     │ Batch  │
    └────────┴───────────────┴───────────────┴──────────┴────────┘
                             │
                    ┌────────▼────────┐
                    │   AIAgent       │
                    │ run_conversation│
                    └─────────────────┘
```

**关键决策**：A2A adapter 不应从修改 `AIAgent` 主循环开始，而是像 ACP 一样作为独立适配层包住同步 AIAgent，暴露 HTTP+JSON 协议服务。

---

## 八、推荐的全局源码阅读路径

```
Phase 0: 00-repo-map.md（本文档）
  ↓ 建立全貌
Phase 1: Tool System
  阅读顺序：tools/registry.py → model_tools.py → toolsets.py → tools/approval.py → tools/terminal_tool.py
  理由：最容易形成"源码→行为→测试"闭环
  ↓
Phase 2: Prompt Assembly
  阅读顺序：agent/prompt_builder.py → agent/skill_commands.py → tools/memory_tool.py → skills/*/SKILL.md
  ↓
Phase 3: AIAgent Turn Lifecycle
  阅读顺序：run_agent.py:__init__ → chat() → run_conversation() → _invoke_tool() → _compress_context() → _persist_session()
  注意：16k LOC 不要线性读，按调用链切片
  ↓
Phase 4: SessionDB / Memory / Compression
  阅读顺序：hermes_state.py → agent/context_compressor.py → tools/memory_tool.py
  ↓
Phase 5: Gateway
  阅读顺序：gateway/platforms/base.py → gateway/platforms/webhook.py → gateway/run.py → gateway/delivery.py → gateway/session.py
  ↓
Phase 6: ACP Adapter（A2A 直接参考）
  阅读顺序：acp_adapter/entry.py → acp_adapter/server.py → acp_adapter/session.py → acp_adapter/tools.py → acp_adapter/permissions.py
```

---

## 九、下一步

- Phase 1 的 Module Orientation 和 Reading Guide 见 `01-tool-runtime.md`
- 代码证据索引见 `00-code-evidence-index.md`
