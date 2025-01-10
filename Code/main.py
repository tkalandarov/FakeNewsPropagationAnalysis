from Code.Graph.NewsSpreadGraph import NewsSpreadGraph

# Initialize and build the separate graphs
graph_builder_v2 = NewsSpreadGraph()
graph_builder_v2.load_data()
graph_builder_v2.create_separate_news_graphs()

# Save the graphs to a CSV file
graph_builder_v2.save_to_csv("separate_news_graphs.csv")
