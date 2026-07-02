import logging
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.models.incident import Incident
from app.models.connector_config import ConnectorConfig
from app.connectors.sources.grafana import GrafanaSourceConnector
from app.connectors.sources.zabbix import ZabbixSourceConnector
from app.connectors.sources.wazuh import WazuhSourceConnector
from app.connectors.channels.teams import TeamsChannelConnector
from app.connectors.channels.telegram import TelegramChannelConnector
from app.connectors.channels.whatsapp import WhatsAppChannelConnector
from app.connectors.channels.glpi import GLPIChannelConnector
from app.services.analyzer import analyzer_service

logger = logging.getLogger(__name__)

# Registry
SOURCE_CONNECTORS = {
    "grafana": GrafanaSourceConnector(),
    "zabbix": ZabbixSourceConnector(),
    "wazuh": WazuhSourceConnector()
}

CHANNEL_CONNECTORS = {
    "teams": TeamsChannelConnector(),
    "telegram": TelegramChannelConnector(),
    "whatsapp": WhatsAppChannelConnector(),
    "glpi": GLPIChannelConnector()
}

async def process_incoming_alert(source_name: str, payload: Dict[str, Any], db: Session):
    logger.info(f"Received alert from {source_name}")
    
    source = SOURCE_CONNECTORS.get(source_name)
    if not source:
        logger.error(f"Unknown source connector: {source_name}")
        return
        
    # 1. Parse Alert
    incident_data = source.parse_alert(payload)
    if not incident_data:
        return
        
    # 2. Get Context
    logs = await source.get_logs(incident_data)
    metrics = await source.get_metrics(incident_data)
    
    incident_data["logs_context"] = logs
    incident_data["metrics_context"] = metrics
    
    # 3. Analyze with AI
    analysis = await analyzer_service.analyze_incident(incident_data)
    
    # 4. Save to DB
    db_incident = Incident(
        alert_name=incident_data.get("alert_name"),
        severity=incident_data.get("severity"),
        source=incident_data.get("source"),
        instance=incident_data.get("instance"),
        raw_payload=incident_data.get("raw_payload"),
        logs_context=logs,
        metrics_context=metrics,
        root_cause=analysis.get("root_cause"),
        evidence=analysis.get("evidence"),
        remediation=analysis.get("remediation"),
        urgency=analysis.get("urgency"),
        delivery_status={}
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    
    # 5. Send to Channels
    active_channels = db.query(ConnectorConfig).filter(
        ConnectorConfig.connector_type == "channel",
        ConnectorConfig.is_active == True
    ).all()
    
    status = {}
    for ch_config in active_channels:
        ch_impl = CHANNEL_CONNECTORS.get(ch_config.name)
        if ch_impl:
            success = await ch_impl.send_message(incident_data, analysis, ch_config.credentials)
            status[ch_config.name] = "success" if success else "failed"
            
    db_incident.delivery_status = status
    db.commit()
    
    logger.info(f"Incident {db_incident.id} processed and sent to channels.")
