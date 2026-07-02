from sqlalchemy import Column, Integer, String, Boolean, JSON
from app.models.base import Base

class ConnectorConfig(Base):
    __tablename__ = "connector_configs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    connector_type = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    credentials = Column(JSON, nullable=False)
