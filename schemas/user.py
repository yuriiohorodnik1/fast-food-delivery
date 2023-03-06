from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    """Base user schema."""
    first_name: str = Field(..., min_length=1, max_length=40, example='Yurii')
    last_name: str = Field(..., min_length=1, max_length=40, example='Ohorodnik')
    email: EmailStr = Field(...)


class UserIn(UserBase):
    """User create schema."""
    password: str = Field(..., min_length=8, max_length=40)


class UserOut(UserBase):
    """User instance response schema"""
    id: int = Field(...)

    class Config:
        orm_mode = True
