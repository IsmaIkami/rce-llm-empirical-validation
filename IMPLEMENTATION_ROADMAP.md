# RCE-LLM Empirical Validation - Implementation Roadmap

**Author:** Ismail Sialyen
**Date:** November 10, 2025
**Purpose:** Full empirical validation of RCE-LLM publication claims
**Repository:** rce-llm-empirical-validation

---

## ✅ APPROVED SCOPE

### Deliverables:
1. **1000 queries** across F1-F5 task families (200 each)
2. **4 baseline systems** implemented and benchmarked
3. **Static results page** with verbose pipeline details
4. **Full statistical validation** aligned with publication Table 1
5. **Computational profiling** (complexity, energy)
6. **Same layout/design** as original interface

### No Interactive Testing:
- Results presentation only (no query input)
- Pre-computed benchmarks displayed
- Verbose mode for pipeline inspection

---

## PHASE 1: Dataset Generation (4-6 hours)

### Task 1.1: F1 - Units Consistency (200 queries)
**Aligned with Publication (p. 10):**
> "Dimensional analysis problems requiring unit conversion and consistency checking"

**Generation Strategy:**
```python
# Examples:
- "A car travels 60 km/h for 30 minutes. How far in meters?"
- "Convert 100 kg·m/s² to Newtons"
- "If pressure is 101,325 Pa, what is it in atmospheres?"
```

**Validation Method:** Automated ±5% tolerance
**Source:** Programmatically generated with dimensional patterns

---

### Task 1.2: F2 - Temporal Reasoning (200 queries)
**Aligned with Publication (p. 10):**
> "Time-based calculations involving scheduling, duration, and chronological ordering"

**Generation Strategy:**
```python
# Examples:
- "Meeting starts 9:30 AM, lasts 2h 45min. When does it end?"
- "Event A at 14:00, Event B 3 hours later. What time is Event B?"
- "Flight departs 08:15, arrives 13:40. Flight duration?"
```

**Validation Method:** Exact time/duration matching
**Source:** Programmatically generated time calculation patterns

---

### Task 1.3: F3 - Compositional Arithmetic (200 queries)
**Aligned with Publication (p. 11):**
> "Multi-step word problems requiring arithmetic operations with numerical consistency"

**Generation Strategy:**
```python
# Examples (GSM8K-style):
- "Sarah has 12 apples. She gives 3 to Tom and buys 8 more. How many apples does Sarah have?"
- "A store sells shirts for $15 each. If you buy 4 shirts with a 10% discount, how much do you pay?"
```

**Validation Method:** Exact numerical accuracy ±5%
**Source:** GSM8K-inspired patterns with distractors

---

### Task 1.4: F4 - Coreference Resolution (200 queries)
**Aligned with Publication (p. 11):**
> "Winograd-style pronoun resolution tasks with consistency requirements across paraphrases"

**Generation Strategy:**
```python
# Examples:
- "The trophy doesn't fit in the suitcase because it is too large. What is too large?"
- "Alice told Bob that she would help him. Who will help whom?"
```

**Validation Method:** Antecedent accuracy matching
**Source:** Winograd schema + generated paraphrases

---

### Task 1.5: F5 - Factual Grounding (200 queries)
**Aligned with Publication (p. 11):**
> "Question-answering tasks requiring specific URL citations with entailment verification"

**Generation Strategy:**
```python
# Examples:
- "What is the capital of France?" → Requires source URL
- "Who wrote '1984'?" → Requires factual citation
```

**Validation Method:** Entailment score ≥ 0.9 + URL citation
**Source:** Real knowledge base queries from Wikipedia/factual databases

---

## PHASE 2: Baseline Implementation (3-4 hours)

### Task 2.1: LLM Baseline
**Aligned with Publication (p. 11):**
> "Vanilla language model with standard decoding"

**Implementation:**
```python
def llm_baseline(query):
    """Pure Llama 3.2 without retrieval or validation"""
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": query}],
        options={"temperature": 0.1}
    )
    return response['message']['content']
```

---

### Task 2.2: LLM+RAG Baseline
**Aligned with Publication (p. 11):**
> "Retrieval-augmented generation with document retrieval"

