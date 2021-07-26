# Multi-Factor_Modeling

Multi-Factor Modeling with Technical Indictors: Anlysis of the relationship between technical indicators and equity risk premium.

Objective: analyze the effectiveness of technical indicators to identify excess returns. Historical prices will be used to generate common indicators and for each indicator, they are evaluated using the Fama-French model.

Calculations generated by TA-Lib, documentation: https://cryptotrader.org/talib


# Usage
Provided a *ticker* and *period (1mo, 1y, 3y, max, etc.)*

```df = get_historical_prices(*ticker,*period)```

## To display buy and sell signals given the indicator

### BollingerBands
```Plot_Signal_Indicator_Signals(Indicator)```
Indicator is the name of the TA (Ex: 'MACD', 'BB', 'RSI')

# Fama French 3-Factor Model


## OLS Regression Model Fama-French 3 Factors

### FF3F(Indicator)
Example:
```FF3F('BB')```
