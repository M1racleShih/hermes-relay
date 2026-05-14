# Reference Sources

Use these as starting points. Verify current source before making upstream changes.

## Hermes

- GitHub: https://github.com/NousResearch/hermes-agent
- Docs: https://hermes-agent.nousresearch.com/docs
- Architecture: https://hermes-agent.nousresearch.com/docs/developer-guide/architecture
- Agent Loop Internals: https://hermes-agent.nousresearch.com/docs/developer-guide/agent-loop
- Prompt Assembly: https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly
- Provider Runtime: https://hermes-agent.nousresearch.com/docs/developer-guide/provider-runtime
- Tools Runtime: https://hermes-agent.nousresearch.com/docs/developer-guide/tools-runtime
- Gateway Internals: https://hermes-agent.nousresearch.com/docs/developer-guide/gateway-internals
- Session Storage: https://hermes-agent.nousresearch.com/docs/developer-guide/session-storage
- ACP Internals: https://hermes-agent.nousresearch.com/docs/developer-guide/acp-internals
- Contributing: https://github.com/NousResearch/hermes-agent/blob/main/CONTRIBUTING.md

## A2A

- A2A Spec: https://a2a-protocol.org/latest/specification/
- A2A GitHub: https://github.com/a2aproject/A2A
- Agent Card discovery: `/.well-known/agent-card.json`

## Local source setup

```bash
export HERMES_SRC="$HOME/code/hermes-agent"
```

Then use `rg`, `fd`, `pytest`, and `scripts/run_tests.sh` inside the Hermes source tree.
