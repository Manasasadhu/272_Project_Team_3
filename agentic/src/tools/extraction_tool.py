"""External extraction tool integration with Java backend"""
import httpx
import logging
from typing import Dict, Any
from tools.base_tool import BaseTool, ToolResult
from infrastructure.config import config
from infrastructure.exceptions import ToolExecutionError

logger = logging.getLogger(__name__)

class ExtractionTool(BaseTool):
    """Extraction tool for structured data from paper sources via Java backend"""
    
    def __init__(self):
        self.api_url = config.JAVA_TOOLS_URL
        self.timeout = config.JAVA_TOOLS_EXTRACT_TIMEOUT
        logger.info(f"ExtractionTool initialized with backend URL: {self.api_url}")
    
    def get_name(self) -> str:
        return "extract_paper"
    
    def execute(self, params: Dict[str, Any]) -> ToolResult:
        """
        Execute paper content extraction via Java backend /api/tools/extract endpoint
        
        Args:
            params: Dict with keys:
                - source_url (str, required): Paper URL (ArXiv, DOI, or PDF URL)
        
        Returns:
            ToolResult with extracted content or failure information
        """
        try:
            # Validate required parameters
            if not params.get("source_url"):
                return ToolResult(
                    success=False,
                    error="MISSING_SOURCE_URL",
                    data=None,
                    metadata={"error_message": "source_url parameter is required"}
                )
            
            source_url = params.get("source_url", "").strip()
            
            logger.debug(f"Extracting content from: {source_url}")
            
            # Call Java backend
            response = self._call_java_backend(source_url)
            
            # Parse response structure
            extracted_content = response.get("extracted_content", {})
            metadata = response.get("metadata", {})
            extraction_metrics = response.get("extraction_metrics", {})
            
            # Check extraction success flag
            extraction_success = metadata.get("extraction_success", False)
            
            if not extraction_success:
                failure_reason = metadata.get("failure_reason", "Unknown extraction failure")
                logger.warning(f"Extraction failed for {source_url}: {failure_reason}")
                return ToolResult(
                    success=False,
                    error="EXTRACTION_FAILED",
                    data=None,
                    metadata={
                        "failure_reason": failure_reason,
                        **extraction_metrics
                    }
                )
            
            # Successful extraction
            logger.info(f"Successfully extracted content from: {source_url}")
            return ToolResult(
                success=True,
                data={
                    "title": extracted_content.get("title", ""),
                    "abstract": extracted_content.get("abstract", ""),
                    "key_findings": extracted_content.get("key_findings", []),
                    "methodology": extracted_content.get("methodology", ""),
                    "citations": extracted_content.get("citations", [])
                },
                metadata={
                    "extraction_timestamp": metadata.get("extraction_timestamp"),
                    "source_url": metadata.get("source_url"),
                    **extraction_metrics
                }
            )
            
        except httpx.TimeoutException as e:
            logger.error(f"Extraction API timeout: {str(e)}")
            raise ToolExecutionError(f"Extraction service timeout after {self.timeout}s")
        except httpx.ConnectError as e:
            logger.error(f"Cannot connect to extraction service at {self.api_url}: {str(e)}")
            raise ToolExecutionError(f"Cannot reach extraction service at {self.api_url}")
        except httpx.HTTPError as e:
            logger.error(f"Extraction API HTTP error: {str(e)}")
            if hasattr(e, 'response') and e.response:
                raise ToolExecutionError(f"Extraction API error {e.response.status_code}: {str(e)}")
            raise ToolExecutionError(f"Extraction API error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during extraction: {str(e)}", exc_info=True)
            raise ToolExecutionError(f"Extraction failed: {str(e)}")
    
    def _call_java_backend(self, source_url: str) -> Dict[str, Any]:
        """
        Call Java backend /api/tools/extract endpoint
        
        Args:
            source_url: URL of the paper (ArXiv, DOI, or PDF)
        
        Returns:
            Parsed JSON response from Java backend with extraction results
        
        Raises:
            httpx.HTTPError: On network/HTTP errors
        """
        request_payload = {
            "source_url": source_url
        }
        
        extract_endpoint = f"{self.api_url}/api/tools/extract"
        logger.debug(f"Calling Java backend: POST {extract_endpoint}")
        logger.debug(f"Request payload: {request_payload}")
        logger.debug(f"Timeout: {self.timeout}s")
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                logger.debug(f"Client created, sending POST request")
                response = client.post(
                    extract_endpoint,
                    json=request_payload,
                    headers={"Content-Type": "application/json"}
                )
                logger.debug(f"Response received: {response}")
                if response is None:
                    raise ToolExecutionError(f"Java backend returned no response. Endpoint: {extract_endpoint}")
                response.raise_for_status()
                return response.json()
        except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPError) as e:
            logger.error(f"httpx error: {type(e).__name__}: {str(e)}")
            raise
        except AttributeError as e:
            if "'NoneType' object has no attribute" in str(e):
                logger.error(f"httpx internal error - response object is None: {str(e)}")
                raise ToolExecutionError(f"Cannot connect to Java backend at {extract_endpoint}: Connection failed")
            raise
        except Exception as e:
            logger.error(f"Unexpected error calling Java backend: {type(e).__name__}: {str(e)}", exc_info=True)
            raise
