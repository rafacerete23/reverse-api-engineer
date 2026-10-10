"""Import Reverse API Engineer collections into Harken's local analytics store."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def _as_text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value.strip() or None
    if isinstance(value, (int, float)):
        return str(value)
    return None


def _load_collection(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() in {".jsonl", ".ndjson"}:
        values: list[dict[str, Any]] = []
        with path.open(encoding="utf-8") as collection_file:
            for line_number, line in enumerate(collection_file, start=1):
                if not line.strip():
                    continue
                try:
                    value = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"invalid JSON on line {line_number}: {exc.msg}") from exc
                if isinstance(value, dict):
                    values.append(value)
        return values

    with path.open(encoding="utf-8") as collection_file:
        value = json.load(collection_file)
    if isinstance(value, dict):
        value = value.get("items", value.get("posts", value.get("data")))
    if not isinstance(value, list):
        raise ValueError("expected a JSON array or an object containing an items array")
    return [item for item in value if isinstance(item, dict)]


def _created_at(item: dict[str, Any]) -> datetime | None:
    raw = item.get("created_at") or item.get("published_at") or item.get("timestamp")
    if not isinstance(raw, str) or not raw.strip():
        return None
    try:
        return datetime.fromisoformat(raw.strip().replace("Z", "+00:00"))
    except ValueError:
        return None


def _score(item: dict[str, Any]) -> int | None:
    engagement = item.get("engagement")
    candidates = [
        item.get("score"),
        item.get("likes_count"),
        item.get("like_count"),
        item.get("favorite_count"),
        item.get("favorites"),
        item.get("upvotes"),
        item.get("points"),
    ]
    if isinstance(engagement, dict):
        candidates.extend(
            engagement.get(name)
            for name in ("score", "likes", "like_count", "favorites", "upvotes", "points")
        )
    for candidate in candidates:
        if isinstance(candidate, bool):
            continue
        if isinstance(candidate, (int, float)):
            return int(candidate)
        if isinstance(candidate, str):
            try:
                return int(float(candidate))
            except ValueError:
                continue
    return None


def import_collection(input_path: Path, query: str, db_path: str | None = None) -> dict[str, int | str]:
    """Map normalized collector output to Harken mentions, analyze, and persist it."""
    try:
        from harken.analyze.insights import ThemeExtractor
        from harken.analyze.sentiment import LexiconSentiment
        from harken.config import Config
        from harken.models import Mention
        from harken.store import Store
    except ImportError as exc:
        raise RuntimeError(
            "Harken integration is optional. Install it with `uv pip install -e '.[harken]'`."
        ) from exc

    query = query.strip()
    if not query:
        raise ValueError("query must not be empty")
    rows = _load_collection(input_path)
    mentions = []
    skipped = 0
    analyzer = LexiconSentiment()

    for item in rows:
        created_at = _created_at(item)
        source = _as_text(item.get("source_platform") or item.get("source"))
        text = _as_text(item.get("content_text") or item.get("text") or item.get("content")) or ""
        title = _as_text(item.get("title") or item.get("content_title"))
        url = _as_text(item.get("source_url") or item.get("url"))
        author = _as_text(item.get("author_handle") or item.get("author"))

        if created_at is None or source is None or not (text or title or url):
            skipped += 1
            continue

        mention = Mention(
            source=source.lower(),
            query=query,
            author=author,
            title=title,
            text=text,
            url=url,
            created_at=created_at,
            score=_score(item),
        )
        sentiment = analyzer.score(mention.content)
        mention.sentiment = sentiment.label
        mention.sentiment_score = sentiment.score
        mentions.append(mention)

    if not mentions:
        return {"database": db_path or str(Config().db_path), "imported": 0, "new": 0, "skipped": skipped}

    database = db_path or str(Config().db_path)
    with Store(database) as store:
        new_count = store.upsert(mentions, update_theme=False)
        stored = store.mentions(query=query, limit=None)
        ThemeExtractor().extract(stored)
        store.upsert(stored)

    return {"database": database, "imported": len(mentions), "new": new_count, "skipped": skipped}
