# Green-ReRouting
Capstone Project Feature. Algorithm to find and suggest routes that save emissions. Innovation: using multiple modes of transportation. 

Order to Run:
    1. unzip_gtfs: extracts into raw data folder
    2. parse_gtfs: loads all GTFS feeds, filter relevant routes, produces cleaned CSV files
        Output: routes.csv, stops_raw.csv, trips.csv, stop_times.csv
    3. stops: creates nodes
    4. edges: creates edges using route id, stop times, emissions factor
    5. merge: get rid of duplicate edges
    6. build_graph: creates an NetworkX graph 