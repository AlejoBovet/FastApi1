from pydantic import BaseModel


#Entidad User
class User(BaseModel):
    id: str | None
    name: str
    last_name: str
    age: int
    email: str
    password: str