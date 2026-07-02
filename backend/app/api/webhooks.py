from fastapi import APIRouter, Depends, Request, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.incident_service import process_incoming_alert

router = APIRouter()

@router.post("/{source_name}")
async def receive_webhook(source_name: str, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    payload = await request.json()
    
    # Process in background to avoid blocking the webhook sender
    background_tasks.add_task(process_incoming_alert, source_name, payload, db)
    
    return {"status": "accepted", "message": f"Alert from {source_name} queued for processing"}
