import pandas as pd

df = pd.read_csv('72GM_solution.csv')

df.dropna(subset=[['job-Id']], inplace=True)

df['raw-id'] = df['job-Id'].apply(lambda x: x.split("_")[0])

df['cycle'] = df['job-Id'].apply(lambda x: str(x).split("_")[1])

df['arrTime'] = df['arrTime'].apply(lambda x: float(x))

df_0 = df[df['cycle'] == '0']

df_1 = df[df['cycle'] == '1']

df_0.set_index('raw-id', inplace = True)
df_1.set_index('raw-id', inplace = True)

df_diff = df_1['arrTime'] - df_0['arrTime']
#df_diff = df_diff.reset_index()
print (df_diff)

#print(df_diff.sort_values('arrTime', ascending=True))