import time
import numpy as np
import pandas as pd

df = pd.DataFrame(data=np.random.randint(
    1, 11, (100000, 4)), columns=list('ABCD'))
# print(df.head())

# normal 'For' loop
start = time.time()

for idx, row in df.iterrows():
    # creating a new column
    df.at[idx, 'ratio'] = (row['D'] / row['C']) * 100
end = time.time()
# print(end - start)
# 1.42 seconds

# vectorization
start = time.process_time()
df["ratio2"] = (df['D'] / df['C']) * 100
end = time.process_time()
print(end - start)
print(df.head())
# 0.00056 seconds
