# A/B Test Analysis: Site Conversion Optimization
 
**Tools Used:** Python, Pandas, SciPy, Scikit-learn, Matplotlib, StatsModels, Graphviz  

> A rigorous end-to-end evaluation of an A/B test measuring the impact of a new site version on conversion rates—ensuring statistical validity and actionable insights.

---

## Table of Contents

- [Overview](#overview)
- [Real-World Use Cases](#real-world-use-cases)
- [Features](#features)
- [Key Insights](#key-insights)
- [Visuals](#visuals)
- [Installation](#installation)
- [Usage](#usage)
- [Conclusion](#conclusion)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This project evaluates the **effectiveness and validity** of an A/B test designed to boost user conversion rates by testing a redesigned website. It includes:
- Statistical testing of results
- Machine learning-based randomization diagnostics
- Power analysis for sample size estimation
- Bias correction through rebalancing

---

## Real-World Use Cases

- **Marketing and Growth Teams**: Validate experiments before sitewide rollout.
- **Product Managers**: Detect and correct randomization flaws in live experiments.
- **Data Scientists**: Build reusable frameworks for analyzing and validating A/B tests.
- **Analysts**: Apply ML and statistical tools to improve experimentation strategy.

---

## Features

- Cleans and validates A/B test datasets
- Performs Welch’s t-test to compare conversion rates
- Uses decision trees to diagnose randomization bias
- Applies stratified resampling to correct group imbalance
- Computes statistical power and required sample sizes
- Generates annotated visualizations to aid decision-making

---

## Key Insights

### Conversion Impact
- **Control Group:** 4.37% conversion  
- **Test Group:** 5.56% conversion 
- **Welch’s T-Test Result:** p-value = 1.32e-14 → **Statistically significant**  

### Randomization Bias Detected
- Decision tree classification and feature analysis revealed Argentina and Uruguay were **overrepresented in the test group**, violating randomization assumptions:
  - 🇦🇷 Argentina: 17% (test) vs 5% (control)
  - 🇺🇾 Uruguay: 1.7% (test) vs 0.2% (control)

### Correction Strategy
- **Oversampled underrepresented users** from test to augment the control group and rebalance country distributions.
- Post-correction t-test: **p = 0.2545** → **No statistically significant difference** → Original uplift was likely confounded by demographic bias.

### Power Analysis
- **Required sample size per group:** ~14,744 to detect a 1% lift in conversion with 80% power and 5% significance.
- Created sensitivity chart showing how sample size changes with different expected uplifts.

---

## Visuals

![Randomization Tree](randomization_tree.png)  
*Decision tree showing country-level imbalance*

![Sample Size Sensitivity](sample_size_vs_conversion_rate.png)  
*Sample size needed for varying target conversion rates*

---

## Installation

To install the required Python packages:

pip install -r requirements.txt

## Usage

To run the analysis:

python ab_testing_analysis.py

---

## Conclusion

Initial uplift in conversion was driven by flawed randomization. After correction, the new site version did **not** produce a statistically significant improvement. The project highlights the importance of validating A/B test assumptions before acting on results.

---

## Contributing

We welcome community contributions!

1. Fork the repository

2. Create a new branch:

git checkout -b feature/your-feature

3. Make your changes

4. Push to your branch:

git push origin feature/your-feature

5. Submit a Pull Request

## License
This project is licensed under the MIT License.
