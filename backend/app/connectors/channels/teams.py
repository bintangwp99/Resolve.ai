import httpx
import logging
from typing import Dict, Any
from app.connectors.base import ChannelConnector

logger = logging.getLogger(__name__)

class TeamsChannelConnector(ChannelConnector):
    
    async def send_message(self, incident: Dict[str, Any], analysis: Dict[str, Any], config: Dict[str, Any]) -> bool:
        webhook_url = config.get("webhook_url")
        if not webhook_url:
            logger.error("Teams webhook_url not configured")
            return False
            
        payload = {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": {
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "AdaptiveCard",
                        "version": "1.2",
                        "body": [
                            {
                                "type": "TextBlock",
                                "text": f"Incident: {incident.get('alert_name')}",
                                "weight": "Bolder",
                                "size": "Medium"
                            },
                            {
                                "type": "FactSet",
                                "facts": [
                                    {"title": "Severity:", "value": incident.get('severity')},
                                    {"title": "Source:", "value": incident.get('source')},
                                    {"title": "Root Cause:", "value": analysis.get('root_cause', 'N/A')},
                                    {"title": "Urgency:", "value": analysis.get('urgency', 'N/A')}
                                ]
                            }
                        ]
                    }
                }
            ]
        }
        
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(webhook_url, json=payload)
                resp.raise_for_status()
                return True
            except Exception as e:
                logger.error(f"Failed to send Teams message: {str(e)}")
                return False
