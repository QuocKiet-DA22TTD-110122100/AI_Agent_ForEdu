"""
Groq API Helper
Support for Groq's ultra-fast LPU inference (Llama, Mixtral, Gemma models)
API: https://console.groq.com/
"""
import requests
from typing import Dict, List, Optional
import os


class GroqClient:
    """Client for Groq API (OpenAI-compatible)"""
    
    # Fallback models if API fails
    FALLBACK_MODELS = [
        {
            "id": "llama-3.3-70b-versatile",
            "name": "Llama 3.3 70B Versatile",
            "description": "Best overall performance - Latest",
            "context": 128000,
            "speed": "fast"
        },
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
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_models_from_api(self) -> List[Dict]:
        """
        Fetch available models from Groq API
        Endpoint: GET /models
        
        Returns:
            List of model dicts with id, name, description, context, speed
        """
        try:
            url = f"{self.base_url}/models"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            models = data.get('data', [])
            
            # Filter and format models for chat
            chat_models = []
            for model in models:
                model_id = model.get('id', '')
                model_id_lower = model_id.lower()
                
                # Skip non-chat models
                if any(skip in model_id_lower for skip in ['whisper', 'audio', 'guard', 'tts', 'vision']):
                    continue
                
                # Only include known chat models
                if not any(name in model_id_lower for name in ['llama', 'mixtral', 'gemma', 'qwen']):
                    continue
                
                # Skip models with very small context (likely not chat models)
                context = model.get('context_window', 8192)
                if context < 4000:
                    continue
                
                # Speed based on model size
                speed = "fast"
                if '8b' in model_id_lower or '7b' in model_id_lower or '9b' in model_id_lower:
                    speed = "ultra-fast"
                elif '17b' in model_id_lower:
                    speed = "ultra-fast"
                elif '32b' in model_id_lower:
                    speed = "fast"
                elif '70b' in model_id_lower:
                    speed = "fast"
                elif '405b' in model_id_lower:
                    speed = "slow"
                
                # Generate display name
                name = model_id
                if '/' in model_id:
                    name = model_id.split('/')[-1]
                name = name.replace('-', ' ').title()
                
                # Description based on model characteristics
                description = "General purpose chat"
                if '70b' in model_id_lower:
                    description = "Best overall performance"
                elif '8b' in model_id_lower or 'instant' in model_id_lower:
                    description = "Fastest inference"
                elif '32b' in model_id_lower:
                    description = "Balanced performance"
                elif 'versatile' in model_id_lower:
                    description = "Best overall performance"
                if 'scout' in model_id_lower:
                    description = "Efficient reasoning"
                if 'maverick' in model_id_lower:
                    description = "Advanced reasoning"
                
                chat_models.append({
                    "id": model_id,
                    "name": name,
                    "description": description,
                    "context": context,
                    "speed": speed,
                    "owned_by": model.get('owned_by', 'unknown'),
                    "created": model.get('created', 0)
                })
            
            # Sort by context size (larger first) and then by name
            chat_models.sort(key=lambda x: (-x['context'], x['id']))
            
            return chat_models if chat_models else self.FALLBACK_MODELS
            
        except Exception as e:
            print(f"⚠️ Error fetching Groq models from API: {e}")
            return self.FALLBACK_MODELS
    
    @classmethod
    def get_available_models(cls) -> List[Dict]:
        """Get list of fallback Groq models (static)"""
        return cls.FALLBACK_MODELS
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "llama-3.1-70b-versatile",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        stream: bool = False
    ) -> Dict:
        """
        Create chat completion with Groq
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Groq model name
                - llama-3.1-70b-versatile (Best overall)
                - llama-3.1-8b-instant (Fastest)
                - mixtral-8x7b-32768 (Long context)
                - gemma2-9b-it (Lightweight)
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream response
            
        Returns:
            Response dict with 'choices' containing generated text
        """
        url = f"{self.base_url}/chat/completions"
        
        payload = {
            "messages": messages,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        response = requests.post(url, json=payload, headers=self.headers, timeout=30)
        response.raise_for_status()
        
        return response.json()
    
    def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: str = "llama-3.1-70b-versatile"
    ) -> str:
        """
        Simple text generation
        
        Args:
            prompt: User prompt
            system_prompt: Optional system instruction
            model: Groq model name
            
        Returns:
            Generated text string
        """
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        response = self.chat_completion(messages, model=model)
        
        return response['choices'][0]['message']['content']


# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not found in .env")
        exit(1)
    
    client = GroqClient(api_key)
    
    # Test simple generation
    print("Testing Groq API...")
    response = client.generate_text(
        prompt="Explain quantum computing in simple terms",
        system_prompt="You are a helpful AI assistant.",
        model="llama-3.1-70b-versatile"
    )
    
    print("\n✅ Groq Response:")
    print(response)
