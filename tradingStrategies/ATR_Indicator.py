from retrieveData.RetrieveData import df
import plotly.express as px
import plotly.offline as pyo
from tradingStrategies.RSI_Indicator import df

atr_period = 14

# calculating the range of each candle
df['range'] = df['high'] - df['low']

# calculating the average value of ranges
df['atr_14'] = df['range'].rolling(atr_period).mean()

# displaying the results
print(df[['datetime', 'atr_14']])

# plotting the ATR Indicator
fig_atr = px.line(df, x='datetime', y='atr_14', title='ATR Indicator')

# displaying the ATR Figure
pyo.plot(fig_atr, filename='atr_plot.html', auto_open=True)
