from dataclasses import dataclass
import os
from typing import Optional


@dataclass
class OpenAISettings:
    model: str = "gpt-4o-mini"
    api_key: Optional[str] = None
    organization: Optional[str] = None
    temperature: float = 0.1
    max_tokens: int = 2000

    @classmethod
    def from_env(cls) -> "OpenAISettings":
        return cls(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            api_key=os.getenv("OPENAI_API_KEY"),
            organization=os.getenv("OPENAI_ORG"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.2")),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "1200")),
        )


dataclass_transform = dataclass  # alias kept for future config objects
