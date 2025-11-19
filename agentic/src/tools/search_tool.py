"""External search tool integration with Java backend"""
import httpx
import logging
from typing import List, Dict, Any
from tools.base_tool import BaseTool, ToolResult
from infrastructure.config import config
from infrastructure.exceptions import ToolExecutionError

logger = logging.getLogger(__name__)

class SearchTool(BaseTool):
    """Search tool for finding relevant papers via Java backend"""
    
    def __init__(self):
        self.api_url = config.JAVA_TOOLS_URL
        self.search_endpoint = config.JAVA_TOOLS_SEARCH_URL
        self.timeout = config.JAVA_TOOLS_SEARCH_TIMEOUT
        logger.info(f"SearchTool initialized with backend URL: {self.api_url}")
        logger.info(f"SearchTool search endpoint: {self.search_endpoint}")
    
    def get_name(self) -> str:
        return "search_papers"
    
    def execute(self, params: Dict[str, Any]) -> ToolResult:
        """
        Execute paper search via Java backend /api/tools/search endpoint
        
        Args:
            params: Dict with keys:
                - query (str, required): Search query string
                - max_results (int, optional): Maximum results to return (default: 20)
        
        Returns:
            ToolResult with success/failure status and search results
        """
        try:
            # Validate required parameters
            if not params.get("query"):
                return ToolResult(
                    success=False,
                    error="MISSING_QUERY",
                    data={"total_found": 0},
                    metadata={"error_message": "Search query is required"}
                )
            
            query = params.get("query", "").strip()
            max_results = params.get("max_results", 20)
            
            # Ensure max_results is an integer
            if isinstance(max_results, str):
                try:
                    max_results = int(max_results)
                except ValueError:
                    max_results = 20
            
            logger.debug(f"Executing search: query='{query}', max_results={max_results}")
            
            # Call Java backend
            response = self._call_java_backend(query, max_results)
            
            # Parse response
            results = response.get("results", [])
            total_found = response.get("total_found", 0)
            search_metrics = response.get("search_metrics", {})
            
            if not results:
                logger.debug(f"Search returned no results for query: {query}")
                return ToolResult(
                    success=False,
                    error="NO_RESULTS",
                    data={"total_found": 0, "results": []},
                    metadata=search_metrics
                )
            
            logger.info(f"Search completed: found {total_found} papers")
            return ToolResult(
                success=True,
                data={
                    "results": results,
                    "total_found": total_found
                },
                metadata=search_metrics
            )
            
        except httpx.TimeoutException as e:
            logger.error(f"Search API timeout: {str(e)}")
            raise ToolExecutionError(f"Search service timeout after {self.timeout}s")
        except httpx.ConnectError as e:
            logger.error(f"Cannot connect to search service at {self.api_url}: {str(e)}")
            raise ToolExecutionError(f"Cannot reach search service at {self.api_url}")
        except httpx.HTTPError as e:
            logger.error(f"Search API HTTP error: {str(e)}")
            if hasattr(e, 'response') and e.response:
                raise ToolExecutionError(f"Search API error {e.response.status_code}: {str(e)}")
            raise ToolExecutionError(f"Search API error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during search: {str(e)}", exc_info=True)
            raise ToolExecutionError(f"Search failed: {str(e)}")
    
    def _call_java_backend(self, query: str, max_results: int) -> Dict[str, Any]:
        """
        Call Java backend /api/tools/search endpoint
        
        Args:
            query: Search query string
            max_results: Maximum number of results
        
        Returns:
            Parsed JSON response from Java backend
        
        Raises:
            httpx.HTTPError: On network/HTTP errors
        """
        request_payload = {
            "query": query,
            "max_results": max_results
        }
        
        search_endpoint = self.search_endpoint
        logger.debug(f"Calling Java backend: POST {search_endpoint}")
        logger.debug(f"Request payload: {request_payload}")
        logger.debug(f"Timeout: {self.timeout}s")
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                logger.debug(f"Client created, sending POST request")
                response = client.post(
                    search_endpoint,
                    json=request_payload,
                    headers={"Content-Type": "application/json"}
                )
                logger.debug(f"Response received: {response}")
                if response is None:
                    raise ToolExecutionError(f"Java backend returned no response. Endpoint: {search_endpoint}")
                response.raise_for_status()
                return response.json()
        except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPError) as e:
            logger.error(f"httpx error: {type(e).__name__}: {str(e)}")
            raise
        except AttributeError as e:
            if "'NoneType' object has no attribute" in str(e):
                logger.error(f"httpx internal error - response object is None: {str(e)}")
                raise ToolExecutionError(f"Cannot connect to Java backend at {search_endpoint}: Connection failed")
            raise
        except Exception as e:
            logger.error(f"Unexpected error calling Java backend: {type(e).__name__}: {str(e)}", exc_info=True)
            raise
