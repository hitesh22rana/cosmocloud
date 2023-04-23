from fastapi import APIRouter, HTTPException, status, Body
from pymongo.errors import DuplicateKeyError, ConnectionFailure
from bson import ObjectId

from .. lib.validators import validate_string_fields, validate_db_connection, validate_organization_role
from .. lib.helper_functions import get_access_level_enum
from .. database import connect_to_db
from .. models.organizations import OrganizationBaseModel, OrganizationModel, MemberPermissionModel, AddMemberModel, UpdateMemberModel, RemoveMemberModel
from .. schemas.organizations import OrganizationResponse, OrganizationsResponse

router = APIRouter(
    tags=["Organizations"],
    prefix="/organizations",
)

@router.post("/", response_description="Create new organization", status_code=status.HTTP_201_CREATED, response_model=OrganizationResponse)
async def create_organization(organization: OrganizationBaseModel = Body(...)):
    db = await connect_to_db()
    validate_db_connection(db)
    
    validate_string_fields(organization.name, organization.created_by, detail="All the field are required")
    
    try:
        user = await db.users.find_one({"_id": ObjectId(organization.created_by)})
        
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user ID")
    
        organization = OrganizationModel(**organization.dict())

        # Default access level for the creator of the organization is ADMIN
        access_level = get_access_level_enum("ADMIN")
        if access_level is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid access level. Valid access levels are: ADMIN, WRITE, READ"
            )
        
        organization.members.append({"user_id": ObjectId(organization.created_by), "access_level": access_level})
        
        result = await db.organizations.insert_one(organization.dict())
        
        # Add the organization to the user's organizations list
        await db.users.find_one_and_update({"_id": ObjectId(organization.created_by)}, {"$push": {"organizations": ObjectId(result.inserted_id)}})
        return await db.organizations.find_one({ "_id": result.inserted_id })
    
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Organization already exists")
    
    except ConnectionFailure:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create organization."
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
                        
        if result is None or len(result) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Organizations found"
            )
                        
        return {"total_count": total_count, "organizations": result}
    
    except ConnectionFailure:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get organizations."
        )
        
@router.get("/{id_or_name}", response_description="Get a single organization", status_code=status.HTTP_200_OK, response_model=OrganizationResponse)
async def get_organization(id_or_name: str):
    db = await connect_to_db()
    validate_db_connection(db)
    
    if(ObjectId.is_valid(id_or_name)):
        query = {"_id": ObjectId(id_or_name)}
    else:
        query = {"name": id_or_name}
        
    try:
        result = await db.organizations.find_one(query)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
        return result

    except ConnectionFailure:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get organization."
        )
        
@router.post("/{organization_id}/members/{author_id}", response_description="Add a member to an organization", status_code=status.HTTP_200_OK, response_model=OrganizationResponse)
async def add_user_to_organization(organization_id: str, author_id: str,  member: AddMemberModel = Body(...)):
    db = await connect_to_db()
    validate_db_connection(db)
    
    user_id, access_level = member.user_id, member.access_level
    
    validate_string_fields(organization_id, author_id, user_id, detail="All the fields are required")
    validate_organization_role(access_level)
    
    try:
        # Check if the organization exists
        organization = await db.organizations.find_one({"_id": ObjectId(organization_id)})
        if not organization:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
        
        # Check if the user exists
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Check if the author is a ADMIN of the organization
        is_admin = await db.organizations.find_one({"_id": ObjectId(organization_id), "members": {"$elemMatch": {"user_id": ObjectId(author_id), "access_level": "ADMIN"}}})
        if is_admin is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Author is not an ADMIN of the organization")
        
        # Check if the user is already a member of the organization
        is_member = await db.organizations.find_one({"_id": ObjectId(organization_id), "members": {"$elemMatch": {"user_id": ObjectId(user_id)}}})
        if is_member:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists in the organization")
        
        access_level = get_access_level_enum(access_level)
        if access_level is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid access level. Valid access levels are: ADMIN, WRITE, READ"
            )
            
        member = MemberPermissionModel(**({"user_id": ObjectId(user_id), "access_level": access_level}))
        
        await db.organizations.find_one_and_update(
            {"_id": ObjectId(organization_id)},
            {"$push": {"members": member.dict()}}
        )
        
        # Add the organization to the user's organizations list
        await db.users.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$push": {"organizations": ObjectId(organization_id)}}
        )
        
        return await db.organizations.find_one({"_id": ObjectId(organization_id)})
    
    except ConnectionFailure:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add user to organization."
        )
        
