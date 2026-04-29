from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

from server.analyzer import analyze_plant_image
from server.langbly_client import translate_texts

load_dotenv()

app = FastAPI(title="PlantPal API")

# This allows your HTML frontend to talk to this Python backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, you'd restrict this to your actual domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_endpoint(file: UploadFile = File(...), lang: str = Query("en")):
    """
    This endpoint receives an image from the frontend, 
    passes it to your analyzer, and returns the JSON dictionary.
    
    Query Parameters:
    - lang: Language code (en, hi, mr). Defaults to 'en'.
    """
    try:
        # Validate language
        valid_langs = ["en", "hi", "mr"]
        if lang not in valid_langs:
            lang = "en"
        
        # FastAPI gives us a file-like object that PIL (inside your analyzer) can read directly
        results = analyze_plant_image(file.file, language=lang)
        
        if results:
            return {"success": True, "data": results}
        else:
            return {"success": False, "error": "Could not process image."}
            
    except Exception as e:
        return {"success": False, "error": str(e)}


class TranslateRequest(BaseModel):
    text: str | list[str]
    target: str
    source: str | None = "en"


@app.post("/translate")
async def translate_endpoint(payload: TranslateRequest):
    """Translate text using Langbly while keeping the API key server-side."""
    try:
        texts = payload.text if isinstance(payload.text, list) else [payload.text]
        translated = translate_texts(texts, target=payload.target, source=payload.source)
        if not translated:
            return {"success": False, "error": "Translation unavailable"}

        if isinstance(payload.text, list):
            return {"success": True, "translations": translated}

        return {"success": True, "translated": translated[0]}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # Runs the server on port 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)