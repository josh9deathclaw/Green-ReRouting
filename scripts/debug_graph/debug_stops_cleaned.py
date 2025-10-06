import pandas as pd

stops = pd.read_csv('data/processed/stops_cleaned.csv')

print("=== STOPS ANALYSIS ===\n")

print(f"Total stops: {len(stops)}")
print(f"Unique station_ids: {stops['station_id'].nunique()}")
print()

# Check station ID types
print("Sample station IDs:")
print(stops['station_id'].head(20).tolist())
print()

# Check for trains vs trams vs buses
print("\nSample stop names:")
print(stops[['station_id', 'stop_name']].head(20))

# Count potential train stations (usually have 'Station' in name)
train_stations = stops[stops['stop_name'].str.contains('Station', case=False, na=False)]
print(f"\nStops with 'Station' in name: {len(train_stations)}")