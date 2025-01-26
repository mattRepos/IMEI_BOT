from domain.api_client.theneo_client_interface import ImeiCheckClientInterface
import httpx
from domain.entitiy.theneo_service import TheneoService
from domain.entitiy.theneo_imei_info import TheneoImeiResult, TheneoImeiInfo

class TheneoClient(ImeiCheckClientInterface):

    BASE_URL = "https://api.imeicheck.net"

    def __init__(self, api_key: str):
        self.client = httpx.AsyncClient()
        self.api_key = api_key
        self.client.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Accept-Language": "ru"
        })

    async def get_services(self) -> list[TheneoService]:
        url = f"{self.BASE_URL}/v1/services"
        response = await self.client.get(url)
        if response.status_code != 200:
            return {
                "error_code": response.status_code,
                "error_message": response.text
            }
        return [TheneoService(**service) for service in response.json()]

    async def check_imei(self, imei: str, service_id: int) -> TheneoImeiResult:
        url = f"{self.BASE_URL}/v1/checks"
        body = {
            "deviceId": imei,
            "serviceId": service_id
        }
        response = await self.client.post(url, json=body)
        if response.status_code >= 300:
            return TheneoImeiResult(
                id="",
                status=f"bad_request_{response.status_code}",
                amount=None,
                properties=None
            )
        data = response.json()
        if data.get("status") == "successful":
            properties_data = data.get("properties")
            propeties = TheneoImeiInfo(
                imei=properties_data.pop("imei", ""),
                device_name=properties_data.pop("deviceName", ""),
                model_description=properties_data.pop("modelDesc", "Нет описания для данного устройства"),
                embedded_info=properties_data
            )
            return TheneoImeiResult(
                id=data.get("id", ""),
                status=data.get("status", ""),
                amount=data.get("amount", None),
                properties=propeties
            )
        return TheneoImeiResult(
            id=data.get("id", ""),
            status=data.get("status", ""),
        )
