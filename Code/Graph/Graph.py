from Code.Nodes.User.User import User
from Code.Nodes.User.UserNode import UserNode


class Graph:
    def __init__(self, newsID):
        self.nodes = []
        self.edges = []
        self.adjacency = {}
        # self.nodes.append(NewsNode(newsID))

    def addUser(self, userID):
        user = User(userID)
        userNode = UserNode(userID)
        self.nodes.append(userNode)

    def addEdge(self, sourceNode, targetNode):
        pass

    def generateEdges(self):
        pass

    def extractUserNodeFeatures(self):
        for userNode in self.nodes:
            userNode.extractGraphSpecificFeatures(self)

    def extractEdgeFeatures(self):
        pass


