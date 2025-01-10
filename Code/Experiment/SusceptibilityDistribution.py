from Code.Nodes.User.User import User
from Code.Repository.DatasetRepository import DatasetRepository
import matplotlib.pyplot as plt
from collections import Counter
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def createDistribution(data, name):
    # Create the frequency distribution using Counter
    freq_distribution = Counter(data)

    # Extract the unique numbers and their frequencies
    values = list(freq_distribution.keys())
    frequencies = list(freq_distribution.values())

    # Plot the frequency distribution as a bar chart
    plt.bar(values, frequencies, width=0.1)
    plt.xlabel('Numbers')
    plt.ylabel('Frequency')
    plt.title(name)
    plt.show()

def calculateCombinedSus(shareSus, receiveSus):
    return (shareSus + receiveSus) / 2


def assessSusceptibilityDistribution():
    df = DatasetRepository.userEmbeddings.df
    fakeShareSusData = []
    realShareSusData = []
    fakeReceiveSusData = []
    realReceiveSusData = []
    combinedFakeSusData = []
    combinedRealSusData = []
    fakeNewsShared = []
    realNewsShared = []
    for _, row in df.iterrows():
        fakeShareSusData.append(row['fakeShareSusceptibility'])
        realShareSusData.append(row['realShareSusceptibility'])
        fakeReceiveSusData.append(row['fakeReceiveSusceptibility'])
        realReceiveSusData.append(row['realReceiveSusceptibility'])
        combinedFakeSusData.append(
            calculateCombinedSus(row['fakeShareSusceptibility'], row['fakeReceiveSusceptibility']))
        combinedRealSusData.append(
            calculateCombinedSus(row['realShareSusceptibility'], row['realReceiveSusceptibility']))
        fakeNewsShared.append(row['fakeNewsShared'])
        realNewsShared.append(row['realNewsShared'])


    # createDistribution(fakeShareSusData, 'FakeShareSus')
    # createDistribution(realShareSusData, 'RealShareSus')
    # createDistribution(realReceiveSusData, 'RealReceiveSus')
    # createDistribution(fakeReceiveSusData, 'FakeReceiveSus')
    # createDistribution(combinedFakeSusData, 'CombinedFakeSus')
    # createDistribution(combinedRealSusData, 'CombinedReceiveSus')

    return fakeShareSusData, fakeReceiveSusData, fakeNewsShared, realNewsShared

def plotDistribution(xData, yData, sizeData1, sizeData2, xLabel, yLabel):
    # Create the scatter plot
    plt.scatter(xData, yData, s=sizeData1, color='red', alpha=0.6, edgecolors="w")
    plt.scatter(xData, yData, s=sizeData2, color='blue', alpha=0.6, edgecolors="w")

    # Add labels and title
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title('Susceptibility Distribution')

    # Show the plot
    plt.show()


def assessSusceptibilityConfusionMatrix():
    dataset_repository = DatasetRepository()
    users_df = dataset_repository.userData.df
    news_user_df = dataset_repository.userNewsData.df
    user_user_df = dataset_repository.userUserData.df
    fake_news_df = dataset_repository.fakeNewsData.df
    real_news_df = dataset_repository.realNewsData.df
    user_embedding_df = dataset_repository.userEmbeddings.df

    highSusFakeCount = 0
    highSusRealCount = 0
    lowSusFakeCount = 0
    lowSusRealCount = 0
    counter = 0
    for _, row in news_user_df.iterrows():
        print(counter)
        counter += 1
        userIndex = row['userIndex']


        userEmbedding = user_embedding_df[user_embedding_df['userIndex'] == userIndex + 1]
        if len(userEmbedding) == 0:
            continue
        fakeShareSus = userEmbedding['fakeShareSusceptibility'].values[0]
        realShareSus = userEmbedding['realShareSusceptibility'].values[0]
        fakeReceiveSus = userEmbedding['fakeReceiveSusceptibility'].values[0]
        realReceiveSus = userEmbedding['realReceiveSusceptibility'].values[0]

        # if fakeShareSus == 0.0 and realShareSus == 0.0:
        #     print("bad")
        #     continue

        news_index = row['newsIndex']
        if news_index <= len(fake_news_df):
            if fakeShareSus >= 0.5:
                highSusFakeCount += 1
            else:
                if realShareSus >= 0.5:
                    lowSusFakeCount += 1
                else:
                    if fakeReceiveSus >= 0.43:
                        highSusFakeCount += 1
                    else:
                        lowSusFakeCount += 1
        else:
            if realShareSus >= 0.5:
                lowSusRealCount += 1
            else:
                if fakeReceiveSus >= 0.5:
                    highSusRealCount += 1
                else:
                    if realReceiveSus >= 0.57:
                        lowSusRealCount += 1
                    else:
                        highSusRealCount += 1



    print("No of instances where people highly susceptible to sharing fake news shared fake news: " + str(
        highSusFakeCount))
    print("No of instances where people highly susceptible to sharing fake news shared real news: " + str(
        highSusRealCount))
    print("No of instances where people highly susceptible to sharing real news shared fake news: " + str(
        lowSusFakeCount))
    print("No of instances where people highly susceptible to sharing real news shared real news: " + str(
        lowSusRealCount))


# assessSusceptibilityConfusionMatrix()
# fakeShareSusData, fakeReceiveSusData, fakeNewsShared, realNewsShared = assessSusceptibilityDistribution()
# fakeNewsFraction = [fakeNews / (fakeNews + realNews) * 100 for fakeNews, realNews in zip(fakeNewsShared, realNewsShared)]
# realNewsFraction = [realNews / (fakeNews + realNews) * 100 for fakeNews, realNews in zip(fakeNewsShared, realNewsShared)]
# plotDistribution(fakeShareSusData, fakeReceiveSusData, fakeNewsFraction, realNewsFraction,"Share Susceptibility", "Receive Susceptibility")
assessSusceptibilityConfusionMatrix()
