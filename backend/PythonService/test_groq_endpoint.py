#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Minimal test to verify Groq endpoint"""

import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/models/groq")
async def list_groq_models():
    """Test Groq models endpoint"""
    return {
        "models": [
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
            }
        ],
        "provider": "Groq",
        "api_url": "https://console.groq.com/",
        "total": 2
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
