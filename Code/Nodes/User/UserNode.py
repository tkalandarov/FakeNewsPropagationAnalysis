import pandas as pd
from Code.Nodes.Node import Node


class UserNode(Node):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.embedding = {
            "userType": -1,
            "fakeShareSusceptibility": 0,
            "realShareSusceptibility": 0,
            "fakeReceiveSusceptibility": 0,
            "realReceiveSusceptibility": 0,
            "followerCount": 0,
            "followingCount": 0,
            "meanAnger": 0,
            "meanDisgust": 0,
            "meanSadness": 0,
            "meanFear": 0,
            "meanJoy": 0,
            "meanNeutral": 0,
            "meanSurprise": 0,
            "maxSpreadDist": 0,
            "influence": 0,
            "exposure": 0,
            "avNeighbourRealShareSusceptibility": 0,
            "avNeighbourFakeShareSusceptibility": 0
        }
        self.color = 'black'
        self.assignGlobalUserFeatures()

    def assignGlobalUserFeatures(self):
        self.embedding["fakeShareSusceptibility"] = self.user.fakeShareSusceptibility
        self.embedding["realShareSusceptibility"] = self.user.realShareSusceptibility
        self.embedding["fakeReceiveSusceptibility"] = self.user.fakeReceiveSusceptibility
        self.embedding["realReceiveSusceptibility"] = self.user.realReceiveSusceptibility
        self.embedding["followerCount"] = self.user.followerCount
        self.embedding["followingCount"] = self.user.followingCount
        self.embedding["meanAnger"] = self.user.meanAnger
        self.embedding["meanDisgust"] = self.user.meanDisgust
        self.embedding["meanSadness"] = self.user.meanSadness
        self.embedding["meanFear"] = self.user.meanFear
        self.embedding["meanJoy"] = self.user.meanJoy
        self.embedding["meanNeutral"] = self.user.meanNeutral
        self.embedding["meanSurprise"] = self.user.meanSurprise
        self.embedding["influence"] = self.user.influence

    def extractGraphSpecificFeatures(self, graph):
        pass




    


