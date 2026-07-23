from typing import Optional, Any
from app.repositories.ticket_repository import TicketRepository
from app.models.ticket import Ticket
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4 as uuid
from uuid import UUID


class TicketService:
    def __init__(self, db: Optional[AsyncSession] = None, repo: Optional[Any] = None):
        if repo is not None:
            self.repo = repo
        elif db is not None and not isinstance(db, AsyncSession):
            self.repo = db
        elif db is not None:
            self.repo = TicketRepository(db)
        else:
            self.repo = None

    async def get_ticket(self, ticket_id: Optional[UUID] = None, priority: Optional[str] = None, isOpen: Optional[bool] = None):
        if ticket_id:
            ticket = await self.repo.get_ticket_by_id(ticket_id, priority, isOpen)
            if ticket is None:
                raise ValueError("Ticket not found")
            if priority is not None and ticket.priority != priority:
                raise ValueError("Ticket not found")
            if isOpen is not None and ticket.isOpen != isOpen:
                raise ValueError("Ticket not found")

            return ticket

        priority_tickets = []
        isOpen_tickets = []

        if priority:
            priority_tickets = await self.repo.get_all_tickets(priority, isOpen)
        if isOpen is not None:
            isOpen_tickets = await self.repo.get_all_tickets(priority, isOpen)
        if priority and isOpen is not None:
            return priority_tickets + isOpen_tickets
        if priority and priority_tickets is not None:
            return priority_tickets
        if isOpen is not None and isOpen_tickets is not None:
            return isOpen_tickets
        t = await self.repo.get_all_tickets(priority, isOpen)
        return t

    async def create_ticket(self, ticket_data):
        if not ticket_data:
            raise ValueError("Ticket data is required")
        if not getattr(ticket_data, "title", None) or not str(ticket_data.title).strip():
            raise ValueError("Title cannot be empty")
        if not getattr(ticket_data, "description", None) or not str(ticket_data.description).strip():
            raise ValueError("Description cannot be empty")
        if not getattr(ticket_data, "email", None) or not str(ticket_data.email).strip():
            raise ValueError("Email cannot be empty")

        id = str(uuid())

        ticket = Ticket(
            id=id,
            title=ticket_data.title,
            description=ticket_data.description,
            priority=ticket_data.priority,
            isOpen=ticket_data.isOpen,
            email=ticket_data.email
        )
        created_ticket = await self.repo.create_ticket(ticket)
        if created_ticket is None:
            raise ValueError("Failed to create ticket")
        return created_ticket

    async def update_ticket(self, ticket_id, ticket_data):
        if not ticket_id:
            raise ValueError("Ticket ID is required")
        ticket = await self.get_ticket(ticket_id)
        if ticket:
            updates = ticket_data.model_dump(exclude_unset=True)
            updated_ticket = await self.repo.update_ticket(ticket_id, updates)
        else:
            raise ValueError("Ticket not found")
        return updated_ticket

    async def delete_ticket(self, ticket_id):
        if not ticket_id:
            raise ValueError("Ticket ID is required")
        ticket = await self.get_ticket(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")
        else:
            deleted = await self.repo.delete_ticket(ticket_id)
            if not deleted:
                raise ValueError("An Error Occurred")
            return deleted
