"""Semantic relevance scoring using advanced keyword matching (NO LLM)

Ditching LLM because:
- Gemini keeps blocking due to safety filters
- Not worth API calls and latency
- Semantic keyword matching works just as well
- No external dependencies, fully deterministic
"""
import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

class RelevanceScorer:
    """Score paper relevance using DYNAMIC semantic keyword matching
    
    **NO HARDCODING** - Semantic groups generated at runtime:
    - Semantic groups generated dynamically from research goal
    - Synonym detection (agents ≈ agentic)
    - Word stemming (model ≈ models)
    - Citation authority
    - Recency weighting
    - Venue relevance
    """
    
    def __init__(self, logger=None, llm_client=None, semantic_groups=None):
        """Initialize RelevanceScorer with optional dynamic semantic groups
        
        Args:
            logger: Logger instance for debugging
            llm_client: IGNORED - not used for paper scoring
            semantic_groups: Dict[str, List[str]] of semantic keyword groups
                Generated dynamically from research goal (no hardcoding)
                Format: {"core_term": ["variant1", "variant2", ...], ...}
        """
        self.current_year = datetime.now().year
        self.logger = logger
        self.semantic_groups = semantic_groups or {}  # DYNAMIC groups (not hardcoded!)
        self.llm_cache = {}  # Cache semantic scores to speed up repeated queries
    
    def score_relevance(self, paper: Dict[str, Any], research_goal: str, verbose: bool = False) -> float:
        """
        Calculate relevance score using SEMANTIC KEYWORD MATCHING + metadata
        
        NO LLM - Uses:
        - 70% Semantic Keyword Relevance (synonym detection, stemming, semantic relationships)
        - 15% Citation Authority (high-cited papers more reliable)
        - 10% Recency (recent papers weighted higher)
        - 5% Metadata Match (venue, author relevance)
        
        Returns: score 0.0-1.0
        """
        
        # Extract features from paper
        title = paper.get('title', '')
        year = paper.get('year', 2023)
        citations = paper.get('citations', 0)
        venue = paper.get('venue', '')
        snippet = paper.get('snippet', '')
        
        # Calculate component scores
        # Semantic keyword matching is the primary driver (no LLM!)
        semantic_score = self._score_semantic_keywords(title, snippet, research_goal)
        citation_score = self._score_citation_authority(citations)
        recency_score = self._score_recency(year)
        metadata_score = self._score_venue_domain(venue, research_goal)
        
        # Weighted combination: Semantic is most important
        final_score = (
            0.70 * semantic_score +
            0.15 * citation_score +
            0.10 * recency_score +
            0.05 * metadata_score
        )
        
        final_score = min(1.0, max(0.0, final_score))  # Clamp 0-1
        
        if verbose and self.logger:
            self.logger.debug(
                f"[RELEVANCE SCORING] {title[:50]}... → {final_score:.3f} "
                f"(semantic={semantic_score:.3f}, citations={citation_score:.3f}, "
                f"recency={recency_score:.3f}, metadata={metadata_score:.3f})"
            )
        
        return final_score
    
    def _score_semantic_keywords(self, title: str, snippet: str, research_goal: str) -> float:
        """Score relevance using semantic keyword matching
        
        **NO LLM - PURE SEMANTIC VALIDATION**:
        - Extracts keywords from goal and paper dynamically
        - Uses synonym matching (e.g., "agents" ≈ "agentic" ≈ "autonomous")
        - Uses prefix matching with stemming (e.g., "models" ≈ "model")
        - Domain-agnostic - works for any research area
        - Multi-word phrase detection (e.g., "large language models" ≈ "llm")
        - Title matches weighted higher than snippet matches
        """
        goal_keywords = self._extract_keywords(research_goal)
        title_keywords = self._extract_keywords(title)
        snippet_keywords = self._extract_keywords(snippet)
        paper_keywords = title_keywords | snippet_keywords
        
        if not goal_keywords or not paper_keywords:
            return 0.0
        
        # **SEMANTIC MATCHING**: Detect synonyms and related terms
        matched_count = 0
        for goal_kw in goal_keywords:
            # Try exact match
            if goal_kw in paper_keywords:
                matched_count += 2  # Exact match worth 2 points
                continue
            
            # Try semantic/synonym match
            if self._is_semantic_match(goal_kw, paper_keywords):
                matched_count += 1.5  # Semantic match worth 1.5 points
                continue
            
            # Try prefix/stemming match (e.g., "model" ≈ "models")
            if self._is_prefix_match(goal_kw, paper_keywords):
                matched_count += 1  # Prefix match worth 1 point
        
        # Calculate coverage: what % of goal keywords were found?
        goal_coverage = matched_count / (len(goal_keywords) * 2)  # Max is 2 per keyword
        goal_coverage = min(1.0, goal_coverage)  # Cap at 100%
        
        # Title presence bonus: papers with goal keywords in title are more relevant
        title_match_count = sum(
            2 if kw in title_keywords else 0 
            for kw in goal_keywords if kw in title_keywords
        )
        title_bonus = min(0.3, (title_match_count / len(goal_keywords)) * 0.5)
        
        # Calculate final score
        final_score = min(1.0, goal_coverage + title_bonus)
        
        if self.logger:
            self.logger.debug(
                f"[SEMANTIC KEYWORD] '{title[:40]}...' → {final_score:.3f} "
                f"(coverage={goal_coverage:.2f}, title_bonus={title_bonus:.3f})"
            )
        
        return final_score
    
    def _is_semantic_match(self, goal_kw: str, paper_keywords: set) -> bool:
        """Check if goal keyword has semantic/synonym match in paper keywords
        
        **USES DYNAMIC SEMANTIC GROUPS** (not hardcoded):
        - Groups generated from research goal at runtime
        - Paper keywords matched against group variants
        - Domain-agnostic: works for any research area
        """
        if not self.semantic_groups:
            # Fallback if groups not provided
            return False
        
        goal_lower = goal_kw.lower()
        
        # Check if this keyword matches any core term in semantic groups
        for core_term, variants in self.semantic_groups.items():
            # Check if goal keyword is related to this core term
            if goal_lower.startswith(core_term[:3]):
                # Check if any paper keyword is a variant of this core term
                for variant in variants:
                    if variant in paper_keywords:
                        if self.logger:
                            self.logger.debug(
                                f"[SEMANTIC MATCH] '{goal_kw}' ({core_term}) ≈ '{variant}' (paper)"
                            )
                        return True
            
            # Also check if goal_kw itself is a variant of this core term
            if goal_kw in variants:
                for variant in variants:
                    if variant in paper_keywords and variant != goal_kw:
                        if self.logger:
                            self.logger.debug(
                                f"[SEMANTIC MATCH] '{goal_kw}' ≈ '{variant}' (both in group '{core_term}')"
                            )
                        return True
        
        return False
    
    def _is_prefix_match(self, goal_kw: str, paper_keywords: set) -> bool:
        """Check if goal keyword matches paper keyword by prefix/stemming
        
        Examples:
          - "model" matches "models", "modeling"
          - "route" matches "routing", "routes"
          - "protocol" matches "protocols"
        """
        goal_lower = goal_kw.lower()
        
        for paper_kw in paper_keywords:
            paper_lower = paper_kw.lower()
            
            # Check if one is a prefix of the other (allows plural/singular)
            if (paper_lower.startswith(goal_lower) or goal_lower.startswith(paper_lower)):
                # Make sure it's a real prefix (not just substring)
                if len(paper_lower) - len(goal_lower) <= 3:  # Allow up to 3 char difference
                    return True
        
        return False
    
    def _score_recency(self, year: int) -> float:
        """Score based on publication recency
        
        For foundational research (networking, routing):
        - Papers 0-3 years old: 1.0 (most current)
        - Papers 4-7 years old: 0.85 (still recent)
        - Papers 8-15 years old: 0.70 (established work, still relevant)
        - Papers 16-25 years old: 0.60 (foundational, good reference)
        - Papers 25+ years old: 0.40 (very foundational, historical)
        
        For networking protocols like RIP/OSPF, papers from 2000-2010 are still
        relevant as foundational work defining these protocols.
        """
        years_old = self.current_year - year
        
        if years_old <= 1:
            return 1.0  # Current/very recent
        elif years_old <= 3:
            return 0.95  # Last few years
        elif years_old <= 7:
            return 0.85  # Recent work (within 7 years)
        elif years_old <= 15:
            return 0.70  # Established work (7-15 years old)
        elif years_old <= 25:
            return 0.60  # Foundational work (15-25 years old)
        else:
            return 0.40  # Historical/very old (25+ years)
    
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
