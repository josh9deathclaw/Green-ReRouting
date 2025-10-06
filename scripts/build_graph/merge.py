import pandas as pd

PROCESSED_DIR = "data/processed/"

def merge_edges():
    print("Merging duplicate edges...")
    
    # Load raw edges
    edges = pd.read_csv(f'{PROCESSED_DIR}/edges_raw.csv')
    print(f"  Loaded {len(edges)} raw edges")
    
    # Sort by trip_id to ensure consistent "first occurrence"
    edges = edges.sort_values('trip_id')
    
    # Group by station pairs and keep first
    # This keeps the first edge encountered for each (from_station, to_station) pair
    merged = edges.groupby(['from_station', 'to_station']).first().reset_index()
    
    # Drop trip_id column (no longer needed)
    merged = merged.drop(columns=['trip_id'])
    
    print(f"  ✓ Reduced to {len(merged)} unique edges")
    print(f"  Removed {len(edges) - len(merged)} duplicates")
    
    # Check for issues
    zero_time = len(merged[merged['time'] == 0])
    zero_distance = len(merged[merged['distance'] == 0])
    
    if zero_time > 0:
        print(f"  ⚠ Warning: {zero_time} edges have zero travel time")
    if zero_distance > 0:
        print(f"  ⚠ Warning: {zero_distance} edges have zero distance")
    
    # Save
    merged.to_csv(f'{PROCESSED_DIR}/edges_merged.csv', index=False)
    print(f"  ✓ Saved to edges_merged.csv")
    
    # Print some stats
    print(f"\n  Edge Statistics:")
    print(f"    Average time: {merged['time'].mean():.1f} seconds")
    print(f"    Average distance: {merged['distance'].mean():.1f} meters")
    print(f"    Modes: {merged['mode'].value_counts().to_dict()}")
    
    return merged

if __name__ == "__main__":
    merge_edges()