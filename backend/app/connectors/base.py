from abc import ABC, abstractmethod
from typing import Dict, Any

class SourceConnector(ABC):
    """Interface for monitoring sources (Grafana, Zabbix, Wazuh)"""
    
    @abstractmethod
    def parse_alert(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize the incoming webhook payload to a standard Incident dict"""
        pass
        
    @abstractmethod
    async def get_logs(self, context: Dict[str, Any], window_minutes: int = 15) -> str:
        """Fetch logs from the source around the incident time"""
        pass
        
    @abstractmethod
    async def get_metrics(self, context: Dict[str, Any], window_minutes: int = 15) -> str:
        """Fetch metrics/trends from the source around the incident time"""
        pass

class ChannelConnector(ABC):
    """Interface for notification channels (Teams, Telegram, WA, GLPI)"""
    
    @abstractmethod
    async def send_message(self, incident: Dict[str, Any], analysis: Dict[str, Any], config: Dict[str, Any]) -> bool:
        """Send incident details and AI analysis to the channel"""
        pass