**Implementation:**
```python
def llm_rag_baseline(query):
    """Llama 3.2 + retrieval (no RCE validation)"""
    # 1. Retrieve documents
    docs = duckduckgo_search(query, max_results=5)

    # 2. Construct prompt with retrieved context
    prompt = f"Context: {docs}\n\nQuestion: {query}\n\nAnswer:"

    # 3. Generate without validation
    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']
```

---

### Task 2.3: RCE-verify Baseline
**Aligned with Publication (p. 11):**
> "RCE-LLM used as a post-processing verifier/reranker for LLM outputs"

**Implementation:**
```python
def rce_verify_baseline(query):
    """LLM generation → RCE post-processing verification"""
    # 1. Generate answer with LLM
    llm_answer = llm_baseline(query)

    # 2. Use RCE to verify and potentially rerank
    rce_score = rce_engine.verify(llm_answer, query)

    # 3. If coherence < threshold, regenerate
    if rce_score < 0.7:
        return llm_rag_baseline(query)  # Fallback to RAG
    return llm_answer
```

---

### Task 2.4: RCE-LLM (Full Pipeline)
**Aligned with Publication (Algorithm 1, p. 10):**
> "Full end-to-end relational coherence optimization"

**Implementation:** Use existing RCE engine at `/Users/isma/Projects/RCE/rce-deployment`

---

## PHASE 3: Benchmark Execution (6-8 hours)

### Task 3.1: Run 1000 Queries
```bash
#!/bin/bash
# scripts/run_full_benchmark.sh

for family in f1_units f2_temporal f3_arithmetic f4_coreference f5_factual; do
    echo "Running $family benchmarks..."

    for system in llm llm_rag rce_verify rce_llm; do
        python scripts/benchmark_system.py \
            --system $system \
            --dataset datasets/$family/queries.json \
            --output results/${family}_${system}.json
    done
done
```

**Expected Runtime:** ~6-8 hours (1000 queries × 4 systems × ~8s per query)

---

### Task 3.2: Collect Metrics
For each query, record:
- Answer
- F1-Score (F1, F2, F3 families)
- Temporal correctness (F2 family)
- Antecedent accuracy (F4 family)
- Entailment score + URL citation (F5 family)
- Processing time (ms)
- GPU power consumption (W)
- |R| (number of relations)
- n (sequence length)
- Sparsity factor ρ = |R|/n²

---

## PHASE 4: Statistical Analysis (2-3 hours)

### Task 4.1: Compute Aggregate Metrics
**Aligned with Publication (Table 1, p. 12):**

```python
# For each task family F1-F5:
accuracy_by_family = {
    'F1': {
        'LLM': compute_accuracy(results['f1_units']['llm']),
        'LLM+RAG': compute_accuracy(results['f1_units']['llm_rag']),
        'RCE-verify': compute_accuracy(results['f1_units']['rce_verify']),
        'RCE-LLM': compute_accuracy(results['f1_units']['rce_llm'])
    },
    ...
}
```

---

### Task 4.2: Statistical Significance Tests
**Aligned with Publication (Section 5.2, p. 11):**

```python
# ANOVA across 3 systems
f_stat, p_value = scipy.stats.f_oneway(
    rce_llm_scores,
    llm_rag_scores,
    llm_scores
)

# Bonferroni correction for pairwise comparisons
bonferroni_alpha = 0.05 / 3  # 3 comparisons

# Effect size calculations
cohen_d = (mean_rce - mean_rag) / pooled_std
```

---

### Task 4.3: Power Analysis
Ensure n=200 per family provides power > 0.80 for detecting large effects

---

## PHASE 5: Computational Profiling (2-3 hours)

### Task 5.1: Complexity Measurements
**Aligned with Publication (Section 6.1, p. 12):**

```python
# For each RCE query:
profile = {
    'n': sequence_length,
    '|R|': num_relations,
    'rho': num_relations / (sequence_length ** 2),
    'time_retrieval_ms': t1,
    'time_graph_construction_ms': t2,
    'time_coherence_eval_ms': t3,
    'time_optimization_ms': t4,
    'time_generation_ms': t5,
    'total_time_ms': sum([t1, t2, t3, t4, t5])
}
```

