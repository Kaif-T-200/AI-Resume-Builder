"""Groq API provider implementation."""
import os
from typing import Optional
from openai import OpenAI

from resume_ai.providers.base import LLMProvider


class GroqProvider(LLMProvider):
    """Provider for Groq API (uses OpenAI-compatible client)."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is required")
        
        self.model_name = model
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1"
        )

    def complete(self, *, system_prompt: str, user_prompt: str, temperature: float = 0.2, max_tokens: Optional[int] = None) -> str:
        """Call Groq API using OpenAI-compatible interface."""
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens or 2000,
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise RuntimeError(f"Groq API error: {e}")
