import sys
import pandas as pd

# print('Hello pipeline!')

month = int(sys.argv[1])
print(f'Hello pipeline! Running pipeline for month: {month}.')

df = pd.DataFrame({"Day": [1, 2], "No. of customers": [3, 4]})
df['Month'] = month
print(df.head())

df.to_parquet(f"output_{month}.parquet")