#!/usr/bin/env python3
"""
Simple Java backend integration test using only standard library
"""
import json
import urllib.request
import urllib.error
import sys

# Test Configuration
JAVA_BACKEND_URL = "http://localhost:9000"

def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    
    try:
        url = f"{JAVA_BACKEND_URL}/api/tools/health"
        print(f"GET {url}")
        
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            print(f"✅ Response: {json.dumps(data, indent=2)}")
            return data.get("service") == "tools"
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_search():
    """Test search endpoint"""
    print("\n" + "="*60)
    print("TEST 2: Search Endpoint")
    print("="*60)
    
    try:
        url = f"{JAVA_BACKEND_URL}/api/tools/search"
        request_data = {
            "query": "attention mechanism transformers",
            "max_results": 2
        }
        
        print(f"POST {url}")
        print(f"Request: {json.dumps(request_data, indent=2)}")
        
        req = urllib.request.Request(
            url,
            data=json.dumps(request_data).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print(f"✅ Response Status: Success")
            print(f"   - Total Found: {data.get('total_found')}")
            print(f"   - Results: {len(data.get('results', []))}")
            if data.get('results'):
                first = data['results'][0]
                print(f"   - First Result: {first.get('title')[:60]}...")
            print(f"   - Query Time: {data.get('search_metrics', {}).get('query_time_ms')}ms")
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_extract():
    """Test extract endpoint"""
    print("\n" + "="*60)
    print("TEST 3: Extract Endpoint")
    print("="*60)
    
    try:
        url = f"{JAVA_BACKEND_URL}/api/tools/extract"
        request_data = {
            "source_url": "https://arxiv.org/abs/2301.13298"
        }
        
        print(f"POST {url}")
        print(f"Request: {json.dumps(request_data, indent=2)}")
        
        req = urllib.request.Request(
            url,
            data=json.dumps(request_data).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            metadata = data.get('metadata', {})
            content = data.get('extracted_content', {})
            
            print(f"✅ Response Status: Success")
            print(f"   - Extraction Success: {metadata.get('extraction_success')}")
            print(f"   - Source URL: {metadata.get('source_url')}")
            print(f"   - Processing Time: {data.get('extraction_metrics', {}).get('processing_time_ms')}ms")
            print(f"   - Confidence Score: {data.get('extraction_metrics', {}).get('confidence_score')}")
            
            if content:
                print(f"   - Title: {content.get('title', 'N/A')}")
                print(f"   - Key Findings: {len(content.get('key_findings', []))} items")
            
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "█"*60)
    print("█  Java Backend Service Integration Test")
    print("█"*60)
    print(f"\nBackend URL: {JAVA_BACKEND_URL}")
    
    # Run tests
    results = {
        "Health Check": test_health(),
        "Search Endpoint": test_search(),
        "Extract Endpoint": test_extract(),
    }
    
    # Summary
    print("\n" + "█"*60)
    print("█  Test Summary")
    print("█"*60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(results.values())
    print("\n" + "█"*60)
    if all_passed:
        print("█  ✅ ALL TESTS PASSED - Java Backend is working!")
    else:
        print("█  ❌ Some tests failed - Check Java Backend status")
    print("█"*60 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
