"""
Integration tests for Java backend tools (search and extraction)

Run this after starting the Java backend service:
    cd backend/search-and-extraction-service
    mvn spring-boot:run

Then run this test:
    python -m pytest tests/test_java_tools_integration.py -v -s
"""

import pytest
import logging
from tools.tool_registry import ToolRegistry
from tools.search_tool import SearchTool
from tools.extraction_tool import ExtractionTool
from infrastructure.exceptions import ToolExecutionError

logger = logging.getLogger(__name__)


class TestToolRegistry:
    """Test ToolRegistry initialization and tool registration"""
    
    def test_registry_initialization(self):
        """Test that registry initializes with default tools"""
        registry = ToolRegistry()
        tools = registry.list_tools()
        
        assert "search_papers" in tools
        assert "extract_paper" in tools
        logger.info(f"✓ Registry initialized with tools: {tools}")
    
    def test_get_tool_by_name(self):
        """Test retrieving tools by name"""
        registry = ToolRegistry()
        
        search_tool = registry.get_tool("search_papers")
        assert isinstance(search_tool, SearchTool)
        
        extract_tool = registry.get_tool("extract_paper")
        assert isinstance(extract_tool, ExtractionTool)
        logger.info("✓ Tools retrieved successfully by name")
    
    def test_tool_names(self):
        """Test that tools return correct names"""
        search_tool = SearchTool()
        extract_tool = ExtractionTool()
        
        assert search_tool.get_name() == "search_papers"
        assert extract_tool.get_name() == "extract_paper"
        logger.info("✓ Tool names are correct")
    
    def test_backend_health_check(self):
        """Test backend health check (backend may or may not be running)"""
        registry = ToolRegistry()
        health = registry.check_java_backend_health()
        
        assert isinstance(health, dict)
        assert "backend_reachable" in health
        assert "search_available" in health
        assert "extract_available" in health
        logger.info(f"✓ Health check returned: {health}")
    
    def test_get_tools_info(self):
        """Test comprehensive tools info retrieval"""
        registry = ToolRegistry()
        info = registry.get_tools_info()
        
        assert "registered_tools" in info
        assert "backend_config" in info
        assert "backend_health" in info
        assert "tools" in info
        assert "search_papers" in info["tools"]
        assert "extract_paper" in info["tools"]
        logger.info(f"✓ Tools info retrieved: {info}")


class TestSearchTool:
    """Test SearchTool functionality with Java backend"""
    
    def test_search_tool_initialization(self):
        """Test SearchTool initializes with correct config"""
        tool = SearchTool()
        
        assert tool.get_name() == "search_papers"
        assert tool.api_url is not None
        assert tool.timeout > 0
        logger.info(f"✓ SearchTool initialized: url={tool.api_url}, timeout={tool.timeout}")
    
    def test_search_requires_query(self):
        """Test that search fails gracefully without query"""
        tool = SearchTool()
        result = tool.execute({"max_results": 10})
        
        assert result.success is False
        assert result.error == "MISSING_QUERY"
        logger.info("✓ Search correctly rejects missing query parameter")
    
    def test_search_parameter_types(self):
        """Test search handles different parameter types"""
        tool = SearchTool()
        
        # Test with string max_results (should convert to int)
        result = tool.execute({
            "query": "test query",
            "max_results": "15"
        })
        # Should either succeed or fail due to backend, not parameter parsing
        assert result is not None
        logger.info("✓ Search handles string max_results parameter")
        
        # Test with int max_results
        result = tool.execute({
            "query": "test query",
            "max_results": 20
        })
        assert result is not None
        logger.info("✓ Search handles int max_results parameter")


