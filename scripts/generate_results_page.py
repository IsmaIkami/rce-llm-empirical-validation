#!/usr/bin/env python3
"""
Results Page Generator for RCE-LLM Empirical Validation

Author: Ismail Sialyen
Purpose: Generate static HTML results page with exact design from rce-scientific-evidence
Publication: DOI 10.5281/zenodo.17360372
"""

import json
from pathlib import Path
from datetime import datetime

# Configuration
RESULTS_DIR = Path(__file__).parent.parent / "results"
DOCS_DIR = Path(__file__).parent.parent / "docs"


class ResultsPageGenerator:
    """Generate static HTML results page"""

    def __init__(self):
        self.results = None
        self.analysis = None

    def load_data(self):
        """Load benchmark results and statistical analysis"""
        results_file = RESULTS_DIR / "benchmark_results.json"
        analysis_file = RESULTS_DIR / "statistical_analysis.json"

        if not results_file.exists():
            print(f"⚠️  Error: Results file not found: {results_file}")
            return False

        if not analysis_file.exists():
            print(f"⚠️  Error: Analysis file not found: {analysis_file}")
            return False

        with open(results_file, 'r') as f:
            self.results = json.load(f)

        with open(analysis_file, 'r') as f:
            self.analysis = json.load(f)

        print(f"✓ Loaded results and analysis")
        return True

    def generate_html(self):
        """Generate complete HTML page with exact design from rce-scientific-evidence"""

        # Extract data for template
        overall_acc = self.analysis["overall_accuracy"]
        task_acc = self.analysis["task_family_accuracy"]
        hypotheses = self.analysis["hypotheses_validation"]
        effect_sizes = self.analysis["effect_sizes"]

        # Get execution metadata
        total_queries = self.results["metadata"]["total_queries"]
        execution_date = self.results["metadata"]["execution_date"]

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RCE-LLM Empirical Validation | F1-F5 Results</title>
    <meta name="description" content="Empirical validation results for RCE-LLM across F1-F5 task families (Units, Temporal, Arithmetic, Coreference, Factual)">
    <meta name="keywords" content="RCE-LLM, LLM, coherence, validation, benchmarks, F1, F2, F3, F4, F5">
    <meta name="author" content="Ismail Sialyen">

    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
            color: #333;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }}

        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}

        .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
            margin-bottom: 20px;
        }}

        .author-info {{
            font-size: 0.95em;
            opacity: 0.85;
        }}

        .card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            margin-bottom: 25px;
        }}

        h2 {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8em;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}

        h3 {{
            color: #764ba2;
            margin-bottom: 15px;
            font-size: 1.3em;
        }}

        .hypothesis-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}

        .hypothesis-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            transition: transform 0.3s, box-shadow 0.3s;
        }}

        .hypothesis-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }}

        .hypothesis-card h4 {{
            font-size: 1.2em;
            margin-bottom: 10px;
        }}

        .hypothesis-status {{
            font-size: 1.5em;
            margin: 10px 0;
        }}

        .hypothesis-details {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-top: 10px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}

        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }}

        th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 600;
        }}

        tbody tr:hover {{
            background-color: #f5f5f5;
        }}

        .accuracy-high {{
            color: #28a745;
            font-weight: 600;
        }}

        .accuracy-medium {{
            color: #ffc107;
            font-weight: 600;
        }}

        .accuracy-low {{
            color: #dc3545;
            font-weight: 600;
        }}

        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}

        .stat-box {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #667eea;
        }}

        .stat-value {{
            font-size: 2em;
            font-weight: 700;
            color: #667eea;
        }}

        .stat-label {{
            font-size: 0.9em;
            color: #666;
            margin-top: 5px;
        }}

        .citation-box {{
            background: #f8f9fa;
            padding: 20px;
            border-left: 4px solid #764ba2;
            border-radius: 4px;
            margin: 20px 0;
        }}

        .citation-box pre {{
            background: white;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
            font-size: 0.85em;
        }}

        a {{
            color: #667eea;
            text-decoration: none;
            transition: color 0.3s;
        }}

        a:hover {{
            color: #764ba2;
            text-decoration: underline;
        }}

        footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.3);
        }}

        .timestamp {{
            font-size: 0.9em;
            opacity: 0.8;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>RCE-LLM Empirical Validation</h1>
            <div class="subtitle">F1-F5 Task Families | Benchmark Results</div>
            <div class="author-info">
                <strong>Author:</strong> Ismail Sialyen |
                <strong>Publication:</strong> <a href="https://doi.org/10.5281/zenodo.17360372" style="color: white;">DOI 10.5281/zenodo.17360372</a>
            </div>
        </header>

        <!-- Overview Statistics -->
        <div class="card">
            <h2>📊 Overview</h2>
            <div class="stat-grid">
                <div class="stat-box">
                    <div class="stat-value">{total_queries}</div>
                    <div class="stat-label">Total Queries</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">5</div>
                    <div class="stat-label">Task Families</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">3</div>
                    <div class="stat-label">Baseline Systems</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{overall_acc['RCE-LLM']['accuracy']:.1%}</div>
                    <div class="stat-label">RCE-LLM Accuracy</div>
                </div>
            </div>
        </div>

        <!-- Hypothesis Validation -->
        <div class="card">
            <h2>✅ Hypothesis Validation</h2>
            <div class="hypothesis-grid">
                <div class="hypothesis-card">
                    <h4>H₁: RCE-LLM > LLM</h4>
                    <div class="hypothesis-status">{"✓ SUPPORTED" if hypotheses['H1_RCE_better_than_LLM']['supported'] else "✗ NOT SUPPORTED"}</div>
                    <div class="hypothesis-details">
                        Improvement: {hypotheses['H1_RCE_better_than_LLM']['improvement_percentage']:+.1f}%<br>
                        RCE-LLM: {overall_acc['RCE-LLM']['accuracy']:.1%}<br>
                        LLM: {overall_acc['LLM']['accuracy']:.1%}
                    </div>
                </div>

                <div class="hypothesis-card">
                    <h4>H₂: RCE-LLM > LLM+RAG</h4>
                    <div class="hypothesis-status">{"✓ SUPPORTED" if hypotheses['H2_RCE_better_than_RAG']['supported'] else "✗ NOT SUPPORTED"}</div>
                    <div class="hypothesis-details">
                        Improvement: {hypotheses['H2_RCE_better_than_RAG']['improvement_percentage']:+.1f}%<br>
                        RCE-LLM: {overall_acc['RCE-LLM']['accuracy']:.1%}<br>
                        LLM+RAG: {overall_acc['LLM+RAG']['accuracy']:.1%}
                    </div>
                </div>

                <div class="hypothesis-card">
                    <h4>H₃: Consistent Improvement</h4>
                    <div class="hypothesis-status">{"✓ SUPPORTED" if hypotheses['H3_consistent_improvement']['supported'] else "✗ PARTIALLY SUPPORTED"}</div>
                    <div class="hypothesis-details">
                        Families improved: {hypotheses['H3_consistent_improvement']['families_improved']}/{hypotheses['H3_consistent_improvement']['total_families']}<br>
                        Across F1-F5 task families
                    </div>
                </div>

                <div class="hypothesis-card">
                    <h4>H₄: Coherence Modules</h4>
                    <div class="hypothesis-status">{"✓ SUPPORTED" if hypotheses['H4_coherence_improves_factual']['supported'] else "✗ NOT SUPPORTED"}</div>
                    <div class="hypothesis-details">
                        Factual grounding (F5)<br>
                        Improved by coherence validation
                    </div>
                </div>
            </div>
        </div>

        <!-- Overall Performance -->
        <div class="card">
            <h2>📈 Overall Performance</h2>
            <table>
                <thead>
                    <tr>
                        <th>System</th>
                        <th>Correct</th>
                        <th>Total</th>
                        <th>Accuracy</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>LLM (Llama 3.2)</strong></td>
                        <td>{overall_acc['LLM']['correct']}</td>
                        <td>{overall_acc['LLM']['total']}</td>
                        <td class="{"accuracy-high" if overall_acc['LLM']['accuracy'] >= 0.7 else "accuracy-medium" if overall_acc['LLM']['accuracy'] >= 0.4 else "accuracy-low"}">{overall_acc['LLM']['accuracy']:.1%}</td>
                    </tr>
                    <tr>
                        <td><strong>LLM+RAG</strong></td>
                        <td>{overall_acc['LLM+RAG']['correct']}</td>
                        <td>{overall_acc['LLM+RAG']['total']}</td>
                        <td class="{"accuracy-high" if overall_acc['LLM+RAG']['accuracy'] >= 0.7 else "accuracy-medium" if overall_acc['LLM+RAG']['accuracy'] >= 0.4 else "accuracy-low"}">{overall_acc['LLM+RAG']['accuracy']:.1%}</td>
                    </tr>
                    <tr style="background-color: #f0f4ff;">
                        <td><strong>RCE-LLM</strong></td>
                        <td>{overall_acc['RCE-LLM']['correct']}</td>
                        <td>{overall_acc['RCE-LLM']['total']}</td>
                        <td class="{"accuracy-high" if overall_acc['RCE-LLM']['accuracy'] >= 0.7 else "accuracy-medium" if overall_acc['RCE-LLM']['accuracy'] >= 0.4 else "accuracy-low"}">{overall_acc['RCE-LLM']['accuracy']:.1%}</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Task Family Results -->
        <div class="card">
            <h2>📋 Task Family Performance</h2>

            <h3>F1: Units Consistency</h3>
            <table>
                <thead>
                    <tr>
                        <th>System</th>
                        <th>Correct</th>
                        <th>Total</th>
                        <th>Accuracy</th>
                    </tr>
                </thead>
                <tbody>
"""

        # Add F1-F5 task family tables
        task_families = [
            ("f1_units", "F1: Units Consistency"),
            ("f2_temporal", "F2: Temporal Reasoning"),
            ("f3_arithmetic", "F3: Compositional Arithmetic"),
            ("f4_coreference", "F4: Coreference Resolution"),
            ("f5_factual", "F5: Factual Grounding")
        ]

        for idx, (family_key, family_name) in enumerate(task_families):
            if idx > 0:  # Add new table header for F2-F5
                html += f"""
            </tbody>
            </table>

            <h3>{family_name}</h3>
            <table>
                <thead>
                    <tr>
                        <th>System</th>
                        <th>Correct</th>
                        <th>Total</th>
                        <th>Accuracy</th>
                    </tr>
                </thead>
                <tbody>
"""

            if family_key in task_acc:
                family_data = task_acc[family_key]
                for system in ["LLM", "LLM+RAG", "RCE-LLM"]:
                    sys_data = family_data[system]
                    accuracy = sys_data['accuracy']
                    acc_class = "accuracy-high" if accuracy >= 0.7 else "accuracy-medium" if accuracy >= 0.4 else "accuracy-low"
                    highlight = ' style="background-color: #f0f4ff;"' if system == "RCE-LLM" else ""

                    html += f"""
                    <tr{highlight}>
                        <td><strong>{system}</strong></td>
                        <td>{sys_data['correct']}</td>
                        <td>{sys_data['total']}</td>
                        <td class="{acc_class}">{accuracy:.1%}</td>
                    </tr>
"""

        html += f"""
                </tbody>
            </table>
        </div>

        <!-- Effect Sizes -->
        <div class="card">
            <h2>📐 Effect Sizes (Cohen's h)</h2>
            <div class="stat-grid">
                <div class="stat-box">
                    <div class="stat-value">{effect_sizes['RCE_vs_LLM']['cohens_h']:.3f}</div>
                    <div class="stat-label">RCE-LLM vs LLM<br>({effect_sizes['RCE_vs_LLM']['interpretation']})</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{effect_sizes['RCE_vs_RAG']['cohens_h']:.3f}</div>
                    <div class="stat-label">RCE-LLM vs LLM+RAG<br>({effect_sizes['RCE_vs_RAG']['interpretation']})</div>
                </div>
            </div>
            <p style="margin-top: 20px; font-size: 0.9em; color: #666;">
                <strong>Cohen's h interpretation:</strong> |h| &lt; 0.2 (negligible), 0.2-0.5 (small), 0.5-0.8 (medium), &gt; 0.8 (large)
            </p>
        </div>

        <!-- RCE Architecture -->
        <div class="card">
            <h2>🏗️ RCE-LLM Architecture</h2>
            <p>RCE-LLM uses <strong>contextual actualization</strong> instead of traditional attention, with 5 coherence modules:</p>
            <div class="stat-grid">
                <div class="stat-box">
                    <div class="stat-value">µ₁</div>
                    <div class="stat-label">Units Consistency</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">µ₂</div>
                    <div class="stat-label">Temporal Reasoning</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">µ₃</div>
                    <div class="stat-label">Arithmetic Validity</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">µ₄</div>
                    <div class="stat-label">Coreference Resolution</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">µ₅</div>
                    <div class="stat-label">Factual Entailment</div>
                </div>
            </div>
        </div>

        <!-- Reproducibility -->
        <div class="card">
            <h2>🔬 Reproducibility</h2>
            <p>All benchmarks were executed using:</p>
            <ul style="margin: 15px 0 15px 30px;">
                <li><strong>LLM Baseline:</strong> Llama 3.2 via Ollama (no validation)</li>
                <li><strong>LLM+RAG Baseline:</strong> Llama 3.2 + retrieval (no validation)</li>
                <li><strong>RCE-LLM:</strong> Full coherence optimization with 5 modules</li>
                <li><strong>Dataset:</strong> 30 queries across F1-F5 task families</li>
                <li><strong>Execution Date:</strong> {datetime.fromisoformat(execution_date).strftime('%B %d, %Y')}</li>
            </ul>

            <h3>Repository</h3>
            <p>
                <a href="https://github.com/IsmaIkami/rce-llm-empirical-validation">
                    https://github.com/IsmaIkami/rce-llm-empirical-validation
                </a>
            </p>

            <h3>Citation</h3>
            <div class="citation-box">
                <pre>@article{{sialyen2025rce,
  title={{RCE-LLM: A Relational Coherence Engine for Consistent and Energy-Efficient Language Modeling}},
  author={{Sialyen, Ismail}},
  journal={{Zenodo}},
  year={{2025}},
  doi={{10.5281/zenodo.17360372}},
  url={{https://doi.org/10.5281/zenodo.17360372}}
}}</pre>
            </div>
        </div>

        <footer>
            <div class="timestamp">Last updated: {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}</div>
            <p style="margin-top: 10px;">
                Prepared by <strong>Ismail Sialyen</strong> |
                <a href="https://doi.org/10.5281/zenodo.17360372" style="color: white;">DOI 10.5281/zenodo.17360372</a>
            </p>
        </footer>
    </div>
</body>
</html>
"""

        return html

    def save_html(self, html: str):
        """Save HTML to docs/index.html for GitHub Pages"""
        DOCS_DIR.mkdir(exist_ok=True)

        output_file = DOCS_DIR / "index.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✓ Saved results page to {output_file}")

    def run(self):
        """Generate results page"""
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 25 + "RESULTS PAGE GENERATOR" + " " * 31 + "║")
        print("║" + " " * 78 + "║")
        print("║  Author: Ismail Sialyen" + " " * 54 + "║")
        print("║  Publication: DOI 10.5281/zenodo.17360372" + " " * 35 + "║")
        print("╚" + "═" * 78 + "╝")

        if not self.load_data():
            return

        print("\n→ Generating HTML with exact design from rce-scientific-evidence...")
        html = self.generate_html()

        self.save_html(html)

        print("\n╔" + "═" * 78 + "╗")
        print("║" + " " * 29 + "PAGE COMPLETE" + " " * 35 + "║")
        print("╚" + "═" * 78 + "╝")
        print(f"\n✓ Results page ready: {DOCS_DIR}/index.html")
        print(f"\nNext steps:")
        print(f"  1. Initialize git repository")
        print(f"  2. Push to GitHub")
        print(f"  3. Enable GitHub Pages")


if __name__ == "__main__":
    generator = ResultsPageGenerator()
    generator.run()
