from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List
from . import PyObjectId

class OrganizationBaseModel(BaseModel):
    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(..., description="Name of the organization")
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Organization name"
            }
        }
        
class OrganizationModel(OrganizationBaseModel):
    users: List[PyObjectId] = Field([], description="List of users in the organization")
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Organization name",
                "users": ["5f9f1b9b9c9d1b1b8c8c8c8c"]
            }
        }
        
# class AccessLevel(str, Enum):
#     READ = "READ"
#     WRITE = "WRITE"
#     ADMIN = "ADMIN"

# class Permission(BaseModel):
#     _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
#     user_id: PyObjectId = Field(default_factory=PyObjectId)
#     organization_id: PyObjectId = Field(default_factory=PyObjectId)
#     access_level: Dict[str, AccessLevel] = Field(...)
    
#     class Config:
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}
#         schema_extra = {
#             "example": {
#                 "user_id": "5f9f1b9b9c9d1b1b8c8c8c8c",
#                 "organization_id": "5f9f1b9b9c9d1b1b8c8c8c8d",
#                 "access_level": "ADMIN"
#             }
#         }
