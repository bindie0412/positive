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

## 📦 설치 방법

### 1. 저장소 클론

```bash
git clone https://github.com/bindie0412/positive.git
cd positive
```

### 2. Python 가상 환경 생성 (권장)

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# 또는
.venv\Scripts\activate  # Windows
```

### 3. 필수 패키지 설치

```bash
pip install -r requirements.txt
```

## 🚀 실행 방법

### 웹 서버 시작

```bash
python app.py
```

서버가 시작되면 다음 주소로 접속하세요:

```text
http://localhost:8080
```

### 모델 테스트 (선택사항)

```bash
python our_model/improved_emotion_model.py
```

## 📁 프로젝트 구조

```text
positive/
├── app.py                          # Flask 웹 서버 메인 파일
├── requirements.txt                # Python 패키지 의존성
├── diaries.json                    # 저장된 일기 데이터
├── our_model/
│   ├── improved_emotion_model.py   # 개선된 감정 분석 모델
│   ├── emotion_sentimen_dataset.csv # 감정 분석 학습 데이터
│   ├── your_file_name.csv          # 색상 데이터셋
│   └── model_cache.pkl             # 모델 캐시
├── templates/
│   ├── index.html                  # 메인 페이지
│   ├── diary.html                  # 일기 작성 페이지
│   ├── diary_viewer.html           # 일기 상세 조회 페이지
│   └── read-diary.html             # 일기 읽기 페이지
└── static/
    ├── diary.css                   # 일기 스타일
    ├── diary.js                    # 일기 기능 스크립트
    └── styles.css                  # 메인 스타일
```

## 🔌 API 엔드포인트

### 1. 감정 분석 및 색상 추천

```json
POST /api/analyze
Content-Type: application/json

{
  "text": "일기 내용"
}

응답:
{
  "success": true,
  "emotion": "Happiness",
  "color_hex": "#FFD700",
  "color_name": "황금색",
  "tone": "밝고 파스텔 톤"
}
```

### 2. 일기 저장

```json
POST /api/save-diary
Content-Type: application/json

{
  "date": "2025-11-16",
  "title": "일기 제목",
  "content": "일기 내용",
  "emotion": "Happiness",
  "color_hex": "#FFD700",
  "color_name": "황금색",
  "tone": "밝고 파스텔 톤"
}

응답:
{
  "success": true,
  "id": 1731234567890,
  "message": "일기가 저장되었습니다."
}
```

### 3. 일기 목록 조회

```json
GET /api/diaries

응답:
{
  "success": true,
  "diaries": [
    {
      "id": 1731234567890,
      "date": "2025-11-16",
      "title": "일기 제목",
      "content": "일기 내용",
      "emotion": "Happiness",
      "color_hex": "#FFD700",
      ...
    }
  ]
}
```

### 4. 일기 삭제

```json
DELETE /api/diary/<id>

응답:
{
  "success": true,
  "message": "일기가 삭제되었습니다."
}
```

## 🎯 사용 예시

### 1. 웹 브라우저에서 사용

1. `http://localhost:8080` 접속
2. 일기 내용 작성
3. "분석" 버튼 클릭
4. AI가 감정을 분석하고 색상 추천
5. "저장" 버튼으로 일기 저장

### 2. Python 코드에서 사용

```python
from our_model.improved_emotion_model import analyze_emotion_and_color

# 감정 분석 및 색상 추천
result = analyze_emotion_and_color("I'm so happy today!")
print(result)
# 출력: {'emotion': 'Happiness', 'color_hex': '#FFD700', ...}
```

## 📊 감정별 색상 데이터

| 감정 | 색상 | 톤 | 샘플 수 |
|------|------|-----|--------|
| Happiness | 황금색 | 밝고 파스텔 톤 | 248 |
| Sadness | 파란색 | 차분하고 어두운 톤 | 949 |
| Anger | 진한 빨간색 | 강렬하고 어두운 톤 | 395 |
| Fear | 회색 | 어둡고 차분한 톤 | 5,972 |
| Disgust | 연한 초록색 | 차분하고 어두운 톤 | 1,025 |
| Surprise | 핑크색 | 밝고 파스텔 톤 | 20,857 |

## 🔧 트러블슈팅

### 포트 8080이 이미 사용 중인 경우

```python
# app.py의 마지막 줄을 수정하세요:
app.run(host='0.0.0.0', port=8081, debug=False)
```

### 모델 로딩 실패

- `our_model/emotion_sentimen_dataset.csv` 파일 확인
- `our_model/your_file_name.csv` 파일 확인
- 파일이 없으면 기본 색상 매핑 사용

### 패키지 버전 충돌

```bash
# 가상 환경 재설정
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 📝 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 👨‍💻 개발자

- **Repository**: [https://github.com/bindie0412/positive](https://github.com/bindie0412/positive)
- **Branch**: main

## 🤝 기여

버그 리포트나 기능 제안은 GitHub Issues를 통해 제출해주세요.

---

**마지막 업데이트**: 2025년 11월 16일