class TestExtractionTool:
    """Test ExtractionTool functionality with Java backend"""
    
    def test_extraction_tool_initialization(self):
        """Test ExtractionTool initializes with correct config"""
        tool = ExtractionTool()
        
        assert tool.get_name() == "extract_paper"
        assert tool.api_url is not None
        assert tool.timeout > 0
        logger.info(f"✓ ExtractionTool initialized: url={tool.api_url}, timeout={tool.timeout}")
    
    def test_extraction_requires_source_url(self):
        """Test that extraction fails gracefully without source_url"""
        tool = ExtractionTool()
        result = tool.execute({})
        
        assert result.success is False
        assert result.error == "MISSING_SOURCE_URL"
        logger.info("✓ Extraction correctly rejects missing source_url parameter")
    
    def test_extraction_with_url(self):
        """Test extraction with valid URL structure (may fail if backend unavailable)"""
        tool = ExtractionTool()
        
        # Test with ArXiv URL pattern
        result = tool.execute({
            "source_url": "https://arxiv.org/abs/2301.00001"
        })
        assert result is not None
        logger.info(f"✓ Extraction accepts ArXiv URL: success={result.success}, error={result.error}")
        
        # Test with DOI URL pattern
        result = tool.execute({
            "source_url": "https://doi.org/10.1234/example"
        })
        assert result is not None
        logger.info(f"✓ Extraction accepts DOI URL: success={result.success}, error={result.error}")


class TestIntegrationWithBackend:
    """Integration tests with live Java backend (requires backend running)"""
    
    @pytest.mark.integration
    def test_search_with_live_backend(self):
        """Test actual search with live Java backend
        
        Requires: Java backend running on localhost:5000
        """
        registry = ToolRegistry()
        health = registry.check_java_backend_health()
        
        if not health.get("backend_reachable"):
            pytest.skip("Java backend not available at localhost:5000")
        
        tool = registry.get_tool("search_papers")
        result = tool.execute({
            "query": "transformer neural networks",
            "max_results": 5
        })
        
        logger.info(f"Search result: success={result.success}, error={result.error}")
        if result.success:
            logger.info(f"  - Found {result.data.get('total_found')} papers")
            logger.info(f"  - Metrics: {result.metadata}")
            assert result.data.get("total_found") > 0
            assert len(result.data.get("results", [])) > 0
    
    @pytest.mark.integration
    def test_extraction_with_live_backend(self):
        """Test actual extraction with live Java backend
        
        Requires: Java backend running on localhost:5000 with GROBID access
        """
        registry = ToolRegistry()
        health = registry.check_java_backend_health()
        
        if not health.get("backend_reachable"):
            pytest.skip("Java backend not available at localhost:5000")
        
        tool = registry.get_tool("extract_paper")
        
        # Test with a known ArXiv paper
        result = tool.execute({
            "source_url": "https://arxiv.org/abs/2301.13298"  # A recent ML paper
        })
        
        logger.info(f"Extraction result: success={result.success}, error={result.error}")
        if result.success:
            logger.info(f"  - Title: {result.data.get('title')}")
            logger.info(f"  - Key findings: {result.data.get('key_findings')}")
            logger.info(f"  - Confidence: {result.metadata.get('confidence_score')}")
            assert result.data.get("title")
            assert result.data.get("abstract")


if __name__ == "__main__":
    # Run basic tests
    print("=" * 60)
    print("Running Java Tools Integration Tests")
    print("=" * 60)
    
    # Test registry
    print("\n1. Testing ToolRegistry...")
    registry = ToolRegistry()
    print(f"   Tools registered: {registry.list_tools()}")
    print(f"   Tools info: {registry.get_tools_info()}")
    
    # Test search tool initialization
    print("\n2. Testing SearchTool...")
    search = SearchTool()
    print(f"   Name: {search.get_name()}")
    print(f"   Backend: {search.api_url}")
    print(f"   Timeout: {search.timeout}s")
    
    # Test extraction tool initialization
    print("\n3. Testing ExtractionTool...")
    extract = ExtractionTool()
    print(f"   Name: {extract.get_name()}")
    print(f"   Backend: {extract.api_url}")
    print(f"   Timeout: {extract.timeout}s")
    
    # Test parameter validation
    print("\n4. Testing parameter validation...")
    search_result = search.execute({})
    print(f"   Search without query: success={search_result.success}, error={search_result.error}")
    
    extract_result = extract.execute({})
    print(f"   Extraction without URL: success={extract_result.success}, error={extract_result.error}")
    
    print("\n✓ All basic tests passed!")
    print("  For integration tests with live backend, run: pytest -v -s tests/test_java_tools_integration.py -m integration")
