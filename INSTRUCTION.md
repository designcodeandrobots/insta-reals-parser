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
4. После `SUCCEEDED` скачивает датасет
5. Сохраняет CSV: `num, url, views, likes, comments, duration_sec, upload_date, caption`
6. Выводит топ-10 по просмотрам

## Apify API

- Базовый URL: `https://api.apify.com/v2`
- Запуск актора: `POST /acts/apify~instagram-reel-scraper/runs?token=<TOKEN>`
- Input: `{"username": ["<username>"], "maxItems": <N>}`
- Статус run: `GET /actor-runs/<runId>?token=<TOKEN>` → поле `data.status`
- Скачать данные: `GET /datasets/<datasetId>/items?token=<TOKEN>`
- Поле с просмотрами в ответе: `videoViewCount`

## Зависимости

Только стандартная библиотека Python: `csv`, `json`, `urllib`, `pathlib`, `sys`, `time`.

## Где брать Apify API token

`https://console.apify.com/settings/integrations` → Personal API tokens → Create token

## Типичные ошибки

- `invalid-input: Field input.username must be array` — username нужно передавать как список: `["username"]`
- `HTTP 400` при запуске — проверить поля input по документации актора
- Пустой `videoViewCount` — бывает у Stories и фото, у Reels всегда заполнен
