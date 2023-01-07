
from pydantic import BaseModel, Field

class TodoIn(BaseModel):
    title : str
    description : str 
    priority : int = Field(default= None,  gt=0, lt=3)
    complete : bool 
