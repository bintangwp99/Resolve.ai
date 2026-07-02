# Resolve.ai

Resolve.ai is a plugin-based system to receive alerts from monitoring tools (Grafana, Zabbix, Wazuh), gather contextual data (logs, metrics), analyze the root cause using an LLM (OpenRouter), and forward the analysis to notification channels (Teams, Telegram, WhatsApp, GLPI).

## Features
- **Plugin Architecture**: Easily add new `SourceConnector` or `ChannelConnector`.
- **AI Analysis**: Uses OpenRouter API with fallback support (e.g. `openai/gpt-oss-120b:free` -> `google/gemini-1.5-pro`).
- **Web UI**: Manage configurations, view incidents, and chat with the AI manually.
- **Security**: JWT-based authentication, RBAC, and encrypted configuration storage.

## Setup Instructions

### 1. Environment Variables
Create a `.env` file in the `backend` directory based on `.env.example`:
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
SECRET_KEY=CHANGE_THIS_SECRET_KEY
```

### 2. Running Locally with Docker Compose
```bash
docker-compose up --build
```
- Backend API is accessible at `http://localhost:8000`
- Frontend UI is accessible at `http://localhost:5173`

### 3. Dummy Payloads for Testing

You can simulate alerts without setting up actual monitoring tools using `curl`.

#### Test Grafana Webhook
```bash
curl -X POST http://localhost:8000/api/v1/webhooks/grafana \
-H "Content-Type: application/json" \
-d '{
  "alerts": [
    {
      "status": "firing",
      "labels": {
        "alertname": "High CPU Usage",
        "severity": "critical",
        "instance": "db-server-01",
        "job": "node_exporter"
      },
      "annotations": {
        "summary": "CPU usage is above 90%",
        "description": "CPU usage on db-server-01 has been above 90% for the last 5 minutes."
      },
      "startsAt": "2026-07-02T10:00:00Z"
    }
  ]
}'
```

#### Test Zabbix Webhook
```bash
curl -X POST http://localhost:8000/api/v1/webhooks/zabbix \
-H "Content-Type: application/json" \
-d '{
  "EventName": "Memory usage > 90%",
  "EventSeverity": "High",
  "Host": "web-server-02",
  "EventTime": "2026-07-02T10:05:00Z"
}'
```

#### Test Wazuh Webhook
```bash
curl -X POST http://localhost:8000/api/v1/webhooks/wazuh \
-H "Content-Type: application/json" \
-d '{
  "rule": {
    "level": 12,
    "description": "Multiple failed login attempts",
    "id": "5710"
  },
  "agent": {
    "name": "auth-gateway"
  },
  "timestamp": "2026-07-02T10:10:00+0000",
  "full_log": "Jul  2 10:10:00 auth-gateway sshd[1234]: Failed password for invalid user admin from 192.168.1.100 port 55555 ssh2"
}'
```

## Connector Configuration

Access the web UI at `http://localhost:5173` and go to **Settings** to add your channel credentials (e.g. Telegram Bot Token, Twilio Account SID, GLPI URL & Tokens). The application will dynamically use these settings when an incident occurs.
