from retrieveData.RetrieveData import df
import plotly.express as px
import plotly.offline as pyo


# setting the RSI Period
rsi_period = 14

# to calculate RSI, we first need to calculate the exponential weighted aveage gain and loss during the period
df['gain'] = (df['close'] - df['open']).apply(lambda x: x if x > 0 else 0)
df['loss'] = (df['close'] - df['open']).apply(lambda x: -x if x < 0 else 0)

# here we use the same formula to calculate Exponential Moving Average
df['ema_gain'] = df['gain'].ewm(span=rsi_period, min_periods=rsi_period).mean()
df['ema_loss'] = df['loss'].ewm(span=rsi_period, min_periods=rsi_period).mean()

# the Relative Strength is the ratio between the exponential avg gain divided by the exponential avg loss
df['rs'] = df['ema_gain'] / df['ema_loss']

# the RSI is calculated based on the Relative Strength using the following formula
df['rsi_14'] = 100 - (100 / (df['rs'] + 1))

# displaying the results
print(df[['datetime', 'rsi_14', 'rs', 'ema_gain', 'ema_loss']])
# plotting the RSI
fig_rsi = px.line(df, x='datetime', y='rsi_14', title='RSI Indicator')

# RSI commonly uses oversold and overbought levels, usually at 70 and 30
overbought_level = 70
oversold_level = 30

# adding oversold and overbought levels to the plot
fig_rsi.add_hline(y=overbought_level, opacity=0.5, line_dash="dash", annotation_text="Overbought", annotation_position="bottom right")
fig_rsi.add_hline(y=oversold_level, opacity=0.5, line_dash="dash", annotation_text="Oversold", annotation_position="top right")

# showing the RSI Figure
pyo.plot(fig_rsi, filename='rsi_plot.html', auto_open=True)
