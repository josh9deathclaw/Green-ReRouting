import pandas as pd

edges = pd.read_csv('data/processed/edges_raw.csv', low_memory=False)

print("=== EDGE ANALYSIS ===\n")

# Check data types
print("Column types:")
print(edges.dtypes)
print()

# Check for issues
print(f"Total edges: {len(edges)}")
print(f"Unique from_stations: {edges['from_station'].nunique()}")
print(f"Unique to_stations: {edges['to_station'].nunique()}")
print()

# Mode distribution
print("Mode distribution:")
print(edges['mode'].value_counts())
print()

# Time statistics
print("Time statistics:")
print(edges['time'].describe())
print()

# Check for weird times
print("\nEdges with time > 1 hour (3600s):")
long_edges = edges[edges['time'] > 3600].sort_values('time', ascending=False).head(10)
print(long_edges[['from_station', 'to_station', 'route_name', 'mode', 'time', 'distance']])
print()

# Check for zero times
print(f"\nEdges with zero time: {len(edges[edges['time'] == 0])}")
zero_time = edges[edges['time'] == 0].head(10)
print(zero_time[['from_station', 'to_station', 'route_name', 'mode', 'time', 'distance']])
print()

# Check station IDs
print("\nSample station IDs:")
print("From stations:", edges['from_station'].head(10).tolist())
print("To stations:", edges['to_station'].head(10).tolist())