import networkx as nx
import pandas as pd
from Code.Repository.DatasetRepository import DatasetRepository


class NewsSpreadGraph:
    def __init__(self):
        print("Initializing GraphBuilderV2...")
        self.dataset_repository = DatasetRepository()
        self.graphs = {}  # Dictionary to store separate graphs for each news article
        print("GraphBuilderV2 initialized.")

    def load_data(self):
        print("Loading data from DatasetRepository...")
        # Load datasets into pandas DataFrames
        self.users_df = self.dataset_repository.userData.df
        self.news_user_df = self.dataset_repository.userNewsData.df
        self.user_user_df = self.dataset_repository.userUserData.df
        self.fake_news_df = self.dataset_repository.fakeNewsData.df
        self.real_news_df = self.dataset_repository.realNewsData.df
        print("Data loaded successfully.")

    def create_separate_news_graphs(self):
        print("Creating separate graphs for each news article...")

        # Merge real and fake news into a single DataFrame
        all_news_df = pd.concat([self.fake_news_df, self.real_news_df], ignore_index=True)

        # Create separate graphs for each news article
        for _, news in all_news_df.iterrows():
            news_id = news['id']
            news_graph = nx.DiGraph()  # Create a directed graph for each news article

            # Add the news node
            news_graph.add_node(news_id, node_type='news')

            # Find users who shared this news
            news_index = all_news_df.index[all_news_df['id'] == news_id].tolist()[0] + 1
            shared_users = self.news_user_df[self.news_user_df['newsIndex'] == news_index]['userIndex']

            # Add users who shared the news as nodes and create news-user edges
            for user_idx in shared_users:
                user_id = self.users_df.iloc[user_idx - 1]['userID']
                news_graph.add_node(user_id, node_type='user')
                news_graph.add_edge(news_id, user_id, edge_type='news-user')

            # Add followers of users who shared the news
            for user_idx in shared_users:
                user_id = self.users_df.iloc[user_idx - 1]['userID']
                followers = self.user_user_df[self.user_user_df['followee'] == user_id]['follower']
                for follower in followers:
                    if not news_graph.has_node(follower):
                        news_graph.add_node(follower, node_type='user')
                    news_graph.add_edge(follower, user_id, edge_type='user-user')

            # Store the graph in the dictionary
            self.graphs[news_id] = news_graph
            print(f"Created separate graph for news article: {news_id}")

        print("Separate graphs created successfully.")

    def extract_graph_features(self):
        print("Extracting graph features for CSV...")
        graph_data = []

        for news_id, graph in self.graphs.items():
            # Graph ID
            graph_id = news_id

            # User Nodes
            user_nodes = [node for node, data in graph.nodes(data=True) if data['node_type'] == 'user']
            user_nodes_str = ",".join(map(str, user_nodes))

            # News-User Edge List
            news_user_edges = [f"{news_id}->{user}" for _, user in graph.edges(news_id)]
            news_user_edges_str = ",".join(news_user_edges)

            # User-User Edge List
            user_user_edges = [f"{u1}-{u2}" for u1, u2 in graph.edges if graph[u1][u2]['edge_type'] == 'user-user']
            user_user_edges_str = ",".join(user_user_edges)

            # Append to graph data
            graph_data.append([graph_id, user_nodes_str, news_user_edges_str, user_user_edges_str])

        return pd.DataFrame(graph_data,
                            columns=["Graph ID", "User Nodes", "News-User Edge List", "User-User Edge List"])

    def save_to_csv(self, output_filename="separate_graphs.csv"):
        print(f"Saving graphs to {output_filename}...")
        graph_df = self.extract_graph_features()
        graph_df.to_csv(output_filename, index=False)
        print(f"Graphs saved successfully to {output_filename}.")
