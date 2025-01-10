from select import select

from transformers import pipeline
import pandas as pd

emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base",
                                       return_all_scores=True, device="cpu")
class EmotionExtractor:
    def __init__(self):
        # Load the emotion classification pipeline
        self.emotion_intensity = {'anger': 0, 'disgust': 0, 'fear': 0, 'joy': 0, 'neutral': 0, 'sadness': 0, 'surprise': 0}
        self.token_limit = 512

    def initialize_emotions(self):
        emotion_intensities = {}
        for emotion in self.emotion_intensity.keys():
            emotion_intensities[emotion] = 0
        return emotion_intensities

    def extract(self, texts, emotion_intensities):
        total_tokens = len(texts)
        remaining_tokens = total_tokens

        # Since 512 tokens can be analysed at a time, this
        # loop extracts emotions from the tokens batched by 512
        # and adds the normalized intensities from each batch to
        # get the final intensity
        while remaining_tokens > 0:
            tokens_analysed = min(self.token_limit, remaining_tokens)
            texts = [text[:tokens_analysed] for text in texts]
            remaining_tokens = remaining_tokens - tokens_analysed
            # Extract emotions from the text
            results = emotion_classifier(texts)

            for text, result in zip(texts, results):
                for emotion in result:
                    emotion_intensities[emotion['label']] += emotion['score'] / tokens_analysed

        return emotion_intensities

    def extract_emotion(self, csv_file=None, columns=None, text=None):
        emotion_intensities = self.initialize_emotions()
        if csv_file is not None:
            df = pd.read_csv(csv_file)
            for column in columns:
                texts = df[column].tolist()
                emotion_intensities = self.extract(texts=texts, emotion_intensities=emotion_intensities)
        elif text is not None:
            emotion_intensities = self.extract(texts=text, emotion_intensities=emotion_intensities)

        return emotion_intensities




