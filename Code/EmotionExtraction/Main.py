from Code.EmotionExtraction.EmotionExtractor import EmotionExtractor

extractor = EmotionExtractor()
intensities = extractor.extract_emotion(df='/Users/zaimazarnaz/PycharmProjects/FakeNewsNetwork/Dataset/BuzzFeed_fake_news_content.csv', columns=['tile', 'text'])
print(intensities)