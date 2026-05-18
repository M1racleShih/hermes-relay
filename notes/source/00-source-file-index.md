# 代码证据索引

本索引把"结论"与"证据"分离。笔记负责叙述和理解，本索引提供精确的源码文件路径映射，方便去源码中定位和阅读。

所有路径相对于 `~/opensource/hermes-agent/`。

最后校验：2026-05-18，使用 `wc -l` 与 `rg -n` 对关键入口、函数和 LOC 做只读抽查。

---

## 1. 入口与启动链路

### CLI 入口

| 文件 | LOC | 职责 |
|------|-----|------|
| `cli.py` | 13,809 | `HermesCLI` 类，CLI 交互循环、斜杠命令分发、Rich UI |
| `hermes_cli/commands.py` | — | `COMMAND_REGISTRY`，斜杠命令定义中心 |
| `hermes_cli/runtime_provider.py` | — | provider/model 解析与初始化 |
| `hermes_cli/env_loader.py` | — | `.env` 加载 |
| `hermes_cli/skin_engine.py` | — | CLI 主题引擎 |

### Gateway 入口

| 文件 | LOC | 职责 |
|------|-----|------|
| `gateway/run.py` | 16,858 | `GatewayRunner`，多平台事件路由、session 路由、agent 创建/复用 |
| `gateway/platforms/base.py` | — | Platform adapter interface |
| `gateway/platforms/webhook.py` | — | 简单 adapter 参考实现 |
| `gateway/platforms/api_server.py` | — | API Server adapter |
| `gateway/platforms/telegram.py` | — | Telegram adapter |
| `gateway/platforms/discord.py` | — | Discord adapter |
| `gateway/platforms/feishu.py` | — | Feishu adapter |

### ACP 入口

| 文件 | LOC | 职责 |
|------|-----|------|
| `acp_adapter/entry.py` | 148 | CLI 入口，加载 .env，stderr 日志，启动 ACP |
| `acp_adapter/server.py` | 1,714 | `HermesACPAgent(acp.Agent)`，协议方法实现 |

### Cron 入口

| 文件 | LOC | 职责 |
|------|-----|------|
| `cron/scheduler.py` | 1,820 | `CronScheduler`，定时触发 |
| `cron/jobs.py` | 1,114 | 任务执行、delivery 解析 |

### Batch 入口

| 文件 | LOC | 职责 |
|------|-----|------|
| `batch_runner.py` | 1,302 | 并行批处理 |

---

## 2. 执行内核 (AIAgent)

### 主循环

| 文件 | 行号范围 | 函数/类 | 说明 |
|------|---------|---------|------|
| `run_agent.py` | L1098 | `class AIAgent` | 核心类，~60 个初始化参数 |
| `run_agent.py` | L1121 | `AIAgent.__init__()` | 运行时依赖、provider、tools、callbacks、session |
| `run_agent.py` | L11828 | `run_conversation()` | 主 turn lifecycle，最核心的函数 |
| `run_agent.py` | L15705 | `chat()` | 薄封装，返回最终响应字符串 |
| `run_agent.py` | L10651 | `_invoke_tool()` | tool 调用路由：agent-level vs registry |
| `run_agent.py` | L10390 | `_compress_context()` | 上下文压缩 |
| `run_agent.py` | L4495 | `_persist_session()` | 写入 SessionDB |
| `run_agent.py` | L5269 | `interrupt()` | 中断请求 |
| `run_agent.py` | L287 | `IterationBudget` | 迭代预算管理 |

### Provider 适配

| 文件 | LOC | 职责 |
|------|-----|------|
| `agent/anthropic_adapter.py` | 2,079 | Anthropic native API |
| `agent/codex_responses_adapter.py` | 1,050 | Codex Responses API |
| `agent/gemini_native_adapter.py` | 971 | Gemini native API |
| `agent/gemini_cloudcode_adapter.py` | 909 | Gemini Cloud Code API |
| `agent/bedrock_adapter.py` | 1,276 | AWS Bedrock API |
| `agent/auxiliary_client.py` | 4,754 | 辅助模型调用（压缩摘要等） |
| `agent/credential_pool.py` | 1,603 | 多 API key 轮换 |
| `agent/error_classifier.py` | 1,058 | 错误分类与 fallback 决策 |
| `agent/model_metadata.py` | 1,819 | 模型元数据与能力查询 |

---

## 3. Tool 系统

### 注册与发现

| 文件 | 行号范围 | 函数/类 | 说明 |
|------|---------|---------|------|
| `tools/registry.py` | L77-106 | `ToolEntry` | `__slots__` 优化，11 个字段 |
| `tools/registry.py` | L151-514 | `ToolRegistry` | 模块级单例 |
| `tools/registry.py` | L57-74 | `discover_builtin_tools()` | AST 级自发现 |
| `tools/registry.py` | L234-288 | `register()` | 注册逻辑（含同名冲突检测） |
| `tools/registry.py` | L320-367 | `get_definitions()` | Schema 下发（含 check_fn 过滤） |
| `tools/registry.py` | L373-390 | `dispatch()` | 执行 handler |
| `tools/registry.py` | L126-141 | `_check_fn_cached()` | check_fn 30 秒 TTL 缓存 |

### 编排层

| 文件 | 行号范围 | 函数/类 | 说明 |
|------|---------|---------|------|
| `model_tools.py` | L271-332 | `get_tool_definitions()` | 完整缓存链：toolsets + generation + config_mtime |
| `model_tools.py` | L697-836 | `handle_function_call()` | dispatch 路径：coerce → hook → registry → hook → return |
| `toolsets.py` | — | `TOOLSETS`, `resolve_toolset()` | 平台 preset + composite toolset |

