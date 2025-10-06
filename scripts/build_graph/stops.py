import pandas as pd
import sys
sys.path.append('scripts')
from utils.geo import is_in_melbourne

PROCESSED_DIR = "data/processed/"

MELBOURNE_BOUNDS = {
    'lat_min': -38.5,
    'lat_max': -37.5,
    'lon_min': 144.5,
    'lon_max': 145.5
}

def process_stops():
    print("Processing stops...")
    
    # Load raw stops
    stops = pd.read_csv(f'{PROCESSED_DIR}/stops_raw.csv')
    print(f"  Loaded {len(stops)} raw stops")
    
    # CHANGE: Keep both regular stops (location_type=0) AND parent stations (location_type=1)
    # We need both because stop_times references parent stations for trains
    stops = stops[
        (stops['location_type'].isna()) | 
        (stops['location_type'] == 0) |
        (stops['location_type'] == 1)  # ← ADD THIS
    ]
    print(f"  {len(stops)} after filtering location_type")
    
    # Remove invalid coordinates
    stops = stops[
        (stops['stop_lat'] != 0) & 
        (stops['stop_lon'] != 0) &
        (stops['stop_lat'].notna()) &
        (stops['stop_lon'].notna())
    ]
    print(f"  {len(stops)} after removing invalid coords")
    
    # Filter to Melbourne region
    stops = stops[
        (stops['stop_lat'] >= MELBOURNE_BOUNDS['lat_min']) &
        (stops['stop_lat'] <= MELBOURNE_BOUNDS['lat_max']) &
        (stops['stop_lon'] >= MELBOURNE_BOUNDS['lon_min']) &
        (stops['stop_lon'] <= MELBOURNE_BOUNDS['lon_max'])
    ]
    print(f"  {len(stops)} after filtering to Melbourne")
    
    # For parent stations (location_type=1), use stop_id as station_id
    # For regular stops (location_type=0), group by parent_station if it exists
    stops['station_id'] = stops.apply(
        lambda row: row['stop_id'] if row['location_type'] == 1 
                    else (row['parent_station'] if pd.notna(row['parent_station']) else row['stop_id']),
        axis=1
    )
    
    # Create mapping: ALL stop_ids → station_id (for both platforms and parent stations)
    stop_to_station_map = stops[['stop_id', 'station_id']].copy()
    
    # For parent stations, also map them to themselves
    # This handles cases where stop_times references parent station directly
    parent_stations = stops[stops['location_type'] == 1][['stop_id']].copy()
    parent_stations['station_id'] = parent_stations['stop_id']
    stop_to_station_map = pd.concat([stop_to_station_map, parent_stations], ignore_index=True)
    
    # Remove duplicates (keep first)
    stop_to_station_map = stop_to_station_map.drop_duplicates(subset=['stop_id'], keep='first')
    
    # Create unique stations (one per station_id)
    stations = stops.groupby('station_id').first().reset_index()
    stations = stations[['station_id', 'stop_name', 'stop_lat', 'stop_lon']]
    
    print(f"  ✓ Created {len(stations)} unique stations")
    print(f"  ✓ Created {len(stop_to_station_map)} stop→station mappings")
    
    # Save
    stations.to_csv(f'{PROCESSED_DIR}/stops_cleaned.csv', index=False)
    stop_to_station_map.to_csv(f'{PROCESSED_DIR}/stop_to_station_map.csv', index=False)
    
    print(f"  ✓ Saved to stops_cleaned.csv and stop_to_station_map.csv")
    
    return stations, stop_to_station_map

if __name__ == "__main__":
    process_stops()