#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

import uvicorn
from main import app
from fastapi import HTTPException

# Add Groq models endpoint directly
@app.get("/api/models/groq", tags=["Models"])
async def list_groq_models():
    """Liệt kê các Groq models có sẵn"""
    try:
        models = [
            {
                "id": "llama-3.1-70b-versatile",
                "name": "Llama 3.1 70B",
                "description": "Best overall performance",
                "context": 32768,
                "speed": "fast"
            },
            {
                "id": "llama-3.1-8b-instant",
                "name": "Llama 3.1 8B Instant",
                "description": "Fastest inference",
                "context": 32768,
                "speed": "ultra-fast"
            },
            {
                "id": "mixtral-8x7b-32768",
                "name": "Mixtral 8x7B",
                "description": "Long context specialist",
                "context": 32768,
                "speed": "fast"
            },
            {
                "id": "gemma2-9b-it",
                "name": "Gemma 2 9B",
                "description": "Lightweight & efficient",
                "context": 8192,
                "speed": "ultra-fast"
            }
        ]
        
        return {
            "models": models,
            "provider": "Groq",
            "api_url": "https://console.groq.com/",
            "total": len(models)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
