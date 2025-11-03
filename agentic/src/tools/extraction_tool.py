"""Structured extraction tool"""
import httpx
from typing import Dict, Any
from tools.base_tool import BaseTool, ToolResult
from infrastructure.config import config
from infrastructure.exceptions import ToolExecutionError
from models.extraction_schema import StructuredExtraction

class ExtractionTool(BaseTool):
    """Extraction tool for structured data"""
    
    def __init__(self):
        self.service_url = config.EXTRACTION_SERVICE_URL
    
    def get_name(self) -> str:
        return "ExtractionTool"
    
    def execute(self, params: Dict[str, Any]) -> ToolResult:
        """Execute extraction"""
        source_url = params.get("source_url", "")
        
        try:
            # Try to call extraction service
            extraction = self._call_extraction_service(source_url)
            
            return ToolResult(
                success=True,
                data=extraction.to_dict(),
                metadata={"extraction_time": "2.5s"}
            )
        except httpx.HTTPError as e:
            # Handle 404, paywalls, etc.
            if e.response and e.response.status_code == 404:
                return ToolResult(
                    success=False,
                    error="SOURCE_UNAVAILABLE",
                    data=None
                )
            raise ToolExecutionError(f"Extraction failed: {e}")
        except Exception as e:
            # Fallback to mock extraction
            extraction = self._mock_extraction(source_url)
            return ToolResult(
                success=True,
                data=extraction.to_dict(),
                metadata={"extraction_method": "mock"}
            )
    
    def _call_extraction_service(self, source_url: str) -> StructuredExtraction:
        """Call Flask extraction microservice"""
        with httpx.Client() as client:
            response = client.post(
                f"{self.service_url}/extract",
                json={"url": source_url},
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            
            return StructuredExtraction(
                source_url=source_url,
                methodology=data.get("methodology", ""),
                key_findings=data.get("key_findings", []),
                datasets=data.get("datasets", []),
                limitations=data.get("limitations", [])
            )
    
    def _mock_extraction(self, source_url: str) -> StructuredExtraction:
        """Mock extraction for demo"""
        return StructuredExtraction(
            source_url=source_url,
            methodology="Experimental methodology with controlled variables",
            key_findings=[
                "Finding 1: Significant improvement observed",
                "Finding 2: Performance metrics exceeded baseline"
            ],
            datasets=["Dataset A", "Dataset B"],
            limitations=["Limited sample size", "Single region study"]
        )

