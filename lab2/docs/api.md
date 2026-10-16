# API лабораторной работы №2

Базовый адрес при локальном запуске: `http://localhost:1880`.

Все маршруты используют метод `GET` и не требуют авторизации.

## GET /api/text

Возвращает простое текстовое приветствие. Параметры отсутствуют.

Запрос для Windows:

```powershell
curl.exe -i http://localhost:1880/api/text
```

Успешный ответ — `200 OK`, `Content-Type: text/plain; charset=utf-8`:

```text
Hello from Sandrakula! Node-RED Lab 2.
```

## GET /api/info

Возвращает JSON-информацию о студенте и лабораторной. Параметры отсутствуют.

Запрос для Windows:

```powershell
curl.exe -i http://localhost:1880/api/info
```

Успешный ответ — `200 OK`, `Content-Type: application/json; charset=utf-8`:

```json
{
  "student": "Sandrakula",
  "lab": "Node-RED Lab 2"
}
```

## GET /api/items

Ищет демонстрационный элемент по query parameter `id`. Доступны элементы:

- `1` — Notebook;
- `2` — Mouse;
- `3` — Keyboard.

`id` обязателен и должен быть положительным целым числом без посторонних символов.

### Успешный запрос

```powershell
curl.exe -i "http://localhost:1880/api/items?id=1"
```

Ответ — `200 OK`:

```json
{
  "id": 1,
  "name": "Notebook"
}
```

### Некорректный id

```powershell
curl.exe -i "http://localhost:1880/api/items?id=abc"
```

Ответ — `400 Bad Request`:

```json
{
  "error": "Invalid item id"
}
```

Строки наподобие `1abc`, ноль, отрицательные и небезопасно большие целые числа также получают статус `400`.

### Параметр id отсутствует

```powershell
curl.exe -i http://localhost:1880/api/items
```

Ответ — `400 Bad Request`:

```json
{
  "error": "Missing item id"
}
```

### Элемент не найден

```powershell
curl.exe -i "http://localhost:1880/api/items?id=999"
```

Ответ — `404 Not Found`:

```json
{
  "error": "Item not found"
}
```

Для всех ответов `/api/items` используется `Content-Type: application/json; charset=utf-8`.
