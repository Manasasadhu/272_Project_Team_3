"""External search tool integration"""
import httpx
from typing import List, Dict, Any
from tools.base_tool import BaseTool, ToolResult
from infrastructure.config import config
from infrastructure.exceptions import ToolExecutionError
from models.research_goal import SourceCandidate

class SearchTool(BaseTool):
    """Search tool for finding relevant sources"""
    
    def __init__(self):
        self.api_url = "http://search_service:5000"  # Default search service URL
        self.timeout = 30.0  # Longer timeout for search service
    
    def get_name(self) -> str:
        return "SearchTool"
    
    def execute(self, params: Dict[str, Any]) -> ToolResult:
        """Execute search via external API"""
        try:
            search_params = {
                "query": params.get("query", ""),
                "filters": {
                    "year_range": {
                        "start": params.get("year_from"),
                        "end": params.get("year_to")
                    },
                    "source_types": params.get("source_types", ["academic", "technical"]),
                    "min_quality_score": params.get("min_quality", 0.7)
                },
                "max_results": params.get("limit", 20)
            }
            
            response = self._call_search_api(search_params)
            
            if not response.get("results"):
                return ToolResult(
                    success=False,
                    error="NO_RESULTS",
                    data={"total_found": 0},
                    metadata=response.get("search_metrics", {})
                )
            
            return ToolResult(
                success=True,
                data={
                    "results": response.get("results", []),
                    "total_found": response.get("total_found", 0)
                },
                metadata=response.get("search_metrics", {})
            )
        except httpx.HTTPError as e:
            if e.response and e.response.status_code == 429:
                raise ToolExecutionError("Search API rate limit exceeded")
            raise ToolExecutionError(f"Search API error: {str(e)}")
        except Exception as e:
            raise ToolExecutionError(f"Search failed: {str(e)}")
    
    def _call_search_api(self, search_params: Dict[str, Any]) -> Dict[str, Any]:
        """Call search service API"""
        headers = {
            "Content-Type": "application/json"
        }
        
        with httpx.Client() as client:
            response = client.post(
                f"{self.api_url}/api/tools/search",
                json=search_params,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
    
    def _mock_search(self, query: str, limit: int) -> List[Dict]:
        """Mock search for demo purposes"""
        # Return mock sources
        return [
            {
                "url": f"https://example.com/paper-{i}",
                "title": f"Research Paper {i} on {query}",
                "authors": [f"Author {i}A", f"Author {i}B"],
                "year": 2023 + (i % 2),
                "citations": 20 + i * 5,
                "source_type": "academic_paper"
            }
            for i in range(min(limit, 15))
        ]

