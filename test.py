import unittest
import pandas as pd

# Import the DataFrame created in the data retrieval step
from retrieveData.RetrieveData import df 

class TestDataValidation(unittest.TestCase):
    def test_decimal_values(self):
        # Check if Open, High, Low, and Close are decimals
        self.assertTrue(df['open'].dtype == 'float64')
        self.assertTrue(df['high'].dtype == 'float64')
        self.assertTrue(df['low'].dtype == 'float64')
        self.assertTrue(df['close'].dtype == 'float64')

    def test_integer_volume(self):
        # Check if Volume is an integer
        self.assertTrue(df['volume'].dtype == 'int64')

    def test_string_instrument(self):
        # Check if Instrument is a string
        self.assertTrue(df['instrument'].dtype == 'object')  # 'object' represents strings in Pandas

    def test_datetime_datetime(self):
        # Check if 'datetime' is a datetime object with the expected format
        self.assertTrue(pd.api.types.is_datetime64_dtype(df['datetime']))


if __name__ == '__main__':
    unittest.main()
