import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Add nodes with cluster labels
G.add_node(1, node_type='user', cluster='A')
G.add_node(2, node_type='user', cluster='A')
G.add_node(3, node_type='user', cluster='B')
G.add_node(4, node_type='user', cluster='B')
G.add_node(5, node_type='user', cluster='C')

# Add directed edges between nodes
G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5)])

# Save the graph in GEXF format
nx.write_gexf(G, "colored_graph.gexf")
