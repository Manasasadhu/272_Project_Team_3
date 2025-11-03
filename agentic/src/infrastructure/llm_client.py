"""LLM client wrapper"""
from openai import OpenAI
from infrastructure.config import config
from infrastructure.exceptions import AgentExecutionError

class LLMClient:
    """OpenAI LLM client"""
    
    def __init__(self):
        self.api_key = config.OPENAI_API_KEY
        self.model = config.LLM_MODEL
        self.client = None
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            import warnings
            warnings.warn("OPENAI_API_KEY not configured. LLM operations will fail.")
    
    def _ensure_configured(self):
        """Ensure API key is configured"""
        if not self.api_key or not self.client:
            raise AgentExecutionError("OPENAI_API_KEY not configured")
    
    def generate_completion(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """Generate completion from prompt"""
        self._ensure_configured()
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise AgentExecutionError(f"LLM API error: {e}")
    
    def generate_json(self, prompt: str, temperature: float = 0.3) -> dict:
        """Generate JSON response"""
        self._ensure_configured()
        json_prompt = f"{prompt}\n\nRespond in valid JSON format only."
        response = self.generate_completion(json_prompt, temperature, max_tokens=3000)
        try:
            import json
            return json.loads(response)
        except:
            # Fallback: try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            raise AgentExecutionError("Failed to parse JSON response")

