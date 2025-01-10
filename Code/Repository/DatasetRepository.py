import os
import pandas as pd
from pathlib import Path

from Code.Repository.Repository import Repository


file_path = os.path.join(Path(__file__).parent.parent.parent.resolve(), 'Dataset', 'BuzzFeedNews.csv')
if not os.path.isfile(file_path):
    print(file_path)
    raise FileNotFoundError(f"The file {file_path} does not exist.")

class DatasetRepository:
    newsData = Repository(file_path, pd.read_csv(file_path))
    userData = Repository(os.path.join(Path(__file__).parent.parent.parent.resolve(), 'Dataset', 'BuzzFeedUser.csv'), pd.read_csv(os.path.join(Path(__file__).parent.parent.parent.resolve(), 'Dataset', 'BuzzFeedUser.csv')))
    realNewsData = Repository(os.path.join(Path(__file__).parent.parent.parent.resolve(), 'Dataset', 'BuzzFeed_real_news_content.csv'), pd.read_csv(os.path.join(Path(__file__).parent.parent.parent.resolve(), 'Dataset', 'BuzzFeed_real_news_content.csv')))
    fakeNewsData = Repository(os.path.join(Path(__file__).parent.parent.parent.resolve(), 'Dataset', 'BuzzFeed_fake_news_content.csv'), pd.read_csv(os.path.join(Path(__file__).parent.parent.parent.resolve(), 'Dataset', 'BuzzFeed_fake_news_content.csv')))
    userUserData = Repository(os.path.join(Path(__file__).parent.parent.parent.resolve(), 'Dataset', 'BuzzFeedUserUser.csv'), pd.read_csv(os.path.join(Path(__file__).parent.parent.parent.resolve(), 'Dataset', 'BuzzFeedUserUser.csv')))
    userNewsData = Repository(os.path.join(Path(__file__).parent.parent.parent.resolve(), 'Dataset', 'BuzzFeedNewsUser.csv'), pd.read_csv(os.path.join(Path(__file__).parent.parent.parent.resolve(), 'Dataset', 'BuzzFeedNewsUser.csv')))
    userEmbeddings = Repository(os.path.join(Path(__file__).parent.parent.parent.resolve(), 'Dataset', 'UserEmbeddings.csv'), pd.read_csv(os.path.join(Path(__file__).parent.parent.parent.resolve(), 'Dataset', 'UserEmbeddings.csv')))