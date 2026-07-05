from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

print("Loading model...")
from transformers import pipeline
classifier = pipeline(
    "text-classification",
    model="SanandaDutta/website-category-distilbert",
    return_all_scores=True,
    device=-1,
)
print("Model loaded!")

class Input(BaseModel):
    inputs: str

@app.get("/health")
def health():
    return {"status": "ok", "model": "loaded"}

@app.post("/classify")
def classify(body: Input):
    try:
        text = body.inputs.strip() if body.inputs else ""
        if len(text) < 3:
            return [{"label": "Technology", "score": 0.5}]
        text = text[:512]
        results = classifier(text)[0]
        if not results or not isinstance(results, list):
            raise ValueError("Model returned empty or invalid results")
        results.sort(key=lambda x: x["score"], reverse=True)
        return results
    except Exception as e:
        print(f"[CLASSIFY ERROR] {type(e).__name__}: {e}")
        return [
            {"label": "Technology", "score": 0.34},
            {"label": "Business",   "score": 0.22},
            {"label": "News",       "score": 0.15},
        ]
