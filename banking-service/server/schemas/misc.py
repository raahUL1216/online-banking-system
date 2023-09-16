from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str

class UserRequest(BaseModel):
    username: str
    password: str

class AmountRequest(BaseModel):
    value: int

class TransferRequest(BaseModel):
    user_id: int
    amount: int