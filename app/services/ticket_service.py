
from typing import Optional
from app.repositories.ticket_repository import TicketRepository
from app.models.ticket import Ticket
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4 as uuid
class TicketService:
    def __init__(self,db: AsyncSession):
        self.repo  = TicketRepository(db)
    async def get_ticket(self, ticket_id: Optional[str] = None, priority: Optional[str] = None,isOpen:Optional[bool]=None):

        if ticket_id:
           ticket =await self.repo.get_ticket_by_id(ticket_id,priority,isOpen)
           if ticket is None:
               raise HTTPException(status_code=404, detail="Ticket not found")
           if priority is not None and ticket.priority != priority:
                 raise HTTPException(status_code=404, detail="Ticket not found")
           if isOpen is not None and ticket.isOpen != isOpen:
                 raise HTTPException(status_code=404, detail="Ticket not found")

           return ticket
        priority_tickets = []
        isOpen_tickets = []
        
        if priority:
            priority_tickets=await self.repo.get_all_tickets(priority,isOpen)
        if isOpen is not None:
            isOpen_tickets= await self.repo.get_all_tickets(priority,isOpen)
        if priority and isOpen is not None:
            
            return priority_tickets+isOpen_tickets
        if priority and priority_tickets is not None:
            return priority_tickets
        if isOpen is not None and isOpen_tickets is not None:
            return isOpen_tickets
        t=await self.repo.get_all_tickets(priority,isOpen)
        return t
        
        
        
        

    async def create_ticket(self, ticket_data):
        id = str(uuid())
        if ticket_data.title is None:
            raise HTTPException(status_code=422, detail="Title cannot be null")   
        
        ticket = Ticket(
            id=id,
            title=ticket_data.title,
            description=ticket_data.description,
            priority=ticket_data.priority,
            isOpen=ticket_data.isOpen,
            email=ticket_data.email
        )
        created_ticket = await self.repo.create_ticket(ticket)
        return created_ticket
    async def update_ticket(self, ticket_id, ticket_data):
         ticket=self.get_ticket(ticket_id)
         if ticket:
             updates = ticket_data.model_dump(exclude_unset=True)
             updated_ticket = await self.repo.update_ticket(ticket_id, updates)
         else:  
             raise HTTPException(status_code=404,detail="Ticket not found")
         return updated_ticket
    async def delete_ticket(self,ticket_id):
        ticket=self.get_ticket(ticket_id)
        if not  ticket:
             raise HTTPException(status_code=404,detail="Ticket not Found")
        else:
            deleted = await self.repo.delete_ticket(
            ticket_id)
            if not deleted:
             raise HTTPException(
                status_code=400,
                detail="An Error Occurred"
            )
        
               

         
        
        
        
        
         

        
               
        
 




      

