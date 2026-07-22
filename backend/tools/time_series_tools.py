import yfinance as yf
import pandas as pd
from prophet import Prophet
from langchain_core.tools import tool
import warnings
import random
from statsmodels.tsa.arima.model import ARIMA
from arch import arch_model

# Suppress prophet warnings
warnings.filterwarnings('ignore', category=FutureWarning)

@tool
def prophet_forecaster(ticker: str, periods: int = 30) -> str:
    """Uses the Meta Prophet model to forecast the future stock price.
    Fetches the last 2 years of daily closing prices and predicts the next 'periods' days.
    Returns the predicted trend and seasonality decomposition."""
    try:
        data = yf.download(ticker, period="2y", progress=False)
        if data.empty:
            return f"Failed to fetch historical data for {ticker}"
            
        # Prepare data for Prophet (requires 'ds' and 'y' columns)
        df = data.reset_index()[['Date', 'Close']]
        
        # Handle multi-level columns in newer yfinance versions
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        df.columns = ['ds', 'y']
        
        # Handle timezone naive/aware issues
        df['ds'] = df['ds'].dt.tz_localize(None)
        
        # Fit Prophet
        m = Prophet(daily_seasonality=False)
        m.fit(df)
        
        # Predict
        future = m.make_future_dataframe(periods=periods)
        forecast = m.predict(future)
        
        # Extract results
        latest = df.iloc[-1]
        predicted_end = forecast.iloc[-1]
        
        start_price = round(float(latest['y']), 2)
        end_price = round(float(predicted_end['yhat']), 2)
        lower_bound = round(float(predicted_end['yhat_lower']), 2)
        upper_bound = round(float(predicted_end['yhat_upper']), 2)
        
        # Detect seasonality strength roughly
        yearly_impact = "Significant yearly seasonality detected." if 'yearly' in forecast.columns else "Minimal yearly seasonality."
        weekly_impact = "Significant weekly seasonality detected." if 'weekly' in forecast.columns else "Minimal weekly seasonality."
        
        trend = "bullish" if end_price > start_price else "bearish"
        percent_change = round(((end_price - start_price) / start_price) * 100, 2)
        
        report = f"--- Prophet Time Series Forecast for {ticker} ({periods} days) ---\n"
        report += f"Current Price (End of historical data): ${start_price}\n"
        report += f"Predicted Price in {periods} days: ${end_price}\n"
        report += f"Confidence Interval: [${lower_bound} - ${upper_bound}]\n"
        report += f"Overall Trend: {trend.upper()} ({percent_change}% predicted change)\n"
        report += f"Seasonality: {yearly_impact} {weekly_impact}\n"
        
        return report
        
    except Exception as e:
        return f"Error running Prophet forecaster: {str(e)}"

@tool
def arima_forecaster_tool(ticker: str, periods: int = 10, num_searches: int = 10) -> str:
    """Uses a Random Search Auto-ARIMA model to forecast linear dependencies in stock price.
    Randomly searches (p,d,q) combinations and selects the one with the lowest AIC score."""
    try:
        data = yf.download(ticker, period="1y", progress=False)
        if data.empty:
            return f"Failed to fetch historical data for {ticker}"
            
        df = data['Close']
        if isinstance(df, pd.DataFrame):
            df = df.iloc[:, 0]
            
        best_aic = float('inf')
        best_order = None
        best_model = None
        
        # Random Search Implementation
        for _ in range(num_searches):
            p = random.randint(0, 5)
            d = random.randint(0, 2)
            q = random.randint(0, 5)
            order = (p, d, q)
            
            try:
                model = ARIMA(df, order=order)
                fitted = model.fit()
                if fitted.aic < best_aic:
                    best_aic = fitted.aic
                    best_order = order
                    best_model = fitted
            except:
                continue
                
        if best_model is None:
            return "ARIMA Random Search failed to find a converging model."
            
        forecast = best_model.forecast(steps=periods)
        predicted_end = round(float(forecast.iloc[-1]), 2)
        start_price = round(float(df.iloc[-1]), 2)
        
        report = f"--- ARIMA Forecast for {ticker} ({periods} days) ---\n"
        report += f"Optimal Parameters (Random Search): ARIMA{best_order}\n"
        report += f"Best AIC Score: {round(best_aic, 2)}\n"
        report += f"Current Price: ${start_price}\n"
        report += f"Predicted Price: ${predicted_end}\n"
        return report
    except Exception as e:
        return f"Error running ARIMA: {str(e)}"

@tool
def garch_volatility_tool(ticker: str) -> str:
    """Uses the GARCH(1,1) econometric model to forecast volatility (risk/variance) of the stock."""
    try:
        data = yf.download(ticker, period="2y", progress=False)
        if data.empty:
            return f"Failed to fetch historical data for {ticker}"
            
        # Calculate daily returns for GARCH
        df = data['Close']
        if isinstance(df, pd.DataFrame):
            df = df.iloc[:, 0]
            
        returns = 100 * df.pct_change().dropna()
        
        # Fit GARCH(1, 1)
        model = arch_model(returns, vol='Garch', p=1, q=1)
        fitted = model.fit(disp='off')
        
        # Forecast variance
        forecast = fitted.forecast(horizon=5)
        latest_var = forecast.variance.iloc[-1].values[-1]
        latest_vol = round(float(latest_var ** 0.5), 2)
        
        report = f"--- GARCH(1,1) Volatility Forecast for {ticker} ---\n"
        report += f"Predicted annualized volatility is roughly {round(latest_vol * (252**0.5), 2)}%\n"
        report += f"Daily Expected Volatility: {latest_vol}%\n"
        report += "Note: High volatility means wider predicted price swings (higher risk).\n"
        return report
    except Exception as e:
        return f"Error running GARCH: {str(e)}"
