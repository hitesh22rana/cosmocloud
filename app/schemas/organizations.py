from pydantic import BaseModel
from typing import List
from bson import ObjectId

from .. models.organizations import OrganizationModel

class OrganizationResponse(OrganizationModel):    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        orm_mode = True
        
class OrganizationsResponse(BaseModel):
    total_count : int
    users : List[OrganizationModel]
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        orm_mode = True