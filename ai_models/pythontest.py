import pandas as pd



df_chains = pd.DataFrame(pd.read_csv('chains.csv'), columns=("company", "chain", "type", "status"))
df_chains = pd.DataFrame(df_chains['status'] != "completed")

df_industries = pd.DataFrame(pd.read_csv('industries.csv'))
df_daterange = pd.DataFrame(pd.read_csv('daterange.csv'))
  
for index, chain in df_chains.iterrows():

    df_chains.loc[index, ['status']] = "completed"