### 安全

| 文件 | 职责 |
|------|------|
| `tools/approval.py` | 危险命令审批链（hardline/dangerous/yolo/session） |
| `tools/terminal_tool.py` | 终端工具，check_fn 探测 |
| `tools/path_security.py` | 路径安全检查 |

### 重点工具

| 文件 | 职责 |
|------|------|
| `tools/file_tools.py` | 文件读写编辑 |
| `tools/web_tools.py` | Web 搜索与提取 |
| `tools/browser_tool.py` | 浏览器工具 |
| `tools/delegate_tool.py` | 子 agent 派遣 |
| `tools/memory_tool.py` | 持久化记忆 |
| `tools/mcp_tool.py` | MCP tool 发现与注册 |
| `tools/code_execution_tool.py` | 代码执行 |
| `tools/cronjob_tools.py` | Cron job 管理 |

---

## 4. Prompt 与 Context

| 文件 | LOC | 关键函数 | 说明 |
|------|-----|---------|------|
| `agent/prompt_builder.py` | 1,456 | `build_skills_system_prompt()`, `load_soul_md()`, `build_context_files_prompt()` | SOUL.md、context files、skills index 组装 |
| `agent/skill_commands.py` | 501 | skill 命令解析与运行时 skill 内容注入 | `/skill` 加载完整内容后作为 user message 注入 |
| `agent/context_compressor.py` | 1,583 | — | 长对话压缩 |

---

## 5. 持久化

| 文件 | LOC | 职责 |
|------|-----|------|
| `hermes_state.py` | 2,966 | SessionDB — SQLite + FTS5 |
| `trajectory_compressor.py` | — | 对话轨迹压缩 |
| `tools/checkpoint_manager.py` | — | Checkpoint 管理 |
| `tools/tool_result_storage.py` | — | Tool 结果存储 |

---

## 6. Gateway 详细

| 文件 | 职责 |
|------|------|
| `gateway/session.py` | `SessionStore`, `SessionEntry`, `SessionContext`, `SessionSource` |
| `gateway/delivery.py` | `DeliveryRouter`, `DeliveryTarget` |
| `gateway/pairing.py` | 配对管理 |
| `gateway/hooks.py` | Hook 系统 |
| `gateway/status.py` | Gateway 状态 |

---

## 7. ACP Adapter 详细

| 文件 | LOC | 关键函数/类 | 说明 |
|------|-----|------------|------|
| `acp_adapter/server.py` | 1,714 | `HermesACPAgent` | ACP 协议方法实现 |
| `acp_adapter/server.py` | L737 | `initialize()` | session 初始化 |
| `acp_adapter/server.py` | L862 | `_replay_session_history()` | history replay |
| `acp_adapter/session.py` | 628 | `SessionManager`, `SessionState` | live session 管理 |
| `acp_adapter/tools.py` | 1,180 | — | MCP resource 映射、tool 池桥接 |
| `acp_adapter/events.py` | 194 | — | AIAgent callback → ACP event 桥接 |
| `acp_adapter/permissions.py` | 141 | — | 危险命令审批映射 |
| `acp_adapter/auth.py` | 24 | — | 认证桩 |

---

## 8. Cron 详细

| 文件 | 行号范围 | 函数 | 说明 |
|------|---------|------|------|
| `cron/jobs.py` | L395 | `_resolve_delivery_targets()` | delivery target 解析 |
| `cron/jobs.py` | L482 | `_deliver_result()` | 结果投递 |
| `cron/jobs.py` | L697 | `_run_job_script()` | 脚本执行 |

---

## 9. 插件系统

| 目录 | 职责 |
|------|------|
| `plugins/memory/` | Memory provider 插件（honcho, mem0, supermemory） |
| `plugins/model-providers/` | 推理后端插件（openrouter, anthropic, gmi） |
| `plugins/context_engine/` | Context engine 插件 |
| `plugins/kanban/` | Multi-agent board + worker |
| `plugins/image_gen/` | 图片生成 |
| `plugins/observability/` | Metrics/traces/logs |

---

## 10. 测试

| 目录 | 说明 |
|------|------|
| `tests/` | ~17k tests across ~900 files |
| `tests/test_*tool*.py` | Tool 相关测试 |
| `tests/acp/` | ACP adapter 测试 |

---

## 11. 验证记录

本索引用下面的只读命令校验关键源码锚点：

```bash
wc -l /home/shq/opensource/hermes-agent/cli.py \
  /home/shq/opensource/hermes-agent/gateway/run.py \
  /home/shq/opensource/hermes-agent/acp_adapter/server.py \
  /home/shq/opensource/hermes-agent/run_agent.py \
  /home/shq/opensource/hermes-agent/agent/prompt_builder.py \
  /home/shq/opensource/hermes-agent/agent/skill_commands.py

rg -n "class AIAgent|def run_conversation|def chat\\(|def _invoke_tool|def _compress_context|def _persist_session|def interrupt\\(" \
  /home/shq/opensource/hermes-agent/run_agent.py

rg -n "def build_skills_system_prompt|def load_soul_md|def build_context_files_prompt|def _build_skill_message" \
  /home/shq/opensource/hermes-agent/agent/prompt_builder.py \
  /home/shq/opensource/hermes-agent/agent/skill_commands.py
```

校验结论：AIAgent 主循环锚点、prompt/skill 关键函数和核心入口 LOC 均已重新对齐；本索引仍是快速定位表，不替代专题笔记中的调用链解释。
