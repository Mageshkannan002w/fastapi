from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.ticket import TicketCreateResponse, TicketDeleteResponse, TicketUpdateResponse, TicketCreate, TicketGetResponse, TicketUpdateData
from app.services.ticket_service import TicketService

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("/")
async def create_ticket(ticket_data: TicketCreate, db: AsyncSession = Depends(get_db)):
    ticket_service = TicketService(db)
    created_ticket = await ticket_service.create_ticket(ticket_data)
    return TicketCreateResponse(
        ticket_id=str(created_ticket.id),
        status=201,
        message="Ticket created successfully",
    )


@router.get("/get_tickets", response_model=TicketGetResponse)
async def get_ticket(db: AsyncSession = Depends(get_db), ticket_id: Optional[UUID] = None, priority: Optional[str] = None, isOpen: Optional[bool] = None):
    ticket_service = TicketService(db)
    try:
        ticket = await ticket_service.get_ticket(ticket_id, priority, isOpen)

        if ticket is None:
            raise HTTPException(status_code=404, detail="Ticket not found")
        if ticket:
            return TicketGetResponse(
                status=200,
                message="Tickets found successfully",
                ticket=ticket
            )
        return TicketGetResponse(
            status=200,
            message="Ticket fetched successfully no records found",
            ticket=[]
        )
    except (HTTPException, ValueError) as e:
        detail = getattr(e, "detail", str(e))
        return TicketGetResponse(
            ticket_id=ticket_id,
            status=404,
            message=detail,
            ticket=None
        )


@router.put("/update", response_model=TicketUpdateResponse)
async def update_ticket(ticket_id: UUID, ticket_data: TicketUpdateData, db: AsyncSession = Depends(get_db)):
    ticket_service = TicketService(db)
    try:
        await ticket_service.update_ticket(ticket_id, ticket_data)
        return TicketUpdateResponse(
            ticket_id=ticket_id,
            status=200,
            message="Ticket updated successfully",
        )
    except (HTTPException, ValueError) as e:
        detail = getattr(e, "detail", str(e))
        return TicketUpdateResponse(
            ticket_id=ticket_id,
            status=404,
            message=detail,
            priority=None
        )


@router.delete("/delete", response_model=TicketDeleteResponse)
async def delete_ticket(ticket_id: UUID, db: AsyncSession = Depends(get_db)):
    ticket_service = TicketService(db)
    try:
        await ticket_service.delete_ticket(ticket_id)
        return TicketDeleteResponse(
            ticket_id=ticket_id,
            status=200,
            message="Ticket deleted successfully"
        )
    except (HTTPException, ValueError) as e:
        detail = getattr(e, "detail", str(e))
        return TicketDeleteResponse(
            ticket_id=ticket_id,
            status=404,
            message=detail
        )
