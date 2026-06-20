from abc import ABC, abstractmethod
from app.services.ai.provider_router import AIProviderRouter

class Agent(ABC):
    name: str

    def __init__(self, router: AIProviderRouter | None = None):
        self.router = router or AIProviderRouter()

    @abstractmethod
    async def run(self, payload: dict) -> dict:
        raise NotImplementedError
