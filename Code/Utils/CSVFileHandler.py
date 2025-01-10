import csv
import os
import pandas as pd


from Code.Repository.DatasetRepository import DatasetRepository


class CSVFileHandler:
    @staticmethod
    def createFile(fileName, directory, columns):
        filePath = os.path.join(directory, fileName + '.csv')

        # Create the CSV file with the header
        with open(filePath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(columns)  # Write the header

        print(f"CSV file created at: {filePath}")
        pass

    @staticmethod
    def addRow(row, filePath=None, df=None):
        if df is None and filePath is not None:
            df = pd.read_csv(filePath)
        df.loc[len(df)] = row
        # df._append(row, ignore_index=True)
        df.to_csv(filePath, index=False)

    @staticmethod
    def updateData(filePath, column, row, newData):
        df = pd.read_csv(filePath)
        df.loc[row, column] = newData
        df.to_csv(filePath, index=False)

    @staticmethod
    def deleteFile(filePath):
        # Delete the CSV file
        if os.path.exists(filePath):
            os.remove(filePath)
            print(f"{filePath} has been deleted.")
        else:
            print(f"{filePath} does not exist.")

# CSVFileHandler.createFile('UserEmbeddings', '/Users/zaimazarnaz/PycharmProjects/FakeNewsNetwork/Dataset',
#                           ['userIndex', 'fakeShareSusceptibility', 'realShareSusceptibility', 'fakeReceiveSusceptibility', 'realReceiveSusceptibility',
#                            'fakeNewsShared', 'realNewsShared', 'totalNewsShared',
#                            'followerCount', 'followingCount',
#                            'meanAnger', 'meanDisgust', 'meanSadness', 'meanFear', 'meanJoy', 'meanNeutral', 'meanSurprise',
#                            'maxSpreadDist', 'influence', 'exposure',
#                            'avNeighbourRealShareSusceptibility', 'avNeighbourFakeShareSusceptibility'])
# CSVFileHandler.deleteFile('/Users/zaimazarnaz/PycharmProjects/FakeNewsNetwork/Dataset/UserEmbeddings.csv')
# CSVFileHandler.addRow({"userIndex":14}, DatasetRepository.userEmbeddings.path)
# row = DatasetRepository.userEmbeddings.df.index[DatasetRepository.userEmbeddings.df['userIndex'] == 12]
# print(DatasetRepository.userEmbeddings.df)
# CSVFileHandler.updateData(DatasetRepository.userEmbeddings.path, 'fakeShareSusceptibility', row,123)

# CSVFileHandler.addRow({"userIndex":2,"fakeShareSusceptibility":0.54}, DatasetRepository.userEmbeddings.path)
# CSVFileHandler.addRow({"userIndex":10013}, '/Users/zaimazarnaz/PycharmProjects/FakeNewsNetwork/Dataset/UserEmbeddings.csv.csv')
# df = pd.read_csv('/Users/zaimazarnaz/PycharmProjects/FakeNewsNetwork/Dataset/BuzzFeedUser.csv')
# userEmbedding = pd.read_csv('/Users/zaimazarnaz/PycharmProjects/FakeNewsNetwork/Dataset/UserEmbeddings.csv.csv')
# for index in range(1, 1000):
#     CSVFileHandler.addRow({"userIndex":index}, df=userEmbedding, filePath='/Users/zaimazarnaz/PycharmProjects/FakeNewsNetwork/Dataset/UserEmbeddings.csv.csv')
#     print(f"{index} has been added.")

# CSVFileHandler.addRow({"userIndex":3}, df=userEmbedding, filePath='/Users/zaimazarnaz/PycharmProjects/FakeNewsNetwork/Dataset/UserEmbeddings.csv.csv')
