import networkx as nx, pickle
import pandas as pd
G = pickle.load(open('data/processed/pt_graph.gpickle','rb'))

source = 'vic:rail:FSS'   # change to actual ids
target = 'vic:rail:RMD'

print(source in G, target in G)
# which component?
components = list(nx.strongly_connected_components(G))
node_to_comp = {n:i for i, comp in enumerate(components) for n in comp}
print("comp sizes sample", [len(c) for c in components[:5]])
if source in node_to_comp and target in node_to_comp:
    print("same component?", node_to_comp[source]==node_to_comp[target])
else:
    print("One of nodes not present in components map")

print("neighbors from source:", list(G.successors(source))[:10])
print("incoming to target:", list(G.predecessors(target))[:10])

try:
    path = nx.shortest_path(G.to_undirected(), source, target, weight='time')
    print("undirected path exists, length:", len(path))
except nx.NetworkXNoPath:
    print("no undirected path either")

path = nx.shortest_path(G, source, target, weight='time')
for u,v in zip(path[:-1], path[1:]):
    print(u, "->", v, G[u][v]['mode'], G[u][v]['time'], G[u][v]['distance'], G[u][v].get('route_name'))


import networkx as nx
import pickle

with open("data/processed/pt_graph.gpickle", "rb") as f:
    G = pickle.load(f)

src, dst = "vic:rail:FSS", "vic:rail:RMD"

print("Directed path exists (nx.has_path)?", nx.has_path(G, src, dst))
print("Undirected path exists?", nx.has_path(G.to_undirected(), src, dst))

try:
    path = nx.shortest_path(G, src, dst, weight='time')
    print("Directed path found:", path)
except nx.NetworkXNoPath:
    print("❌ No directed path found")

# Check edge weights for invalid values
invalid_weights = [(u,v,d['time']) for u,v,d in G.edges(data=True) if pd.isna(d['time']) or d['time'] <= 0]
print("Invalid time edges:", len(invalid_weights))
