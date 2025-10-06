import networkx as nx
import pickle

def load_graph():
    with open('data/processed/pt_graph.gpickle', 'rb') as f:
        return pickle.load(f)

def test_graph():
    print("Loading graph...")
    G = load_graph()
    
    print(f"\nGraph Statistics:")
    print(f"  Nodes: {G.number_of_nodes()}")
    print(f"  Edges: {G.number_of_edges()}")
    print(f"  Avg degree: {sum(dict(G.degree()).values()) / G.number_of_nodes():.2f}")
    
    # Mode distribution
    modes = {}
    for u, v, data in G.edges(data=True):
        mode = data.get('mode', 'unknown')
        modes[mode] = modes.get(mode, 0) + 1
    
    print(f"\n  Mode Distribution:")
    for mode, count in sorted(modes.items(), key=lambda x: x[1], reverse=True):
        print(f"    {mode}: {count} edges")
    
    # Sample nodes
    print(f"\n  Sample Stations:")
    for node in list(G.nodes())[:5]:
        data = G.nodes[node]
        print(f"    {data['stop_name']} ({node})")
    
    # Sample edges
    print(f"\n  Sample Edges:")
    for u, v, data in list(G.edges(data=True))[:3]:
        from_name = G.nodes[u]['stop_name']
        to_name = G.nodes[v]['stop_name']
        print(f"    {from_name} → {to_name}")
        print(f"      Mode: {data['mode']}, Time: {data['time']:.0f}s, Distance: {data['distance']:.0f}m")
    
    # Test query
    print(f"\n  Testing Query:")
    print(f"    Find all stations reachable from first node...")
    first_node = list(G.nodes())[0]
    reachable = len(nx.descendants(G, first_node))
    print(f"    ✓ Can reach {reachable} stations")

if __name__ == "__main__":
    test_graph()