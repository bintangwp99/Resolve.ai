from typing import Dict, Any
from app.connectors.base import SourceConnector

class WazuhSourceConnector(SourceConnector):
    
    def parse_alert(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        rule = payload.get('rule', {})
        agent = payload.get('agent', {})
        
        return {
            "alert_name": rule.get('description', 'Unknown Wazuh Alert'),
            "severity": str(rule.get('level', 'high')),
            "source": "wazuh",
            "instance": agent.get('name', 'unknown'),
            "triggered_at": payload.get('timestamp'),
            "raw_payload": payload
        }

    async def get_logs(self, context: Dict[str, Any], window_minutes: int = 15) -> str:
        return f"Wazuh Full Log: {context.get('raw_payload', {}).get('full_log', 'N/A')}"
        
    async def get_metrics(self, context: Dict[str, Any], window_minutes: int = 15) -> str:
        return "Metrics context: Wazuh alerts typically do not have metrics."
