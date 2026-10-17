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

## Задание 2.7 — MQTT

MQTT — лёгкий протокол обмена сообщениями по модели «издатель — брокер — подписчик». Отправитель публикует сообщение в именованный топик, брокер принимает его и передаёт всем клиентам, подписанным на этот топик. Поэтому отправителю и получателю не требуется напрямую обращаться друг к другу.

В работе используется публичный брокер **HiveMQ**:

- адрес: `broker.hivemq.com`;
- порт: `1883`;
- топик: `student/Sandrakula/lab2/temperature`;
- QoS: `0`;
- конфиденциальные данные не передаются.

На вкладке **«2.7 — MQTT»** созданы две связанные через брокер ветки:

1. `Inject → Function → MQTT Out` — публикация температуры;
2. `MQTT In → Debug` — подписка и отображение полученного сообщения.

Inject запускает первую ветку каждые 5 секунд. Function выполняет JavaScript-код:

```javascript
msg.payload = Number((20 + Math.random() * 15).toFixed(1));
msg.topic = "student/Sandrakula/lab2/temperature";
return msg;
```

`Math.random()` создаёт случайную дробь, после чего формула переводит её в диапазон от 20 до 35 °C. `toFixed(1)` оставляет один знак после запятой, а `Number(...)` гарантирует числовой тип `msg.payload`. MQTT Out публикует сообщение в HiveMQ, MQTT In подписан на точно такой же топик, а Debug выводит полный объект `msg` вместе с `topic`, `payload`, `qos` и `retain`.

Реальная проверка выполнена двумя способами. Node-RED сообщил о подключении обеих MQTT-нод к `broker.hivemq.com:1883`. Затем для входящей Debug-ноды временно включили вывод в журнал контейнера: именно после прохождения `MQTT In → Debug` последовательно получены значения `21`, `34.3`, `34` и `26.5` с интервалом 5 секунд. Во время проверки в редакторе дополнительно получены `24.4`, `30.3` и `28.3`; у каждого сообщения был топик `student/Sandrakula/lab2/temperature`, QoS `0` и числовой payload. После проверки вывод Debug в консоль выключен, обычный вывод в боковую панель сохранён.

Экспорт потока: `lab2/flows/flow-07-mqtt.json`. Скриншот с полной схемой, состоянием «подключен» у MQTT Out и MQTT In и тремя входящими сообщениями: [07-mqtt.png](../screenshots/07-mqtt.png).

## Задание 2.8 — GET-эндпоинты

На отдельной вкладке **«2.8 — GET Endpoints»** созданы три HTTP-маршрута. Каждый маршрут имеет собственную цепочку `HTTP In → Function → HTTP Response`:

- HTTP In принимает GET-запрос по заданному URL;
- Function формирует `msg.payload`, задаёт `msg.statusCode` и заголовок `Content-Type`;
- HTTP Response отправляет рассчитанный ответ клиенту.

Реализованы маршруты:

- `/api/text` — текст `Hello from Sandrakula! Node-RED Lab 2.`;
- `/api/info` — JSON ровно с полями `student` и `lab`;
- `/api/items` — поиск Notebook, Mouse или Keyboard по query parameter `id`.

В обработчике `/api/items` значение читается из `msg.req.query.id`. Регулярное выражение `^[1-9]\\d*$` не допускает строки наподобие `1abc`, ноль и отрицательные числа. После преобразования дополнительно проверяется `Number.isSafeInteger`. Отсутствующий или некорректный параметр возвращает `400`, неизвестный корректный id — `404`, найденный элемент — `200`.

### Результаты HTTP-проверки

| Запрос | Фактический статус | Результат |
|---|---:|---|
| `GET /api/text` | 200 | текстовое приветствие, `text/plain; charset=utf-8` |
| `GET /api/info` | 200 | `{"student":"Sandrakula","lab":"Node-RED Lab 2"}` |
| `GET /api/items?id=1` | 200 | `{"id":1,"name":"Notebook"}` |
| `GET /api/items?id=abc` | 400 | `{"error":"Invalid item id"}` |
| `GET /api/items?id=999` | 404 | `{"error":"Item not found"}` |
| `GET /api/items` | 400 | `{"error":"Missing item id"}` |

Все статусы, тела и заголовки проверены реальными запросами `curl.exe -i`. Полная документация с готовыми командами находится в [api.md](api.md). Экспорт вкладки: `lab2/flows/flow-08-endpoints.json`.

Скриншоты: [полная схема](../screenshots/08-endpoints-flow.png), [текстовый ответ](../screenshots/08-api-text.png), [JSON-информация](../screenshots/08-api-info.png), [успешный поиск](../screenshots/08-api-items-success.png), [ошибка 400](../screenshots/08-api-items-error-400.png), [ошибка 404](../screenshots/08-api-items-error-404.png).

## Задание 2.9 — Dashboard

На отдельной вкладке **«2.9 — Dashboard»** создан поток `Inject → Function`, от выхода Function проведены два соединения: одно к Gauge, другое к Chart.

- Inject **«Temperature every 5 sec»** автоматически отправляет сообщение каждые 5 секунд. Начальный `msg.payload` — число `1`, `msg.topic` — `lab2/Sandrakula/temperature`.
- Function **«Generate temperature»** генерирует случайную температуру в диапазоне 20–35 °C с одним знаком после запятой:

```javascript
const minTemp = 20;
const maxTemp = 35;

const temperature = Math.round(
    (Math.random() * (maxTemp - minTemp) + minTemp) * 10
) / 10;

msg.payload = temperature;
msg.topic = "Temperature";
return msg;
```

