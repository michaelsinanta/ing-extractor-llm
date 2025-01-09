from app.utils import Singleton
from anthropic import Anthropic
from openai import OpenAI
from app import config


class ClaudeService(Singleton):
    def build(self):
        self._client = Anthropic(api_key=config.CLAUDE_API_KEY)

    def get_client(self) -> Anthropic:
        return self._client


class OpenAIService(Singleton):
    def build(self):
        self._client = OpenAI(api_key=config.OPENAI_API_KEY)

    def get_client(self) -> OpenAI:
        return self._client
