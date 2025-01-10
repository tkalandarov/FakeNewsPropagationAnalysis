import pandas as pd
import warnings

from Code.EmotionExtraction.EmotionExtractor import EmotionExtractor
from Code.Repository.DatasetRepository import DatasetRepository
from Code.Utils.CSVFileHandler import CSVFileHandler


# Suppress all warnings
warnings.filterwarnings("ignore")

class User:
    def __init__(self, userID):
        self.userID = userID
        self.index = User.getIndex(userID)

        self.fakeShareSusceptibility = None
        self.realShareSusceptibility = None
        self.fakeReceiveSusceptibility = None
        self.realReceiveSusceptibility = None
        self.fakeNewsShared = None
        self.realNewsShared = None
        self.totalNewsShared = None
        self.followerCount = None
        self.followingCount = None
        self.meanAnger = None
        self.meanDisgust = None
        self.meanSadness = None
        self.meanFear = None
        self.meanJoy = None
        self.meanNeutral = None
        self.meanSurprise = None
        self.influence = None

        self.sharedFakeNews = None
        self.sharedRealNews = None
        self.following = None
        self.followers = None

        self.emotionExtractor = EmotionExtractor()

    @staticmethod
    def getIndex(userID):
        df = DatasetRepository.userData.df
        # Get the index
        try:
            return df[df['userID'] == userID].index.values[0] + 1
        except ValueError:
            return -1

    @staticmethod
    def getID(userIndex):
        df = DatasetRepository.userData.df
        return df.loc[userIndex - 1]['userID']

    def getUserFeatures(self):
        user_embeddings = DatasetRepository.userEmbeddings.df[DatasetRepository.userEmbeddings.df['userIndex'] == self.index+1]

        if len(user_embeddings.values) <= 0:
            return False

        self.fakeShareSusceptibility = user_embeddings['fakeShareSusceptibility'].iloc[0]
        self.realShareSusceptibility = user_embeddings['realShareSusceptibility'].iloc[0]
        self.fakeReceiveSusceptibility = user_embeddings['fakeReceiveSusceptibility'].iloc[0]
        self.realReceiveSusceptibility = user_embeddings['realReceiveSusceptibility'].iloc[0]
        self.fakeNewsShared = user_embeddings['fakeNewsShared'].iloc[0]
        self.realNewsShared = user_embeddings['realNewsShared'].iloc[0]
        self.totalNewsShared = user_embeddings['totalNewsShared'].iloc[0]
        self.followerCount = user_embeddings['followerCount'].iloc[0]
        self.followingCount = user_embeddings['followingCount'].iloc[0]
        self.meanAnger = user_embeddings['meanAnger'].iloc[0]
        self.meanDisgust = user_embeddings['meanDisgust'].iloc[0]
        self.meanSadness = user_embeddings['meanSadness'].iloc[0]
        self.meanFear = user_embeddings['meanFear'].iloc[0]
        self.meanJoy = user_embeddings['meanJoy'].iloc[0]
        self.meanNeutral = user_embeddings['meanNeutral'].iloc[0]
        self.meanSurprise = user_embeddings['meanSurprise'].iloc[0]

        return True

    def extractUserFeatures(self):
        self.fakeShareSusceptibility = self.getFakeNewsShareSusceptibility()
        self.realShareSusceptibility = self.getRealNewsShareSusceptibility()
        self.fakeReceiveSusceptibility = self.getFakeReceiveSusceptibility()
        self.realReceiveSusceptibility = self.getRealReceiveSusceptibility()
        self.fakeNewsShared = len(self.sharedFakeNews)
        self.realNewsShared = len(self.sharedRealNews)
        self.totalNewsShared = self.fakeNewsShared + self.realNewsShared
        self.followerCount = len(self.getFollowers(self.index))
        self.followingCount = len(self.getFollowing(self.index))

        self.getEmotion()

    def getSharedFakeNews(self, index=None):
        if index is None:
            index = self.index

        sharedNewsIndices = (
                    DatasetRepository.userNewsData.df[DatasetRepository.userNewsData.df['userIndex'] == index][
                        'newsIndex'] - 1).tolist()
        sharedFakeNewsIndices = [index for index in sharedNewsIndices if index >= len(DatasetRepository.fakeNewsData.df)]
        sharedFakeNewsIds = DatasetRepository.newsData.df.loc[sharedFakeNewsIndices]
        sharedFakeNewsIds['newsID'] = sharedFakeNewsIds['newsID'].str[9:] + '-Webpage'
        sharedFakeNewsIds = sharedFakeNewsIds['newsID'].tolist()
        sharedFakeNews = DatasetRepository.fakeNewsData.df[
            DatasetRepository.fakeNewsData.df['id'].isin(sharedFakeNewsIds)]

        return sharedFakeNews

    def getSharedRealNews(self, index=None):
        if index is None:
            index = self.index
        sharedNewsIndices = (
                    DatasetRepository.userNewsData.df[DatasetRepository.userNewsData.df['userIndex'] == index][
                        'newsIndex'] - 1).tolist()
        sharedRealNewsIndices = [index for index in sharedNewsIndices if index < len(DatasetRepository.fakeNewsData.df)]
        sharedRealNewsIds = DatasetRepository.newsData.df.loc[sharedRealNewsIndices]
        sharedRealNewsIds['newsID'] = sharedRealNewsIds['newsID'].str[9:] + '-Webpage'
        sharedRealNewsIds = sharedRealNewsIds['newsID'].tolist()
        sharedRealNews = DatasetRepository.realNewsData.df[
            DatasetRepository.realNewsData.df['id'].isin(sharedRealNewsIds)]

        return sharedRealNews

    def getFollowers(self, index=None):
        if index is None:
            if self.followers is None:
                self.followers = DatasetRepository.userUserData.df[DatasetRepository.userUserData.df['followee'] == self.index][
                    'follower'].tolist()
            return self.followers
        else:
            self.followers = DatasetRepository.userUserData.df[DatasetRepository.userUserData.df['followee'] == index][
                'follower'].tolist()
            return self.followers

    def getFollowing(self, index=None):
        if index is None:
            if self.following is None:
                self.following = DatasetRepository.userUserData.df[DatasetRepository.userUserData.df['follower'] == self.index][
                    'followee'].tolist()
            return self.following
        else:
            self.following = DatasetRepository.userUserData.df[DatasetRepository.userUserData.df['follower'] == index][
                'followee'].tolist()
            return self.following

    def getReceivedNews(self, index):
        following = self.getFollowing(index)
        fakeNews = pd.DataFrame()
        realNews = pd.DataFrame()

        for userIndex in following:
            sharedFakeNews = self.getSharedFakeNews(userIndex)
            sharedRealNews = self.getSharedRealNews(userIndex)
            if len(sharedFakeNews) > 0:
                fakeNews = pd.concat([fakeNews, sharedFakeNews], ignore_index=True)
            if len(sharedRealNews) > 0:
                realNews = pd.concat([realNews, sharedRealNews], ignore_index=True)
        return fakeNews, realNews

    def getFakeNewsShareSusceptibility(self):
        if self.fakeShareSusceptibility is None:
            self.sharedFakeNews = self.getSharedFakeNews()
            self.fakeShareSusceptibility = round(
                len(self.sharedFakeNews) / (len(self.sharedFakeNews) + len(self.sharedRealNews)), 2)
        return self.fakeShareSusceptibility

    def getRealNewsShareSusceptibility(self):
        if self.realShareSusceptibility is None:
            self.sharedRealNews = self.getSharedRealNews()
            self.realShareSusceptibility = round(
                len(self.sharedRealNews) / (len(self.sharedFakeNews) + len(self.sharedRealNews)), 2)
        return self.realShareSusceptibility

    def getFakeReceiveSusceptibility(self):
        if self.fakeReceiveSusceptibility is None:
            receivedFakeNews, receivedRealNews = self.getReceivedNews(self.index)
            if len(receivedFakeNews) + len(receivedRealNews) == 0:
                self.fakeReceiveSusceptibility = 0
            else:
                self.fakeReceiveSusceptibility = round(
                    len(receivedFakeNews) / (len(receivedFakeNews) + len(receivedRealNews)), 2)
        return self.fakeReceiveSusceptibility

    def getRealReceiveSusceptibility(self):
        if self.realReceiveSusceptibility is None:
            receivedFakeNews, receivedRealNews = self.getReceivedNews(self.index)
            if len(receivedFakeNews) + len(receivedRealNews) == 0:
                self.realReceiveSusceptibility = 0
            else:
                self.realReceiveSusceptibility = round(
                    len(receivedRealNews) / (len(receivedFakeNews) + len(receivedRealNews)), 2)
        return self.realReceiveSusceptibility

    def getAverageEmotionFromSet(self, newsDF, totalValues):
        for index, news in newsDF.iterrows():
            emotions = self.emotionExtractor.extract_emotion(text=[news['text']])
            for emotion, intensity in emotions.items():
                totalValues[emotion] += intensity
        return totalValues

    def getEmotion(self):
        if self.meanAnger is None:
            totalValues = {key: 0.0 for key in self.emotionExtractor.emotion_intensity}
            totalValues = self.getAverageEmotionFromSet(self.sharedFakeNews, totalValues)
            totalValues = self.getAverageEmotionFromSet(self.sharedRealNews, totalValues)

            totalNewsShared = len(self.sharedFakeNews) + len(self.sharedRealNews)
            self.meanAnger = totalValues['anger'] / totalNewsShared
            self.meanJoy = totalValues['joy'] / totalNewsShared
            self.meanSadness = totalValues['sadness'] / totalNewsShared
            self.meanDisgust = totalValues['disgust'] / totalNewsShared
            self.meanFear = totalValues['fear'] / totalNewsShared
            self.meanNeutral = totalValues['neutral'] / totalNewsShared
            self.meanSurprise = totalValues['surprise'] / totalNewsShared

        return self.meanAnger, self.meanJoy, self.meanSadness, self.meanDisgust, self.meanFear, self.meanNeutral, self.meanSurprise

    def addUserToRepo(self):
        CSVFileHandler.addRow({"userIndex":self.index,
                               "fakeShareSusceptibility":self.fakeShareSusceptibility,
                               "realShareSusceptibility":self.realShareSusceptibility,
                               "fakeReceiveSusceptibility":self.fakeReceiveSusceptibility,
                               "realReceiveSusceptibility":self.realReceiveSusceptibility,
                               "fakeNewsShared":self.fakeNewsShared,
                               "realNewsShared":self.realNewsShared,
                               "totalNewsShared":self.totalNewsShared,
                               "followingCount":self.followingCount,
                               "followerCount":self.followerCount,
                               "meanAnger":self.meanAnger,
                               "meanJoy":self.meanJoy,
                               "meanSadness":self.meanSadness,
                               "meanDisgust":self.meanDisgust,
                               "meanFear":self.meanFear,
                               "meanNeutral":self.meanNeutral,
                               "meanSurprise":self.meanSurprise},
                              filePath=DatasetRepository.userEmbeddings.path)



    def print_user(self):
        print("Fake news share sus: " + str(self.fakeShareSusceptibility))
        print("Real news share sus: " + str(self.realShareSusceptibility))
        print("Fake news received sus: " + str(self.fakeReceiveSusceptibility))
        print("Real news received sus: " + str(self.realReceiveSusceptibility))
        print("Fake news shared: "+str(self.fakeNewsShared))
        print("Real news shared: "+str(self.realNewsShared))
        print("Total news shared: "+str(self.totalNewsShared))
        print("Followers: " + str(self.followerCount))
        print("Following: " + str(self.followingCount))
        print("Emotions: " +
              "mean anger: " + str(self.meanAnger) +
              "mean disgust: " + str(self.meanDisgust) +
              "mean sadness: " + str(self.meanSadness) +
              "mean fear: " + str(self.meanFear) +
              "mean joy: " + str(self.meanJoy) +
              "mean neutral: " + str(self.meanNeutral) +
              "mean surprise: " + str(self.meanSurprise))
