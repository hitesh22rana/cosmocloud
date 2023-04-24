from pydantic import BaseModel, Field
from typing import List
from bson import ObjectId

from .. models import PyObjectId
from .. models.users import UserModel

"""
Response schema for a user
"""
class UserResponse(UserModel):
    id: PyObjectId = Field(alias="_id")
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        orm_mode = True
       
"""
Response schema for a list of users
""" 
class UsersResponse(BaseModel):
    total_count : int
    users : List[UserResponse]
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        orm_mode = True