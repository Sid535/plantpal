from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from server.analyzer import analyze_plant_image

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
async def analyze_endpoint(file: UploadFile = File(...)):
    """
    This endpoint receives an image from the frontend, 
    passes it to your analyzer, and returns the JSON dictionary.
    """
    try:
        # FastAPI gives us a file-like object that PIL (inside your analyzer) can read directly
        results = analyze_plant_image(file.file)
        
        if results:
            return {"success": True, "data": results}
        else:
            return {"success": False, "error": "Could not process image."}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # Runs the server on port 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)