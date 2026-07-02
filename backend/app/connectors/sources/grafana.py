from typing import Dict, Any
from app.connectors.base import SourceConnector

class GrafanaSourceConnector(SourceConnector):
    
    def parse_alert(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        alerts = payload.get('alerts', [])
        if not alerts:
            return {}
            
        first_alert = alerts[0]
        labels = first_alert.get('labels', {})
        
        return {
            "alert_name": labels.get('alertname', 'Unknown Alert'),
            "severity": labels.get('severity', 'critical'),
            "source": "grafana",
            "instance": labels.get('instance', 'unknown'),
            "triggered_at": first_alert.get('startsAt'),
            "raw_payload": payload
        }

    async def get_logs(self, context: Dict[str, Any], window_minutes: int = 15) -> str:
        # Implementation to fetch from Loki API
        return "Log context: (dummy logs from Grafana/Loki for MVP)"
        
    async def get_metrics(self, context: Dict[str, Any], window_minutes: int = 15) -> str:
        # Implementation to fetch from Grafana Data Source API
        return "Metrics context: (dummy metrics from Grafana API for MVP)"
