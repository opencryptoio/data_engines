import pandas as pd



df_chains = pd.read_csv('chains.csv', header=0)
print(df_chains.columns)

df_chains = pd.DataFrame(df_chains[df_chains['status'] != "completed"])

print(df_chains)

df_industries = pd.DataFrame(pd.read_csv('industries.csv'))

df_industries.loc[:,'status'] = 'completed'
df_industries.to_csv("industries.csv")

df_daterange = pd.DataFrame(pd.read_csv('daterange.csv'))
  
for index, chain in df_chains.iterrows():

    df_chains.loc[index, ['status']] = "completed"
    df_chains.to_csv("chains.csv")

