# Journal 2026-05-17: Phase 1 切片 1-1

## 本次切片

- **阶段来源**：Phase 1 / 切片 1-1
- **回答的问题**：ToolEntry 数据结构和 registry 的注册/查询/dispatch 内部机制

## 阅读源码

- `tools/registry.py` (563 行，全部精读)
- `toolsets.py` (866 行，全部精读)
- `model_tools.py` (865 行，精读 L271-836)
- `run_agent.py` (抽样 L10651-10719，确认 agent-level tool 截获)

## 关键发现

1. **AST 自发现**：`discover_builtin_tools()` 不 import 再检测，而是先 AST 扫描 module-body 级的 `registry.register()` 调用，通过后才 import。避免 import 副作用。

2. **双层缓存**：`get_tool_definitions()` 有自身缓存（key = toolsets + generation + config mtime），`get_definitions()` 内部有 check_fn 的 TTL 缓存（30s）。两层独立工作。

3. **动态 schema 修正**：`_compute_tool_definitions()` 在 registry 返回 schemas 后，还会做 execute_code sandbox 工具列表、discord intents、browser_navigate 引用修正。这是 model_tools 层的额外逻辑，不在 registry 中。

4. **Agent-level tools 截获**：`run_agent._invoke_tool()` 直接处理 todo/memory/session_search，需要 `_todo_store`, `_memory_store`, `session_db` 等 agent 级状态。`model_tools.handle_function_call()` 对这些 tool 返回 stub error 作为安全网。

5. **Registration shadowing 保护**：同名 tool 不同 toolset 的注册会被 REJECTED（除非都是 MCP）。这意味着 A2A adapter 不能覆盖内置工具。

## 产出文件

- `notes/source/01a-registry-dispatch-deep.md`

## 下一次继续

`tools/approval.py` + `tools/terminal_tool.py` 的安全审批链，回答：危险命令如何被拦截和审批？
