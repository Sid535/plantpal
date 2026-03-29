from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os

from server.analyzer import analyze_plant_image

app = FastAPI(title="PlantPal API")

# CORS — keep this for dev convenience if you ever test from a different origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Serve the frontend ──────────────────────────────────────────────────────
# Place index.html / styles.css / app.js in a folder called "static"
# alongside this main.py file.  Then visit http://localhost:8000
STATIC_DIR = os.path.join(os.path.dirname(__file__), "client")

@app.get("/")
async def serve_index():
    """Serve the frontend entry point."""
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

# ───────────────────────────────────────────────────────────────────────────

@app.post("/analyze")
async def analyze_endpoint(file: UploadFile = File(...)):
    """
    Receives an image from the frontend, passes it to the analyzer,
    and returns the result as JSON.
    """
    try:
        if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
            return {"success": False, "error": "Invalid file type. Use JPG, PNG or WEBP."}

        results = analyze_plant_image(file.file)

        if results:
            return {"success": True, "data": results}
        else:
            return {"success": False, "error": "Could not process image."}

    except Exception as e:
        return {"success": False, "error": str(e)}

# Serve all other static assets (CSS, JS, images …)
app.mount("/", StaticFiles(directory=STATIC_DIR), name="client")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)