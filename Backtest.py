import pandas as pd
from tradingStrategies.ATR_Indicator import df
import plotly.express as px
import plotly.offline as pyo


# class Position contains data about trades opened/closed during the backtest
class Position:
    def __init__(self, open_datetime, open_price, order_type, volume, sl, tp):
        self.open_datetime = open_datetime
        self.open_price = open_price
        self.order_type = order_type
        self.volume = volume
        self.sl = sl
        self.tp = tp
        self.close_datetime = None
        self.close_price = None
        self.profit = None
        self.status = 'open'

    def close_position(self, close_datetime, close_price):
        self.close_datetime = close_datetime
        self.close_price = close_price
        self.profit = (self.close_price - self.open_price) * self.volume if self.order_type == 'buy' \
            else (self.open_price - self.close_price) * self.volume
        self.status = 'closed'

    def _asdict(self):
        return {
            'open_datetime': self.open_datetime,
            'open_price': self.open_price,
            'order_type': self.order_type,
            'volume': self.volume,
            'sl': self.sl,
            'tp': self.tp,
            'close_datetime': self.close_datetime,
            'close_price': self.close_price,
            'profit': self.profit,
            'status': self.status,
        }


# class Strategy defines trading logic and evaluates the backtest based on opened/closed positions
class Strategy:
    def __init__(self, df, starting_balance):
        self.starting_balance = starting_balance
        self.positions = []
        self.data = df

    # return backtest result
    def get_positions_df(self):
        df = pd.DataFrame([position._asdict() for position in self.positions])
        df['pnl'] = df['profit'].cumsum() + self.starting_balance
        return df

    # add Position class to the list
    def add_position(self, position):
        self.positions.append(position)
        return True

    # close positions when stop loss or take profit is reached
    def close_tp_sl(self, data):
        for pos in self.positions:
            if pos.status == 'open':
                if (pos.sl >= data['close'] and pos.order_type == 'buy'):
                    pos.close_position(data['datetime'], pos.sl)
                elif (pos.sl <= data['close'] and pos.order_type == 'sell'):
                    pos.close_position(data['datetime'], pos.sl)
                elif (pos.tp <= data['close'] and pos.order_type == 'buy'):
                    pos.close_position(data['datetime'], pos.tp)
                elif (pos.tp >= data['close'] and pos.order_type == 'sell'):
                    pos.close_position(data['datetime'], pos.tp)

    # check for open positions
    def has_open_positions(self):
        for pos in self.positions:
            if pos.status == 'open':
                return True
        return False

    # strategy logic how positions should be opened/closed
    def logic(self, data):
        # if no position is open
        if not self.has_open_positions():
            # if RSI is less than 30 -> BUY
            if data['rsi_14'] < 30:
                # Position variables
                open_datetime = data['datetime']
                open_price = data['close']
                order_type = 'buy'
                volume = data['volume']
                sl = open_price - 2 * data['atr_14']
                tp = open_price + 2 * data['atr_14']
                self.add_position(Position(open_datetime, open_price, order_type, volume, sl, tp))

            # if RSI is greater than 70 -> SELL
            elif data['rsi_14'] > 70:
                # Position variables
                open_datetime = data['datetime']
                open_price = data['close']
                order_type = 'sell'
                volume = data['volume']
                sl = open_price + 2 * data['atr_14']
                tp = open_price - 2 * data['atr_14']
                self.add_position(Position(open_datetime, open_price, order_type, volume, sl, tp))

    # logic
    def run(self):
        # data represents a moment in time while iterating through the backtest
        for i, data in self.data.iterrows():
            # close positions when stop loss or take profit is reached
            self.close_tp_sl(data)
            # strategy logic
            self.logic(data)

        return self.get_positions_df()

# Preparing the data for backtest
backtest_df = df[14:]  # removing NaN values
# print(backtest_df)


# Running the backtest
rsi_strategy = Strategy(backtest_df, starting_balance=100000)
backtest_results = rsi_strategy.run()
# print(backtest_results)


#Visualize the backtest
# Filter closed positions
backtest_result = backtest_results[backtest_results['status'] == 'closed']

# Visualization Setup
fig_backtest = px.line(df, x='datetime', y=['close'], title='RSI Strategy - Trades')

# Adding Trades to the Plot
for i, position in backtest_result.iterrows():
    if position.status == 'closed':
        fig_backtest.add_shape(type="line",
            x0=position.open_datetime, y0=position.open_price, x1=position.close_datetime, y1=position.close_price,
            line=dict(
                color="green" if position.profit >= 0 else "red",
                width=3)
            )

# Display the Plot
pyo.plot(fig_backtest, filename='backtest_plot.html', auto_open=True)

# Plotting Pnl

fig_pnl = px.line(backtest_result, x='close_datetime', y='pnl', title='Profit and Loss Over Time')
pyo.plot(fig_pnl, filename='pnl_plot.html', auto_open=True)
