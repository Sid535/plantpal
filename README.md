---
title: Plantpal
emoji: 🌿
colorFrom: green
colorTo: green
sdk: docker
pinned: false
---

# PlantPal

An AI-powered plant disease diagnosis app. Upload a photo of a plant leaf, and PlantPal identifies the species and any visible disease, then returns a diagnosis — severity, urgency, treatment, and prevention — in **English, Hindi, or Marathi**.

Built as a mini-project (Group A12).

## How It Works

1. The frontend sends an uploaded leaf image to the backend.
2. A transfer-learning image classification model (built on a pretrained CNN, fine-tuned on a Kaggle plant disease dataset) predicts the plant species and disease.
3. The backend looks up structured diagnosis info for that prediction — severity, urgency, what it is, treatment steps, and prevention — from a curated disease knowledge base.
4. That information is returned in the requested language. Common diseases have hand-written English/Hindi/Marathi translations built in; anything not yet covered can fall back to the Langbly Translate API if configured.

## Features

- **Image-based plant disease detection** using a fine-tuned CNN (transfer learning)
- **Grad-CAM visualization** — generates a heatmap showing which regions of the leaf image the model weighted most heavily, so predictions aren't a black box
- **Structured diagnosis output** — not just a label, but severity, urgency, treatment, and prevention guidance
- **Multilingual support** — English, Hindi, and Marathi, with a documented process (`TRANSLATION_GUIDE.md`) for adding more diseases/languages
- **FastAPI backend** serving both the prediction API and the static frontend
- **Dockerized** for reproducible deployment — deployed on Hugging Face Spaces, with a GitHub Action that auto-syncs the Space on every push to `main`

## Tech Stack

**Backend**
- **Python 3.12+**
- **[FastAPI](https://fastapi.tiangolo.com/)** + **Uvicorn** — API server
- **TensorFlow** — model training/inference
- **scikit-learn, pandas, matplotlib, seaborn** — data prep, evaluation, and visualization during model development
- **OpenCV (headless), Pillow** — image preprocessing and Grad-CAM overlay rendering
- **httpx + python-dotenv** — optional Langbly Translate API integration for on-demand translation

**Frontend**
- Plain **HTML/CSS**, with **TypeScript** (compiled to JS via `npm`/`tsc`) for client-side logic

**Infra**
- **Docker** — containerized for deployment
- **[uv](https://docs.astral.sh/uv/)** — Python dependency management
- **GitHub Actions** — auto-syncs `main` to the Hugging Face Space on every push
- **Kaggle** — source dataset, pulled via `generate_classes.py`

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Sid535/plantpal.git
   cd plantpal
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. (Optional) Create a `.env` file if you want on-demand translation for diseases not yet pre-translated:
   ```
   LANGBLY_API_KEY=your_api_key_here
   ```
   Without this, the app still works fully for any disease already covered in `server/translations_hi.py` / `server/translations_mr.py`.

4. Run the app:
   ```bash
   uv run main.py
   ```
   Visit `http://localhost:8000`.

> If you edit `client/app.ts`, recompile it to regenerate `client/app.js` (the browser only ever loads the compiled `.js`):
> ```bash
> npm install typescript   # first time only
> npx tsc client/app.ts --target ES2022 --module commonjs --ignoreConfig
> ```

## Running with Docker

The container listens on port `7860` (Hugging Face Spaces' standard port for Docker-based Spaces):

```bash
docker build -t plantpal .
docker run -p 7860:7860 plantpal
```

Visit `http://localhost:7860`. If you have a `LANGBLY_API_KEY` set, pass it through with `--env-file .env`.

## Live Demo

Deployed on Hugging Face Spaces: **[huggingface.co/spaces/Sid535/Plantpal](https://huggingface.co/spaces/Sid535/Plantpal)**

## Project Structure

```
plantpal/
├── client/
│   ├── index.html
│   ├── styles.css
│   ├── app.ts / app.js         # Frontend logic (TS compiled to JS)
│   └── translations/           # Frontend-side translation strings
├── server/
│   ├── analyzer.py             # Runs inference on uploaded images
│   ├── model_config.py
│   ├── train_model.py
│   ├── evaluate_model.py
│   ├── test_model.py
│   ├── dataset_tools.py
│   ├── treatments.py           # Disease → treatment/prevention knowledge base
│   ├── translations.py         # English disease info
│   ├── translations_hi.py      # Hindi translations
│   ├── translations_mr.py      # Marathi translations
│   ├── langbly_client.py       # Optional translation API fallback
│   └── models/                 # Trained model artifacts
├── generate_classes.py         # Pulls/prepares the Kaggle dataset
├── main.py                     # FastAPI app entry point
├── .github/workflows/
│   └── sync-to-hub.yml         # Auto-syncs main to the Hugging Face Space on push
├── Dockerfile
├── pyproject.toml
├── uv.lock
└── TRANSLATION_GUIDE.md        # How to add more diseases/languages
```

## Adding a New Disease or Language

See `TRANSLATION_GUIDE.md` for the step-by-step process — diseases are added to `server/translations.py` in English first, then translated into Hindi and Marathi following the existing structure (severity, urgency, description, treatment, prevention, expert note).

## Notes

- This started as a group mini-project focused on the core image classifier, then was independently extended with structured multilingual diagnosis output and Grad-CAM explainability — aimed at making plant health guidance accessible beyond English, which matters for practical use in India.
- The model, treatment knowledge base, and translation content are for informational purposes and aren't a substitute for professional agricultural advice.

## License

MIT
