from pydantic import BaseModel, Field
class SummarizeRequest(BaseModel):
    ticket_description: str = Field(min_length=10, max_length=5_000)
 
 
class SummarizeResponse(BaseModel):
    summary: str
    suggested_response: str