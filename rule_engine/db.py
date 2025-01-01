from pydantic import BaseModel, EmailStr, ValidationError

from motor.motor_asyncio import AsyncIOMotorClient


# MongoDB setup
mongo_client = AsyncIOMotorClient("mongodb://aveen:mops@mongo:27017/iot_db?authSource=admin")

db = mongo_client.iot_db  # Specify the database
instant= db.instant
ongoing=db.ongoing
# Data model for validation
class IoTData(BaseModel):
    device_id: str
    name: str
    email: EmailStr
    age: int
    x_factor: float
