from fastapi import APIRouter, HTTPException, status, Body
from pymongo.errors import DuplicateKeyError

from .. lib.validators import validate_string_fields, validate_db_connection
from .. database import connect_to_db
from .. models.organizations import OrganizationBaseModel, OrganizationModel
from .. schemas.organizations import OrganizationResponse, OrganizationsResponse

router = APIRouter(
    tags=["Organizations"],
    prefix="/organizations",
)

@router.post("/", response_description="Create new organization", status_code=status.HTTP_201_CREATED, response_model=OrganizationResponse)
async def create_organization(organization: OrganizationBaseModel = Body(...)):
    db = await connect_to_db()
    validate_db_connection(db)
    
    validate_string_fields(organization.name, detail="Name field is required")
    
    try:
        organization = OrganizationModel(**organization.dict())
        result = await db.organizations.insert_one(organization.dict())
        return await db.organizations.find_one({ "_id": result.inserted_id })
    
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Organization already exists")
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create organization. Error: {e}"
        )
        
@router.get("/", response_description="List all organizations", status_code=status.HTTP_200_OK, response_model=OrganizationsResponse)
async def get_organizations(name: str = None, limit: int = 10, offset: int = 0):
    db = await connect_to_db()
    validate_db_connection(db)
    
    # Query parameters
    query = {}
    if name:
        query = {"name": {"$regex": name, "$options": "i"}}
        
    try:
        # Pagination
        total_count = await db.organizations.count_documents(query)
        result = await db.organizations\
                        .find(query)\
                        .skip(offset)\
                        .limit(limit)\
                        .to_list(length=limit)
                        
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Organizations found"
            )
                        
        return {"total_count": total_count, "users": result}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get organizations. Error: {e}"
        )