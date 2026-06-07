> **Для AI-ассистентов:** см. [INSTRUCTION.md](./INSTRUCTION.md) — полное описание проекта.

# instagram-views

Собирает просмотры, лайки и комментарии Instagram Reels для любого публичного аккаунта. Работает через [Apify](https://apify.com) — не требует авторизации в Instagram и не нарушает Terms of Service.

Результат — CSV-файл с метриками по каждому ролику.

## Требования

- Python 3.8+
- Аккаунт на [apify.com](https://apify.com) есть бесплатный тариф

## Установка

```bash
git clone https://github.com/designcodeandrobots/insta-reals-parser.git
cd insta-reals-parser
```

Сторонних зависимостей нет — используется только стандартная библиотека Python.

## Установка через AI-чат

Если хочешь развернуть проект через Claude или другой AI-ассистент — скинь ему ссылку на репозиторий и напиши:

> Склонируй репозиторий https://github.com/designcodeandrobots/insta-reals-parser и запусти `fetch_views.py`. Инструкция в INSTRUCTION.md.

## Использование

```bash
python3 fetch_views.py
```

Скрипт спросит:
1. **Apify API ключ** — где взять: [console.apify.com/settings/integrations](https://console.apify.com/settings/integrations)
2. **Instagram аккаунт** — например `anarbachoo` или `@anarbachoo`
3. **Сколько роликов** собрать (по умолчанию 100)
4. **Куда сохранить** CSV (по умолчанию `<аккаунт>_views.csv`)

### Пример сессии

```
==================================================
  instagram-views
  Просмотры Instagram Reels через Apify
==================================================

Apify API ключ: (получить → https://console.apify.com/settings/integrations)
> apify_api_...

Instagram аккаунт (например: anarbachoo)
> anarbachoo

Сколько роликов собрать? [100]
> 100

Куда сохранить CSV? [anarbachoo_views.csv]
>

▶ Запускаем Apify для @anarbachoo, до 100 роликов...
  Run ID: mF93REMcbO9rnNn3a
  .......... SUCCEEDED

✅ Готово. Скачиваем результаты...

Собрано роликов: 100, с просмотрами: 100
Файл: /Users/.../anarbachoo_views.csv

ТОП-10 по просмотрам:
   1,864,045  likes=264,682  Ваши варианты пж 👇🏻 ...
     554,678  likes= 65,579  почти все лучшее было придумано...
     ...
```

## Формат CSV

| Колонка | Описание |
|---|---|
| `num` | Порядковый номер |
| `url` | Ссылка на ролик |
| `views` | Просмотры |
| `likes` | Лайки |
| `comments` | Комментарии |
| `duration_sec` | Длительность в секундах |
| `upload_date` | Дата публикации (YYYY-MM-DD) |
| `caption` | Подпись (первые 120 символов) |

## Стоимость

Apify даёт $5 бесплатно при регистрации. Один запуск на 100 роликов стоит ~$0.10–0.30.
