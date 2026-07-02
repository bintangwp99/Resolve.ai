import httpx
import logging
from typing import Dict, Any
from app.connectors.base import ChannelConnector

logger = logging.getLogger(__name__)

class GLPIChannelConnector(ChannelConnector):
    
    async def send_message(self, incident: Dict[str, Any], analysis: Dict[str, Any], config: Dict[str, Any]) -> bool:
        api_url = config.get("api_url")
        app_token = config.get("app_token")
        user_token = config.get("user_token")
        
        if not all([api_url, app_token, user_token]):
            logger.error("GLPI config missing")
            return False
            
        headers = {
            "App-Token": app_token,
            "Authorization": f"user_token {user_token}"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                session_resp = await client.get(f"{api_url}/initSession", headers=headers)
                session_resp.raise_for_status()
                session_token = session_resp.json().get("session_token")
                
                ticket_headers = {
                    "App-Token": app_token,
                    "Session-Token": session_token,
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "input": {
                        "name": f"Incident: {incident.get('alert_name')}",
                        "content": f"Severity: {incident.get('severity')}<br>Root Cause: {analysis.get('root_cause')}<br>Remediation: {analysis.get('remediation')}",
                        "status": 1, # New
                        "urgency": 4 if str(analysis.get('urgency')).lower() == 'critical' else 3
                    }
                }
                
                ticket_resp = await client.post(f"{api_url}/Ticket", headers=ticket_headers, json=payload)
                ticket_resp.raise_for_status()
                return True
            except Exception as e:
                logger.error(f"Failed to create GLPI ticket: {str(e)}")
                return False
