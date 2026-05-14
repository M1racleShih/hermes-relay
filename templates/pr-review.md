# PR Review Checklist

PR:
Scope:

## Layer touched

- [ ] CLI
- [ ] Gateway
- [ ] ACP
- [ ] Tools
- [ ] Agent loop
- [ ] Provider runtime
- [ ] SessionDB
- [ ] Skills
- [ ] Security
- [ ] Install/packaging

## Invariants

- [ ] Message role alternation preserved
- [ ] Tool call/result pairs preserved
- [ ] Prompt cache stability not accidentally broken
- [ ] Session lineage unaffected or intentionally migrated
- [ ] Gateway running-agent guard unaffected
- [ ] Approval/security flow unaffected
- [ ] Cross-platform behavior considered

## Tests

```bash
scripts/run_tests.sh path/to/test.py -q
```

## Manual verification


## Risk notes