**Expected Result:** ρ ≈ 0.1-0.3 (demonstrating sparsity)

---

### Task 5.2: Energy Measurements
**Aligned with Publication (Table 2, p. 13):**

```bash
# Monitor GPU power during benchmark
nvidia-smi --query-gpu=power.draw --format=csv,noheader,nounits -l 1 > gpu_power.log

# Calculate energy consumption
energy_kwh = (average_power_watts * time_hours) / 1000
co2_kg = energy_kwh * 0.5  # Grid carbon intensity
```

---

## PHASE 6: Static Results Page with Verbose Mode (3-4 hours)

### Task 6.1: Main Results Page
**Layout:** Same as existing interface (docs/index.html)

**Content Sections:**
1. **Hero Section:** Publication title + DOI
2. **Hypothesis Validation Cards:** H₁-H₄ with badges
3. **Performance Table:** Replicate Table 1 with 1000-query results
4. **Pipeline Architecture:** 6-stage diagram
5. **Verbose Toggle:** Button to expand detailed metrics

---

### Task 6.2: Verbose Mode Implementation
**For each pipeline stage, show:**

**📥 Stage 1: Retrieval (Verbose)**
```
Domain: {domain}
Search Engine: DuckDuckGo
Retrieved Documents: {num_docs}
Source Tokens: {tokens}
Retrieval Time: {ms}ms
Average Confidence: {conf}

Retrieved Facts:
1. "{fact1}" [confidence: {c1}]
2. "{fact2}" [confidence: {c2}]
...
```

**🕸️ Stage 3: Graph Construction (Verbose)**
```
Vertices (V): {num_vertices}
Relations (R): {num_relations}
Sparsity: |R|/n² = {rho}

Entity Embeddings:
- Dimension: 96D (spaCy)
- Total Elements: {V × 96}
- Memory: {kb} KB

Constructed Relations:
1. (entity1, relation_type, entity2) [confidence: {c}]
...
```

**📊 Stage 4: Coherence Evaluation (Verbose)**
```
Module Evaluations:
┌─────────────────────────────────────┐
│ μ_units (Dimensional Analysis)      │
├─────────────────────────────────────┤
│ Status: applicable / not_applicable │
│ Score: {score}                      │
│ Details: ...                        │
└─────────────────────────────────────┘

Weighted Coherence:
μ(Ω|C) = Σ w_k × μ_k
       = {w1}×{μ1} + ... + {w5}×{μ5}
       = {final_coherence}
```

---

### Task 6.3: Results Presentation
Display pre-computed results from 1000-query benchmark:
- Table 1 reproduction with actual data
- Per-family breakdowns
- Statistical significance indicators
- Energy efficiency comparisons

---

## PHASE 7: Documentation & Validation (2-3 hours)

### Task 7.1: README.md
Document:
- Repository purpose
- How to reproduce benchmarks
- Citation information
- Link to publication

---

### Task 7.2: Publication Alignment Checklist
Verify every claim in publication is substantiated:
- [x] Table 1 (F1-F5 performance)
- [x] Complexity reduction (Section 6.1)
- [x] Energy efficiency (Table 2)
- [x] 4 baselines (Section 5.2)
- [x] Statistical validation
- [x] Verbose pipeline trace

---

## TOTAL TIMELINE: 20-28 HOURS

### Breakdown:
1. Dataset Generation: 4-6h
2. Baseline Implementation: 3-4h
3. Benchmark Execution: 6-8h
4. Statistical Analysis: 2-3h
5. Computational Profiling: 2-3h
6. Results Page: 3-4h
7. Documentation: 2-3h

---

## NEXT STEPS

**Awaiting your approval to proceed with:**
1. ✅ Phase 1: Generate 1000 queries across F1-F5
2. ✅ Phase 2: Implement 4 baselines
3. ✅ Phase 3: Run benchmarks (6-8 hour execution)
4. ✅ Phase 4-7: Analysis, profiling, visualization, docs

**Once approved, I'll begin with Phase 1 (dataset generation).**

---

*Author: Ismail Sialyen*
*Date: November 10, 2025*
*Repository: /Users/isma/Projects/RCE/rce-llm-empirical-validation*
