import httpx
import logging
from typing import Dict, Any
from app.connectors.base import ChannelConnector

logger = logging.getLogger(__name__)

class WhatsAppChannelConnector(ChannelConnector):
    
    async def send_message(self, incident: Dict[str, Any], analysis: Dict[str, Any], config: Dict[str, Any]) -> bool:
        # MVP: Using Twilio API
        account_sid = config.get("account_sid")
        auth_token = config.get("auth_token")
        from_number = config.get("from_number")
        to_number = config.get("to_number")
        
        if not all([account_sid, auth_token, from_number, to_number]):
            logger.error("WhatsApp (Twilio) config missing")
            return False
            
        message = f"🚨 AIOps Alert: {incident.get('alert_name')}\nRoot Cause: {analysis.get('root_cause')}"
        
        url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
        
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    url, 
                    auth=(account_sid, auth_token),
                    data={"From": from_number, "To": to_number, "Body": message}
                )
                resp.raise_for_status()
                return True
            except Exception as e:
                logger.error(f"Failed to send WhatsApp message: {str(e)}")
                return False
