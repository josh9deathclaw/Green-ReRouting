import pandas as pd
import os

print("Checking raw GTFS files for buses...\n")

for feed_id, folder in [('4', '4_metro_bus'), ('6', '6_regional_bus')]:
    routes_file = f'data/raw/{folder}/routes.txt'
    if os.path.exists(routes_file):
        routes = pd.read_csv(routes_file)
        print(f"{folder}:")
        print(f"  Total routes: {len(routes)}")
        print(f"  Route types: {routes['route_type'].value_counts().to_dict()}")
        print(f"  Sample routes: {routes['route_short_name'].head(10).tolist()}\n")
    else:
        print(f"⚠ {routes_file} NOT FOUND\n")