# Redis в лабораторной работе №4

## Запуск

Redis 7 запускается вместе с n8n через `docker compose up -d`. Порт `6379` опубликован на хосте, данные сохраняются в `lab4/redis-data` благодаря AOF (`appendonly yes`).

## Подключение из n8n

В n8n используется credential **Redis Lab4**:

- Host: `host.docker.internal`;
- Port: `6379`;
- Database Number: `0`;
- SSL: выключен.

Если n8n и Redis запущены одним `docker-compose.yml`, вместо `host.docker.internal` допустимо имя сервиса `redis`.

## Создание и чтение

Workflow `flow-09-redis.json` выполняет последовательность:

1. `Manual Trigger` запускает проверку.
2. `Redis Set sandrakula` создаёт ключ `sandrakula` со строковым значением `Lab 4 value created by Sandrakula`.
3. `Redis Get sandrakula` читает только что сохранённое значение в поле `redisValue`.

Контроль из контейнера:

```powershell
docker compose exec redis redis-cli GET sandrakula
```

## Удаление и проверка отсутствия

Workflow `flow-10-redis.json` выполняет:

1. `Redis Delete sandrakula` удаляет ключ.
2. `Redis Exists sandrakula` проверяет его отсутствие; ожидаемый результат — `0`/`false`.

Контроль из контейнера:

```powershell
docker compose exec redis redis-cli EXISTS sandrakula
```

Redis хранит пары «ключ → значение» в оперативной памяти и отвечает очень быстро. В работе ключ используется как уникальный идентификатор, а команды `SET`, `GET`, `DEL` и `EXISTS` демонстрируют полный жизненный цикл записи.
