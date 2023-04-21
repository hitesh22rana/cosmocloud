from pydantic import BaseModel
from typing import List
from bson import ObjectId

from .. models.users import UserModel

class UserResponse(UserModel):
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        orm_mode = True
        
class UsersResponse(BaseModel):
    total_count : int
    users : List[UserModel]
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        orm_mode = True