# -*- coding: utf-8 -*-
"""
개선된 감정 분석 및 색상 추천 모델
서버 시작 시 로드되어 빠른 응답 제공
"""

import pandas as pd
import numpy as np
import pickle
import os
import sys
import re
import colorsys
import random
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

class ImprovedEmotionAnalyzer:
    def __init__(self):
        self.text_model = None
        self.text_vectorizer = None
        self.color_model = None
        self.color_encoder = None
        self.emotion_colors = {
            'Happiness': {'color': '#FFD700', 'color_name': '황금색', 'tone': '밝고 파스텔 톤'},
            'Sadness': {'color': '#4682B4', 'color_name': '파란색', 'tone': '차분하고 어두운 톤'},
            'Anger': {'color': '#DC143C', 'color_name': '진한 빨간색', 'tone': '강렬하고 어두운 톤'},
            'Fear': {'color': '#808080', 'color_name': '회색', 'tone': '어둡고 차분한 톤'},
            'Disgust': {'color': '#9ACD32', 'color_name': '연한 초록색', 'tone': '차분하고 어두운 톤'},
            'Surprise': {'color': '#FF69B4', 'color_name': '핑크색', 'tone': '밝고 파스텔 톤'}
        }
        # 색상 데이터셋 저장
        self.color_dataset = None
        self.emotion_colors_data = {}
        self._load_models()
    
    def _load_models(self):
        """서버 시작 시 모델들을 로드"""
        print("🚀 개선된 모델 로딩 시작...")
        
        # 1. 텍스트 감정 분석 모델 로드
        self._load_text_model()
        
        # 2. 색상 기반 감정 예측 모델 로드
        self._load_color_model()
        
        # 3. 색상 데이터셋 로드 (랜덤 색상 추출용)
        self._load_color_dataset()
        
        print("✅ 모든 모델 로딩 완료!")
    
    def _load_color_dataset(self):
        """색상 데이터셋 로드 (랜덤 색상 추출용)"""
        try:
            csv_path = os.path.join(os.path.dirname(__file__), 'your_file_name.csv')
            
            if not os.path.exists(csv_path):
                print(f"⚠️ 색상 데이터셋 파일을 찾을 수 없습니다: {csv_path}")
                return
            
            print("🎨 색상 데이터셋 로딩 중...")
            self.color_dataset = pd.read_csv(csv_path)
            
            # 에러 데이터 제외
            self.color_dataset = self.color_dataset[self.color_dataset['is_error'] == False]
            
            # 감정별로 색상 데이터 그룹화
            for emotion in self.color_dataset['emotion'].unique():
                emotion_data = self.color_dataset[self.color_dataset['emotion'] == emotion]
                self.emotion_colors_data[emotion] = emotion_data[['h', 's', 'v']].values
            
            print(f"📊 색상 데이터셋 로드 완료: {len(self.color_dataset)}개 샘플")
            for emotion, data in self.emotion_colors_data.items():
                print(f"   {emotion}: {len(data)}개 색상")
                
        except Exception as e:
            print(f"❌ 색상 데이터셋 로딩 실패: {e}")
            self.color_dataset = None
            self.emotion_colors_data = {}
    
    def _load_text_model(self):
        """텍스트 감정 분석 모델 로드"""
        try:
            # 캐시 파일 경로
            cache_dir = os.path.dirname(__file__)
            cache_file = os.path.join(cache_dir, 'model_cache.pkl')
            
            # 캐시된 모델이 있으면 로드
            if os.path.exists(cache_file):
                try:
                    with open(cache_file, 'rb') as f:
                        cached_data = pickle.load(f)
                        self.text_model = cached_data.get('text_model')
                        self.text_vectorizer = cached_data.get('text_vectorizer')
                        if self.text_model and self.text_vectorizer:
                            print("✅ 캐시된 텍스트 모델 로드 완료!")
                            return
                except Exception as e:
                    print(f"⚠️ 캐시 로드 실패: {e}, 새로 학습합니다...")
            
            # 데이터셋 로드
            csv_path = os.path.join(os.path.dirname(__file__), 'emotion_sentimen_dataset.csv')
            
            if not os.path.exists(csv_path):
                print(f"⚠️ 데이터셋 파일을 찾을 수 없습니다: {csv_path}")
                return
            
            print("📊 데이터셋 로딩 중...")
            df = pd.read_csv(csv_path, encoding='latin1')
            
            # 데이터 정제
            df_renamed = df.rename(columns={'Emotion': 'label', 'text': 'text'})
            df_clean = df_renamed[['text', 'label']].copy()
            
            # 텍스트 정제 (영어 전용)
            def clean_text(text):
                if not isinstance(text, str):
                    return ""
                text = text.lower()
                text = re.sub(r'[^a-zA-Z\s]', '', text)
                text = re.sub(r'\s+', ' ', text).strip()
                return text
            
            df_clean['text'] = df_clean['text'].apply(clean_text)
            df_clean.dropna(subset=['text', 'label'], inplace=True)
            df_final = df_clean[df_clean['text'] != ""]
            
            # 라벨 매핑 (neutral 제외)
            label_map = {
                'happiness': 'joy', 'fun': 'joy', 'enthusiasm': 'joy', 'relief': 'joy', 'love': 'joy',
                'sadness': 'sadness', 'empty': 'sadness', 'boredom': 'sadness',
                'anger': 'anger',
                'worry': 'fear',
                'hate': 'disgust',
                'surprise': 'surprise'
            }
            
            df_final['label'] = df_final['label'].map(label_map)
            df_final = df_final.dropna(subset=['label'])
            
            print(f"📈 {len(df_final)}개 샘플로 모델 학습 중...")
            
            # 훈련/테스트 분리
            X = df_final['text']
            y = df_final['label']
            
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # TF-IDF 벡터화
            self.text_vectorizer = TfidfVectorizer(
                max_features=5000,
                stop_words='english'
            )
            X_train_tfidf = self.text_vectorizer.fit_transform(X_train)
            X_test_tfidf = self.text_vectorizer.transform(X_test)
            
            # 모델 학습
            self.text_model = LogisticRegression(
                max_iter=1000,
                random_state=42,
                class_weight='balanced'
            )
            self.text_model.fit(X_train_tfidf, y_train)
            
            # 성능 평가
            y_pred = self.text_model.predict(X_test_tfidf)
            accuracy = accuracy_score(y_test, y_pred)
            print(f"📊 텍스트 모델 정확도: {accuracy * 100:.2f}%")
            
            # 모델 학습 후 캐시 저장
            try:
                cache_data = {
                    'text_model': self.text_model,
                    'text_vectorizer': self.text_vectorizer
                }
                with open(cache_file, 'wb') as f:
                    pickle.dump(cache_data, f)
                print("💾 모델을 캐시에 저장했습니다.")
            except Exception as e:
                print(f"⚠️ 캐시 저장 실패: {e}")
            
        except Exception as e:
            print(f"❌ 텍스트 모델 로딩 실패: {e}")
            self.text_model = None
            self.text_vectorizer = None
    
    def _load_color_model(self):
        """색상 기반 감정 예측 모델 로드 (colorchoosing.py 기반)"""
        try:
            # 캐시 파일 경로
            cache_dir = os.path.dirname(__file__)
            cache_file = os.path.join(cache_dir, 'model_cache.pkl')
            
            # 캐시된 모델이 있으면 로드
            if os.path.exists(cache_file):
                try:
                    with open(cache_file, 'rb') as f:
                        cached_data = pickle.load(f)
                        self.color_model = cached_data.get('color_model')
                        self.color_encoder = cached_data.get('color_encoder')
                        if self.color_model and self.color_encoder:
                            print("✅ 캐시된 색상 모델 로드 완료!")
                            return
                except Exception as e:
                    print(f"⚠️ 색상 모델 캐시 로드 실패: {e}")
            
            # HSV 색상 데이터셋 로드 (your_file_name.csv)
            csv_path = os.path.join(os.path.dirname(__file__), 'your_file_name.csv')
            
            if not os.path.exists(csv_path):
                print(f"⚠️ 색상 데이터셋 파일을 찾을 수 없습니다: {csv_path}")
                # 기본 색상 매핑만 사용
                return
            
            print("🎨 색상 데이터셋 로딩 중...")
            data = pd.read_csv(csv_path)
            
            # 특징과 라벨 분리
            X = data[['h', 's', 'v']]
            y = data['emotion']
            
            # 라벨 인코딩
            self.color_encoder = LabelEncoder()
            y_encoded = self.color_encoder.fit_transform(y)
            
            # 훈련/테스트 분리
            X_train, X_test, y_train, y_test = train_test_split(
                X, y_encoded, test_size=0.2, random_state=42
            )
            
            # 모델 학습
            self.color_model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.color_model.fit(X_train, y_train)
            
            # 성능 평가
            y_pred = self.color_model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            print(f"🎯 색상 모델 정확도: {accuracy * 100:.2f}%")
            
            # 모델 학습 후 캐시 저장
            try:
                with open(cache_file, 'rb') as f:
                    cache_data = pickle.load(f)
            except:
                cache_data = {}
            
            cache_data['color_model'] = self.color_model
            cache_data['color_encoder'] = self.color_encoder
            
            try:
                with open(cache_file, 'wb') as f:
                    pickle.dump(cache_data, f)
                print("💾 색상 모델을 캐시에 저장했습니다.")
            except Exception as e:
                print(f"⚠️ 색상 모델 캐시 저장 실패: {e}")
            
        except Exception as e:
            print(f"❌ 색상 모델 로딩 실패: {e}")
            self.color_model = None
            self.color_encoder = None
    
    def analyze_emotion(self, text):
        """메인 감정 분석 함수"""
        if not isinstance(text, str) or not text.strip():
            return 'Happiness'
        
        # 1. 한국어 키워드 우선 분석
        korean_result = self._analyze_korean_emotion(text)
        if korean_result:
            return korean_result
        
        # 2. 영어 키워드 분석
        english_result = self._analyze_english_emotion(text)
        if english_result:
            return english_result
        
        # 3. ML 모델 사용 (영어 텍스트만)
        ml_result = self._analyze_with_ml(text)
        if ml_result:
            return ml_result
        
        # 4. 기본값
        return 'Happiness'
    
    def _analyze_korean_emotion(self, text):
        """한국어 텍스트 감정 분석"""
        text_lower = text.lower()
        
        korean_emotions = {
            'Fear': [
                '무서워', '무섭다', '무서운', '두려워', '두려운', '겁', '겁나', '겁나는',
                '恐慌', '소름', '소름끼치다', '무서움', '무서웠다', '무서웠다',
                '무서워서', '무서워서', '무서워서', '무서워서', '무서워서'
            ],
            'Happiness': [
                '행복', '행복해', '행복한', '좋아', '좋다', '좋은', '기쁘다', '기쁜',
                '웃다', '웃음', '즐겁다', '즐거운', '사랑', '사랑해', '완벽', '최고',
                '행복했다', '행복했다', '행복했다', '행복했다', '행복했다'
            ],
            'Sadness': [
                '슬프다', '슬픈', '울다', '울음', '외롭다', '외로운', '우울', '상처',
                '아프다', '아픈', '눈물', '슬픔', '울었다', '울었다', '울었다'
            ],
            'Anger': [
                '화', '화나', '화나다', '짜증', '짜증나', '짜증나다', '화', '성나',
                '미치다', '미운', '화났다', '화났다', '화났다'
            ],
            'Disgust': [
                '역겹다', '역겹다', '구역', '구역하다', '역겹다', '구역'
            ],
            'Surprise': [
                '놀라다', '놀라운', '충격', '깜짝', '우와', '대박', '놀랐다', '놀랐다'
            ]
        }
        
        # 키워드 매칭
        for emotion, keywords in korean_emotions.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return emotion
        
        return None
    
    def _analyze_english_emotion(self, text):
        """영어 텍스트 감정 분석"""
        text_lower = text.lower()
        
        english_emotions = {
            'Fear': [
                'scared', 'afraid', 'worried', 'anxious', 'nervous', 'terrified',
                'panic', 'fear', 'dread', 'horror', 'scary', 'frightened', 'frightening',
                'strange', 'noise', 'pounding', 'cant sleep', 'cant sleep', 'sleep',
                'shivering', 'trembling', 'uneasy', 'uncomfortable', 'threat'
            ],
            'Happiness': [
                'happy', 'joy', 'glad', 'excited', 'wonderful', 'amazing', 
                'great', 'good', 'love', 'smile', 'laugh', 'fun', 'best', 'perfect',
                'sun', 'shining', 'aced', 'test', 'favorite', 'song', 'wonderful day'
            ],
            'Sadness': [
                'sad', 'cry', 'tears', 'lonely', 'depressed', 'down', 'blue',
                'hurt', 'pain', 'sorrow', 'grief', 'miserable', 'lonely'
            ],
            'Anger': [
                'angry', 'mad', 'furious', 'rage', 'hate', 'annoyed', 'irritated',
                'frustrated', 'outraged', 'pissed', 'livid'
            ],
            'Disgust': [
                'disgusted', 'gross', 'sick', 'nauseated', 'revolted', 'repulsed',
                'awful', 'terrible', 'horrible', 'disgusting'
            ],
            'Surprise': [
                'surprised', 'shocked', 'amazed', 'astonished', 'wow',
                'incredible', 'unexpected', 'startled', 'suddenly'
            ]
        }
        
        # 키워드 매칭 점수 계산
        emotion_scores = {}
        for emotion, keywords in english_emotions.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
                words = text_lower.split()
                for word in words:
                    if keyword in word or word in keyword:
                        score += 0.5
            emotion_scores[emotion] = score
        
        if emotion_scores and max(emotion_scores.values()) > 0:
            return max(emotion_scores, key=emotion_scores.get)
        
        return None
    
    def _analyze_with_ml(self, text):
        """ML 모델을 사용한 감정 분석"""
        if self.text_model is not None and self.text_vectorizer is not None:
            try:
                # 영어 텍스트만 ML 모델에 사용
                english_text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
                if english_text.strip() and len(english_text.split()) >= 3:
                    text_vector = self.text_vectorizer.transform([english_text])
                    prediction = self.text_model.predict(text_vector)[0]
                    
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
                print(f"ML 모델 분석 실패: {e}", file=sys.stderr)
        
        return None
    
    def hsv_to_hex(self, h, s, v):
        """HSV를 HEX 색상으로 변환"""
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
    
    def get_color_from_dataset(self, emotion):
        """데이터셋에서 해당 감정의 색상을 랜덤으로 추출"""
        if self.emotion_colors_data and emotion in self.emotion_colors_data:
            # 해당 감정의 색상 중에서 랜덤으로 하나 선택
            color_data = self.emotion_colors_data[emotion]
            if len(color_data) > 0:
                selected_hsv = random.choice(color_data)
                h, s, v = selected_hsv
                
                # 감정 톤에 따른 색상 보정
                corrected_hsv = self._adjust_color_tone(h, s, v, emotion)
                
                # HEX 색상으로 변환
                hex_color = self.hsv_to_hex(*corrected_hsv)
                
                return {
                    'hsv': corrected_hsv,
                    'hex': hex_color,
                    'from_dataset': True
                }
        
        # 데이터셋에 없으면 기본 색상 사용
        if emotion in self.emotion_colors:
            default_color = self.emotion_colors[emotion]['color']
            return {
                'hsv': None,
                'hex': default_color,
                'from_dataset': False
            }
        
        # 최종 폴백
        return {
            'hsv': None,
            'hex': '#FFD700',
            'from_dataset': False
        }
    
    def _adjust_color_tone(self, h, s, v, emotion):
        """감정에 따른 색상 톤 보정"""
        # 부정적인 감정과 긍정적인 감정 정의
        negative_emotions = ['Anger', 'Disgust', 'Fear', 'Sadness']
        positive_emotions = ['Happiness', 'Surprise']
        
        if emotion in negative_emotions:
            # 어둡고 차분한 톤으로 보정
            adjusted_s = max(0.2, min(0.7, s * 0.7))
            adjusted_v = max(0.2, min(0.6, v * 0.6))
        elif emotion in positive_emotions:
            # 밝고 파스텔 톤으로 보정
            adjusted_s = max(0.1, min(0.4, s * 0.5))
            adjusted_v = max(0.8, min(1.0, v * 0.2 + 0.8))
        else:
            # 기본 보정
            adjusted_s = max(0.1, min(0.8, s))
            adjusted_v = max(0.3, min(1.0, v))
        
        return (h, adjusted_s, adjusted_v)
    
    def get_color_name_from_hsv(self, h, s, v):
        """HSV 값에서 색상 이름 추출 (간단한 버전)"""
        # HSV를 RGB로 변환
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        
        # RGB 값을 기반으로 색상 이름 결정
        if r > 0.8 and g > 0.8 and b < 0.3:
            return "노란색"
        elif r > 0.7 and g < 0.3 and b < 0.3:
            return "빨간색"
        elif r < 0.3 and g > 0.7 and b < 0.3:
            return "초록색"
        elif r < 0.3 and g < 0.3 and b > 0.7:
            return "파란색"
        elif r > 0.7 and g < 0.5 and b > 0.7:
            return "핑크색"
        elif r < 0.3 and g < 0.3 and b < 0.3:
            return "회색"
        elif r > 0.5 and g > 0.5 and b > 0.5:
            return "밝은 색"
        else:
            return "중간 톤"
    
    def analyze_emotion_and_color(self, diary_entry, show_visualization=False):
        """메인 분석 함수"""
        emotion = self.analyze_emotion(diary_entry)
        result = self.get_color_recommendation(emotion)
        print(f"🤖 AI 분석: {emotion}")
        return result
    
    def get_color_recommendation(self, emotion):
        """감정에 따른 색상 추천 (데이터셋 기반 랜덤 추출)"""
        # 데이터셋에서 해당 감정의 색상 랜덤 추출
        color_info = self.get_color_from_dataset(emotion)
        
        if color_info['from_dataset'] and color_info['hsv']:
            # 데이터셋에서 추출한 색상 사용
            h, s, v = color_info['hsv']
            color_name = self.get_color_name_from_hsv(h, s, v)
            
            # 감정 톤 결정
            negative_emotions = ['Anger', 'Disgust', 'Fear', 'Sadness']
            if emotion in negative_emotions:
                tone = "차분하고 어두운 톤"
            else:
                tone = "밝고 파스텔 톤"
            
            return {
                'emotion': emotion,
                'color_hex': color_info['hex'],
                'color_name': color_name,
                'tone': tone,
                'source': 'dataset'
            }
        else:
            # 기본 색상 사용 (폴백)
            if emotion in self.emotion_colors:
                color_data = self.emotion_colors[emotion]
                return {
                    'emotion': emotion,
                    'color_hex': color_data['color'],
                    'color_name': color_data['color_name'],
                    'tone': color_data['tone'],
                    'source': 'default'
                }
            
            # 최종 폴백
            return {
                'emotion': 'Happiness',
                'color_hex': self.emotion_colors['Happiness']['color'],
                'color_name': self.emotion_colors['Happiness']['color_name'],
                'tone': self.emotion_colors['Happiness']['tone'],
                'source': 'fallback'
            }
        

# 전역 인스턴스
improved_analyzer = ImprovedEmotionAnalyzer()

def analyze_emotion_and_color(diary_entry, show_visualization=False):
    """외부에서 호출할 함수"""
    return improved_analyzer.analyze_emotion_and_color(diary_entry, show_visualization)

if __name__ == "__main__":
    # 테스트
    test_cases = [
        "I heard a strange noise outside my window late tonight. My heart is pounding and I cant sleep.",
        "I watched very scary movie. and I was so scared...",
        "The sun is shining, I aced the test, and my favorite song just came on. What a perfect day.",
        "무서운 영화 봤어",
        "너무 행복해"
    ]
    
    print("🧪 개선된 모델 테스트:")
    for text in test_cases:
        result = analyze_emotion_and_color(text)
        print(f"텍스트: {text[:50]}...")
        print(f"결과: {result}")
        print()