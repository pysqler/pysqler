format:
	uv run ruff format

lint: format
	if { git diff --name-only --cached; git ls-files -m; } | grep '.py'; then \
		uv run ruff check --fix; \
		uv run mypy .; \
	fi
	uv run codespell --write-changes --skip htmlcov .

pre-commit: lint

run:
	uv run python __main__.py

generate-requirements:
	uv export --no-hashes --format requirements-txt > requirements.txt
