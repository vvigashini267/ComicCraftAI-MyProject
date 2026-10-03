
import time
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
    """Call Gemini, retry temporary errors, and validate its response."""

    if not settings.GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Add your Gemini API key to Streamlit Secrets."
        )

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    response = None
    max_attempts = 3

    for attempt in range(max_attempts):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": schema,
                },
            )
            break

        except Exception as exc:
            error_message = str(exc)
            error_upper = error_message.upper()

            temporary_error = (
                "503" in error_upper
                or "UNAVAILABLE" in error_upper
                or "429" in error_upper
                or "RESOURCE_EXHAUSTED" in error_upper
                or "500" in error_upper
                or "INTERNAL SERVER ERROR" in error_upper
            )

            if not temporary_error or attempt == max_attempts - 1:
                raise RuntimeError(
                    f"Gemini API error: {type(exc).__name__}: {exc}"
                ) from exc

            # Wait 2 seconds, then 4 seconds before retrying.
            time.sleep(2 ** (attempt + 1))

    if response is None or not response.text:
        raise RuntimeError(
            "Gemini returned an empty response. "
            "Please try again with a different story idea."
        )

    try:
        return schema.model_validate_json(response.text)
    except Exception as exc:
        raise RuntimeError(
            f"Could not validate Gemini's response: {exc}"
        ) from exc
