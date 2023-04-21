from fastapi import APIRouter, HTTPException, status, Body
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from .. lib.validators import validate_string_fields, validate_db_connection
from .. database import connect_to_db
from .. models.users import UserBaseModel, UserModel
from .. schemas.users import UserResponse, UsersResponse

router = APIRouter(
    tags=["Users"],
    prefix="/users",
)

@router.post("/", response_description="Create new user", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user: UserBaseModel = Body(...)):
    db = await connect_to_db()
    validate_db_connection(db)
    
    validate_string_fields(user.name, user.email, detail="Both name and email fields are required")
    
    try:
        user = UserModel(**user.dict())
        result = await db.users.insert_one(user.dict())
        return await db.users.find_one({ "_id": result.inserted_id })
    
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user. Error: {e}"
        )
        
@router.get("/", response_description="List all users", status_code=status.HTTP_200_OK, response_model=UsersResponse)
async def get_users(name: str = None, limit: int = 10, offset: int = 0):
    db = await connect_to_db()
    validate_db_connection(db)

    # Query parameters
    query = {}
    if name:
        query = {"name": {"$regex": name, "$options": "i"}}

    try:
        # Pagination
        total_count = await db.users.count_documents(query)
        result = await db.users\
                        .find(query)\
                        .skip(offset)\
                        .limit(limit)\
                        .to_list(length=limit)
                        
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No users found"
            )
                        
        return {"total_count": total_count, "users": result}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get users. Error: {e}"
        )
        
@router.get("/{user_id_or_email}", response_description="Get a single user", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(user_id_or_email: str):
    db = await connect_to_db()
    validate_db_connection(db)
    
    if(ObjectId.is_valid(user_id_or_email)):
        query = {"_id": ObjectId(user_id_or_email)}
    else:
        query = {"email": user_id_or_email}
    
    try:
        result = await db.users.find_one(query)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user. Error: {e}"
        )