import httpx
import json
from typing import Dict, Any, List
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class AIAnalyzer:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = settings.OPENROUTER_BASE_URL
        self.default_model = settings.DEFAULT_MODEL
        self.fallback_models = settings.FALLBACK_MODELS
        
        self.system_prompt = """
You are an expert SRE / on-call assistant. Your task is to analyze monitoring alerts, logs, and metrics context to provide structured incident response insights.
Return ONLY a valid JSON object matching this schema, without markdown formatting or other text:
{
    "root_cause": "Detailed explanation of the likely root cause",
    "evidence": "Specific evidence from logs/metrics supporting the root cause",
    "remediation": "Step-by-step actionable remediation steps for the on-call engineer",
    "urgency": "critical|high|medium|low"
}

Do not hallucinate data that is not in the provided context. If data is missing, mention what needs to be checked manually in the remediation section.
"""

    async def _call_openrouter(self, model: str, prompt: str) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "AIOps Assistant",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"}
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60.0
            )
            response.raise_for_status()
            data = response.json()
            content = data['choices'][0]['message']['content']
            # Some models might return markdown code block even when asked not to
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:-3].strip()
            return json.loads(content)

    async def analyze_incident(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Analyze the following incident context:\n\n{json.dumps(incident_data, indent=2)}"
        
        models_to_try = [self.default_model] + self.fallback_models
        
        for model in models_to_try:
            try:
                logger.info(f"Attempting analysis with model {model}...")
                result = await self._call_openrouter(model, prompt)
                logger.info(f"Successfully analyzed incident with model {model}")
                return result
            except Exception as e:
                logger.warning(f"Model {model} failed: {str(e)}. Trying next model if available...")
                
        # If all models fail
        logger.error("All OpenRouter models failed to provide an analysis.")
        return {
            "root_cause": "AI Analysis Failed. Please check logs manually.",
            "evidence": "N/A",
            "remediation": "1. Manually review logs and metrics.\n2. Check AI Engine API status and limits.",
            "urgency": str(incident_data.get('severity', 'high')).lower()
        }

analyzer_service = AIAnalyzer()
