from pydantic import BaseModel, Field

class TheneoImeiInfo(BaseModel):
    imei: str
    device_name: str = ""
    model_description: str = ""
    embedded_info: dict = {}

class TheneoImeiResult(BaseModel):
    id: str
    status: str
    amount: str | None = None
    properties: TheneoImeiInfo | None = None