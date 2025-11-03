"""Academic search tool"""
import httpx
from typing import List, Dict, Any
from tools.base_tool import BaseTool, ToolResult
from infrastructure.config import config
from infrastructure.exceptions import ToolExecutionError
from models.research_goal import SourceCandidate

class SearchTool(BaseTool):
    """Search tool for academic sources"""
    
    def __init__(self):
        self.api_key = config.SEMANTIC_SCHOLAR_API_KEY
        self.base_url = "https://api.semanticscholar.org/graph/v1"
    
    def get_name(self) -> str:
        return "SearchTool"
    
    def execute(self, params: Dict[str, Any]) -> ToolResult:
        """Execute search"""
        query = params.get("query", "")
        limit = params.get("limit", 20)
        
        try:
            # Use Semantic Scholar API or fallback to mock data for demo
            if self.api_key:
                sources = self._search_semantic_scholar(query, limit)
            else:
                # Mock data for demo if API key not configured
                sources = self._mock_search(query, limit)
            
            return ToolResult(
                success=True,
                data=sources,
                metadata={"total_found": len(sources)}
            )
        except Exception as e:
            raise ToolExecutionError(f"Search failed: {e}")
    
    def _search_semantic_scholar(self, query: str, limit: int) -> List[Dict]:
        """Search Semantic Scholar API"""
        headers = {"x-api-key": self.api_key} if self.api_key else {}
        
        with httpx.Client() as client:
            response = client.get(
                f"{self.base_url}/paper/search",
                params={"query": query, "limit": limit, "fields": "title,authors,year,url,citationCount"},
                headers=headers,
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            
            sources = []
            for paper in data.get("data", []):
                sources.append({
                    "url": paper.get("url", ""),
                    "title": paper.get("title", ""),
                    "authors": [a.get("name", "") for a in paper.get("authors", [])],
                    "year": paper.get("year", 2024),
                    "citations": paper.get("citationCount", 0),
                    "source_type": "academic_paper"
                })
            return sources
    
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

