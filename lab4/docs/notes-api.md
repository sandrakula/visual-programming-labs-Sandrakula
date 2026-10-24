# Ачивка 5.2 — REST API заметок с Redis

Реализованы два независимых workflow:

- `POST /webhook/lab4/sandrakula/notes` — проверяет поля `title` и `text`, создаёт идентификатор и сохраняет JSON заметки под ключом `notes:sandrakula:<id>`;
- `GET /webhook/lab4/sandrakula/notes` — получает все ключи по маске `notes:sandrakula:*` и возвращает записи клиенту.

Пример создания:

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://localhost:5678/webhook/lab4/sandrakula/notes `
  -ContentType application/json `
  -Body '{"title":"Защита","text":"Повторить ноды n8n"}'
```

Пример чтения:

```powershell
Invoke-RestMethod http://localhost:5678/webhook/lab4/sandrakula/notes
```

Для публикации webhook соответствующие workflow нужно активировать после привязки credential **Redis Lab4**.
