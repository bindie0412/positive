# -*- coding: utf-8 -*-
"""
간단한 감정 분석 및 색상 추천 모델
Python 3.13 호환 버전
"""

import re
import colorsys
import os

class SimpleEmotionAnalyzer:
    def __init__(self):
        # 감정 키워드 사전
        self.emotion_keywords = {
            'Happiness': {
                'keywords': ['happy', 'joy', 'glad', 'excited', 'wonderful', 'amazing', 'great', 'good', 'love', 'smile', 'laugh', 'fun', 'best', 'perfect', 'awesome', 'fantastic', 'excellent', 'brilliant', 'superb', 'magnificent'],
                'color': '#FFD700',  # 금색
                'color_name': '황금색',
                'tone': '밝고 파스텔 톤'
            },
            'Sadness': {
                'keywords': ['sad', 'cry', 'tears', 'lonely', 'depressed', 'down', 'blue', 'hurt', 'pain', 'sorrow', 'grief', 'miserable', 'unhappy', 'disappointed', 'heartbroken', 'devastated', 'tragic', 'melancholy'],
                'color': '#4682B4',  # 스틸 블루
                'color_name': '파란색',
                'tone': '차분하고 어두운 톤'
            },
            'Anger': {
                'keywords': ['angry', 'mad', 'furious', 'rage', 'hate', 'annoyed', 'irritated', 'frustrated', 'pissed', 'outraged', 'livid', 'seething', 'wrathful', 'hostile', 'aggressive', 'violent'],
                'color': '#DC143C',  # 크림슨
                'color_name': '진한 빨강',
                'tone': '차분하고 어두운 톤'
            },
            'Fear': {
                'keywords': ['scared', 'afraid', 'worried', 'anxious', 'nervous', 'terrified', 'panic', 'fear', 'dread', 'horror', 'frightened', 'alarmed', 'uneasy', 'tense', 'stressed'],
                'color': '#808080',  # 그레이
                'color_name': '밤색',
                'tone': '차분하고 어두운 톤'
            },
            'Disgust': {
                'keywords': ['disgusted', 'gross', 'sick', 'nauseated', 'revolted', 'repulsed', 'awful', 'terrible', 'horrible', 'nasty', 'dirty', 'filthy', 'contaminated', 'corrupt'],
                'color': '#9ACD32',  # 옐로우 그린
                'color_name': '황록색',
                'tone': '차분하고 어두운 톤'
            },
            'Surprise': {
                'keywords': ['surprised', 'shocked', 'amazed', 'astonished', 'wow', 'incredible', 'unbelievable', 'unexpected', 'sudden', 'startled', 'bewildered', 'stunned', 'dumbfounded'],
                'color': '#FF69B4',  # 핫 핑크
                'color_name': '보라색',
                'tone': '밝고 파스텔 톤'
            }
        }
        
        print("간단한 감정 분석 모델 초기화 완료!")

    def clean_text(self, text):
        """텍스트 전처리"""
        if not isinstance(text, str):
            return ""
        text = text.lower()
        # 특수문자 제거 (한국어와 영어만 남김)
        text = re.sub(r'[^가-힣a-zA-Z\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def analyze_emotion(self, text):
        """감정 분석"""
        cleaned_text = self.clean_text(text)
        words = cleaned_text.split()
        
        emotion_scores = {}
        
        # 각 감정별 키워드 매칭 점수 계산
        for emotion, data in self.emotion_keywords.items():
            score = 0
            for word in words:
                if word in data['keywords']:
                    score += 1
            emotion_scores[emotion] = score
        
        # 가장 높은 점수를 가진 감정 선택
        if emotion_scores:
            max_emotion = max(emotion_scores, key=emotion_scores.get)
            if emotion_scores[max_emotion] > 0:
                return max_emotion
        
        # 키워드가 없으면 기본값
        return 'Neutral'

    def get_color_recommendation(self, emotion):
        """감정에 따른 색상 추천"""
        if emotion in self.emotion_keywords:
            data = self.emotion_keywords[emotion]
            return {
                'emotion': emotion,
                'color_hex': data['color'],
                'color_name': data['color_name'],
                'tone': data['tone']
            }
        else:
            # 기본값
            return {
                'emotion': 'Neutral',
                'color_hex': '#667eea',
                'color_name': '파란색',
                'tone': '기본 톤'
            }

    def analyze_emotion_and_color(self, diary_entry, show_visualization=False):
        """감정 분석 및 색상 추천 (기존 API와 호환)"""
        emotion = self.analyze_emotion(diary_entry)
        result = self.get_color_recommendation(emotion)
        
        print(f"감정 분석 결과: {emotion}")
        
        return result

# 전역 인스턴스 생성
analyzer = SimpleEmotionAnalyzer()

# 기존 API와 호환되는 함수
def analyze_emotion_and_color(diary_entry, show_visualization=False):
    """기존 combined_text_emotion_color_model.py와 호환되는 함수"""
    return analyzer.analyze_emotion_and_color(diary_entry, show_visualization)

if __name__ == "__main__":
    # 테스트
    test_texts = [
        "I am so happy today! This is wonderful!",
        "I feel sad and lonely",
        "I'm angry about this situation",
        "I'm worried about tomorrow",
        "This is disgusting and awful"
    ]
    
    for text in test_texts:
        result = analyze_emotion_and_color(text)
        print(f"텍스트: {text}")
        print(f"결과: {result}")
        print("-" * 50)