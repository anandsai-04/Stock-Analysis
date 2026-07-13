---
name: quant-domain-analysis
description: Performs multi-company comparisons and evaluates financial metrics against domain-specific baselines (Tech, Finance, EV, etc.).
---

# Quant Domain Analysis Skill

This skill dictates how to contextualize raw financial data based on the industry sector.

## Workflow

1. **Sector Identification**: Determine the company's domain (e.g., Tech, Finance, Consumer, EV, Medicine, Petrochemical).
2. **Peer Discovery**: Find 2-3 direct competitors in the same sector.
3. **Baseline Loading**: Load the expected healthy ranges for Liquidity, Solvency, Activity, and Profitability ratios for that specific domain.
4. **Contextual Evaluation**: Evaluate the company's metrics against the domain baselines. A high Debt-to-Equity might be flagged as a critical risk in Tech, but marked as normal operating leverage in Finance.
5. **Multi-Company Comparison**: Normalize data across competitors and generate a side-by-side analysis, explicitly adjusting interpretations based on the domain context.
