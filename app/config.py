from pathlib import Path

# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"

# ==========================================================
# AI Configuration
# ==========================================================

GEMINI_MODEL = "models/gemini-3.5-flash-lite"

DEFAULT_TEMPERATURE = 0.3

# ==========================================================
# PDF Processing
# ==========================================================

WORDS_PER_MINUTE = 200

# ==========================================================
# File Types
# ==========================================================

PDF_EXTENSION = ".pdf"
TEXT_EXTENSION = ".txt"

# ==========================================================
# AI Output
# ==========================================================

AI_FOLDER_NAME = "ai"

SUMMARY_SUFFIX = "_summary.md"
NOTES_SUFFIX = "_notes.md"
FLASHCARDS_SUFFIX = "_flashcards.json"
TOPICS_SUFFIX = "_topics.json"
DIFFICULTY_SUFFIX = "_difficulty.json"
