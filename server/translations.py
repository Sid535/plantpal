"""Backend translations for disease info, treatments, and prevention."""

from __future__ import annotations

from functools import lru_cache

from server.langbly_client import translate_texts
from server.treatments import PLANT_INFO
from server.translations_hi import HI_TRANSLATIONS
from server.translations_mr import MR_TRANSLATIONS

DISEASE_TRANSLATIONS = {
    "hi": HI_TRANSLATIONS,
    "mr": MR_TRANSLATIONS,
}


def _translate_info(info: dict, language: str) -> dict:
    context = "plant disease diagnosis and care guidance"
    instructions = (
        "Keep emojis, scientific names, product names, and units unchanged. "
        "Preserve the original meaning."
    )

    single_fields = [
        "display_name",
        "severity",
        "urgency",
        "what_is_it",
        "expert_note",
        "fun_fact",
    ]
    list_fields = [
        "treatment",
        "prevention",
        "care_tips",
    ]

    texts: list[str] = []
    mapping: list[tuple] = []

    for field in single_fields:
        value = info.get(field)
        if isinstance(value, str) and value.strip():
            texts.append(value)
            mapping.append(("single", field))

    for field in list_fields:
        values = info.get(field)
        if isinstance(values, list):
            for idx, item in enumerate(values):
                if isinstance(item, str) and item.strip():
                    texts.append(item)
                    mapping.append(("list", field, idx))

    translated = translate_texts(
        texts,
        target=language,
        source="en",
        context=context,
        instructions=instructions,
    )

    if len(translated) != len(texts):
        return {}

    result: dict = {}
    for meta, value in zip(mapping, translated):
        if meta[0] == "single":
            result[meta[1]] = value
        else:
            field = meta[1]
            idx = meta[2]
            result.setdefault(field, [])
            while len(result[field]) <= idx:
                result[field].append("")
            result[field][idx] = value

    return result


@lru_cache(maxsize=512)
def _translate_disease_cached(disease_key: str, language: str) -> dict:
    info = PLANT_INFO.get(disease_key)
    if not info:
        return {}

    return _translate_info(info, language)


def get_translated_info(disease_key: str, language: str = "en") -> dict:
    """Get translated disease info. Returns empty dict if missing."""
    if language == "en":
        return {}

    if language in DISEASE_TRANSLATIONS:
        static_info = DISEASE_TRANSLATIONS[language].get(disease_key)
        if static_info:
            return static_info

    return _translate_disease_cached(disease_key, language)
