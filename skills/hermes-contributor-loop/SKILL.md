---
name: hermes-contributor-loop
description: Workflow for turning Hermes source understanding into small upstream-quality commits or PR slices.
version: 1.0.0
author: Sherlock Shi
license: MIT
metadata:
  hermes:
    tags: [Hermes, Contribution, PR, Testing]
    requires_toolsets: [terminal]
---
# Hermes Contributor Loop

## When to Use

Use this skill when preparing a patch, test plan, issue analysis, or PR decomposition for Hermes.

## Procedure

1. Classify the change layer.
2. State the invariant that must not break.
3. Identify the smallest patch slice.
4. Find existing tests near the touched subsystem.
5. Add or draft tests before broad refactor.
6. Check cross-platform implications.
7. Write a focused commit message using Conventional Commits.
8. Prepare PR notes:
   - what changed;
   - why;
   - how tested;
   - platforms considered;
   - risks and rollback.

## Verification

Prefer:

```bash
scripts/run_tests.sh path/to/relevant_tests.py -q
```

Fallback:

```bash
pytest path/to/relevant_tests.py -q
```

## Pitfalls

- Do not mix unrelated refactor with feature work.
- Do not add dependencies without checking optional extras/lazy-deps policy.
- Do not duplicate provider/auth/session logic.
