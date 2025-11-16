# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import re
import os
import pickle
import sys

class SimpleEmotionAnalyzer:
    def __init__(self):
        self.vectorizer = None
        self.model = None
        self.accuracy = None
        self.emotion_colors = {
            'joy': {'color': '#FFD700', 'color_name': 'golden', 'tone': 'bright'},
            'sadness': {'color': '#4682B4', 'color_name': 'blue', 'tone': 'dark'},
            'anger': {'color': '#DC143C', 'color_name': 'crimson', 'tone': 'dark'},
            'fear': {'color': '#808080', 'color_name': 'gray', 'tone': 'dark'},
            'disgust': {'color': '#9ACD32', 'color_name': 'yellow-green', 'tone': 'dark'},
            'surprise': {'color': '#FF69B4', 'color_name': 'pink', 'tone': 'bright'}
        }
        self._load_or_train_model()
    
    def clean_text(self, text):
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _load_or_train_model(self):
        csv_path = os.path.join(os.path.dirname(__file__), 'emotion_sentimen_dataset.csv')
        model_cache_path = os.path.join(os.path.dirname(__file__), 'model_cache.pkl')
        
        if os.path.exists(model_cache_path):
            try:
                with open(model_cache_path, 'rb') as f:
                    cached = pickle.load(f)
                    self.vectorizer = cached['vectorizer']
                    self.model = cached['model']
                    self.accuracy = cached['accuracy']
                print("OK: Loaded cached model!")
                return
            except Exception as e:
                print(f"WARN: Cache load failed: {e}")
        
        if os.path.exists(csv_path):
            try:
                self._train_model_from_dataset(csv_path)
                self._save_model_cache(model_cache_path)
                print("OK: ML model trained and cached!")
                return
            except Exception as e:
                print(f"WARN: Dataset training failed: {e}")
        
        self._setup_default_model()
    
    def _train_model_from_dataset(self, csv_path):
        print("Loading dataset...", file=sys.stderr)
        df = pd.read_csv(csv_path, encoding='latin1', on_bad_lines='skip')
        
        try:
            df_renamed = df.rename(columns={'Emotion': 'label', 'text': 'text'})
            df_clean = df_renamed[['text', 'label']].copy()
        except KeyError:
            raise ValueError("Dataset must have 'Emotion' and 'text' columns")
        
        print("Cleaning text...", file=sys.stderr)
        df_clean['text'] = df_clean['text'].apply(self.clean_text)
        df_clean = df_clean.dropna(subset=['text', 'label'])
        df_clean = df_clean[df_clean['text'] != ""]
        
        label_map = {
            'happiness': 'joy', 'fun': 'joy', 'enthusiasm': 'joy',
            'relief': 'joy', 'love': 'joy',
            'sadness': 'sadness', 'empty': 'sadness', 'boredom': 'sadness',
            'anger': 'anger', 'worry': 'fear', 'hate': 'disgust',
            'surprise': 'surprise'
        }
        
        df_clean['label'] = df_clean['label'].map(label_map)
        df_clean = df_clean.dropna(subset=['label'])
        
        print(f"Training with {len(df_clean)} samples", file=sys.stderr)
        
        X = df_clean['text']
        y = df_clean['label']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        X_test_tfidf = self.vectorizer.transform(X_test)
        
        self.model = LogisticRegression(
            max_iter=1000, random_state=42, class_weight='balanced'
        )
        self.model.fit(X_train_tfidf, y_train)
        
        y_pred = self.model.predict(X_test_tfidf)
        from sklearn.metrics import accuracy_score
        self.accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {self.accuracy * 100:.2f}%", file=sys.stderr)
    
    def _save_model_cache(self, cache_path):
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump({
                    'vectorizer': self.vectorizer,
                    'model': self.model,
                    'accuracy': self.accuracy
                }, f)
        except Exception as e:
            print(f"WARN: Could not cache model: {e}", file=sys.stderr)
    
    def _setup_default_model(self):
        self.model = None
        self.vectorizer = None
        print("WARN: Using keyword fallback", file=sys.stderr)
    
    def analyze_emotion(self, text):
        cleaned_text = self.clean_text(text)
        
        if self.model is not None and self.vectorizer is not None:
            try:
                text_vector = self.vectorizer.transform([cleaned_text])
                prediction = self.model.predict(text_vector)[0]
                
                emotion_map = {
                    'joy': 'Happiness',
                    'sadness': 'Sadness',
                    'anger': 'Anger',
                    'fear': 'Fear',
                    'disgust': 'Disgust',
                    'surprise': 'Surprise'
                }
                return emotion_map.get(prediction, 'Happiness')
            except Exception as e:
                return 'Happiness'
        
        return self._keyword_analysis(cleaned_text)
    
    def _keyword_analysis(self, cleaned_text):
        keywords = {
            'Happiness': ['happy', 'joy', 'glad', 'excited', 'wonderful', 'amazing', 
                         'great', 'good', 'love', 'smile', 'laugh', 'fun', 'best'],
            'Sadness': ['sad', 'cry', 'tears', 'lonely', 'depressed', 'down', 'blue',
                       'hurt', 'pain', 'sorrow', 'grief', 'miserable'],
            'Anger': ['angry', 'mad', 'furious', 'rage', 'hate', 'annoyed', 'irritated',
                     'frustrated', 'outraged'],
            'Fear': ['scared', 'afraid', 'worried', 'anxious', 'nervous', 'terrified',
                    'panic', 'fear', 'dread', 'horror'],
            'Disgust': ['disgusted', 'gross', 'sick', 'nauseated', 'revolted', 'repulsed',
                       'awful', 'terrible', 'horrible'],
            'Surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'wow',
                        'incredible', 'unexpected', 'startled']
        }
        
        words = cleaned_text.split()
        scores = {emotion: 0 for emotion in keywords.keys()}
        
        for emotion, kwords in keywords.items():
            for word in words:
                if word in kwords:
                    scores[emotion] += 1
        
        max_score = max(scores.values()) if scores else 0
        return max(scores, key=scores.get) if max_score > 0 else 'Happiness'
    
    def get_color_recommendation(self, emotion):
        emotion_lower = emotion.lower()
        if emotion == 'Happiness':
            emotion_lower = 'joy'
        
        if emotion_lower in self.emotion_colors:
            color_data = self.emotion_colors[emotion_lower]
            return {
                'emotion': emotion,
                'color_hex': color_data['color'],
                'color_name': color_data['color_name'],
                'tone': color_data['tone']
            }
        
        return {
            'emotion': 'Happiness',
            'color_hex': self.emotion_colors['joy']['color'],
            'color_name': self.emotion_colors['joy']['color_name'],
            'tone': self.emotion_colors['joy']['tone']
        }
    
    def analyze_emotion_and_color(self, diary_entry, show_visualization=False):
        emotion = self.analyze_emotion(diary_entry)
        result = self.get_color_recommendation(emotion)
        print(f"Emotion: {emotion}")
        return result

analyzer = SimpleEmotionAnalyzer()

def analyze_emotion_and_color(diary_entry, show_visualization=False):
    return analyzer.analyze_emotion_and_color(diary_entry, show_visualization)

if __name__ == "__main__":
    test_texts = [
        ("I am so happy today!", "Happiness"),
        ("I feel sad and lonely", "Sadness"),
        ("I'm so angry", "Anger"),
    ]
    
    for text, expected in test_texts:
        result = analyzer.analyze_emotion_and_color(text)
        actual = result.get('emotion')
        print(f"[{'OK' if actual == expected else 'FAIL'}] {text} -> {actual}")
