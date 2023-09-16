from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str

class UserRequest(BaseModel):
    username: str
    password: str