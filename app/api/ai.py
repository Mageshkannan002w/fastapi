from fastapi import APIRouter, Depends, HTTPException, status
 
from app.schemas.ai import SummarizeRequest, SummarizeResponse
from app.services.aws_bedrock_service import (
    BedrockService,
    BedrockServiceError,
    FakeBedrockService,
)
 
 
router = APIRouter(prefix="/ai", tags=["AI"])
def get_bedrock_service() -> BedrockService:
    return BedrockService()
 
@router.post("/summarize", response_model=SummarizeResponse)
def summarize_ticket(
    payload: SummarizeRequest,
    service: BedrockService | FakeBedrockService=Depends(get_bedrock_service)
) :
    try:
        return service.summarize_ticket(payload.ticket_description)
    except BedrockServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The AI service is temporarily unavailable",
        ) from exc