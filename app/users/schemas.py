from pydantic import BaseModel, EmailStr, constr



class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=20)
    email: EmailStr
    password:  constr(min_length=5, max_length=20)

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



