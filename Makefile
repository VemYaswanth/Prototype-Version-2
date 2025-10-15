.PHONY: up down logs fmt test seed

up:
    docker compose up -d --build

down:
    docker compose down -v

logs:
    docker compose logs -f

test:
    pytest -q

seed:
    psql postgres://postgres:postgres@localhost:5432/securitydb \
        -f backend/migrations/0001_init.sql