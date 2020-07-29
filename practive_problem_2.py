import pandas as pd

filename = 'chicago.csv'

# load data file into a dataframe
df = pd.read_csv(filename)

# print value counts for each user type
user_types = df.groupby('User Type')['User Type'].count()

print(user_types)