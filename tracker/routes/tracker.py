from fastapi import FastAPI, HTTPException, Depends ,APIRouter,Request
from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime
from mongoengine.errors import ValidationError
from tracker.models import Event

router = APIRouter()
# Pydantic models
class EventCreate(BaseModel):
    eventType: str
    eventDetails: Dict[str, Optional[str]]
    timestamp: datetime
    user_id: str

@router.post("/")
def track_event(event: EventCreate, request: Request):
    user_agent = request.headers.get('User-Agent', 'Unknown')
    client_ip = request.client.host if request.client else 'Unknown'
    try:
        new_event = Event(
            event_type=event.eventType,
            event_details=event.eventDetails,
            timestamp=event.timestamp,
            user_id=event.user_id,
            device=user_agent,
            ip_address=client_ip
        )
        new_event.save()
        return {"message": "Event tracked successfully"}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))