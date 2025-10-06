import pandas as pd
import os

RAW_DIR = "data/raw/"
PROCESSED_DIR = "data/processed/"

FEEDS = {
    "1": "1_regional_train",
    "2": "2_metro_train",
    "3": "3_metro_tram",
    "4": "4_metro_bus",
    "6": "6_regional_bus",
    "11": "11_skybus"
}

# Route types we want
ROUTE_TYPES = {0, 1, 2, 3, 4, 6, 11}

def load_and_concat(filename):
    """Load a file from all feeds and concatenate"""
    dfs = []
    for feed_id, folder in FEEDS.items():
        filepath = os.path.join(RAW_DIR, folder, filename)
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            df['feed_source'] = folder  # Track which feed it came from
            dfs.append(df)
        else:
            print(f"⚠ Missing {filename} in {folder}")
    
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

def parse_gtfs():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    print("Loading routes...")
    routes = load_and_concat('routes.txt')
    
    print(routes['feed_source'].unique())
    # Filter by route type
    routes = routes[routes['route_type'].isin(ROUTE_TYPES)]
    
    # Remove replacement buses
    routes = routes[~routes['route_long_name'].str.contains('Replacement', case=False, na=False)]
    
    print(f"  ✓ {len(routes)} routes after filtering")
    routes.to_csv(f'{PROCESSED_DIR}/routes.csv', index=False)
    
    print("Loading stops...")
    stops = load_and_concat('stops.txt')
    print(f"  ✓ {len(stops)} stops loaded")
    stops.to_csv(f'{PROCESSED_DIR}/stops_raw.csv', index=False)
    
    print("Loading trips...")
    trips = load_and_concat('trips.txt')
    
    # Only keep trips for our filtered routes
    trips = trips[trips['route_id'].isin(routes['route_id'])]
    
    # Merge with routes to get route_type AND keep feed_source
    trips = trips.merge(
        routes[['route_id', 'route_type', 'feed_source']], 
        on='route_id', 
        how='left',
        suffixes=('', '_from_route')
    )
    
    print(f"  ✓ {len(trips)} trips after filtering")
    trips.to_csv(f'{PROCESSED_DIR}/trips.csv', index=False)
    
    print("Loading stop_times...")
    stop_times = load_and_concat('stop_times.txt')
    
    # Only keep stop_times for our filtered trips
    stop_times = stop_times[stop_times['trip_id'].isin(trips['trip_id'])]
    print(f"  ✓ {len(stop_times)} stop_times after filtering")
    stop_times.to_csv(f'{PROCESSED_DIR}/stop_times.csv', index=False)
    
    print("\n✓ All files parsed and saved to data/processed/")

if __name__ == "__main__":
    parse_gtfs()