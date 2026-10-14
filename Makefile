.PHONY: up down logs seed reset test test-fast demo migrate warm install

install:
	uv sync --frozen
	cd apps/web && pnpm install

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

migrate:
	alembic -c db/migrations/alembic.ini upgrade head

migrate-sql:
	alembic -c db/migrations/alembic.ini upgrade head --sql

fixtures:
	uv run python db/seed/generate_fixtures.py

seed:
	uv run python db/seed/seed_demo.py

reset:
	@echo "TODO D-06: branch-reset path + reseed + baseline checksum, target <60s (Fri)"

test:
	uv run pytest -q

test-fast:
	uv run pytest -q -m "not live_armoriq and not e2e"

demo:
	@echo "TODO: warm Neon + start tunnel (if Mode A) + open web"

warm:
	uv run python scripts/warm_neon.py
