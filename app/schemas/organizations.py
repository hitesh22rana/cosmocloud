from pydantic import BaseModel, Field
from typing import List
from bson import ObjectId

from .. models import PyObjectId
from .. models.organizations import OrganizationModel

"""
Response schema for an organization
"""
class OrganizationResponse(OrganizationModel):
    id: PyObjectId = Field(alias="_id")
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        orm_mode = True
    
"""
Response schema for a list of organizations
"""
class OrganizationsResponse(BaseModel):
    total_count : int
    organizations : List[OrganizationResponse]
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        orm_mode = True