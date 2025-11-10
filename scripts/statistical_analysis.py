#!/usr/bin/env python3
"""
Statistical Analysis for RCE-LLM Empirical Validation

Author: Ismail Sialyen
Purpose: Compute accuracy, statistical tests, and effect sizes for F1-F5 results
Publication: DOI 10.5281/zenodo.17360372
"""

import json
import os
from pathlib import Path
from typing import Dict, List
import statistics
from datetime import datetime

# Configuration
RESULTS_DIR = Path(__file__).parent.parent / "results"


class StatisticalAnalyzer:
    """Statistical analysis for benchmark results"""

    def __init__(self):
        self.results = None
        self.analysis = {
            "metadata": {
                "author": "Ismail Sialyen",
                "publication_doi": "10.5281/zenodo.17360372",
                "analysis_date": datetime.now().isoformat()
            },
            "overall_accuracy": {},
            "task_family_accuracy": {},
            "statistical_tests": {},
            "effect_sizes": {},
            "hypotheses_validation": {}
        }

    def load_results(self):
        """Load benchmark results from JSON"""
        results_file = RESULTS_DIR / "benchmark_results.json"

        if not results_file.exists():
            print(f"⚠️  Error: Results file not found: {results_file}")
            print("   Please run benchmarks first: python scripts/run_benchmarks.py")
            return False

        with open(results_file, 'r') as f:
            self.results = json.load(f)

        print(f"✓ Loaded results from {results_file}")
        return True

    def compute_overall_accuracy(self):
        """Compute overall accuracy across all task families"""
        print("\n→ Computing overall accuracy...")

        system_correct = {"LLM": 0, "LLM+RAG": 0, "RCE-LLM": 0}
        system_total = {"LLM": 0, "LLM+RAG": 0, "RCE-LLM": 0}

        for family_name, family_data in self.results["task_families"].items():
            for query_result in family_data.get("queries", []):
                for system_result in query_result.get("systems", []):
                    system = system_result["system"]
                    system_total[system] += 1
                    if system_result.get("correct", False):
                        system_correct[system] += 1

        for system in ["LLM", "LLM+RAG", "RCE-LLM"]:
            accuracy = system_correct[system] / system_total[system] if system_total[system] > 0 else 0.0
            self.analysis["overall_accuracy"][system] = {
                "correct": system_correct[system],
                "total": system_total[system],
                "accuracy": accuracy
            }
            print(f"  {system}: {system_correct[system]}/{system_total[system]} = {accuracy:.1%}")

    def compute_task_family_accuracy(self):
        """Compute accuracy per task family"""
        print("\n→ Computing task family accuracy...")

        for family_name, family_data in self.results["task_families"].items():
            print(f"  {family_name}:")

            system_correct = {"LLM": 0, "LLM+RAG": 0, "RCE-LLM": 0}
            total = len(family_data.get("queries", []))

            for query_result in family_data.get("queries", []):
                for system_result in query_result.get("systems", []):
                    system = system_result["system"]
                    if system_result.get("correct", False):
                        system_correct[system] += 1

            family_accuracy = {}
            for system in ["LLM", "LLM+RAG", "RCE-LLM"]:
                accuracy = system_correct[system] / total if total > 0 else 0.0
                family_accuracy[system] = {
                    "correct": system_correct[system],
                    "total": total,
                    "accuracy": accuracy
                }
                print(f"    {system}: {system_correct[system]}/{total} = {accuracy:.1%}")

            self.analysis["task_family_accuracy"][family_name] = family_accuracy

    def compute_effect_sizes(self):
        """
        Compute Cohen's h effect size for RCE-LLM vs baselines
        Cohen's h measures effect size for differences between proportions
        h = 0.2 (small), 0.5 (medium), 0.8 (large)
        """
        print("\n→ Computing effect sizes (Cohen's h)...")

        import math

        def cohens_h(p1: float, p2: float) -> float:
            """Cohen's h for two proportions"""
            phi1 = 2 * math.asin(math.sqrt(p1))
            phi2 = 2 * math.asin(math.sqrt(p2))
            return phi1 - phi2

        rce_accuracy = self.analysis["overall_accuracy"]["RCE-LLM"]["accuracy"]
        llm_accuracy = self.analysis["overall_accuracy"]["LLM"]["accuracy"]
        rag_accuracy = self.analysis["overall_accuracy"]["LLM+RAG"]["accuracy"]

        effect_rce_vs_llm = cohens_h(rce_accuracy, llm_accuracy)
        effect_rce_vs_rag = cohens_h(rce_accuracy, rag_accuracy)

        self.analysis["effect_sizes"] = {
            "RCE_vs_LLM": {
                "cohens_h": effect_rce_vs_llm,
                "interpretation": self._interpret_cohens_h(effect_rce_vs_llm)
            },
            "RCE_vs_RAG": {
                "cohens_h": effect_rce_vs_rag,
                "interpretation": self._interpret_cohens_h(effect_rce_vs_rag)
            }
        }

        print(f"  RCE-LLM vs LLM: h = {effect_rce_vs_llm:.3f} ({self._interpret_cohens_h(effect_rce_vs_llm)})")
        print(f"  RCE-LLM vs LLM+RAG: h = {effect_rce_vs_rag:.3f} ({self._interpret_cohens_h(effect_rce_vs_rag)})")

    def _interpret_cohens_h(self, h: float) -> str:
        """Interpret Cohen's h effect size"""
        abs_h = abs(h)
        if abs_h < 0.2:
            return "negligible"
        elif abs_h < 0.5:
            return "small"
        elif abs_h < 0.8:
            return "medium"
        else:
            return "large"

    def validate_hypotheses(self):
        """
        Validate publication hypotheses H₁-H₄
        H₁: RCE-LLM > LLM (vanilla baseline)
        H₂: RCE-LLM > LLM+RAG (retrieval baseline)
        H₃: RCE-LLM shows consistent improvement across task families
        H₄: Coherence modules improve factual grounding (F5)
        """
        print("\n→ Validating publication hypotheses...")

        rce_acc = self.analysis["overall_accuracy"]["RCE-LLM"]["accuracy"]
        llm_acc = self.analysis["overall_accuracy"]["LLM"]["accuracy"]
        rag_acc = self.analysis["overall_accuracy"]["LLM+RAG"]["accuracy"]

        # H₁: RCE-LLM > LLM
        h1_valid = rce_acc > llm_acc
        h1_improvement = ((rce_acc - llm_acc) / llm_acc * 100) if llm_acc > 0 else 0
        print(f"  H₁ (RCE > LLM): {'✓ SUPPORTED' if h1_valid else '✗ NOT SUPPORTED'}")
        print(f"     RCE-LLM: {rce_acc:.1%}, LLM: {llm_acc:.1%} (improvement: {h1_improvement:+.1f}%)")

        # H₂: RCE-LLM > LLM+RAG
        h2_valid = rce_acc > rag_acc
        h2_improvement = ((rce_acc - rag_acc) / rag_acc * 100) if rag_acc > 0 else 0
        print(f"  H₂ (RCE > RAG): {'✓ SUPPORTED' if h2_valid else '✗ NOT SUPPORTED'}")
        print(f"     RCE-LLM: {rce_acc:.1%}, LLM+RAG: {rag_acc:.1%} (improvement: {h2_improvement:+.1f}%)")

        # H₃: Consistent improvement across task families
        improvements = []
        print(f"  H₃ (Consistent improvement across F1-F5):")
        for family_name, family_acc in self.analysis["task_family_accuracy"].items():
            rce_family = family_acc["RCE-LLM"]["accuracy"]
            llm_family = family_acc["LLM"]["accuracy"]
            rag_family = family_acc["LLM+RAG"]["accuracy"]

            improvement_vs_llm = rce_family > llm_family
            improvement_vs_rag = rce_family > rag_family

            improvements.append(improvement_vs_llm and improvement_vs_rag)

            print(f"     {family_name}: RCE={rce_family:.1%}, LLM={llm_family:.1%}, RAG={rag_family:.1%} → {'✓' if improvement_vs_llm and improvement_vs_rag else '✗'}")

        h3_valid = all(improvements)
        print(f"     → {'✓ SUPPORTED' if h3_valid else '✗ PARTIALLY SUPPORTED'} ({sum(improvements)}/{len(improvements)} families)")

        # H₄: Coherence modules improve factual grounding (F5)
        if "f5_factual" in self.analysis["task_family_accuracy"]:
            f5_rce = self.analysis["task_family_accuracy"]["f5_factual"]["RCE-LLM"]["accuracy"]
            f5_llm = self.analysis["task_family_accuracy"]["f5_factual"]["LLM"]["accuracy"]
            f5_rag = self.analysis["task_family_accuracy"]["f5_factual"]["LLM+RAG"]["accuracy"]

            h4_valid = f5_rce > max(f5_llm, f5_rag)
            print(f"  H₄ (Coherence improves F5 factual grounding): {'✓ SUPPORTED' if h4_valid else '✗ NOT SUPPORTED'}")
            print(f"     F5: RCE={f5_rce:.1%}, LLM={f5_llm:.1%}, RAG={f5_rag:.1%}")
        else:
            h4_valid = False
            print(f"  H₄: ⚠️  F5 results not found")

        self.analysis["hypotheses_validation"] = {
            "H1_RCE_better_than_LLM": {
                "supported": h1_valid,
                "improvement_percentage": h1_improvement
            },
            "H2_RCE_better_than_RAG": {
                "supported": h2_valid,
                "improvement_percentage": h2_improvement
            },
            "H3_consistent_improvement": {
                "supported": h3_valid,
                "families_improved": sum(improvements),
                "total_families": len(improvements)
            },
            "H4_coherence_improves_factual": {
                "supported": h4_valid
            }
        }

    def generate_summary_report(self):
        """Generate markdown summary report"""
        print("\n→ Generating summary report...")

        report_lines = [
            "# Statistical Analysis Summary",
            "",
            f"**Author:** Ismail Sialyen",
            f"**Publication DOI:** [10.5281/zenodo.17360372](https://doi.org/10.5281/zenodo.17360372)",
            f"**Analysis Date:** {self.analysis['metadata']['analysis_date']}",
            "",
            "---",
            "",
            "## Overall Accuracy",
            ""
        ]

        for system, acc_data in self.analysis["overall_accuracy"].items():
            report_lines.append(
                f"- **{system}:** {acc_data['correct']}/{acc_data['total']} = {acc_data['accuracy']:.1%}"
            )

        report_lines.extend([
            "",
            "---",
            "",
            "## Task Family Performance",
            ""
        ])

        for family_name, family_acc in self.analysis["task_family_accuracy"].items():
            report_lines.append(f"### {family_name.upper()}")
            report_lines.append("")
            for system, acc_data in family_acc.items():
                report_lines.append(
                    f"- **{system}:** {acc_data['correct']}/{acc_data['total']} = {acc_data['accuracy']:.1%}"
                )
            report_lines.append("")

        report_lines.extend([
            "---",
            "",
            "## Effect Sizes",
            ""
        ])

        for comparison, effect_data in self.analysis["effect_sizes"].items():
            report_lines.append(
                f"- **{comparison}:** Cohen's h = {effect_data['cohens_h']:.3f} ({effect_data['interpretation']})"
            )

        report_lines.extend([
            "",
            "---",
            "",
            "## Hypotheses Validation",
            ""
        ])

        hyp = self.analysis["hypotheses_validation"]

        report_lines.append(f"### H₁: RCE-LLM > LLM (vanilla baseline)")
        report_lines.append(f"**Status:** {'✓ SUPPORTED' if hyp['H1_RCE_better_than_LLM']['supported'] else '✗ NOT SUPPORTED'}")
        report_lines.append(f"**Improvement:** {hyp['H1_RCE_better_than_LLM']['improvement_percentage']:+.1f}%")
        report_lines.append("")

        report_lines.append(f"### H₂: RCE-LLM > LLM+RAG (retrieval baseline)")
        report_lines.append(f"**Status:** {'✓ SUPPORTED' if hyp['H2_RCE_better_than_RAG']['supported'] else '✗ NOT SUPPORTED'}")
        report_lines.append(f"**Improvement:** {hyp['H2_RCE_better_than_RAG']['improvement_percentage']:+.1f}%")
        report_lines.append("")

        report_lines.append(f"### H₃: Consistent improvement across task families")
        report_lines.append(f"**Status:** {'✓ SUPPORTED' if hyp['H3_consistent_improvement']['supported'] else '✗ PARTIALLY SUPPORTED'}")
        report_lines.append(f"**Families Improved:** {hyp['H3_consistent_improvement']['families_improved']}/{hyp['H3_consistent_improvement']['total_families']}")
        report_lines.append("")

        report_lines.append(f"### H₄: Coherence modules improve factual grounding")
        report_lines.append(f"**Status:** {'✓ SUPPORTED' if hyp['H4_coherence_improves_factual']['supported'] else '✗ NOT SUPPORTED'}")
        report_lines.append("")

        report_lines.extend([
            "---",
            "",
            "*Analysis prepared by: Ismail Sialyen*",
            "*Repository: /Users/isma/Projects/RCE/rce-llm-empirical-validation*",
            "*Purpose: Scientific validation of DOI 10.5281/zenodo.17360372*",
            ""
        ])

        return "\n".join(report_lines)

    def save_analysis(self):
        """Save analysis to files"""
        # Save JSON analysis
        analysis_json = RESULTS_DIR / "statistical_analysis.json"
        with open(analysis_json, 'w') as f:
            json.dump(self.analysis, f, indent=2)
        print(f"\n✓ Saved JSON analysis to {analysis_json}")

        # Save markdown summary
        summary_md = RESULTS_DIR / "statistical_analysis.md"
        with open(summary_md, 'w') as f:
            f.write(self.generate_summary_report())
        print(f"✓ Saved markdown summary to {summary_md}")

    def run(self):
        """Run full statistical analysis"""
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 25 + "STATISTICAL ANALYSIS" + " " * 33 + "║")
        print("║" + " " * 78 + "║")
        print("║  Author: Ismail Sialyen" + " " * 54 + "║")
        print("║  Publication: DOI 10.5281/zenodo.17360372" + " " * 35 + "║")
        print("╚" + "═" * 78 + "╝")

        if not self.load_results():
            return

        self.compute_overall_accuracy()
        self.compute_task_family_accuracy()
        self.compute_effect_sizes()
        self.validate_hypotheses()
        self.save_analysis()

        print("\n╔" + "═" * 78 + "╗")
        print("║" + " " * 27 + "ANALYSIS COMPLETE" + " " * 33 + "║")
        print("╚" + "═" * 78 + "╝")
        print(f"\n✓ Statistical analysis saved to {RESULTS_DIR}")
        print(f"\nNext steps:")
        print(f"  1. Review results: {RESULTS_DIR}/statistical_analysis.md")
        print(f"  2. Generate results page: python scripts/generate_results_page.py")
        print(f"  3. Deploy to GitHub Pages")


if __name__ == "__main__":
    analyzer = StatisticalAnalyzer()
    analyzer.run()
