# Лабораторная работа №2. Основы работы с Node-RED

**Дисциплина:** «Технологии визуального программирования»  
**Студент:** Sandrakula  
**Группа:** `[ГРУППА]`

## Цель работы

Освоить запуск Node-RED в контейнере Docker, обеспечить постоянное хранение его данных и изучить обработку сообщений с помощью нод Inject, Function, Switch, Change, Template, HTTP Request и Debug.

## Установка и версии

Node-RED запущен из официального Docker-образа `nodered/node-red:5.0.8` с помощью Docker Compose.

- Node-RED: **5.0.8**;
- Node.js: **v24.21.0**;
- адрес редактора: [http://localhost:1880](http://localhost:1880).

Фактические версии получены из журнала запущенного контейнера. Скриншот: [00-nodejs-version.png](../screenshots/00-nodejs-version.png).

## Настройка Docker

Конфигурация находится в `lab2/docker-compose.yml`. Контейнер имеет имя `visual-programming-lab2-nodered`, а порт редактора опубликован как `1880:1880`.

Каталог `lab2/node-red-data` подключён к `/data` контейнера как bind mount. В нём Node-RED хранит `flows.json`, настройки и другие рабочие данные. Каталог исключён из Git, поскольку может содержать локальное состояние, токены и зашифрованные учётные данные.

После развёртывания потоков контейнер был перезапущен. Node-RED снова вернул все сохранённые вкладки и ноды, что подтверждает постоянство данных в `/data`.

## Задание 2.1 — Inject → Debug

Создана отдельная вкладка **«2.1 — Inject Debug»** со связью `Inject → Debug`.

Параметры Inject:

- `msg.payload` — строка `Sandrakula`;
- `msg.topic` — `lab2/Sandrakula/basic`;
- повтор — каждые 5 секунд.

Нода Debug настроена на вывод полного объекта `msg`. Экспорт потока сохранён в `lab2/flows/flow-01-inject-debug.json` и тот же поток реально развёрнут в работающем Node-RED.

## Результат проверки 2.1

Редактор отвечает с HTTP-кодом `200`. В панели Debug зафиксирована последовательность сообщений с шагом 5 секунд; каждое содержит `payload: "Sandrakula"`, `topic: "lab2/Sandrakula/basic"` и служебный `_msgid`.

Скриншот результата: [01-inject-debug.png](../screenshots/01-inject-debug.png).

## Задание 2.2 — Function

На отдельной вкладке **«2.2 — Function»** создан поток `Inject → Function → Debug`. Inject передаёт число `6`. Function вычисляет квадраты чисел от 1 до входного значения, складывает их и формирует объект результата.

В JavaScript-коде используются обязательные конструкции:

- `const` для входного числа, массива и итогового объекта;
- `let` для накапливаемой суммы и категории результата;
- цикл `for` для перебора чисел;
- массив `squares` для квадратов;
- `if/else` для определения категории;
- объект `result`, который записывается в `msg.payload`.

При входном числе `6` получен массив `[1, 4, 9, 16, 25, 36]`, сумма `91` и категория «большой результат». Экспорт: `lab2/flows/flow-02-function.json`. Скриншот: [02-function.png](../screenshots/02-function.png).

## Задание 2.3 — Switch

На вкладке **«2.3 — Switch»** создан поток с двумя Inject: оба передают число в Function, затем Switch проверяет именно `msg.payload`.

Function использует ту же идею суммы квадратов, сохраняет подробности вычисления в объекте `msg.calculation`, а числовую сумму — в `msg.payload`. Switch имеет два выхода:

1. `msg.payload >= 50`;
2. все остальные значения (`otherwise`).

Число `6` даёт `91` и попадает в первую ветку. Число `3` даёт `14` и попадает во вторую ветку. Обе ветки реально проверены через отдельные Debug-ноды. Экспорт: `lab2/flows/flow-03-switch.json`. Скриншот: [03-switch.png](../screenshots/03-switch.png).

## Задание 2.4 — Change

На вкладке **«2.4 — Change»** создан поток `Inject → Change → Debug`. Change выполняет три операции:

- задаёт `msg.topic = "lab2/Sandrakula/change"`;
- создаёт `msg.timestamp` выражением JSONata `$millis()`;
- заменяет `msg.payload` на строку `Сообщение обработано для Sandrakula`.

Debug выводит полный объект сообщения. В реальном запуске подтверждены все три изменённых поля; timestamp получен во время обработки сообщения. Экспорт: `lab2/flows/flow-04-change.json`. Скриншот: [04-change.png](../screenshots/04-change.png).

## Задание 2.5 — Template

На вкладке **«2.5 — Template»** создан поток `Inject → Template → Debug`. Inject формирует объект с полями `student`, `subject`, `lab` и задаёт topic `lab2/Sandrakula/template`.

Template использует синтаксис Mustache, берёт значения из `msg.payload` и записывает в `msg.payload` разобранный JSON-объект. При реальном ручном запуске получен результат:

```json
{
  "student": "Sandrakula",
  "subject": "Visual Programming",
  "lab": "Node-RED",
  "message": "Student Sandrakula is working with Node-RED"
}
```

Экспорт: `lab2/flows/flow-05-template.json`. Скриншот: [05-template.png](../screenshots/05-template.png).

## Задание 2.6 — HTTP Request

На вкладке **«2.6 — HTTP Request»** создан поток `Inject → HTTP Request → Debug`. После ручного запуска HTTP Request выполняет метод GET по адресу `https://jsonplaceholder.typicode.com/todos/1` и разбирает тело ответа как JSON.

В реальном запуске получен `statusCode: 200`. В `msg.payload` находится объект с полями `userId: 1`, `id: 1`, `title: "delectus aut autem"` и `completed: false`. Debug выводит полный объект `msg`, поэтому одновременно видны разобранное тело ответа и код состояния HTTP. Экспорт: `lab2/flows/flow-06-http-request.json`. Скриншот: [06-http-request.png](../screenshots/06-http-request.png).

## Итог этапа 3

В Node-RED одновременно доступны шесть отдельных вкладок: 2.1–2.6. Каждый поток сохранён отдельным импортируемым JSON-файлом. Перед развёртыванием новых потоков создана локальная резервная копия, а после перезапуска контейнера подтверждена сохранность всех шести вкладок в bind mount `/data`.

## Использованные AI-промпты

Ключевые примеры запросов к AI:

- «Настрой Node-RED через Docker Compose на порту 1880 с постоянным локальным каталогом `/data`».
- «Создай и реально разверни поток Inject → Debug с `payload = Sandrakula`, заданным topic и интервалом 5 секунд».
- «Проверь HTTP-доступность, версии, сохранность потока после перезапуска и подготовь реальные скриншоты».
- «Оформи отчёт и короткую пошаговую инструкцию для демонстрации преподавателю».
- «Напиши Function для вычисления суммы квадратов с `let`, `const`, `if/else`, циклом, массивом и объектом».
- «Настрой Switch по `msg.payload` с отдельными ветками для результата не меньше 50 и остальных значений».
- «Настрой Change для topic, текста payload и текущего timestamp через JSONata `$millis()`».
- «Создай Template с Mustache-переменными, который преобразует входной объект в JSON с сообщением о студенте Sandrakula».
- «Настрой HTTP Request для GET-запроса к JSONPlaceholder, разбери ответ как JSON и проверь `statusCode: 200`».

