import streamlit as st

from app.schemas import PromptRequest
from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.services.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf


st.set_page_config(
    page_title="ComicCraft AI",
    page_icon="🎨",
    layout="wide",
)


st.title("🎨 ComicCraft AI")

st.subheader(
    "AI Comic Story Creator using Gemini Models"
)

st.write(
    "Create a personalized 5-panel comic story "
    "using Gemini AI and AI-generated images."
)


st.header("📝 Create Your Comic")


story_idea = st.text_area(
    "Story Idea",
    value=(
        "A brave young farmer named Ravi discovers "
        "a magical seed that can save his village "
        "from a terrible drought."
    ),
)


character_name = st.text_input(
    "Main Character",
    value="Ravi",
)


setting = st.text_input(
    "Setting",
    value=(
        "A small village surrounded by "
        "mountains and farmland"
    ),
)


tone = st.text_input(
    "Tone",
    value="Adventure and inspirational",
)


art_style = st.text_input(
    "Art Style",
    value="Cinematic comic style",
)


create_button = st.button(
    "✨ Create My Comic",
    type="primary",
)


if create_button:

    if not story_idea.strip():

        st.error(
            "Please enter a story idea."
        )

        st.stop()

    try:

        # --------------------------------------
        # Create request
        # --------------------------------------

        user_request = PromptRequest(
            prompt=story_idea,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )


        # --------------------------------------
        # Generate outline
        # --------------------------------------

        st.info(
            "🧠 Generating story outline..."
        )

        outline = generate_outline(
            user_request
        )


        # --------------------------------------
        # Generate story
        # --------------------------------------

        st.info(
            "✍️ Writing the 5-panel story..."
        )

        story = generate_story(
            user_request,
            outline,
        )

        st.success(
            "Story generated successfully!"
        )


        # --------------------------------------
        # Display story
        # --------------------------------------

        st.header(
            f"📖 {story.title}"
        )


        for panel in story.panels:

            st.subheader(
                f"Panel {panel.panel_number}"
            )

            st.write(
                f"**Scene:** "
                f"{panel.scene_description}"
            )

            st.write(
                f"**Caption:** "
                f"{panel.caption}"
            )

            if panel.narration:

                st.write(
                    f"**Narration:** "
                    f"{panel.narration}"
                )

            if panel.dialogue:

                st.write(
                    f"**Dialogue:** "
                    f"{panel.dialogue}"
                )


        # --------------------------------------
        # Generate images
        # --------------------------------------

        st.info(
            "🎨 Creating comic panel images..."
        )

        image_paths = []


        for panel in story.panels:

            filename = (
                f"streamlit_panel_"
                f"{panel.panel_number}.png"
            )

            image_path = generate_image(
                panel.image_prompt,
                filename,
            )

            image_paths.append(
                image_path
            )


        # --------------------------------------
        # Check image count
        # --------------------------------------

        if len(story.panels) != len(image_paths):

            raise ValueError(
                f"Story panels: {len(story.panels)}, "
                f"Images: {len(image_paths)}"
            )


        st.success(
            "Comic images created!"
        )


        # --------------------------------------
        # Display all panels
        # --------------------------------------

        st.header(
            "🖼️ Comic Panels"
        )


        for index, image_path in enumerate(
            image_paths,
            start=1,
        ):

            st.subheader(
                f"Panel {index}"
            )

            st.image(
                image_path,
                use_container_width=True,
            )


        # --------------------------------------
        # Build comic panel data
        # --------------------------------------

        st.info(
            "🖼️ Preparing comic layout..."
        )

        comic_panels = build_comic_layout(
            story.panels,
            image_paths,
        )

        st.success(
            "Comic layout created!"
        )


        # --------------------------------------
        # Create PDF containing ALL panels
        # --------------------------------------

        st.info(
            "📄 Creating PDF with all 5 panels..."
        )

        pdf_path = save_pdf(
            image_paths,
            "generated_images/comic_page.pdf",
        )


        st.success(
            "🎉 Your 5-panel comic PDF is ready!"
        )


        # --------------------------------------
        # Download PDF
        # --------------------------------------

        with open(
            pdf_path,
            "rb",
        ) as pdf_file:

            st.download_button(
                label="📥 Download Complete Comic PDF",
                data=pdf_file,
                file_name="ComicCraft_Complete_Comic.pdf",
                mime="application/pdf",
            )


    except Exception as e:

        st.error(
            "Something went wrong while generating the comic."
        )

        st.exception(e)
