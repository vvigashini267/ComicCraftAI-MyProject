
from typing import TypeVar

from google import genai
from pydantic import BaseModel

from app.config import settings

T = TypeVar("T", bound=BaseModel)


def generate_structured(
    model: str,
    prompt: str,
    schema: type[T],
) -> T:
    """Call Gemini and validate its structured response."""

    if not settings.GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Add your Gemini API key to Streamlit Secrets."
        )

    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)

        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": schema,
            },
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response. "
                "Please try a different story idea."
            )

        return schema.model_validate_json(response.text)

    except RuntimeError:
        raise

    except Exception as exc:
        raise RuntimeError(
            f"Gemini API error: {type(exc).__name__}: {exc}"
        ) from exc
