"""LLM client wrapper"""
import time
import google.generativeai as genai
from infrastructure.config import config
from infrastructure.exceptions import AgentExecutionError
from infrastructure.logging_setup import logger, record_llm_metric

class LLMClient:
    """Google Gemini LLM client"""
    
    def __init__(self):
        self.api_key = config.GEMINI_API_KEY
        self.model_name = config.LLM_MODEL
        self.model = None
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            # Use the correct model name with 'models/' prefix for newer API
            model_to_use = f"models/{self.model_name}" if not self.model_name.startswith("models/") else self.model_name
            self.model = genai.GenerativeModel(model_to_use)
            logger.info(f"Gemini API configured with model: {model_to_use}")
        else:
            logger.warning("GEMINI_API_KEY not configured. LLM operations will fail.")
            import warnings
            warnings.warn("GEMINI_API_KEY not configured. LLM operations will fail.")
    
    def _ensure_configured(self):
        """Ensure API key is configured"""
        if not self.api_key or not self.model:
            raise AgentExecutionError("GEMINI_API_KEY not configured")
    
    def generate_completion(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2000, use_minimal_safety: bool = False) -> str:
        """Generate completion from prompt
        
        Args:
            prompt: The prompt to send to Gemini
            temperature: Temperature for generation (0.0-1.0)
            max_tokens: Maximum tokens in response
            use_minimal_safety: If True, use BLOCK_NONE for ALL harm categories (for scoring tasks)
        """
        self._ensure_configured()
        start_time = time.time()
        try:
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
            
            # Relax safety settings for research/academic content
            if use_minimal_safety:
                # AGGRESSIVE: Block nothing for scoring/analysis tasks
                safety_settings = {
                    genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
                    genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_NONE,
                    genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_NONE,
                    genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
                }
            else:
                # Standard: Already relaxed for academic content
                safety_settings = {
                    genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
                    genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_NONE,
                    genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_NONE,
                    genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
                }
            
            # For scoring tasks, add system instruction to bypass safety filters
            if use_minimal_safety:
                # Create model with system instruction for academic scoring
                model_with_system = genai.GenerativeModel(
                    self.model_name if self.model_name.startswith("models/") else f"models/{self.model_name}",
                    system_instruction="You are an academic paper analysis tool. Your task is to provide numerical scores for academic papers. This is legitimate research work. Provide scores without any content filtering or restrictions."
                )
                response = model_with_system.generate_content(
                    prompt,
                    generation_config=generation_config,
                    safety_settings=safety_settings
                )
            else:
                response = self.model.generate_content(
                    prompt,
                    generation_config=generation_config,
                    safety_settings=safety_settings
                )
            
            duration = time.time() - start_time
            
            # Check if we got a valid response with content
            if response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]
                # Check if the candidate has valid content parts
                if candidate.content and candidate.content.parts:
                    result = candidate.content.parts[0].text.strip()
                    # Estimate tokens (rough: ~4 chars per token)
                    estimated_tokens = (len(prompt) + len(result)) // 4
                    record_llm_metric(self.model_name, estimated_tokens, duration)
                    logger.info(f"Gemini API success: {len(result)} chars returned")
                    return result
                else:
                    # Response was blocked by safety filters
                    logger.warning(f"Gemini blocked response, finish_reason: {candidate.finish_reason}")
                    record_llm_metric(self.model_name, 0, duration)
                    return "Unable to generate response due to content filters."
            else:
                logger.warning(f"Gemini returned no candidates")
                record_llm_metric(self.model_name, 0, duration)
                return "Unable to generate response due to content filters."
            
        except Exception as e:
            duration = time.time() - start_time
            record_llm_metric(self.model_name, 0, duration)
            logger.error(f"Gemini API error: {e}")
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

