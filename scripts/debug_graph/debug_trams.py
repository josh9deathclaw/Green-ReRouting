import pandas as pd

routes = pd.read_csv('data/processed/routes.csv')
print(routes['feed_source'].unique())


df = pd.read_csv("data/raw/3_metro_tram/routes.txt")
print(df['route_type'].unique())