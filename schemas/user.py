from pydantic import BaseModel, EmailStr

# Schema for register route in authentication
class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    qualification: str
    aim: str

# Schema for login route in authentication
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

