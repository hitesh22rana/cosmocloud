from bson import ObjectId
from enum import Enum

"""
JSON Friendly ObjectId
"""
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

"""
Access level for an organization member (Enum)
"""
class AccessLevel(str, Enum):
    READ = "READ"
    WRITE = "WRITE"
    ADMIN = "ADMIN"