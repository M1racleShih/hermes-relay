# A2A PR Readiness Checklist

## Scope

- [ ] This PR is one logical slice.
- [ ] It does not mix refactor, feature, docs, and tests beyond the slice.
- [ ] It declares what A2A operations are supported.
- [ ] It declares what A2A operations are not supported.

## Security

- [ ] A2A server is opt-in.
- [ ] Remote access requires localhost-only mode or auth by default.
- [ ] AgentCard does not leak secrets, memory, prompt, local paths, raw tool internals.
- [ ] Raw reasoning is not streamed.
- [ ] Task access is scoped to client/context.
- [ ] Dangerous commands still require Hermes approval.

## Runtime reuse

- [ ] Reuses provider runtime resolver.
- [ ] Reuses AIAgent instead of duplicating agent loop.
- [ ] Reuses SessionDB or has a clear task persistence design.
- [ ] Reuses callback/permission patterns from ACP where appropriate.

## Tests

- [ ] AgentCard generation tests.
- [ ] Task state transition tests.
- [ ] message:send tests.
- [ ] streaming tests if included.
- [ ] cancellation tests if included.
- [ ] auth rejection tests.
- [ ] no live network required in unit tests.
- [ ] cross-platform-sensitive code reviewed.

## Docs

- [ ] CLI command documented.
- [ ] Example curl provided.
- [ ] Security warning included.
- [ ] A2A version/scope documented.
