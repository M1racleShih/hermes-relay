.PHONY: doctor new-log open-plan tree

doctor:
	python3 scripts/doctor.py

new-log:
	@test -n "$(TITLE)" || (echo "Usage: make new-log TITLE=your-title" && exit 1)
	python3 scripts/new-session.py "$(TITLE)"

open-plan:
	@echo "Read LEARNING_PLAN.md, then SOURCE_MAP.md, then ROADMAP_A2A.md"

tree:
	find . -maxdepth 3 -type f | sort
