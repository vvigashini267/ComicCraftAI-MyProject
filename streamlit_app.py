import os
from pathlib import Path

import streamlit as st


# ---------------------------------------------------------
# Load secrets from Streamlit Cloud / local environment
# ---------------------------------------------------------
def load_secrets():
    secret_keys = [
        "GEMINI_API_KEY",
        "GEMINI_OUTLINE_MODEL",
        "GEMINI_STORY_MODEL",
        "IMAGE_PROVIDER",
        "HF_API_KEY",
        "HF_IMAGE_MODEL",
        "LOCAL_IMAGE_MODEL",
        "IMAGE_WIDTH",
        "IMAGE_HEIGHT",
        "IMAGE_STEPS",
        "IMAGE_GUIDANCE",
        "MAX_PANELS",
        "MAX_PROMPT_LENGTH",
    ]

    for key in secret_keys:
        try:
            if key in st.secrets:
                os.environ[key] = str(st.secrets[key])
        except Exception:
            pass


load_secrets()


# Import ComicCraft modules AFTER loading secrets
from app.pipeline import build_comic
from app.schemas import PromptRequest


# ---------------------------------------------------------
# Streamlit page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="ComicCraft AI",
    page_icon="🎨",
    layout="wide",
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.title("🎨 ComicCraft AI")
st.subheader("AI Comic Story Creator using Gemini Models")

st.write(
    "Create a personalized 5-panel comic story using Gemini AI "
    "and AI-generated images."
)

st.divider()


# ---------------------------------------------------------
# Input section
# ---------------------------------------------------------
st.header("📝 Create Your Comic")

prompt = st.text_area(
    "Story Idea",
    placeholder=(
        "Example: A brave young farmer discovers a new way "
        "to save his village..."
    ),
    height=150,
)

col1, col2 = st.columns(2)

with col1:
    character_name = st.text_input(
        "Main Character",
        value="Main Character",
    )

    setting = st.text_input(
        "Setting",
        value="A realistic Indian setting",
    )

with col2:
    tone = st.selectbox(
        "Tone",
        [
            "Inspirational",
            "Funny",
            "Dramatic",
            "Emotional",
            "Adventure",
        ],
    )

    art_style = st.selectbox(
        "Art Style",
        [
            "Cinematic comic style",
            "2D cartoon style",
            "3D cartoon style",
            "Realistic comic style",
            "Anime style",
        ],
    )


# ---------------------------------------------------------
# Generate Comic
# ---------------------------------------------------------
if st.button(
    "🚀 Generate Comic",
    type="primary",
    width="stretch",
):

    if not prompt.strip():
        st.warning("Please enter a story idea first.")
        st.stop()

    try:
        user_request = PromptRequest(
            prompt=prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )
    except Exception:
        st.error(
            "Please check your inputs: the story idea must be "
            "at least 3 characters and not too long."
        )
        st.stop()

    try:
        with st.status(
            "Creating your comic...",
            expanded=True,
        ) as status:

            result = build_comic(user_request, on_progress=st.write)

            status.update(
                label="Comic generated successfully! 🎉",
                state="complete",
            )

        # -------------------------------------------------
        # Display result
        # -------------------------------------------------
        st.divider()

        st.header(f"📖 {result.title}")

        for panel in result.panels:

            st.subheader(f"Panel {panel.panel_number}")

            st.image(
                str(panel.image_path),
                width="stretch",
            )

            if panel.caption:
                st.write(f"**Caption:** {panel.caption}")

            if panel.scene_description:
                st.write(f"**Scene:** {panel.scene_description}")

            if panel.narration:
                st.write(f"**Narration:** {panel.narration}")

            if panel.dialogue:
                st.write(f"**Dialogue:** {panel.dialogue}")

            st.divider()

        # -------------------------------------------------
        # PDF download
        # -------------------------------------------------
        if result.pdf_path.exists():

            st.download_button(
                label="📥 Download Comic PDF",
                data=result.pdf_path.read_bytes(),
                file_name=result.pdf_filename,
                mime="application/pdf",
                width="stretch",
            )

    except Exception as error:

        st.error(
            "Something went wrong while generating "
            "the comic."
        )

        st.exception(error)


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.divider()

st.caption(
    "ComicCraft AI • Powered by Gemini + Hugging Face"
)