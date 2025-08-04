from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None  # ✅ was 'username'

class User(BaseModel):
    email: str
    role: str

class LoginInput(BaseModel):
    email: str  # ✅ was 'username'
    password: str