@router.patch("/{organization_id}/members/{author_id}", response_description="Update a member's access level", status_code=status.HTTP_200_OK, response_model=OrganizationResponse)
async def update_user_access_level(organization_id: str, author_id: str, member: UpdateMemberModel = Body(...)):
    db = await connect_to_db()
    validate_db_connection(db)
    
    user_id, access_level = member.user_id, member.access_level
    
    validate_string_fields(organization_id, author_id, user_id, detail="All the fields are required")
    validate_organization_role(access_level)
    
    try:
        # Check if the organization exists
        organization = await db.organizations.find_one({"_id": ObjectId(organization_id)})
        if not organization:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
        
        # Check if the author is a ADMIN of the organization
        is_admin = await db.organizations.find_one({"_id": ObjectId(organization_id), "members": {"$elemMatch": {"user_id": ObjectId(author_id), "access_level": "ADMIN"}}})
        if is_admin is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Author is not an ADMIN of the organization")
        
        # Check if the user is already a member of the organization
        is_member = await db.organizations.find_one({"_id": ObjectId(organization_id), "members": {"$elemMatch": {"user_id": ObjectId(user_id)}}})
        if is_member is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist in the organization")
        
        access_level = get_access_level_enum(access_level)
        if access_level is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid access level. Valid access levels are: ADMIN, WRITE, READ"
            )
            
        await db.organizations.find_one_and_update(
            {"_id": ObjectId(organization_id), "members.user_id": ObjectId(user_id)},
            {"$set": {"members.$.access_level": access_level}}
        )
        
        return await db.organizations.find_one({"_id": ObjectId(organization_id)})
    
    except ConnectionFailure:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user access level."
        )

@router.delete("/{organization_id}/members/{author_id}", response_description="Remove a member from an organization", status_code=status.HTTP_200_OK, response_model=OrganizationResponse)
async def remove_user_from_organization(organization_id: str, author_id: str, member: RemoveMemberModel = Body(...)):
    db = await connect_to_db()
    validate_db_connection(db)
    
    user_id = member.user_id
    
    validate_string_fields(organization_id, author_id, user_id, detail="All the fields are required")
    
    try:
        # Check if the organization exists
        organization = await db.organizations.find_one({"_id": ObjectId(organization_id)})
        if not organization:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
        
        # Security check - Check if the member is the person who created the organization
        is_creator = organization["created_by"] == ObjectId(user_id)
        if is_creator:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot remove the creator of the organization")
        
        # Check if the author is a ADMIN of the organization
        is_admin = await db.organizations.find_one({"_id": ObjectId(organization_id), "members": {"$elemMatch": {"user_id": ObjectId(author_id), "access_level": "ADMIN"}}})
        if is_admin is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Author is not an ADMIN of the organization")
        
        # Check if the user is a member of the organization
        is_member = await db.organizations.find_one({"_id": ObjectId(organization_id), "members": {"$elemMatch": {"user_id": ObjectId(user_id)}}})
        if is_member is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist in the organization")
        
        await db.organizations.find_one_and_update(
            {"_id": ObjectId(organization_id)},
            {"$pull": {"members": {"user_id": ObjectId(user_id)}}}
        )
        
        # Remove the organization from the user's organizations list
        await db.users.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$pull": {"organizations": ObjectId(organization_id)}}
        )
        
        return await db.organizations.find_one({"_id": ObjectId(organization_id)})
    
    except ConnectionFailure:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove user from organization."
        )