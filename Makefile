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
	@echo "TODO D-02: alembic upgrade head + security SQL (Person B schema, Person A security)"

seed:
	@echo "TODO S-02: uv run python -m db.seed.seed_demo (Person B)"

reset:
	@echo "TODO D-06: truncate + reseed + baseline checksum, target <60s"

test:
	uv run pytest -q

test-fast:
	uv run pytest -q -m "not live_armoriq and not e2e"

demo:
	@echo "TODO: warm Neon + start tunnel (if Mode A) + open web"

warm:
	uv run python scripts/warm_neon.py
