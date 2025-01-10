import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import matplotlib.cm as cm

# Define the adjacency matrix
adj_matrix = [
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
    [0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0]
]

# Feature vectors for each node
feature_vectors = [
    [0.75, 0.16, 0.7],
    [0.33, 0.07, 0.25],
    [0.16, 0.3, 0.76],
    [0.45, 0.25, 0.1],
    [0.57, 0.07, 0.72],
    [0.3, 0.53, 0.3],
    [0.93, 0.09, 0.2],
    [0.68, 0.95, 0.06],
    [0.85, 0.19, 0.8],
    [0.76, 0.23, 0.94]
]

# Extract individual feature sets (1st, 2nd, 3rd features)
first_feature = [vec[0] for vec in feature_vectors]
second_feature = [vec[1] for vec in feature_vectors]
third_feature = [vec[2] for vec in feature_vectors]

# Get the global min and max across all features for consistent normalization
all_features = first_feature + second_feature + third_feature
global_min = min(all_features)
global_max = max(all_features)

# Normalize using the global min and max
norm = plt.Normalize(global_min, global_max)

# Create colors for each graph based on the normalized features
colors1 = cm.Reds(norm(first_feature))
colors2 = cm.Reds(norm(second_feature))
colors3 = cm.Reds(norm(third_feature))

# Create a graph using NetworkX
G = nx.from_numpy_array(np.array(adj_matrix))

# Create subplots for the three graphs
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Draw the first graph (colored by 1st feature)
nx.draw(G, with_labels=True, node_color=colors1, font_weight='bold', node_size=700, edge_color='gray', ax=axes[0])
axes[0].set_title('Graph Colored by 1st Feature')

# Draw the second graph (colored by 2nd feature)
nx.draw(G, with_labels=True, node_color=colors2, font_weight='bold', node_size=700, edge_color='gray', ax=axes[1])
axes[1].set_title('Graph Colored by 2nd Feature')

# Draw the third graph (colored by 3rd feature)
nx.draw(G, with_labels=True, node_color=colors3, font_weight='bold', node_size=700, edge_color='gray', ax=axes[2])
axes[2].set_title('Graph Colored by 3rd Feature')

# Adjust spacing to make room for the colorbar
plt.subplots_adjust(right=0.85)

# Add a single colorbar on the right side of the plots
cbar_ax = fig.add_axes([0.91, 0.15, 0.01, 0.7])  # Position of colorbar (left, bottom, width, height)
cbar = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cm.Reds), cax=cbar_ax)
cbar.set_label('Feature Intensity')

plt.show()
