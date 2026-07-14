# How to Add More Diseases to Backend Translations

The multilingual disease translation system is now live! Here's how to expand it.

## Quick Overview
- **Backend translations file**: `server/translations.py`
- **Disease structure**: Each disease has display_name, severity, urgency, what_is_it, treatment, prevention, expert_note
- **How to add**: Follow the pattern and add to DISEASE_TRANSLATIONS dictionary in each language section

## Step-by-Step: Adding a New Disease

### 1. Get the Disease Key
From `server/treatments.py`, find the key format, e.g.: `"Apple___Apple_scab"`

### 2. Add to English First
```python
"Apple___Apple_scab": {
    "display_name": "Apple — Apple Scab",
    "severity": "🟡 Moderate",
    "urgency": "Act within 3-4 days",
    "what_is_it": "...",
    "treatment": ["...", "..."],
    "prevention": ["...", "..."],
    "expert_note": "..."
}
```

### 3. Translate to Hindi (hi) and Marathi (mr)
Copy the structure and translate each field:
- **display_name**: Plant name + disease name in that language
- **severity**: Use emojis (🟡🟠🔴) + severity level in that language
- **urgency**: Time frame in that language
- **what_is_it**: Full description translated
- **treatment**: List of treatment steps translated
- **prevention**: List of prevention strategies translated
- **expert_note**: Important notes translated

### Example Template
```python
"YourDisease___Name": {
    "display_name": "[Plant — Disease Name]",
    "severity": "[Emoji] [Severity Level]",
    "urgency": "[Time Frame]",
    "what_is_it": "[Full description]",
    "treatment": [
        "Step 1",
        "Step 2",
        "Step 3"
    ],
    "prevention": [
        "Strategy 1",
        "Strategy 2"
    ],
    "expert_note": "[Important note]"
}
```

## Testing
1. Add disease to all three languages (en, hi, mr)
2. Restart the backend: `python main.py`
3. Upload a plant image and verify disease info appears in selected language

## Automatic Fallback
- If a disease translation is missing → Falls back to English
- If disease not in translations at all → Uses data from `server/treatments.py`
- This ensures the system never breaks, even with incomplete translations

## Batch Addition
For multiple diseases, copy the entire disease block from `treatments.py` and translate all fields for each language section in `translations.py`.
