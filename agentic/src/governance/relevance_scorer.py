"""Semantic relevance scoring using multi-factor heuristics (no LLM needed)"""
import re
from typing import Dict, List, Any, Optional
from datetime import datetime

class RelevanceScorer:
    """Score paper relevance using linguistic and metadata heuristics"""
    
    def __init__(self, logger=None):
        self.current_year = datetime.now().year
        self.logger = logger
    
    def score_relevance(self, paper: Dict[str, Any], research_goal: str, verbose: bool = False) -> float:
        """
        Calculate relevance score using weighted multi-factor approach
        
        Factors:
        - 40% Title-goal keyword overlap (semantic relevance)
        - 30% Recency weighting (recent papers valued higher)
        - 20% Citation authority (high-cited papers trusted)
        - 10% Venue/domain matching (conference prestige proxy)
        
        Returns: score 0.0-1.0
        """
        
        # Extract features from paper
        title = paper.get('title', '').lower()
        year = paper.get('year', 2023)
        citations = paper.get('citations', 0)
        venue = paper.get('venue', '').lower()
        snippet = paper.get('snippet', '').lower()
        
        # Calculate component scores
        keyword_score = self._score_keyword_overlap(title, snippet, research_goal)
        recency_score = self._score_recency(year)
        citation_score = self._score_citation_authority(citations)
        venue_score = self._score_venue_domain(venue, research_goal)
        
        # Weighted combination
        final_score = (
            0.40 * keyword_score +
            0.30 * recency_score +
            0.20 * citation_score +
            0.10 * venue_score
        )
        
        final_score = min(1.0, max(0.0, final_score))  # Clamp 0-1
        
        # Log details if requested
        if verbose and self.logger:
            self.logger.debug(
                f"[HEURISTIC BREAKDOWN] {title[:50]}... → {final_score:.3f} "
                f"(keyword={keyword_score:.3f}, recency={recency_score:.3f}, "
                f"citations={citation_score:.3f}, venue={venue_score:.3f})"
            )
        
        return final_score
    
    def _score_keyword_overlap(self, title: str, snippet: str, research_goal: str) -> float:
        """Score based on keyword overlap between paper and research goal
        
        Returns: 0.0-1.0
        """
        # Extract keywords (nouns, important terms)
        goal_keywords = self._extract_keywords(research_goal)
        paper_keywords = self._extract_keywords(title + " " + snippet)
        
        if not goal_keywords or not paper_keywords:
            return 0.3  # Minimal relevance if no keywords
        
        # IMPROVED: Boost technical keywords (3x weight for high-value terms)
        technical_keywords = {'transformer', 'neural', 'network', 'deep', 'learning', 
                              'optimization', 'efficiency', 'architecture', 'model', 
                              'training', 'algorithm', 'framework', 'inference', 
                              'attention', 'encoder', 'decoder', 'bert', 'gpt',
                              'nlp', 'vision', 'gpu', 'accelerate', 'parallelization'}
        
        # Weight goal keywords: technical terms worth 3x, regular terms worth 1x
        weighted_goal = set()
        for kw in goal_keywords:
            if kw in technical_keywords:
                weighted_goal.add(kw)  # Add multiple times for higher weight
                weighted_goal.add(kw + "_TECH")  # Marker for technical terms
            else:
                weighted_goal.add(kw)
        
        # Same for paper keywords
        weighted_paper = set()
        for kw in paper_keywords:
            if kw in technical_keywords:
                weighted_paper.add(kw)
                weighted_paper.add(kw + "_TECH")
            else:
                weighted_paper.add(kw)
        
        # Jaccard similarity on weighted sets
        overlap = len(weighted_goal & weighted_paper)
        union = len(weighted_goal | weighted_paper)
        
        if union == 0:
            return 0.0
        
        jaccard_score = overlap / union
        
        # Bonus: exact phrase matches or multi-word matches
        # Check if important bigrams appear (e.g., "transformer", "neural network")
        exact_match_bonus = 0.0
        for kw in goal_keywords:
            if kw in paper_keywords:
                # Higher bonus for technical keywords
                if kw in technical_keywords:
                    exact_match_bonus += 0.08
                else:
                    exact_match_bonus += 0.03
        
        exact_match_bonus = min(0.3, exact_match_bonus)  # Cap bonus at 0.3
        
        return min(1.0, jaccard_score + exact_match_bonus)
    
    def _score_recency(self, year: int) -> float:
        """Score based on publication recency
        
        2024-2025 papers: 1.0 (most recent, highest value)
        2023 papers: 0.75
        2022 papers: 0.5
        2021 and earlier: 0.2
        """
        years_old = self.current_year - year
        
        if years_old <= 1:
            return 1.0  # Current/very recent
        elif years_old == 2:
            return 0.75  # Last year
        elif years_old == 3:
            return 0.5  # 2-3 years old
        else:
            return 0.2  # Older papers have much lower weight
    
    def _score_citation_authority(self, citations: int) -> float:
        """Score based on citation count (influence/authority)
        
        Uses logarithmic scale (citation count doesn't scale linearly with quality)
        
        1000+ citations: 1.0 (highly influential)
        500+ citations: 0.95
        100+ citations: 0.85
        50+ citations: 0.70
        20+ citations: 0.55
        10+ citations: 0.40
        <10 citations: 0.20 (possibly new work)
        """
        if citations >= 1000:
            return 1.0
        elif citations >= 500:
            return 0.95
        elif citations >= 100:
            return 0.85
        elif citations >= 50:
            return 0.70
        elif citations >= 20:
            return 0.55
        elif citations >= 10:
            return 0.40
        else:
            return 0.20
    
    def _score_venue_domain(self, venue: str, research_goal: str) -> float:
        """Score based on venue prestige and domain relevance
        
        Returns: 0.0-1.0
        """
        research_goal_lower = research_goal.lower()
        
        # Premium ML/AI venues for general AI/ML research
        premium_venues = [
            'neurips', 'nips',           # Top ML conference
            'icml',                       # Top ML conference  
            'iclr',                       # Top learning conference
            'iccv', 'cvpr',              # Computer vision
            'emnlp', 'acl', 'naacl',     # NLP conferences
            'aaai',                       # General AI
            'ijcai',                      # Joint AI conference
            'jmlr',                       # Journal of ML Research
        ]
        
        # Check if venue matches premium conferences
        venue_score = 0.3  # Default for unknown venues
        
        for premium in premium_venues:
            if premium in venue:
                venue_score = 0.95  # High prestige
                break
        
        # Domain-specific adjustments
        if 'transformer' in research_goal_lower or 'nlp' in research_goal_lower:
            if any(kw in venue for kw in ['acl', 'emnlp', 'naacl']):
                venue_score = 1.0  # Perfect match
            elif 'neurips' in venue or 'icml' in venue:
                venue_score = 0.9  # Good for NLP at general ML venues
        
        if 'computer vision' in research_goal_lower or 'vision' in research_goal_lower:
            if any(kw in venue for kw in ['cvpr', 'iccv']):
                venue_score = 1.0  # Perfect match
        
        return venue_score
    
    def _extract_keywords(self, text: str) -> set:
        """Extract important keywords from text
        
        Removes common words, extracts 3+ character terms
        """
        # Common words to filter
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
            'have', 'has', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'that', 'this', 'these', 'those', 'as', 'which', 'who', 'what', 'where',
            'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most',
            'some', 'any', 'it', 'its', 'our', 'your', 'their', 'can', 'may',
            'must', 'shall', 'review', 'analysis', 'study', 'research', 'paper',
            'et', 'al', 'survey', 'literature', 'a', 'b', 'c',  # Single letters
        }
        
        # Extract words (remove special chars, split)
        words = re.findall(r'\b[a-z]{3,}\b', text.lower())
        
        # Filter stopwords and return unique terms
        keywords = {w for w in words if w not in stopwords and len(w) >= 3}
        
        return keywords
    
    def batch_score(self, papers: List[Dict[str, Any]], research_goal: str, verbose: bool = False) -> List[float]:
        """Score a batch of papers efficiently
        
        Args:
            papers: List of paper dictionaries
            research_goal: Research goal string
            verbose: If True, logs detailed breakdown for each paper
            
        Returns:
            List of relevance scores (0.0-1.0)
        """
        return [self.score_relevance(paper, research_goal, verbose=verbose) for paper in papers]
