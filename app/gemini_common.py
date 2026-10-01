
import random
import time
from typing import TypeVar

from google import genai
from pydantic import BaseModel

from app.config import settings

T = TypeVar("T", bound=BaseModel)

MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 2


def generate_structured(model: str, prompt: str, schema: type[T]) -> T:
    """Call Gemini with retry handling and validate structured JSON output."""

    if not settings.GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add your Gemini API key "
            "to the .env file or Streamlit Cloud secrets."
        )

    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    response = None

    for attempt in range(MAX_RETRIES + 1):
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
            status_code = getattr(exc, "code", None)
            if status_code is None:
                status_code = getattr(exc, "status_code", None)

            # Retry only temporary availability, rate-limit,
            # and server errors.
            retryable = (
                status_code in (429, 500, 502, 503, 504)
                or "503 UNAVAILABLE" in str(exc)
            )

            if not retryable or attempt >= MAX_RETRIES:
                if retryable:
                    except Exception as exc:
                       raise RuntimeError(
                           f"Gemini API error: {type(exc).__name__}: {exc}"
                       ) from exc
                raise

            delay = INITIAL_RETRY_DELAY * (2 ** attempt)
            delay += random.uniform(0, 1)

            print(
                f"Gemini temporary error ({status_code}). "
                f"Retrying in {delay:.1f} seconds "
                f"(attempt {attempt + 1}/{MAX_RETRIES})..."
            )
            time.sleep(delay)

    if response is None or not response.text:
        raise RuntimeError(
            "Gemini returned an empty response. Please try again "
            "or reword your story idea."
        )

    try:
        return schema.model_validate_json(response.text)
    except Exception as exc:
        raise RuntimeError(
            "Gemini returned a response that could not be validated. "
            "Please try generating the comic again."
        ) from exc
