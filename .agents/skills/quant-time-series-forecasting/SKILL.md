---
name: quant-time-series-forecasting
description: Performs time-series forecasting, trend decomposition, and vertical analysis (common-size statements) on financial data using Prophet.
---

# Quant Time Series & Forecasting Skill

This skill dictates how to perform rigorous statistical forecasting and vertical analysis.

## Workflow

1. **Vertical Analysis (Common-Size Statements)**: Before running predictions, convert raw balance sheet and income statement metrics into percentages (% of Total Assets, % of Total Revenue). This normalizes data for easier trend spotting.
2. **Historical Data Fetch**: Use `yfinance` to pull 2 to 5 years of daily closing prices.
3. **Data Cleaning**: Use Pandas to handle NaN values and format the dataframe to the `(ds, y)` format required by Prophet.
4. **Model Fitting**: Fit the `Prophet` model.
5. **Prediction**: Predict 30 to 90 days into the future.
6. **Decomposition**: Extract the trend, weekly seasonality, and yearly seasonality components.
7. **Interpretation**: Analyze the decomposition to declare whether recent price movements are driven by regular seasonal patterns or random anomalous events.
