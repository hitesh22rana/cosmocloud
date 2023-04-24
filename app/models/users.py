from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from typing import List

from . import PyObjectId

"""
Request model for creating a new user
"""
class UserBaseModel(BaseModel):
    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(..., description="Name of the user")
    email: EmailStr = Field(..., description="Email address of the user")
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
            }
        }

"""
Response model for a list of users
"""
class UserModel(UserBaseModel):
    organizations: List[PyObjectId] = Field([], description="List of organizations the user belongs to")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "organizations": ["5f9f1b9b9c9d1b1b8c8c8c8c"]
            }
        }