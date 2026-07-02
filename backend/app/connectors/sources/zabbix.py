from typing import Dict, Any
from app.connectors.base import SourceConnector

class ZabbixSourceConnector(SourceConnector):
    
    def parse_alert(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "alert_name": payload.get('EventName', 'Unknown Zabbix Alert'),
            "severity": payload.get('EventSeverity', 'High'),
            "source": "zabbix",
            "instance": payload.get('Host', 'unknown'),
            "triggered_at": payload.get('EventTime'),
            "raw_payload": payload
        }

    async def get_logs(self, context: Dict[str, Any], window_minutes: int = 15) -> str:
        return "Log context: (dummy logs from Zabbix for MVP)"
        
    async def get_metrics(self, context: Dict[str, Any], window_minutes: int = 15) -> str:
        return "Metrics context: (dummy metrics from Zabbix API for MVP)"
