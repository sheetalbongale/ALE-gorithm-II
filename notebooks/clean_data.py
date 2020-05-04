import os
import pandas as pd
import numpy as np

csv_path = os.path.join("../data/csv/clean_reviews_sm.csv")
TextFileReader = pd.read_csv(csv_path, chunksize=1000)  # the number of rows per chunk

dfList = []
for df in TextFileReader:
    dfList.append(df)

df = pd.concat(dfList,sort=False)
df=df.sample(n=4000000)
df = df.groupby('username').filter(lambda x: len(x) > 50)
df = df.groupby('beer_id').filter(lambda x: len(x) > 500)
df.to_csv("../data/csv/reviews_cleaned_reduced_500.csv",index=False)
print(df.shape)