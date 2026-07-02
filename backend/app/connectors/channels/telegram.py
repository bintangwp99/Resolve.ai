import httpx
import logging
from typing import Dict, Any
from app.connectors.base import ChannelConnector

logger = logging.getLogger(__name__)

class TelegramChannelConnector(ChannelConnector):
    
    async def send_message(self, incident: Dict[str, Any], analysis: Dict[str, Any], config: Dict[str, Any]) -> bool:
        bot_token = config.get("bot_token")
        chat_id = config.get("chat_id")
        
        if not bot_token or not chat_id:
            logger.error("Telegram bot_token or chat_id not configured")
            return False
            
        message = (
            f"🚨 *Incident Alert*\n"
            f"Name: {incident.get('alert_name')}\n"
            f"Severity: {incident.get('severity')}\n"
            f"Source: {incident.get('source')}\n\n"
            f"🔍 *Analysis*\n"
            f"Root Cause: {analysis.get('root_cause')}\n"
            f"Remediation: {analysis.get('remediation')}"
        )
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"})
                resp.raise_for_status()
                return True
            except Exception as e:
                logger.error(f"Failed to send Telegram message: {str(e)}")
                return False
