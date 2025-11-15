"""Vector-based memory storage using ChromaDB for semantic search"""
import os
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib
import time

class VectorMemory:
    """Vector-based memory for semantic search and similarity matching"""
    
    def __init__(self):
        """Initialize ChromaDB client with retry logic"""
        chroma_host = os.getenv("CHROMA_HOST", "localhost")
        chroma_port = int(os.getenv("CHROMA_PORT", "8000"))
        
        # Retry connection up to 3 times with delays
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.client = chromadb.HttpClient(
                    host=chroma_host,
                    port=chroma_port,
                    settings=Settings(
                        anonymized_telemetry=False,
                        allow_reset=True
                    )
                )
                
                # Test connection by trying to heartbeat
                self.client.heartbeat()
                
                # Create collections for different memory types
                self.search_patterns = self.client.get_or_create_collection(
                    name="search_patterns",
                    metadata={"description": "Successful search query patterns"}
                )
                
                self.source_contents = self.client.get_or_create_collection(
                    name="source_contents",
                    metadata={"description": "Source content for duplicate detection"}
                )
                
                from infrastructure.logging_setup import logger
                logger.info(f"Vector memory connected to ChromaDB at {chroma_host}:{chroma_port}")
                break
                
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff: 1s, 2s, 4s
                    continue
                else:
                    # Final attempt failed
                    raise ConnectionError(f"Could not connect to ChromaDB after {max_retries} attempts: {e}")
    
    # Search Pattern Methods
    def save_search_pattern(self, query: str, success_metrics: Dict[str, Any]):
        """Save search pattern with embedding for semantic retrieval"""
        pattern_id = self._generate_id(query)
        
        metadata = {
            "query": query,
            "success_rate": float(success_metrics.get("success_rate", 0)),
            "quality_score": float(success_metrics.get("quality_score", 0)),
            "avg_sources": float(success_metrics.get("avg_sources", 0)),
            "timestamp": datetime.now().isoformat()
        }
        
        # ChromaDB automatically generates embeddings
        self.search_patterns.upsert(
            ids=[pattern_id],
            documents=[query],
            metadatas=[metadata]
        )
    
    def get_similar_patterns(self, research_goal: str, limit: int = 5, 
                            min_success_rate: float = 0.7) -> List[Dict[str, Any]]:
        """Get semantically similar successful search patterns"""
        try:
            results = self.search_patterns.query(
                query_texts=[research_goal],
                n_results=limit,
                where={"success_rate": {"$gte": min_success_rate}}
            )
            
            if not results['ids'][0]:
                return []
            
            patterns = []
            for i, pattern_id in enumerate(results['ids'][0]):
                patterns.append({
                    "query": results['metadatas'][0][i]['query'],
                    "success_rate": results['metadatas'][0][i]['success_rate'],
                    "quality_score": results['metadatas'][0][i]['quality_score'],
                    "avg_sources": results['metadatas'][0][i]['avg_sources'],
                    "distance": results['distances'][0][i]  # Similarity score
                })
            
            return patterns
        except Exception as e:
            from infrastructure.logging_setup import logger
            logger.warning(f"Vector search failed, returning empty: {e}")
            return []
    
    # Source Duplicate Detection Methods
    def check_duplicate_source(self, content: str, source_url: str, 
                               similarity_threshold: float = 0.15) -> Optional[Dict[str, Any]]:
        """Check if source content is duplicate of existing source
        
        Returns duplicate info if found, None otherwise.
        Lower distance = more similar (threshold 0.15 = ~85% similar)
        """
        if not content or len(content) < 100:  # Skip very short content
            return None
        
        # Truncate very long content for efficiency
        content_sample = content[:2000] if len(content) > 2000 else content
        
        try:
            results = self.source_contents.query(
                query_texts=[content_sample],
                n_results=1,
                where={"url": {"$ne": source_url}}  # Exclude same URL
            )
            
            if not results['ids'][0]:
                return None
            
            # Check if distance indicates duplicate
            distance = results['distances'][0][0]
            if distance < similarity_threshold:
                return {
                    "is_duplicate": True,
                    "duplicate_url": results['metadatas'][0][0]['url'],
                    "similarity": 1 - distance,  # Convert distance to similarity %
                    "original_quality": results['metadatas'][0][0].get('quality_score', 0)
                }
            
            return None
        except Exception as e:
            from infrastructure.logging_setup import logger
            logger.warning(f"Duplicate check failed: {e}")
            return None
    
    def save_source_content(self, source_url: str, content: str, 
                           quality_metrics: Dict[str, Any]):
        """Save source content embedding for duplicate detection"""
        if not content or len(content) < 100:
            return
        
        source_id = self._generate_id(source_url)
        content_sample = content[:2000] if len(content) > 2000 else content
        
        metadata = {
            "url": source_url,
            "quality_score": float(quality_metrics.get("quality_score", 0)),
            "extraction_success": bool(quality_metrics.get("extraction_success", False)),
            "citations": int(quality_metrics.get("citations", 0)),
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            self.source_contents.upsert(
                ids=[source_id],
                documents=[content_sample],
                metadatas=[metadata]
            )
        except Exception as e:
            from infrastructure.logging_setup import logger
            logger.warning(f"Failed to save source content: {e}")
    
    # Utility Methods
    def _generate_id(self, text: str) -> str:
        """Generate unique ID from text"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        try:
            return {
                "search_patterns_count": self.search_patterns.count(),
                "source_contents_count": self.source_contents.count()
            }
        except:
            return {"error": "Unable to fetch stats"}
