# INSTRUCTION.md — для AI-ассистентов

## Что делает этот проект

`instagram-views` — CLI-скрипт на Python, который собирает метрики Instagram Reels (просмотры, лайки, комментарии) для любого публичного аккаунта через Apify API.

Instagram не отдаёт `view_count` через публичный API без авторизации. Apify обходит это ограничение через актор `apify/instagram-reel-scraper`, который возвращает поле `videoViewCount`.

## Файлы проекта

```
instagram-views/
├── fetch_views.py   — единственный скрипт, точка входа
├── README.md        — инструкция для пользователя (русский)
└── INSTRUCTION.md   — этот файл
```

## Как работает скрипт

1. Запрашивает у пользователя: Apify API token, Instagram username, лимит роликов, путь для CSV
2. Запускает Apify актор `apify~instagram-reel-scraper` через REST API
3. Поллит статус run каждые 10 секунд
4. После `SUCCEEDED` скачивает датасет с параметром `limit=N` (Apify игнорирует `maxItems` в input и отдаёт весь аккаунт — лимит применяется на этапе скачивания датасета)
5. Сохраняет CSV: `num, url, views, likes, comments, duration_sec, upload_date, caption, audio_url`
6. Выводит топ-10 по просмотрам

## Apify API

- Базовый URL: `https://api.apify.com/v2`
- Запуск актора: `POST /acts/apify~instagram-reel-scraper/runs?token=<TOKEN>`
- Input: `{"username": ["<username>"], "maxItems": <N>}`
- Статус run: `GET /actor-runs/<runId>?token=<TOKEN>` → поле `data.status`
- Скачать данные: `GET /datasets/<datasetId>/items?token=<TOKEN>&limit=<N>`
- Поле с просмотрами в ответе: `videoViewCount`
- Поле с аудиодорожкой: `audioUrl` (прямая ссылка на mp3/m4a, можно скачать и транскрибировать через Whisper)

## Зависимости

Только стандартная библиотека Python: `csv`, `json`, `urllib`, `pathlib`, `sys`, `time`.

## Где брать Apify API token

`https://console.apify.com/settings/integrations` → Personal API tokens → Create token

## Типичные ошибки

- `invalid-input: Field input.username must be array` — username нужно передавать как список: `["username"]`
- `HTTP 400` при запуске — проверить поля input по документации актора
- Пустой `videoViewCount` — бывает у Stories и фото, у Reels всегда заполнен
- Apify возвращает больше роликов чем указано в `maxItems` — лимит нужно применять через `?limit=N` при скачивании датасета
