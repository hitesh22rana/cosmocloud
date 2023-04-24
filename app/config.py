from pydantic import BaseSettings

"""
Settings for the application are defined here i.e. environment variables
"""
class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_name: str

    class Config:
        env_file = ".env"

settings = Settings()