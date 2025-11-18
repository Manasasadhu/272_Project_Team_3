#!/usr/bin/env python3
"""
Quick integration test demonstrating Python tools calling Java backend

Usage:
    1. Start Java backend: java -jar backend/search-and-extraction-service/target/*.jar
    2. Run this script: python agentic/test_integration_flow.py
"""

import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from tools.tool_registry import ToolRegistry
from infrastructure.config import config


def test_backend_health():
    """Test 1: Check if Java backend is reachable"""
    print("\n" + "="*60)
    print("TEST 1: Java Backend Health Check")
    print("="*60)
    
    registry = ToolRegistry()
    health = registry.check_java_backend_health()
    
    print(f"\nBackend URL: {config.JAVA_TOOLS_URL}")
    print(f"Backend Reachable: {health['backend_reachable']}")
    print(f"Search Available: {health['search_available']}")
    print(f"Extract Available: {health['extract_available']}")
    
    if not health['backend_reachable']:
        print("\n⚠️  Backend is NOT reachable!")
        print(f"   Make sure Java backend is running on {config.JAVA_TOOLS_URL}")
        return False
    
    print("\n✅ Backend is reachable!")
    return True


def test_search_tool():
    """Test 2: Search tool integration"""
    print("\n" + "="*60)
    print("TEST 2: Search Tool Integration")
    print("="*60)
    
    registry = ToolRegistry()
    search_tool = registry.get_tool("search_papers")
    
    print(f"\nTool Name: {search_tool.get_name()}")
    print(f"Backend URL: {search_tool.api_url}")
    print(f"Timeout: {search_tool.timeout}s")
    
    # Test 2a: Parameter validation
    print("\n--- Test 2a: Parameter Validation ---")
    result = search_tool.execute({})
    print(f"Execute with no params: success={result.success}, error={result.error}")
    assert not result.success and result.error == "MISSING_QUERY"
    print("✅ Parameter validation works")
    
    # Test 2b: Actual search
    print("\n--- Test 2b: Actual Search ---")
    try:
        print("Searching for: 'transformer neural networks'")
        result = search_tool.execute({
            "query": "transformer neural networks",
            "max_results": 3
        })
        
        print(f"Result success: {result.success}")
        print(f"Result error: {result.error}")
        
        if result.success:
            print(f"Papers found: {result.data.get('total_found')}")
            print(f"Query time: {result.metadata.get('query_time_ms')}ms")
            
            if result.data.get('results'):
                print("\nFirst result:")
                first = result.data['results'][0]
                print(f"  Title: {first.get('title')}")
                print(f"  URL: {first.get('url')}")
                print(f"  Citations: {first.get('citations')}")
            
            print("✅ Search tool works!")
        else:
            print(f"Search failed: {result.error}")
            print(f"Metadata: {result.metadata}")
            
    except Exception as e:
        print(f"❌ Search failed with exception: {e}")
        import traceback
        traceback.print_exc()


def test_extraction_tool():
    """Test 3: Extraction tool integration"""
    print("\n" + "="*60)
    print("TEST 3: Extraction Tool Integration")
    print("="*60)
    
    registry = ToolRegistry()
    extract_tool = registry.get_tool("extract_paper")
    
    print(f"\nTool Name: {extract_tool.get_name()}")
    print(f"Backend URL: {extract_tool.api_url}")
    print(f"Timeout: {extract_tool.timeout}s")
    
    # Test 3a: Parameter validation
    print("\n--- Test 3a: Parameter Validation ---")
    result = extract_tool.execute({})
    print(f"Execute with no params: success={result.success}, error={result.error}")
    assert not result.success and result.error == "MISSING_SOURCE_URL"
    print("✅ Parameter validation works")
    
    # Test 3b: ArXiv extraction
    print("\n--- Test 3b: ArXiv Paper Extraction ---")
    try:
        arxiv_url = "https://arxiv.org/abs/2301.13298"
        print(f"Extracting from: {arxiv_url}")
        result = extract_tool.execute({"source_url": arxiv_url})
        
        print(f"Result success: {result.success}")
        if result.success:
            content = result.data
            print(f"  Title: {content.get('title')[:50]}...")
            print(f"  Abstract: {content.get('abstract')[:100]}...")
            print(f"  Key findings: {len(content.get('key_findings', []))} items")
            print(f"  Confidence: {result.metadata.get('confidence_score')}")
            print("✅ Extraction works!")
        else:
            print(f"Extraction failed: {result.error}")
            print(f"Reason: {result.metadata.get('failure_reason')}")
            
    except Exception as e:
        print(f"❌ Extraction failed with exception: {e}")
        import traceback
        traceback.print_exc()


def test_tools_info():
    """Test 4: Comprehensive tools info"""
    print("\n" + "="*60)
    print("TEST 4: Tools Registry Info")
    print("="*60)
    
    registry = ToolRegistry()
    info = registry.get_tools_info()
    
    print(f"\nRegistered Tools: {info.get('registered_tools')}")
    print(f"Backend URL: {info['backend_config'].get('url')}")
    print(f"Search Timeout: {info['backend_config'].get('search_timeout')}s")
    print(f"Extract Timeout: {info['backend_config'].get('extract_timeout')}s")
    
    print(f"\nBackend Health:")
    health = info['backend_health']
    print(f"  Reachable: {health.get('backend_reachable')}")
    print(f"  Search Available: {health.get('search_available')}")
    print(f"  Extract Available: {health.get('extract_available')}")


def main():
    """Run all integration tests"""
    print("\n" + "█"*60)
    print("█  Java Backend ← → Python Tools Integration Test")
    print("█"*60)
    
    try:
        # Test 1: Health check
        if not test_backend_health():
            print("\n❌ Backend is not reachable. Start it first:")
            print("   cd backend/search-and-extraction-service")
            print("   java -jar target/*.jar")
            return
        
        # Test 2: Search tool
        test_search_tool()
        
        # Test 3: Extraction tool
        test_extraction_tool()
        
        # Test 4: Tools info
        test_tools_info()
        
        print("\n" + "█"*60)
        print("█  ✅ All integration tests completed!")
        print("█"*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
