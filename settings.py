"""Chapter 15 application settings."""
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
KNOWLEDGE_FILE = PROJECT_DIR / "data" / "support_faq.json"
OLLAMA_HOST = "http://localhost:11434"
MODEL_NAME = "qwen3.5:9b"  # Change to qwen3.5:4b if needed.
MAX_INPUT = 2500
