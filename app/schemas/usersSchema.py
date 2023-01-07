from pydantic import BaseModel, Field


class UserBaseSchema(BaseModel):
    email       : str
    username    : str
    fname       : str
    lnam        : str
    is_active   : bool
# Pydantic's orm_mode will tell the Pydantic model to read the data 
# even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).
    class Config:
        orm_mode = True



class UserInSchema(UserBaseSchema):
    password : str

    class Config:
        orm_mode = True


class UserOutSchema(UserBaseSchema):
    pass



class UserInDbSchema(UserInSchema):
    hashed_password : str