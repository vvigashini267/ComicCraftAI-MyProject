from app.config import settings
from app.exporters import save_pdf
from app.schemas import ComicPanel


def test_pdf_export_handles_non_latin1_text(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "EXPORTS_DIR", tmp_path)

    panel = ComicPanel(
        panel_number=1,
        scene_description="Ravi\u2019s first day \u2014 a \u201cnew\u201d start\u2026",
        caption="\u0ba4\u0bae\u0bbf\u0bb4\u0bcd caption",
        narration="Narration",
        dialogue="Hello!",
        image_prompt="prompt",
        image_path=str(tmp_path / "missing.png"),
    )

    output = save_pdf("A \u201cGreat\u201d Story", [panel], "test.pdf")

    assert output.exists()
    assert output.read_bytes().startswith(b"%PDF")
