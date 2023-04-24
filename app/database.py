from .config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

"""Environment Variables"""
DATABASE_HOSTNAME = settings.database_hostname
DATABASE_PORT = settings.database_port
DATABASE_NAME = settings.database_name

"""
Connect to MongoDB server and return database object
"""
db = None

async def connect_to_db():
    global db
    if db is not None:
        return db
    try:
        client = AsyncIOMotorClient(DATABASE_HOSTNAME, DATABASE_PORT)
        db = client[DATABASE_NAME]
        
        # Create unique index on email
        await db.users.create_index("email", unique=True)
        # Create unique index on name
        await db.organizations.create_index("name", unique=True)
        await db.organizations.create_index("created_by", unique=True)
        
        print(f"Connected to MongoDB server at {DATABASE_HOSTNAME}:{DATABASE_PORT}")
        return db
    except ConnectionFailure:
        print(f"Error connecting to MongoDB server at {DATABASE_HOSTNAME}:{DATABASE_PORT}")
        return None