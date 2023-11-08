import pandas as pd

googleSheetId = '1-rIkEb94tZ69FvsjXnfkVETYu6rftF-8'
worksheetName = 'HINDALCO'

URL = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(
	googleSheetId,
	worksheetName
)

df = pd.read_csv(URL)

# Covert datetime column to datetime datatype
df['datetime'] = pd.to_datetime(df['datetime'])

# print(df)
# print(df['datetime'].dtype)
