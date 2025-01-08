from pydantic import BaseModel, EmailStr, constr, ConfigDict



class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=20)
    email: EmailStr
    password: constr(min_length=5, max_length=20)

    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    username: str
    email: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)



class UserUpdate(BaseModel):
    username: str | None
    email: EmailStr | None
    model_config = ConfigDict(from_attributes=True)








