# 🎨 감정 분석 일기장 (Emotion Analysis Diary)

AI 기반 감정 분석 및 색상 추천 시스템을 갖춘 웹 일기장 애플리케이션입니다.

## 📋 프로젝트 개요

이 프로젝트는 사용자가 작성한 일기의 감정을 AI가 자동으로 분석하고, 감정에 맞는 색상을 추천해주는 웹 애플리케이션입니다.

### ✨ 주요 기능

- **감정 분석**: 텍스트 기반 감정 인식 (한국어, 영어 지원)
  - 행복 (Happiness)
  - 슬픔 (Sadness)
  - 분노 (Anger)
  - 두려움 (Fear)
  - 혐오 (Disgust)
  - 놀람 (Surprise)

- **색상 추천**: 감정에 맞는 색상 자동 추천
- **일기 저장**: JSON 기반 일기 데이터 저장
- **일기 조회**: 저장된 일기 목록 및 상세 조회
- **일기 삭제**: 불필요한 일기 삭제

### 🤖 AI 모델 성능

- **텍스트 감정 분석 모델**: 97.00% 정확도
- **색상 기반 감정 예측 모델**: 89.86% 정확도
- **학습 데이터**: 165,017개 샘플

## 🛠️ 기술 스택

- **Backend**: Flask 3.1.2
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Processing**: Pandas 2.3.3, NumPy 2.3.4
- **Machine Learning**: Scikit-learn 1.7.2
- **Visualization**: Matplotlib 3.10.7, Seaborn 0.13.2
- **CORS**: Flask-CORS 6.0.1

## 📦 설치 및 실행 방법

### 1. 저장소 클론

```bash
git clone https://github.com/bindie0412/positive.git
cd positive
```

### 2. Python 가상 환경 생성 (권장)

```bash
python -m venv .venv
```

### 3. 가상 환경 활성화

**macOS/Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

### 4. 패키지 설치

```bash
pip install -r requirements.txt
```

### 5. 프로젝트 실행

#### ⭐ 개선된 모델 사용 (기본값, 권장)

```bash
python app.py
```

**특징:**
- 텍스트 감정 분석: 97% 정확도
- 색상 모델: 89.86% 정확도
- 첫 실행 시 모델 학습: 약 1-2분 소요
- 이후 실행: 약 10-20초 소요

#### 📌 기본 모델 사용 (빠른 실행)

```bash
USE_IMPROVED_MODEL=false python app.py
```

**특징:**
- 빠른 시작 (모델 학습 없음)
- 기본 색상 매핑만 사용
- 감정 분석 정확도 낮음

### 6. 웹 브라우저에서 접속

```
http://localhost:8080
```

---

## ⚠️ improved_emotion_model 사용 시 주의사항

### 첫 실행 시 모델 로딩

첫 실행 시 다음과 같은 로그가 표시됩니다:

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
- 이후 실행: 약 10-20초

### 필수 데이터 파일

다음 파일들이 `our_model/` 폴더에 존재해야 합니다:

```
our_model/
├── emotion_sentimen_dataset.csv    # 텍스트 감정 분석용 (165,017개 샘플)
├── your_file_name.csv              # 색상 추천용 (29,446개 샘플)
└── improved_emotion_model.py        # 모델 파일
```

### 모델 로딩 실패 시

모델 로딩에 실패하면 자동으로 `simple_emotion_model`로 폴백됩니다:

```
❌ 개선된 AI 모델 로딩 실패: ...
🔄 폴백 모델 사용 (simple_emotion_model)
```

---

## 🚀 빠른 시작 가이드

### 시나리오 1: 최고 성능 원함 (권장)

```bash
# 1. 가상 환경 활성화
source .venv/bin/activate

# 2. 패키지 설치
pip install -r requirements.txt

# 3. 개선된 모델로 실행 (기본값)
python app.py

# 4. 브라우저에서 접속
# http://localhost:8080
```

### 시나리오 2: 빠른 시작 원함

```bash
# 1. 가상 환경 활성화
source .venv/bin/activate

# 2. 패키지 설치
pip install -r requirements.txt

# 3. 기본 모델로 실행
USE_IMPROVED_MODEL=false python app.py

# 4. 브라우저에서 접속
# http://localhost:8080
```

### 시나리오 3: improved_emotion_model 사용 안 함

#### 방법 A: 환경 변수 사용 (권장)

```bash
USE_IMPROVED_MODEL=false python app.py
```

#### 방법 B: 파일 이름 변경

```bash
mv our_model/improved_emotion_model.py our_model/improved_emotion_model.py.bak
python app.py
```

#### 방법 C: app.py 수정

`app.py`의 모델 로딩 부분을 다음과 같이 수정:

```python
# improved 모델을 사용하지 않고 simple 모델 직접 사용
from simple_emotion_model import analyze_emotion_and_color
AI_MODEL_AVAILABLE = True
print("📌 기본 모델 사용 (simple_emotion_model)")
```

---

## 📊 API 엔드포인트

### 1. 감정 분석 및 색상 추천

```bash
POST /api/analyze
Content-Type: application/json

{
  "text": "오늘 정말 행복한 하루였어!"
}
```

**응답:**
```json
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

## 🔧 문제 해결

### Q: 포트 8080이 이미 사용 중입니다

**해결책:**

```python
# app.py의 마지막 줄 수정
app.run(host='0.0.0.0', port=8081, debug=False, use_reloader=False)
```

### Q: 모델 로딩이 실패했습니다

**확인 사항:**

1. 데이터 파일 존재 확인:
   ```bash
   ls -la our_model/*.csv
   ```

2. 필요한 패키지 설치 확인:
   ```bash
   pip install -r requirements.txt
   ```

### Q: 서버가 느립니다

**원인:** 첫 실행 시 모델 학습으로 인한 지연 (정상)

**해결책:**
- 첫 실행은 1-2분 소요
- 이후 요청은 빠르게 처리됨

### Q: 한국어가 깨져서 나옵니다

**해결책:** 파일 상단에 인코딩 설정 확인

```python
# -*- coding: utf-8 -*-
```

---

## 📁 프로젝트 구조

```
positive/
├── app.py                          # Flask 메인 서버
├── requirements.txt                # 패키지 의존성
├── SETUP.md                        # 상세 설정 가이드
├── README.md                       # 이 파일
├── diaries.json                    # 저장된 일기 데이터
├── our_model/
│   ├── improved_emotion_model.py   # 개선된 감정 분석 모델 ⭐
│   ├── simple_emotion_model.py     # 기본 감정 분석 모델
│   ├── emotion_sentimen_dataset.csv # 텍스트 감정 분석 데이터
│   ├── your_file_name.csv          # 색상 추천 데이터
│   └── model_cache.pkl             # 캐시된 모델
├── static/
│   ├── styles.css
│   ├── script.js
│   ├── diary.css
│   └── diary.js
└── templates/
    ├── index.html
    ├── diary.html
    └── diary_viewer.html
```

---

## 📝 라이선스

이 프로젝트는 개인 학습 목적으로 만들어졌습니다.

---

**마지막 업데이트:** 2025-11-16
