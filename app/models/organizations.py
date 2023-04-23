from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List

from . import PyObjectId, AccessLevel

class OrganizationBaseModel(BaseModel):
    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(..., description="Name of the organization")
    created_by: PyObjectId = Field(..., description="User ID of the user who created the organization")
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Organization name",
                "created_by": "user_id"
            }
        }
        
class MemberPermissionModel(BaseModel):
    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId = Field(...)
    access_level: AccessLevel = Field(...)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "user_id": "user_id",
                "access_level": "ADMIN"
            }
        }
        
class OrganizationModel(OrganizationBaseModel):
    members: List[MemberPermissionModel] = Field([], description="List of users in the organization")
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Organization name",
                "members": ["user_id"]
            }
        }
        
class AddMemberModel(BaseModel):
    user_id: PyObjectId = Field(...)
    access_level: AccessLevel = Field(...)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "user_id": "user_id",
                "access_level": "ADMIN"
            }
        }
        
class UpdateMemberModel(AddMemberModel):    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "user_id": "user_id",
                "access_level": "ADMIN"
            }
        }
        
class RemoveMemberModel(BaseModel):
    user_id: PyObjectId = Field(...)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "user_id": "user_id"
            }
        }