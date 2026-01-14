import os
from typing import Optional
from openai import OpenAI

from resume_ai.config import OpenAISettings
from resume_ai.providers.base import LLMProvider


class OpenAIProvider(LLMProvider):
    def __init__(self, settings: Optional[OpenAISettings] = None):
        self.settings = settings or OpenAISettings.from_env()
        api_key = self.settings.api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required")
        self.client = OpenAI(api_key=api_key, organization=self.settings.organization)

    def complete(self, *, system_prompt: str, user_prompt: str, temperature: float = 0.2, max_tokens: Optional[int] = None) -> str:
        response = self.client.chat.completions.create(
            model=self.settings.model,
            temperature=temperature,
            max_tokens=max_tokens or self.settings.max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        message = response.choices[0].message.content
        if not message:
            raise RuntimeError("OpenAI returned empty content")
        return message.strip()
