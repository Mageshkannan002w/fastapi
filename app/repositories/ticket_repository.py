
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Ticket
from datetime import datetime, timezone

from app.schemas.ticket import PriorityEnum

class TicketRepository:
    def __init__(self,db:AsyncSession):
        self.db=db
    async def get_ticket_by_id(self,ticket_id:UUID,priority:PriorityEnum =None,isOpen:bool| None=None) -> Ticket | None:
         q = select(Ticket).where(Ticket.id == ticket_id,Ticket.is_deleted==False)
         
         if priority is not None:
             q=q.where(Ticket.priority==priority)
         if isOpen is not None:
             q=q.where(Ticket.isOpen==isOpen)
         result=await self.db.execute(q)
         return result.scalar_one_or_none()
    async def get_all_tickets(self,priority:PriorityEnum | None,isOpen:bool| None) -> list[Ticket]:
        q=select(Ticket).where(Ticket.is_deleted==False)
        if priority is not None:
            q=q.where(Ticket.priority==priority)
        if isOpen is not None:
            q=q.where(Ticket.isOpen==isOpen)
        result=await self.db.execute(q)
        return result.scalars().all()
    async def create_ticket(self,ticket:Ticket) -> Ticket:
        self.db.add(ticket)
        await self.db.flush()
        await self.db.refresh(ticket)
        return ticket

    async def update_ticket(self, ticket_id: UUID,update_data:dict) -> Ticket | None:
        ticket = await self.get_ticket_by_id(ticket_id)
        if not ticket:
            return None
        for key, value in update_data.items():
            if hasattr(ticket, key):
                setattr(ticket, key, value)
        ticket.updated_at = datetime.now(timezone.utc)
        await self.db.flush()
        await self.db.refresh(ticket)
        return ticket
    async def delete_ticket(self, ticket_id: UUID) -> bool:
        ticket = await self.get_ticket_by_id(ticket_id)
        if not ticket:
            return False
        ticket.is_deleted = True
        ticket.deleted_at = datetime.now(timezone.utc)
        await self.db.flush()
        return True
    
             
        


