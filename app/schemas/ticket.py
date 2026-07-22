

import enum
from pydantic import BaseModel,ConfigDict
from typing import Optional
from sqlalchemy import  Enum
from uuid import UUID
class PriorityEnum(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
class TicketCreate(BaseModel):
    
    title: str
    description: str
    priority: PriorityEnum= PriorityEnum.LOW
    isOpen:bool=True
    email: str
    

class TicketCreateResponse(BaseModel):
    ticket_id: str
    status: int
    message: str
     
class TicketResponse(BaseModel):
    id: UUID
    title: str
    description: str
    priority: PriorityEnum
    isOpen: bool
    email: str
    model_config = ConfigDict(from_attributes=True)
class TicketGetResponse(BaseModel):
    status: int
    message: str
    ticket: Optional[list[TicketResponse] | TicketResponse] = None
class TicketUpdate(BaseModel):
    title: str = None
    description: str = None
    priority: PriorityEnum = None

class TicketUpdateData(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    isOpen: Optional[bool] = None
class TicketUpdateResponse(BaseModel):
    ticket_id: str
    status: int
    message: str
class TicketDelete(BaseModel):
    ticket_id: str
class TicketDeleteResponse(BaseModel):
    ticket_id: str
    status: int
    message: str



