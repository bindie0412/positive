# 🎨 감정 분석 일기장 - 설정 및 실행 가이드

## 📋 목차
1. [빠른 시작](#빠른-시작)
2. [상세 설정](#상세-설정)
3. [improved_emotion_model 사용 가이드](#improved_emotion_model-사용-가이드)
4. [문제 해결](#문제-해결)

---

## 빠른 시작

### 1단계: 가상 환경 생성 및 활성화

```bash
# 가상 환경 생성
python -m venv .venv

# 가상 환경 활성화
# macOS/Linux:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate
```

### 2단계: 패키지 설치

```bash
pip install -r requirements.txt
```

### 3단계: 프로젝트 실행

```bash
python app.py
```

### 4단계: 웹 브라우저에서 접속

```
http://localhost:8080
```

---

## 상세 설정

### 프로젝트 구조

```
positive/
├── app.py                          # Flask 메인 서버
├── requirements.txt                # 패키지 의존성
├── diaries.json                    # 저장된 일기 데이터
├── our_model/
│   ├── improved_emotion_model.py   # 개선된 감정 분석 모델 ⭐
│   ├── simple_emotion_model.py     # 기본 감정 분석 모델 (폴백)
│   ├── emotion_sentimen_dataset.csv # 텍스트 감정 분석 데이터
│   ├── your_file_name.csv          # 색상 추천 데이터
│   └── model_cache.pkl             # 캐시된 모델
├── static/
│   ├── styles.css
│   ├── script.js
│   └── diary.css
└── templates/
    ├── index.html
    ├── diary.html
    └── diary_viewer.html
```

### 필수 파일 확인

프로젝트 실행 전에 다음 파일들이 존재하는지 확인하세요:

```bash
# 필수 데이터 파일
ls -la our_model/emotion_sentimen_dataset.csv
ls -la our_model/your_file_name.csv

# 필수 템플릿 파일
ls -la templates/index.html
```

---

## improved_emotion_model 사용 가이드

### ⭐ 개선된 모델의 특징

| 항목 | 설명 |
|------|------|
| **정확도** | 텍스트 감정: 97.00%, 색상: 89.86% |
| **학습 데이터** | 165,017개 텍스트 샘플 + 29,446개 색상 샘플 |
| **지원 언어** | 한국어, 영어 |
| **감정 분류** | Happiness, Sadness, Anger, Fear, Disgust, Surprise |
| **색상 추천** | 감정별 맞춤형 색상 (데이터셋 기반) |

### 🚀 첫 실행 시 주의사항

**첫 실행 시 모델 로딩에 시간이 소요됩니다:**

```
🚀 개선된 모델 로딩 시작...
📊 데이터셋 로딩 중...
📈 165017개 샘플로 모델 학습 중...
📊 텍스트 모델 정확도: 97.00%
🎨 색상 데이터셋 로딩 중...
🎯 색상 모델 정확도: 89.86%
✅ 모든 모델 로딩 완료!
```

**예상 소요 시간:**
- 첫 실행: 약 1-2분
- 이후 실행: 약 10-20초 (모델 재학습)

### 📊 모델 로딩 프로세스

```python
# app.py에서 자동으로 처리됩니다
try:
    from improved_emotion_model import analyze_emotion_and_color
    AI_MODEL_AVAILABLE = True
    print("🤖 개선된 AI 모델 로딩 성공!")
except Exception as e:
    # 폴백: simple_emotion_model 사용
    from simple_emotion_model import analyze_emotion_and_color
    print("🔄 폴백 모델 사용")
```

### ⚠️ improved_emotion_model을 사용하지 않는 경우

만약 `improved_emotion_model.py`를 사용하지 않으려면:

#### 방법 1: 파일 이름 변경
```bash
mv our_model/improved_emotion_model.py our_model/improved_emotion_model.py.bak
```

#### 방법 2: app.py 수정
```python
# app.py의 import 부분을 다음과 같이 수정:
try:
    # improved_emotion_model 사용 안 함
    # from improved_emotion_model import analyze_emotion_and_color
    # AI_MODEL_AVAILABLE = True
    
    # 직접 simple_emotion_model 사용
    from simple_emotion_model import analyze_emotion_and_color
    AI_MODEL_AVAILABLE = True
    print("🔄 기본 모델 사용")
except Exception as e:
    print(f"❌ 모델 로딩 실패: {e}")
    AI_MODEL_AVAILABLE = False
```

#### 방법 3: 환경 변수 사용 (권장)
```bash
# 실행 시 환경 변수 설정
USE_IMPROVED_MODEL=false python app.py
```

그 후 `app.py`를 다음과 같이 수정:
```python
import os

use_improved = os.getenv('USE_IMPROVED_MODEL', 'true').lower() == 'true'

if use_improved:
    try:
        from improved_emotion_model import analyze_emotion_and_color
        AI_MODEL_AVAILABLE = True
    except Exception as e:
        # 폴백...
else:
    from simple_emotion_model import analyze_emotion_and_color
    AI_MODEL_AVAILABLE = True
```

---

## API 엔드포인트

### 1. 감정 분석 및 색상 추천

```bash
POST /api/analyze
Content-Type: application/json

{
  "text": "오늘 정말 행복한 하루였어!"
}

# 응답
{
  "success": true,
  "emotion": "Happiness",
  "color_hex": "#f0e290",
  "color_name": "밝은 색",
  "tone": "밝고 파스텔 톤"
}
```

### 2. 일기 저장

```bash
POST /api/save-diary
Content-Type: application/json

{
  "date": "2025-11-16",
  "title": "오늘의 일기",
  "content": "오늘 정말 행복한 하루였어!",
  "emotion": "Happiness",
  "color_hex": "#f0e290",
  "color_name": "밝은 색",
  "tone": "밝고 파스텔 톤"
}
```

### 3. 일기 목록 조회

```bash
GET /api/diaries

# 응답
{
  "success": true,
  "diaries": [
    {
      "id": 1731779345000,
      "date": "2025-11-16",
      "title": "오늘의 일기",
      "content": "...",
      "emotion": "Happiness",
      "color_hex": "#f0e290",
      "created_at": "2025-11-16 23:42:25"
    }
  ]
}
```

### 4. 개별 일기 조회

```bash
GET /api/diary/<diary_id>
```

### 5. 일기 삭제

```bash
DELETE /api/diary/<diary_id>
```

---

## 문제 해결

### Q1: "모듈을 찾을 수 없습니다" 에러

```
ModuleNotFoundError: No module named 'pandas'
```

**해결책:**
```bash
# 패키지 재설치
pip install -r requirements.txt

# 또는 개별 설치
pip install pandas numpy scikit-learn Flask Flask-CORS
```

### Q2: 모델 로딩이 실패했습니다

```
❌ 개선된 AI 모델 로딩 실패
🔄 폴백 모델 사용
```

**확인 사항:**
1. 데이터 파일 존재 확인:
   ```bash
   ls -la our_model/*.csv
   ```

2. 파일 권한 확인:
   ```bash
   chmod 644 our_model/*.csv
   ```

3. 디스크 공간 확인:
   ```bash
   df -h
   ```

### Q3: 포트 8080이 이미 사용 중입니다

```
Address already in use
```

**해결책:**

#### 방법 1: 포트 변경
```python
# app.py의 마지막 줄 수정
app.run(host='0.0.0.0', port=8081, debug=False, use_reloader=False)
```

#### 방법 2: 기존 프로세스 종료
```bash
# macOS/Linux
lsof -i :8080
kill -9 <PID>

# Windows
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

### Q4: 서버가 느립니다

**원인:** 첫 실행 시 모델 학습으로 인한 지연

**해결책:**
- 첫 실행은 1-2분 소요 (정상)
- 이후 요청은 빠르게 처리됨
- 모델 캐시 파일 확인: `our_model/model_cache.pkl`

### Q5: 한국어가 깨져서 나옵니다

**해결책:**
```python
# app.py에서 인코딩 설정 확인
# 파일 상단에 다음 추가
# -*- coding: utf-8 -*-
```

### Q6: CORS 에러가 발생합니다

```
Access to XMLHttpRequest blocked by CORS policy
```

**해결책:** 이미 `app.py`에 CORS 설정이 되어있습니다
```python
from flask_cors import CORS
CORS(app)  # 모든 도메인 허용
```

---

## 성능 최적화 팁

### 1. 모델 캐싱
```python
# 모델은 서버 시작 시 한 번만 로드됩니다
# 이후 모든 요청은 캐시된 모델을 사용합니다
```

### 2. 배치 처리
```bash
# 여러 일기를 한 번에 분석하려면
# API를 여러 번 호출하는 것보다
# 백엔드에서 배치 처리 구현 권장
```

### 3. 데이터베이스 사용
```python
# 현재: JSON 파일 사용 (개발용)
# 프로덕션: SQLite, PostgreSQL 등 사용 권장
```

---

## 추가 정보

### 감정 분류 기준

| 감정 | 키워드 예시 | 색상 |
|------|-----------|------|
| **Happiness** | 행복, 기쁨, 사랑, 최고 | 황금색/노란색 |
| **Sadness** | 슬픔, 외로움, 우울 | 파란색 |
| **Anger** | 화, 짜증, 분노 | 빨간색 |
| **Fear** | 무서움, 두려움, 불안 | 회색 |
| **Disgust** | 역겨움, 혐오 | 초록색 |
| **Surprise** | 놀람, 충격, 깜짝 | 핑크색 |

### 지원 언어

- ✅ 한국어
- ✅ 영어
- ⚠️ 기타 언어 (제한적 지원)

---

## 라이선스 및 기여

이 프로젝트는 개인 학습 목적으로 만들어졌습니다.

---

**마지막 업데이트:** 2025-11-16
