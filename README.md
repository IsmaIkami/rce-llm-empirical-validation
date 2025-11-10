# RCE-LLM Empirical Validation

**Author:** Ismail Sialyen
**Publication DOI:** [10.5281/zenodo.17360372](https://doi.org/10.5281/zenodo.17360372)
**Purpose:** Empirical validation of RCE-LLM publication claims across F1-F5 task families
**For:** Scientific validation only (non-commercial use)

---

## Overview

This repository provides empirical validation for the RCE-LLM publication:
**"RCE-LLM: A Relational Coherence Engine for Consistent and Energy-Efficient Language Modeling"** by Ismail Sialyen (October 15, 2025).

All benchmarks use **real sources** cited in the publication and validate claims through actual RCE engine execution (NOT projected or hardcoded results).

---

## Task Families Evaluated

Based on publication Section 5.1 (pages 10-11):

### F1 - Units Consistency (8 queries)
Dimensional analysis problems requiring unit conversion and consistency checking.

**Example:** "A car travels 60 km/h for 30 minutes. How far in meters?"
**Coherence Modules:** µ_units, µ_arith
**Validation:** ±5% tolerance on numerical accuracy

### F2 - Temporal Reasoning (8 queries)
Time-based calculations involving scheduling, duration, and chronological ordering.

**Example:** "Meeting starts 9:30 AM, lasts 2h 45min. When does it end?"
**Coherence Modules:** µ_time, µ_arith
**Validation:** Exact time/duration matching

### F3 - Compositional Arithmetic (8 queries)
Multi-step word problems requiring arithmetic operations with numerical consistency.

**Example:** "Sarah has 12 apples. She gives 3 to Tom and buys 8 more. How many?"
**Coherence Modules:** µ_arith
**Validation:** ±5% tolerance on numerical accuracy

### F4 - Coreference Resolution (3 queries)
Winograd-style pronoun resolution tasks with consistency requirements.

**Example:** "The trophy doesn't fit in the suitcase because it is too large. What is too large?"
**Coherence Modules:** µ_coref
**Validation:** Antecedent accuracy

### F5 - Factual Grounding (3 queries)
Question-answering tasks requiring specific URL citations with entailment verification.

**Example:** "What is the capital of France?"
**Coherence Modules:** µ_entail
**Validation:** Entailment score ≥ 0.9 + URL citation

**Total:** 30 queries across 5 task families

---

## Baseline Systems

Aligned with publication Table 1 (page 12):

1. **LLM:** Groq (Llama 3.3 70B) via Groq Cloud API (no retrieval, no validation)
2. **LLM+RAG:** Retrieval-augmented generation with DuckDuckGo search + Groq (Llama 3.3 70B)
3. **RCE-LLM:** Full end-to-end relational coherence optimization (publication Algorithm 1)

---

## Repository Structure

```
rce-llm-empirical-validation/
├── README.md                            # This file
├── LICENSE                              # Tri-partite academic license
├── LICENSING_PROTECTION.md              # IP protection guide
├── SIMPLIFIED_IMPLEMENTATION_PLAN.md    # Implementation roadmap (8-12h)
├── PROGRESS_SUMMARY.md                  # Current status summary
├── datasets/
│   ├── f1_units/queries.json            # ✓ 8 queries
│   ├── f2_temporal/queries.json         # ✓ 8 queries
│   ├── f3_arithmetic/queries.json       # ✓ 8 queries
│   ├── f4_coreference/queries.json      # ✓ 3 queries
│   └── f5_factual/queries.json          # ✓ 3 queries
├── results/                             # Benchmark results (to be generated)
│   ├── f1_results.json
│   ├── f2_results.json
│   ├── f3_results.json
│   ├── f4_results.json
│   ├── f5_results.json
│   └── statistical_analysis.md
├── docs/                                # Static results page (to be created)
│   └── index.html
└── scripts/                             # Benchmark execution scripts
    └── run_benchmarks.sh
```

---

## Next Steps

### Immediate Actions Required:

1. **Verify RCE Engine Status**
   ```bash
   # Check if RCE API is running
   curl -X POST http://localhost:8000/api/v1/query \
     -H "Content-Type: application/json" \
     -d '{"query": "test", "domain": "general"}'
   ```

2. **Run Benchmarks**
   ```bash
   cd /Users/isma/Projects/RCE/rce-llm-empirical-validation
   # Script to be created: will execute all 30 queries through 3 systems
   bash scripts/run_benchmarks.sh
   ```

3. **Generate Statistical Analysis**
   - Compute accuracy per task family
   - Perform statistical tests (ANOVA, t-tests)
   - Calculate effect sizes (Cohen's d/h)
   - Validate publication hypotheses H₁-H₄

4. **Create Results Page**
   - Static HTML with verbose pipeline mode
   - Display benchmark results
   - Show pipeline execution traces
   - Enable toggle for detailed view

5. **Deploy to GitHub Pages**
   - Push repository to GitHub
   - Enable Pages deployment
   - Link from publication DOI record

---

## Key Features

### ✅ Real Sources (NOT Hardcoded)
- F1: NIST standards, physics formulas (Newton's laws, F=ma)
- F2: Standard time calculations, duration arithmetic
- F3: GSM8K-inspired word problems
- F4: Winograd Schema Challenge examples
- F5: Wikipedia/factual database queries

### ✅ Publication Alignment
- Queries match examples from pages 10-11
- Task families exactly as defined in Section 5.1
- Validation metrics match Table 1 specifications
- Coherence modules (µ_units, µ_time, µ_arith, µ_coref, µ_entail) mapped

### ✅ Proprietary Core Protection
- Tri-partite license (MIT + CC BY 4.0 + Proprietary)
- RCE core algorithms NOT disclosed
- Black-box API access only
- Same licensing as agreed in rce-scientific-evidence

### ✅ Scientific Rigor
- Ground truth values for all queries
- Validation tolerances defined
- Statistical tests planned (ANOVA, effect sizes)
- Reproducible benchmark scripts

---

## License

**Tri-partite Academic License:**

- **Benchmark Scripts:** MIT License (freely usable)
- **Documentation:** CC BY 4.0 (attribution required)
- **RCE Core:** Proprietary (not included in this repository)

See [LICENSE](LICENSE) and [LICENSING_PROTECTION.md](LICENSING_PROTECTION.md) for full details.

---

## Citation

If you use this validation repository, please cite:

```bibtex
@software{sialyen2025rce_validation,
  author = {Sialyen, Ismail},
  title = {RCE-LLM Empirical Validation: F1-F5 Task Families},
  year = {2025},
  doi = {10.5281/zenodo.17360372},
  url = {https://github.com/ismailsialyen/rce-llm-empirical-validation}
}
```

---

## Contact

**For Scientific Validation Questions:**
Open an issue in this repository

**For RCE Engine Access:**
Contact via publication email (is.sialyen@gmail.com)

**For Commercial Licensing:**
See LICENSING_PROTECTION.md

---

*Prepared by: Ismail Sialyen*
*Date: November 10, 2025*
*Repository: /Users/isma/Projects/RCE/rce-llm-empirical-validation*
*Purpose: Scientific validation of DOI 10.5281/zenodo.17360372*
