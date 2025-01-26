from abc import ABC, abstractmethod
from domain.entitiy.theneo_service import TheneoService

class ImeiCheckClientInterface(ABC):

    @abstractmethod
    async def check_imei(self, imei: str, service_id: int) -> dict:
        pass

    @abstractmethod
    async def get_services(self) -> list[TheneoService]:
        pass
