import networkx as nx
import pickle
import pandas as pd

def load_graph():
    """Load the PT graph"""
    with open('data/processed/pt_graph.gpickle', 'rb') as f:
        return pickle.load(f)

def validate_graph():
    print("="*60)
    print("PT GRAPH VALIDATION")
    print("="*60)
    
    # Load graph
    print("\n[1/7] Loading graph...")
    G = load_graph()
    print(f"  ✓ Graph loaded")
    
    # Basic statistics
    print("\n[2/7] Basic Statistics:")
    print(f"  Nodes: {G.number_of_nodes()}")
    print(f"  Edges: {G.number_of_edges()}")
    print(f"  Average degree: {sum(dict(G.degree()).values()) / G.number_of_nodes():.2f}")
    
    # Check node attributes
    print("\n[3/7] Validating Node Attributes:")
    sample_node = list(G.nodes(data=True))[0]
    required_node_attrs = ['stop_name', 'lat', 'lon', 'node_type']
    missing_node_attrs = [attr for attr in required_node_attrs if attr not in sample_node[1]]
    
    if missing_node_attrs:
        print(f"  ✗ Missing node attributes: {missing_node_attrs}")
    else:
        print(f"  ✓ All required node attributes present")
    
    # Check edge attributes
    print("\n[4/7] Validating Edge Attributes:")
    sample_edge = list(G.edges(data=True))[0]
    required_edge_attrs = ['route_id', 'mode', 'distance', 'time']
    missing_edge_attrs = [attr for attr in required_edge_attrs if attr not in sample_edge[2]]
    
    if missing_edge_attrs:
        print(f"  ✗ Missing edge attributes: {missing_edge_attrs}")
    else:
        print(f"  ✓ All required edge attributes present")
    
    # Mode distribution
    print("\n[5/7] Mode Distribution:")
    modes = {}
    for u, v, data in G.edges(data=True):
        mode = data.get('mode', 'unknown')
        modes[mode] = modes.get(mode, 0) + 1
    
    for mode, count in sorted(modes.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / G.number_of_edges()) * 100
        print(f"  {mode}: {count} edges ({percentage:.1f}%)")
    
    # Check for graph issues
    print("\n[6/7] Graph Integrity Checks:")
    
    # Isolated nodes
    isolated = list(nx.isolates(G))
    if isolated:
        print(f"  ⚠ Warning: {len(isolated)} isolated nodes")
        if len(isolated) <= 5:
            for node in isolated:
                data = G.nodes[node]
                print(f"    - {data.get('stop_name', 'Unknown')} ({node})")
    else:
        print(f"  ✓ No isolated nodes")
    
    # Weakly connected components
    if not G.is_directed():
        components = list(nx.connected_components(G))
    else:
        components = list(nx.weakly_connected_components(G))
    
    if len(components) == 1:
        print(f"  ✓ Graph is fully connected")
    else:
        print(f"  ⚠ Graph has {len(components)} components")
        component_sizes = sorted([len(c) for c in components], reverse=True)
        print(f"    Largest: {component_sizes[0]} nodes")
        if len(component_sizes) > 1:
            print(f"    Second largest: {component_sizes[1]} nodes")
    
    # Check for zero/negative values
    zero_time = sum(1 for u, v, d in G.edges(data=True) if d.get('time', 0) <= 0)
    zero_distance = sum(1 for u, v, d in G.edges(data=True) if d.get('distance', 0) <= 0)
    
    if zero_time > 0:
        print(f"  ⚠ {zero_time} edges with zero/negative time")
    else:
        print(f"  ✓ No edges with zero/negative time")
    
    if zero_distance > 0:
        print(f"  ⚠ {zero_distance} edges with zero/negative distance")
    else:
        print(f"  ✓ No edges with zero/negative distance")
    
    # Edge statistics
    times = [d.get('time', 0) for u, v, d in G.edges(data=True)]
    distances = [d.get('distance', 0) for u, v, d in G.edges(data=True)]
    
    print(f"\n  Edge Statistics:")
    print(f"    Avg time: {sum(times)/len(times):.1f}s ({sum(times)/len(times)/60:.1f} min)")
    print(f"    Avg distance: {sum(distances)/len(distances):.1f}m ({sum(distances)/len(distances)/1000:.2f} km)")
    
    # Pathfinding tests
    print("\n[7/7] Pathfinding Tests:")
    test_pathfinding(G)
    
    print("\n" + "="*60)
    print("VALIDATION COMPLETE")
    print("="*60)

