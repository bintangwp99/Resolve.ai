from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from app.models.base import Base

class Incident(Base):
    id = Column(Integer, primary_key=True, index=True)
    alert_name = Column(String, index=True)
    severity = Column(String, index=True)
    source = Column(String, index=True)
    instance = Column(String, index=True)
    triggered_at = Column(DateTime, default=datetime.utcnow)
    
    raw_payload = Column(JSON, nullable=True)
    logs_context = Column(JSON, nullable=True)
    metrics_context = Column(JSON, nullable=True)
    
    root_cause = Column(String, nullable=True)
    evidence = Column(String, nullable=True)
    remediation = Column(String, nullable=True)
    urgency = Column(String, nullable=True)
    
    delivery_status = Column(JSON, nullable=True)
