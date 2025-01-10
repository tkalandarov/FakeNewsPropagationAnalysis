import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import pickle

from networkx import nodes
from networkx.algorithms.bipartite import color


from Code.Nodes.User.User import User
from Code.Nodes.User.UserNode import UserNode
from Code.Nodes.NewsNode import NewsNode
from Code.Repository.DatasetRepository import DatasetRepository

from concurrent.futures import ThreadPoolExecutor
import threading


class NewsUserGraphBuilder:
    def __init__(self):
        print("Initializing GraphBuilder...")
        self.dataset_repository = DatasetRepository()
        self.graph = nx.DiGraph()
        print("GraphBuilder initialized.")

    def load_data(self):
        print("Loading data from DatasetRepository...")
        self.users_df = self.dataset_repository.userData.df
        self.news_user_df = self.dataset_repository.userNewsData.df
        self.user_user_df = self.dataset_repository.userUserData.df
        self.fake_news_df = self.dataset_repository.fakeNewsData.df
        self.real_news_df = self.dataset_repository.realNewsData.df
        print("Data loaded successfully.")
        print(f"Users DataFrame: {self.users_df.shape}")
        print(f"News-User DataFrame: {self.news_user_df.shape}")
        print(f"User-User DataFrame: {self.user_user_df.shape}")
        print(f"Fake News DataFrame: {self.fake_news_df.shape}")
        print(f"Real News DataFrame: {self.real_news_df.shape}")

    def create_nodes(self):

        print("Creating nodes...")
        for _, row in self.users_df.iterrows():
            user = User(row['userID'])
            success = user.getUserFeatures()
            if not success:
                continue
            user_node = UserNode(user)
            user_node.color = NewsUserGraphBuilder.assignColor(user)
            self.graph.add_node(row['userID'], node_type='user', embedding=user_node.embedding,
                                color=user_node.color)
            print(f"Added user node: {user.index}")

        # Create News Nodes (Fake and Real)
        for _, row in self.fake_news_df.iterrows():
            news_node = NewsNode()
            news_node.embedding = {'newsType': 'fake', 'title': row['title'], 'content': row['text']}
            self.graph.add_node(row['id'], node_type='fake_news', embedding=news_node.embedding, color='black')
            print(f"Added fake news node: {row['id']}")

        for _, row in self.real_news_df.iterrows():
            news_node = NewsNode()
            news_node.embedding = {'newsType': 'real', 'title': row['title'], 'content': row['text']}
            self.graph.add_node(row['id'], node_type='real_news', embedding=news_node.embedding, color='white')
            print(f"Added real news node: {row['id']}")
        print("Nodes created successfully.")

    def create_edges(self):
        print("Creating edges...")
        # Create User-User Edges
        for _, row in self.user_user_df.iterrows():
            follower = row['follower']
            followee = row['followee']
            if self.graph.has_node(follower) and self.graph.has_node(followee):
                self.graph.add_edge(follower, followee, edge_type='user-user')
                print(f"Added user-user edge: {follower} -> {followee}")

        # Create User-News Edges
        for _, row in self.news_user_df.iterrows():
            user_index = self.users_df.iloc[row['userIndex'] - 1]['userID']
            news_index = row['newsIndex']
            news_id = self.fake_news_df.iloc[news_index - 1]['id'] if news_index <= len(self.fake_news_df) else self.real_news_df.iloc[news_index - len(self.fake_news_df) - 1]['id']
            if self.graph.has_node(user_index) and self.graph.has_node(news_id):
                self.graph.add_edge(user_index, news_id, edge_type='user-news', frequency=row['frequency'])
                print(f"Added user-news edge: {user_index} -> {news_id} with frequency {row['frequency']}")
        print("Edges created successfully.")

    def build_graph(self):
        print("Building the graph...")
        self.load_data()
        self.create_nodes()
        self.create_edges()
        print("Graph built successfully.")
        return self.graph

    def visualize_graph(self):
        print("Visualizing the graph...")
        pos = nx.spring_layout(self.graph)
        node_colors = ['blue' if self.graph.nodes[node]['node_type'] == 'user' else 'red' if self.graph.nodes[node]['embedding']['newsType'] == 'real' else 'green' for node in self.graph.nodes()]
        node_sizes = [self.graph.nodes[n]['size'] for n in self.graph.nodes()]
        nx.draw(self.graph, pos, node_color=node_colors, node_sizes=node_sizes, with_labels=False, edge_color='grey')
        plt.show()
        print("Graph visualization complete.")

    def save_graph(self, filename='social_network.pkl'):
        print(f"Saving the graph to {filename}...")
        with open(filename, 'wb') as f:
            pickle.dump(self.graph, f)
        print(f"Graph saved to {filename}")
        nx.write_gexf(self.graph, "social_network.gexf")

    @staticmethod
    def load_graph(filename='social_network.pkl'):
        print(f"Loading the graph from {filename}...")
        with open(filename, 'rb') as f:
            graph = pickle.load(f)
        print(f"Graph loaded from {filename}")
        return graph

    @staticmethod
    def assignColor(user):
        fakeShareSus = user.fakeShareSusceptibility
        realShareSus = user.realShareSusceptibility
        fakeReceiveSus = user.fakeReceiveSusceptibility

        if fakeShareSus >= 0.7:
            nodeColor = 'red'
        else:
            if realShareSus > 0.7:
                nodeColor = 'blue'
            else:
                if fakeReceiveSus >= 0.43:
                    nodeColor = 'red'
                elif 0.43 > fakeReceiveSus > 0.1:
                    nodeColor = 'blue'
                else:
                    nodeColor = 'green'

        return nodeColor
