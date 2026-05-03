.PHONY: dev prod down down-v logs ps shell-api shell-db migrate seed

# ── Development ───────────────────────────────────────────────
dev:
	docker compose up --build

dev-bg:
	docker compose up --build -d

# ── Production ────────────────────────────────────────────────
prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d

# ── Control ───────────────────────────────────────────────────
down:
	docker compose down

down-v:
	docker compose down -v

logs:
	docker compose logs -f

logs-api:
	docker compose logs -f api

ps:
	docker compose ps

# ── Shells ────────────────────────────────────────────────────
shell-api:
	docker compose exec api bash

shell-db:
	docker compose exec postgres psql -U sis_user -d sis_db

shell-redis:
	docker compose exec redis redis-cli -a $$REDIS_PASSWORD

# ── Database ──────────────────────────────────────────────────
migrate:
	docker compose exec api alembic upgrade head

migrate-down:
	docker compose exec api alembic downgrade -1

seed:
	docker compose exec api python -m app.scripts.seed

# ── Helpers ───────────────────────────────────────────────────
clean:
	docker compose down -v --remove-orphans
	docker system prune -f
