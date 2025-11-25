from pydantic import BaseModel


class LightToggleRequest(BaseModel):
    message: str


class LightToggleResponse(BaseModel):
    topic: str
    payload: str
    status: str

