# Лабораторная работа №4 — n8n

В каталоге находятся Docker-конфигурация, экспортированные workflow, отчёт и подтверждающие скриншоты.

## Быстрый запуск

```powershell
cd lab4
docker compose up -d
docker compose exec n8n n8n import:workflow --separate --input=/flows
```

После запуска редактор доступен по адресу <http://localhost:5678>.

Для Redis-ноды создайте credential типа Redis:

- Host: `host.docker.internal` (или `redis` внутри compose-сети);
- Port: `6379`;
- Database Number: `0`.

Подробности: [docs/report.md](docs/report.md) и [docs/redis.md](docs/redis.md).

