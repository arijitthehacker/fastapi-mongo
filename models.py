
from bson import ObjectId
from pydantic import BaseModel

class BaseItem(BaseModel):
    _id: ObjectId
    name: str
    description: str

class CreateItem(BaseItem):
    pass

class ReadItem(BaseItem):
    pass

class UpdateItem(BaseItem):
    pass

class DeleteItem(BaseModel):
    _id: ObjectId