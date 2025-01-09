import os

PORT = os.environ.get("PORT")
HOST = os.environ.get("HOST")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.environ.get("OPENAI_MODEL_NAME")

CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")
CLAUDE_MODEL_NAME = os.environ.get("CLAUDE_MODEL_NAME")
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "openai")
