from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "ComicCraft"
    APP_ENV: str = "development"
    DEBUG: bool = True

    GEMINI_API_KEY: str = ""

    GEMINI_OUTLINE_MODEL: str = "gemini-3.5-flash-lite"
    GEMINI_STORY_MODEL: str = "gemini-3.5-flash-lite"

    HF_API_KEY: str = ""
    IMAGE_PROVIDER: str = "placeholder"

    HF_IMAGE_MODEL: str = "stabilityai/stable-diffusion-xl-base-1.0"
    LOCAL_IMAGE_MODEL: str = "runwayml/stable-diffusion-v1-5"

    IMAGE_WIDTH: int = 768
    IMAGE_HEIGHT: int = 768
    IMAGE_STEPS: int = 25
    IMAGE_GUIDANCE: float = 7.5

    MAX_PANELS: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
