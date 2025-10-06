import pandas as pd
routes = pd.read_csv("data/processed/routes.csv", dtype=str)
trips = pd.read_csv("data/processed/trips.csv", dtype=str)

# how many routes have empty short name?
print("routes: total", len(routes))
print("routes with empty short_name:", routes['route_short_name'].isna().sum(), 
      "with empty long_name:", routes['route_long_name'].isna().sum())

# check sample rows
print(routes[['route_id','route_short_name','route_long_name','feed_source']].head(10))

# after merge examine trips missing route_short_name (if you kept merged trips)
missing = trips[~trips['route_id'].isin(routes['route_id'])]
print("trip rows whose route_id not present in routes:", len(missing))
print("sample missing route_ids:", missing['route_id'].unique()[:10])
print(routes.groupby('feed_source')['route_short_name'].apply(lambda s: s.isna().sum()))