`Math.random()` создаёт случайную дробь, формула переводит её в диапазон от 20 до 35, а `Math.round(...) / 10` оставляет один знак после запятой. Число записывается в `msg.payload`, а в `msg.topic` — подпись серии `Temperature`.

Dashboard построен на установленном пакете **node-red-dashboard 3.6.6** (классический dashboard с нодами `ui_gauge` и `ui_chart`).

- Dashboard Tab: **«Sandrakula Lab 2»**;
- Dashboard Group: **«Temperature Monitoring»** — в ней размещены обе ноды.

Gauge **«Current Temperature»** показывает текущую температуру: диапазон 0–50 °C, единицы `°C`, значение берётся из `msg.payload`. Chart **«Temperature History»** — линейный график, который накапливает историю по серии `Temperature` и хранит данные за последние 10 минут.

Dashboard доступен по адресу [http://localhost:1880/ui](http://localhost:1880/ui).

### Результаты проверки 2.9

- Страница `/ui` отвечает HTTP-кодом `200`, вкладка Dashboard развёрнута без ошибок.
- Через подключение к socket.io дашборда фактически подтверждено поступление данных: Gauge получает числовые значения температуры (например `33.4`, `27.5`, `33.1`), Chart получает серию `Temperature` с историей значений во времени. Временные метки идут с интервалом около 5 секунд, значения находятся в диапазоне 20–35 °C.
- Обнаружена и исправлена ошибка конфигурации: у ноды `ui_base` отсутствовало обязательное поле `site.sizes`, из-за чего страница падала с ошибкой `Cannot read properties of undefined (reading 'sy')`. После добавления стандартных размеров `sx:48, sy:48, gx:6, gy:6, cx:6, cy:6, px:0, py:0` конфигурация передаётся корректно.
- Визуальное отображение Gauge и Chart в браузере отдельно не проверялось и требует ручного подтверждения на странице `/ui`.

Экспорт потока: `lab2/flows/flow-09-dashboard.json`. Скриншоты: [09-dashboard.png](../screenshots/09-dashboard.png) (интерфейс Dashboard) и [09-dashboard-flow.png](../screenshots/09-dashboard-flow.png) (схема потока).

## Задание 2.10 — Telegram Bot

На отдельной вкладке **«2.10 — Telegram Bot»** создан Telegram-бот `@tvl_lab2_sandrakula_bot`. В работе используется пакет **node-red-contrib-telegrambot 19.0.3** и одна общая конфигурационная нода **«Sandrakula Lab2 Bot»** в режиме Polling.

Поток состоит из трёх веток:

1. `Telegram Command /start → Function → Telegram Sender` — отправляет приветствие и предлагает открыть `/help`.
2. `Telegram Command /help → Function → Telegram Sender` — выводит список доступных команд и описание Echo.
3. `Telegram Receiver → Function → Telegram Sender` — повторяет обычные текстовые сообщения.

Ноды **Telegram Command** принимают только заданные команды. **Telegram Receiver** получает входящие сообщения для Echo. Function **«Echo text»** пропускает только сообщения типа `message` с непустым строковым содержимым и отбрасывает строки, начинающиеся с `/`. Поэтому `/start` и `/help` не попадают в Echo и не дают дублирующихся ответов. **Telegram Sender** использует `msg.payload.chatId`, полученный от входной ноды, и отправляет `msg.payload.content` как сообщение типа `message`.

Токен введён только в credential-поле конфигурационной ноды Node-RED. Он не входит в экспорт `flow-10-telegram.json`, документацию или Git. Все шесть Telegram-нод используют один и тот же Bot config.

### Результаты проверки 2.10

- контейнер `visual-programming-lab2-nodered` работает и имеет статус `healthy`;
- Telegram-ноды показывают состояние `connected`, Polling активен;
- в свежих логах отсутствуют ошибки `bot not initialized`, `401` и `409`;
- `/start` вернул одно приветственное сообщение;
- `/help` вернул одно сообщение со списком команд;
- сообщение `Привет` было повторено как `Привет`;
- сообщение `Проверка 123` было повторено как `Проверка 123`;
- команды не были повторно обработаны веткой Echo.

Экспорт потока: `lab2/flows/flow-10-telegram.json`. Скриншоты: [полная схема Telegram-потока](../screenshots/10-telegram-flow.png) и [реальная переписка с ботом](../screenshots/10-telegram.png).

## Итог этапа 7

В Node-RED одновременно сохранены десять отдельных вкладок: 2.1–2.10. Каждый поток сохранён отдельным импортируемым JSON-файлом. Перед изменением Telegram credential создана локальная резервная копия `flows.json` в исключённой из Git папке `lab2/backups`. Состояние хранится в bind mount `/data`; работоспособность Node-RED, HTTP-маршрутов, MQTT, Dashboard и Telegram-бота подтверждена реальными проверками.

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
- «Создай вкладку MQTT с публикацией случайной температуры каждые 5 секунд в публичный HiveMQ-брокер, подпишись на тот же топик через MQTT In и подтверди несколько реально полученных сообщений».
- «Создай в Node-RED три GET-эндпоинта `/api/text`, `/api/info` и `/api/items?id=...`, корректно установи Content-Type и статусы 200, 400, 404, затем проверь все варианты реальными HTTP-запросами».
- «Создай в Node-RED вкладку 2.9 Dashboard на базе node-red-dashboard 3.6.6: Inject каждые 5 секунд, Function генерирует температуру 20–35 °C, одна Function с двумя выходами на Gauge и Chart; Gauge показывает текущее значение в диапазоне 0–50 °C, Chart — историю за 10 минут; разверни в работающем Node-RED и проверь поступление данных через socket.io».

