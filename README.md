# ComicCraft

ComicCraft is an AI-powered web application that generates personalized
5-panel comics from a user's story idea.

## Features

- Generate a 5-panel comic story
- AI-generated scene descriptions
- AI-generated narration and dialogue
- AI-generated comic illustrations
- Comic preview in the browser
- Export comic as PDF
- FastAPI backend with a Jinja2 frontend
- Optional Streamlit interface
- Gemini AI integration
- Hugging Face and local Stable Diffusion image generation

## Technologies

Python, FastAPI, Jinja2, Google Gemini, Hugging Face, Stable Diffusion,
Pillow, FPDF2, Streamlit

## Run the Project

Create and activate a virtual environment:

```bash
py -3.11 -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your settings file and add your Gemini API key:

```bash
copy .env.example .env          # Windows
# cp .env.example .env          # macOS / Linux
```

Start the FastAPI app:

```bash
uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000.

Or start the Streamlit app instead:

```bash
streamlit run streamlit_app.py
```

## Image providers

Set `IMAGE_PROVIDER` in `.env`:

- `placeholder` - simple test images, no extra setup (default)
- `hf` - Hugging Face Inference API (needs `HF_API_KEY`)
- `local` - Stable Diffusion on your own machine
  (`pip install -r requirements-local-image.txt`)

## Run the tests

```bash
pytest
```