def test_pathfinding(G):
    """Test pathfinding with known Melbourne routes"""
    
    # Find test stations
    test_queries = [
        ('Southern Cross', 'Flinders Street'),
        ('Melbourne Central', 'Flagstaff'),
        ('Richmond', 'Flinders Street'),
    ]
    
    tests_passed = 0
    tests_failed = 0
    
    for origin_name, dest_name in test_queries:
        # Find nodes
        origin_nodes = [n for n, d in G.nodes(data=True) 
                       if origin_name.lower() in d.get('stop_name', '').lower()]
        dest_nodes = [n for n, d in G.nodes(data=True) 
                     if dest_name.lower() in d.get('stop_name', '').lower()]
        
        if not origin_nodes or not dest_nodes:
            print(f"  ⚠ Could not find: {origin_name} → {dest_name}")
            tests_failed += 1
            continue
        
        try:
            # Find shortest path by time
            path = nx.shortest_path(G, origin_nodes[0], dest_nodes[0], weight='time')
            path_time = nx.shortest_path_length(G, origin_nodes[0], dest_nodes[0], weight='time')
            
            # Calculate total distance
            total_distance = sum(
                G[path[i]][path[i+1]]['distance'] 
                for i in range(len(path)-1)
            )
            
            # Get modes used
            modes_used = set()
            for i in range(len(path)-1):
                modes_used.add(G[path[i]][path[i+1]]['mode'])
            
            print(f"  ✓ {origin_name} → {dest_name}")
            print(f"    Path: {len(path)} stops")
            print(f"    Time: {path_time:.0f}s ({path_time/60:.1f} min)")
            print(f"    Distance: {total_distance:.0f}m ({total_distance/1000:.2f} km)")
            print(f"    Modes: {', '.join(modes_used)}")
            
            tests_passed += 1
            
        except nx.NetworkXNoPath:
            print(f"  ✗ No path found: {origin_name} → {dest_name}")
            tests_failed += 1
        except Exception as e:
            print(f"  ✗ Error: {origin_name} → {dest_name} ({e})")
            tests_failed += 1
    
    # Random reachability test
    print(f"\n  Random Reachability Test:")
    random_node = list(G.nodes())[0]
    reachable = len(nx.descendants(G, random_node))
    reachable_pct = (reachable / G.number_of_nodes()) * 100
    print(f"    From random node: can reach {reachable}/{G.number_of_nodes()} nodes ({reachable_pct:.1f}%)")
    
    print(f"\n  Summary: {tests_passed} passed, {tests_failed} failed")

def cross_validate_with_csv():
    """Cross-validate graph with source CSV files"""
    print("\n" + "="*60)
    print("CROSS-VALIDATION WITH SOURCE DATA")
    print("="*60)
    
    # Load graph
    G = load_graph()
    
    # Load source data
    print("\n[1/3] Loading source data...")
    edges_merged = pd.read_csv('data/processed/edges_merged.csv')
    stops_cleaned = pd.read_csv('data/processed/stops_cleaned.csv')
    
    print(f"  edges_merged.csv: {len(edges_merged)} edges")
    print(f"  stops_cleaned.csv: {len(stops_cleaned)} stops")
    
    # Check node count matches
    print("\n[2/3] Node Count Validation:")
    if G.number_of_nodes() == len(stops_cleaned):
        print(f"  ✓ Graph nodes ({G.number_of_nodes()}) matches stops_cleaned ({len(stops_cleaned)})")
    else:
        print(f"  ⚠ Mismatch: Graph has {G.number_of_nodes()} nodes, stops_cleaned has {len(stops_cleaned)}")
    
    # Check edge count (should be less due to invalid edges filtered)
    print("\n[3/3] Edge Count Validation:")
    print(f"  edges_merged.csv: {len(edges_merged)} edges")
    print(f"  Graph: {G.number_of_edges()} edges")
    diff = len(edges_merged) - G.number_of_edges()
    if diff > 0:
        print(f"  ✓ {diff} edges were filtered out (invalid stations)")
    elif diff == 0:
        print(f"  ✓ All edges from CSV are in graph")
    else:
        print(f"  ⚠ Graph has MORE edges than CSV? ({-diff} extra)")
    
    # Sample validation: check if specific edges exist
    print("\n  Sample Edge Validation:")
    for i in range(min(5, len(edges_merged))):
        edge = edges_merged.iloc[i]
        from_s = str(edge['from_station'])
        to_s = str(edge['to_station'])
        
        if G.has_edge(from_s, to_s):
            print(f"  ✓ Edge {from_s} → {to_s} exists")
        else:
            print(f"  ✗ Edge {from_s} → {to_s} NOT in graph")

if __name__ == "__main__":
    validate_graph()
    cross_validate_with_csv()