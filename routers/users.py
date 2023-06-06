from fastapi import HTTPException,APIRouter, status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema
from db.schemas.user import users_schema
from bson import ObjectId

router = APIRouter( prefix="/users", 
                   tags=["users"],
                   responses={status.HTTP_404_NOT_FOUND:{"description": "Not found"}})


#GET
@router.get("/", response_model=list[User])
async def get_users_class():
    return users_schema(db_client.ProyectFastApi1.users.find())

#GET PATH PARAMS
@router.get("/{id}")  
async def user(id: str):
    return search_user("_id", ObjectId(id))

#GET QUERY PARAMS  
@router.get("/")
async def get_user_by_id_params(id: str):
    return search_user("_id",ObjectId(id))

#POST
@router.post("/",response_model=User, status_code=201)
async def create_user(user: User):
    if type(search_user("email",user.email)) == User:
       raise HTTPException(status_code=400, detail="user already exists")
    
    user_dict = dict(user)
    del user_dict["id"]
       
    id = db_client.ProyectFastApi1.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.ProyectFastApi1.users.find_one({"_id":id}))

    return User(**new_user)

#PUT
@router.put("/", response_model=User)
async def update_user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.ProyectFastApi1.users.find_one_and_replace({"_id":ObjectId(user.id)}, user_dict)
        
    except:
        raise HTTPException(status_code=404, detail="user not found") 
    
    return search_user("_id",ObjectId(user.id))
    
#DELETE
@router.delete("/{id}")
async def delete_user(id: str, status_code=status.HTTP_204_NO_CONTENT):
 
    Found = db_client.ProyectFastApi1.users.find_one_and_delete({"_id":ObjectId(id)})

    if not Found:
        return {"message": "user not found"}    
    else:
        return {"message": "user deleted successfully"}


#FUNCTIONS

def search_user(field: str, key):
    
    try:
        user = db_client.ProyectFastApi1.users.find_one({field:key})
        return User(**user_schema(user))
    except:
        return {"message": "user not found"}
    



