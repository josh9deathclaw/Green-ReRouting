import pandas as pd
import networkx as nx
import pickle

PROCESSED_DIR = "data/processed/"

# Emissions factors (kg CO2 per passenger-km)
# These are example values - use your team's actual model
EMISSIONS_FACTORS = {
    'train': 0.041,  # Electric trains are most efficient
    'tram': 0.045,   # Electric trams
    'bus': 0.089     # Diesel/hybrid buses
}

def build_graph(save=True):
    print("Building NetworkX graph...")
    
    # Create directed graph (bidirectional)
    G = nx.DiGraph()
    
    # Load stations (nodes)
    stations = pd.read_csv(f'{PROCESSED_DIR}/stops_cleaned.csv')
    print(f"  Adding {len(stations)} nodes...")
    
    # Add nodes
    for _, station in stations.iterrows():
        G.add_node(
            station['station_id'],
            stop_name=station['stop_name'],
            lat=station['stop_lat'],
            lon=station['stop_lon'],
            node_type='pt_stop'
        )
    
    print(f"  ✓ Added {G.number_of_nodes()} nodes")
    
    # Load edges
    edges = pd.read_csv(f'{PROCESSED_DIR}/edges_merged.csv')
    print(f"  Adding {len(edges)} edges...")
    
    # Add edges
    for _, edge in edges.iterrows():
        # Calculate emissions (kg CO2)
        emissions_factor = EMISSIONS_FACTORS.get(edge['mode'], 0.1)
        emissions = (edge['distance'] / 1000) * emissions_factor  # Convert distance to km
        
        G.add_edge(
            edge['from_station'],
            edge['to_station'],
            route_id=edge['route_id'],
            route_name=edge['route_name'],
            mode=edge['mode'],
            distance=edge['distance'],  # meters
            time=edge['time'],          # seconds
            emissions_factor=emissions_factor,
            emissions=emissions          # kg CO2 for this segment
        )
    
    print(f"  ✓ Added {G.number_of_edges()} edges")
    
    # Save graph
    if save:
        output_path = f'{PROCESSED_DIR}/pt_graph.gpickle'
        with open(output_path, 'wb') as f:
            pickle.dump(G, f, pickle.HIGHEST_PROTOCOL)
        
        print(f"\n✓ Graph saved to {output_path}")
    
    return G

if __name__ == "__main__":
    build_graph()