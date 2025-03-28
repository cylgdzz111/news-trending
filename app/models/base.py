from datetime import datetime
from typing import Any, Optional, Annotated, ClassVar
from bson import ObjectId
from pydantic import BaseModel, Field, BeforeValidator
from pydantic.json_schema import JsonSchemaValue


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_json_schema__(
        cls, _schema_generator, _field_schema
    ) -> JsonSchemaValue:
        return {"type": "string"}
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("无效的ObjectID")
        return ObjectId(v)


class MongoBaseModel(BaseModel):
    """MongoDB模型基类"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True,
        "json_encoders": {ObjectId: str}
    } 