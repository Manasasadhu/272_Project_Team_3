# Agent Memory & Learning System

## Overview

The agent now has a **memory system** that enables it to learn and evolve over time, improving autonomy and quality with each execution.

## How It Works

### 1. **Search Pattern Learning**
- **Stores**: Successful search queries with success rates
- **Uses**: Similar queries for similar research goals
- **Evolution**: Agent learns which query patterns work best

```python
# Example: After executing "distributed consensus blockchain"
# Agent learns: Query "distributed consensus protocols blockchain 2024" has 85% success rate
# Next similar goal → Agent uses this proven pattern
```

### 2. **Source Quality Learning**
- **Stores**: Quality metrics for sources (citations, extraction success, venue)
- **Uses**: Prioritize known high-quality sources
- **Evolution**: Agent learns which sources/venues are reliable

```python
# Example: Agent learns that sources from "IEEE" have 95% extraction success
# Future searches → Prioritize IEEE sources
```

### 3. **Execution Strategy Learning**
- **Stores**: What strategies worked for similar goals
- **Uses**: Adapt strategy based on past success
- **Evolution**: Agent optimizes execution approach per domain

```python
# Example: For "blockchain consensus" goals:
# - Strategy A: 3 queries, 20 sources each → 80% success
# - Strategy B: 5 queries, 10 sources each → 60% success
# Future → Agent prefers Strategy A
```

### 4. **Domain Knowledge Building**
- **Stores**: Key themes, top sources, effective queries per domain
- **Uses**: Enhance planning with domain-specific knowledge
- **Evolution**: Agent becomes domain expert over time

```python
# Example: After multiple "federated learning" jobs:
# Agent builds knowledge base: key themes, reliable sources, proven queries
# Next federated learning goal → Agent uses accumulated knowledge
```

### 5. **Performance Metrics Tracking**
- **Stores**: Execution time, success rates, quality scores
- **Uses**: Track improvement trends
- **Evolution**: Agent monitors own performance and adapts

## Memory Storage

All memory is stored in **Redis** with 30-day TTL:
- `memory:search_pattern:*` - Successful query patterns
- `memory:source_quality:*` - Source quality metrics
- `memory:strategy:*` - Effective strategies per goal type
- `memory:domain:*` - Domain-specific knowledge
- `memory:performance:*` - Performance metrics

## Evolution Timeline

### **Initial State (Day 1)**
- No memory, starts from scratch
- Uses default LLM-generated queries
- No prior knowledge

### **Week 1**
- Builds initial pattern library
- Learns effective search queries
- Identifies reliable sources

### **Month 1**
- Strong pattern recognition
- Domain knowledge emerging
- Optimized strategies per domain

### **Ongoing**
- Continuous improvement
- Adapts to new domains
- Self-optimizes strategies

## Benefits

1. **Better Planning**: Uses proven query patterns
2. **Faster Execution**: Prioritizes known good sources
3. **Higher Quality**: Learns which sources/venues are reliable
4. **Domain Expertise**: Accumulates knowledge per domain
5. **Self-Optimization**: Improves strategies based on outcomes

## Future Enhancements

1. **User Feedback Loop**: Incorporate user ratings to improve
2. **Embedding-Based Similarity**: Better pattern matching
3. **Cross-Domain Transfer**: Apply knowledge across domains
4. **Predictive Quality**: Predict source quality before extraction
5. **Automated Strategy Tuning**: Auto-optimize execution parameters

