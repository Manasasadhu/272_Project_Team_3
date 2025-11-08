"""External extraction tool integration"""
import httpx
from typing import Dict, Any
from tools.base_tool import BaseTool, ToolResult
from infrastructure.config import config
from infrastructure.exceptions import ToolExecutionError
from models.extraction_schema import StructuredExtraction

class ExtractionTool(BaseTool):
    """Extraction tool for structured data from sources"""
    
    def __init__(self):
        self.api_url = "http://extraction_service:5000"  # Default extraction service URL
        self.timeout = 45.0  # Longer timeout for content extraction
    
    def get_name(self) -> str:
        return "ExtractionTool"
    
    def execute(self, params: Dict[str, Any]) -> ToolResult:
        """Execute content extraction"""
        try:
            if not params.get("source_url"):
                return ToolResult(
                    success=False,
                    error="MISSING_SOURCE_URL",
                    data=None
                )
                
            extraction_params = {
                "source_url": params["source_url"],
                "extraction_parameters": {
                    "focus_areas": params.get("focus_areas", []),
                    "required_elements": params.get("required_elements", [
                        "key_findings",
                        "methodology",
                        "conclusions",
                        "citations"
                    ]),
                    "max_length": params.get("max_length", 5000)
                }
            }
            
            response = self._call_extraction_api(extraction_params)
            
            # Check if extraction was successful
            if not response.get("metadata", {}).get("extraction_success", False):
                return ToolResult(
                    success=False,
                    error="EXTRACTION_FAILED",
                    data=None,
                    metadata=response.get("extraction_metrics", {})
                )
            
            return ToolResult(
                success=True,
                data=response.get("extracted_content", {}),
                metadata={
                    **response.get("metadata", {}),
                    **response.get("extraction_metrics", {})
                }
            )
            
        except httpx.HTTPError as e:
            if hasattr(e, 'response') and e.response:
                if e.response.status_code == 404:
                    return ToolResult(
                        success=False,
                        error="SOURCE_UNAVAILABLE",
                        data=None
                    )
                if e.response.status_code == 429:
                    raise ToolExecutionError("Extraction service rate limit exceeded")
            raise ToolExecutionError(f"Extraction service error: {str(e)}")
        except Exception as e:
            raise ToolExecutionError(f"Extraction failed: {str(e)}")
    
    def _call_extraction_api(self, extraction_params: Dict[str, Any]) -> Dict[str, Any]:
        """Call extraction service API endpoint"""
        # TODO: Replace with actual extraction service when available
        # For now, return mock data
        source_url = extraction_params.get("source_url", "")
        return {
            "extracted_content": {
                "title": f"Extracted content from {source_url}",
                "abstract": "This is a mock abstract extracted from the source.",
                "key_findings": ["Finding 1", "Finding 2", "Finding 3"],
                "methodology": "Mock methodology description",
                "citations": []
            },
            "metadata": {
                "source_url": source_url,
                "extraction_timestamp": "2025-11-07T00:00:00Z",
                "extraction_success": True  # ← Added this!
            },
            "extraction_metrics": {
                "processing_time_ms": 500,
                "confidence_score": 0.85
            }
        }
        
        headers = {
            "content-type": "application/json"
        }
        
        try:
            response = httpx.post(
                f"{self.api_url}/api/tools/extract",
                headers=headers,
                json=extraction_params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutError:
            raise ToolExecutionError("Extraction service timeout")
            
        except httpx.TimeoutError:
            raise ToolExecutionError("Extraction API timeout")
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

