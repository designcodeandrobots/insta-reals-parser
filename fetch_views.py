#!/usr/bin/env python3
"""
instagram-views — получает просмотры Instagram Reels через Apify
"""

import csv
import json
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

APIFY_ACTOR = "apify~instagram-reel-scraper"
APIFY_BASE = "https://api.apify.com/v2"


def apify_request(method: str, path: str, token: str, body: dict = None) -> dict:
    url = f"{APIFY_BASE}{path}?token={token}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode()
        print(f"❌ Ошибка Apify ({e.code}): {detail}")
        sys.exit(1)


def ask(prompt: str, default: str = "") -> str:
    try:
        value = input(prompt).strip()
        return value if value else default
    except (KeyboardInterrupt, EOFError):
        print()
        sys.exit(0)


def main():
    print("=" * 50)
    print("  instagram-views")
    print("  Просмотры Instagram Reels через Apify")
    print("=" * 50)
    print()

    # API ключ
    token = ask(
        "Apify API ключ: "
        "(получить → https://console.apify.com/settings/integrations)\n> "
    )
    if not token:
        print("❌ API ключ не введён.")
        sys.exit(1)

    # Аккаунт
    username = ask("\nInstagram аккаунт (например: anarbachoo)\n> ")
    if not username.strip("@"):
        print("❌ Аккаунт не введён.")
        sys.exit(1)
    username = username.lstrip("@")

    # Количество роликов
    limit_str = ask("\nСколько роликов собрать? [100]\n> ", "100")
    try:
        limit = int(limit_str)
    except ValueError:
        limit = 100

    # Выходной файл
    default_csv = f"{username}_views.csv"
    output_str = ask(f"\nКуда сохранить CSV? [{default_csv}]\n> ", default_csv)
    output_csv = Path(output_str)

    print()
    print(f"▶ Запускаем Apify для @{username}, до {limit} роликов...")

    run = apify_request("POST", f"/acts/{APIFY_ACTOR}/runs", token, {
        "username": [username],
        "maxItems": limit,
    })
    run_id = run["data"]["id"]
    print(f"  Run ID: {run_id}")

    # Ждём завершения
    dots = 0
    while True:
        time.sleep(10)
        status = apify_request("GET", f"/actor-runs/{run_id}", token)
        state = status["data"]["status"]
        dots += 1
        print(f"  {'.' * dots} {state}", end="\r")
        if state in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"):
            break

    print()
    if state != "SUCCEEDED":
        print(f"❌ Apify завершился со статусом: {state}")
        sys.exit(1)

    print("✅ Готово. Скачиваем результаты...")

    dataset_id = status["data"]["defaultDatasetId"]
    items_data = apify_request(
        "GET", f"/datasets/{dataset_id}/items", token,
    )
    # items_data может быть списком или dict с полем items
    items = items_data if isinstance(items_data, list) else items_data.get("items", [])
    items = items[:limit]

    results = []
    for i, item in enumerate(items, 1):
        results.append({
            "num": i,
            "url": item.get("url", ""),
            "views": item.get("videoViewCount", ""),
            "likes": item.get("likesCount", ""),
            "comments": item.get("commentsCount", ""),
            "duration_sec": item.get("videoDuration", ""),
            "upload_date": (item.get("timestamp") or "")[:10],
            "caption": (item.get("caption") or "").replace("\n", " ")[:120],
            "audio_url": item.get("audioUrl", ""),
        })

    if not results:
        print("❌ Данных нет. Проверьте название аккаунта.")
        sys.exit(1)

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    successful = [r for r in results if r["views"] != ""]
    print(f"\nСобрано роликов: {len(results)}, с просмотрами: {len(successful)}")
    print(f"Файл: {output_csv.resolve()}")

    top = sorted(
        [r for r in successful if isinstance(r["views"], int)],
        key=lambda x: x["views"],
        reverse=True,
    )
    if top:
        print(f"\nТОП-10 по просмотрам:")
        for r in top[:10]:
            print(f"  {r['views']:>10,}  likes={r['likes']:>6,}  {r['caption'][:55]}")


if __name__ == "__main__":
    main()
