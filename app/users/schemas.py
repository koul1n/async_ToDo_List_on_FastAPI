from pydantic import BaseModel, EmailStr



class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True



class UserUpdate(BaseModel):
    id: int
    username: str | None
    email: EmailStr | None

    class Config:
        from_attributes = True



