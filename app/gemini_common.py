from typing import TypeVar

from google import genai
from pydantic import BaseModel

from app.config import settings

T = TypeVar("T", bound=BaseModel)


def generate_structured(model: str, prompt: str, schema: type[T]) -> T:
    """Call Gemini and return the response parsed into ``schema``."""

    if not settings.GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add your Gemini API key to the .env file."
        )

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": schema,
        },
    )

    # response.text is None when the reply is empty or blocked by safety filters.
    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response. The story idea may have been "
            "blocked by safety filters - try rewording it."
        )

    return schema.model_validate_json(response.text)
