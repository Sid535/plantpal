"""Langbly Translate v2 client."""

from __future__ import annotations

import os
from typing import Iterable, List

import httpx


DEFAULT_BASE_URL = "https://api.langbly.com"
TRANSLATE_PATH = "/language/translate/v2"


def _get_api_key() -> str | None:
    return os.getenv("LANGLY_API_KEY") or os.getenv("LANGBLY_API_KEY")


def _get_base_url() -> str:
    return os.getenv("LANGLY_API_BASE", DEFAULT_BASE_URL).rstrip("/")


def translate_texts(
    texts: Iterable[str],
    target: str,
    source: str | None = "en",
    fmt: str = "text",
    context: str | None = None,
    instructions: str | None = None,
) -> List[str]:
    """Translate a list of texts. Raises RuntimeError on API failure."""
    api_key = _get_api_key()
    if not api_key:
        return []

    items = [t for t in texts if t is not None]
    if not items:
        return []

    payload: dict = {
        "q": items,
        "target": target,
        "format": fmt,
    }
    if source:
        payload["source"] = source
    if context:
        payload["context"] = context
    if instructions:
        payload["instructions"] = instructions

    url = f"{_get_base_url()}{TRANSLATE_PATH}"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key,
    }

    with httpx.Client(timeout=20) as client:
        response = client.post(url, headers=headers, json=payload)
        if response.status_code >= 400:
            raise RuntimeError(f"Langbly error: {response.status_code}")
        data = response.json()

    translations = data.get("data", {}).get("translations", [])
    return [t.get("translatedText", "") for t in translations]
