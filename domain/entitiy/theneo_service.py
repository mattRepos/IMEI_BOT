from pydantic import BaseModel

class TheneoService(BaseModel):
    title: str
    id: int
    price: str
