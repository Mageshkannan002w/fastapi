
from app.core import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime,timezone
from sqlalchemy import DateTime,Enum
import enum
from sqlalchemy.dialects.postgresql import UUID 
class Priority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

def utc_now() -> datetime:
    return datetime.now(timezone.utc)
class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[UUID] = mapped_column( UUID(as_uuid=True),primary_key=True, unique=True, nullable=False)
    title: Mapped[str]=mapped_column(nullable=False)
    description: Mapped[str]
    priority: Mapped[Priority] = mapped_column(Enum(Priority),default=Priority.LOW,nullable=False)
    email: Mapped[str]=mapped_column(nullable=False,unique=True)
    isOpen:Mapped[bool]=mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at:Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    is_deleted:Mapped[bool]=mapped_column(default=False)
    deleted_at:Mapped[datetime | None]=mapped_column(DateTime(timezone=True), default=None)

