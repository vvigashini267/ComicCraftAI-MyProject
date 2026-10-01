import logging
from uuid import uuid4

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app.config import settings
from app.pipeline import ComicResult, build_comic
from app.schemas import PromptRequest
from app.services.image_generator import generate_image

logger = logging.getLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))


class ComicGenerationError(Exception):
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def _generate(user_request: PromptRequest) -> ComicResult:
    """Run the pipeline and turn failures into user-friendly errors."""

    try:
        return build_comic(user_request)
    except RuntimeError as exc:
        # Raised on purpose for known problems (missing API key, blocked reply...)
        logger.warning("Comic generation failed: %s", exc)
        raise ComicGenerationError(str(exc), 503) from exc
    except Exception as exc:
        logger.exception("Unexpected error while generating comic")
        raise ComicGenerationError(
            "Something went wrong while generating your comic. Please try again.",
            500,
        ) from exc


def _index_with_error(
    request: Request,
    message: str,
    status_code: int,
    prompt: str = "",
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": settings.APP_NAME,
            "error": message,
            "prompt": prompt,
        },
        status_code=status_code,
    )


# ============================================================
# HOME PAGE
# ============================================================

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": settings.APP_NAME},
    )


# ============================================================
# GENERATE COMIC - HTML FORM
# ============================================================
# Plain `def` (not `async def`): the pipeline makes blocking network and
# image calls, and FastAPI runs sync handlers in a thread pool so they do
# not freeze the whole server while a comic is being generated.

@router.post("/generate", response_class=HTMLResponse)
def generate_comic(
    request: Request,
    prompt: str = Form(...),
    character_name: str = Form("Main Character"),
    setting: str = Form("A realistic Indian setting"),
    tone: str = Form("Inspirational"),
    art_style: str = Form("Cinematic comic style"),
):
    try:
        user_request = PromptRequest(
            prompt=prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )
    except ValidationError:
        return _index_with_error(
            request,
            "Please check your inputs: the story idea must be between "
            f"3 and {settings.MAX_PROMPT_LENGTH} characters.",
            422,
            prompt,
        )

    try:
        result = _generate(user_request)
    except ComicGenerationError as exc:
        return _index_with_error(request, exc.message, exc.status_code, prompt)

    return templates.TemplateResponse(
        request=request,
        name="comic_preview.html",
        context={
            "title": result.title,
            "panels": result.panels,
            "pdf_filename": result.pdf_filename,
        },
    )


# ============================================================
# GENERATE COMIC - JSON API
# ============================================================

@router.post("/generate-comic/json")
def generate_comic_json(payload: PromptRequest):
    try:
        result = _generate(payload)
    except ComicGenerationError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc

    return {
        "title": result.title,
        # image_path is a server filesystem path - only expose image_url.
        "panels": [
            panel.model_dump(exclude={"image_path"}) for panel in result.panels
        ],
        "pdf_filename": result.pdf_filename,
    }


@router.post("/api/generate-comic")
def api_generate_comic(payload: PromptRequest):
    return generate_comic_json(payload)


# ============================================================
# EXPORT SUCCESS PAGE
# ============================================================

@router.get("/export-success", response_class=HTMLResponse)
def export_success(request: Request, filename: str):
    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={"filename": filename},
    )


# ============================================================
# DOWNLOAD PDF
# ============================================================

@router.get("/download/{filename}")
def download_pdf(filename: str):
    exports_dir = settings.EXPORTS_DIR.resolve()
    file_path = (exports_dir / filename).resolve()

    # Only serve PDFs that sit directly inside the exports folder
    # (blocks "..\\secret" style path traversal, e.g. on Windows).
    if (
        file_path.parent != exports_dir
        or file_path.suffix.lower() != ".pdf"
        or not file_path.is_file()
    ):
        return HTMLResponse(content="PDF file not found.", status_code=404)

    return FileResponse(
        path=str(file_path),
        filename=file_path.name,
        media_type="application/pdf",
    )


# ============================================================
# TEST IMAGE (development only)
# ============================================================

@router.get("/test-image")
def test_image():
    if not settings.DEBUG:
        raise HTTPException(status_code=404, detail="Not found")

    filename = f"test_{uuid4().hex[:8]}.png"

    image_path = generate_image("A simple comic panel test image", filename)

    return {
        "message": "Test image generated successfully.",
        "image_url": f"/static/panels/{image_path.name}",
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@router.get("/health")
def health():
    return {"status": "ok", "app": settings.APP_NAME}
