# 🚀 프로젝트 실행 가이드

## 📌 빠른 실행 (3단계)

### 1단계: 패키지 설치
```bash
pip install -r requirements.txt
```

### 2단계: 프로젝트 실행
```bash
python app.py
```

### 3단계: 브라우저 접속
```
http://localhost:8080
```

---

## 🎯 모델 선택 가이드

### ⭐ 옵션 1: 개선된 모델 사용 (기본값, 권장)

```bash
python app.py
```

**장점:**
- 텍스트 감정 분석: 97% 정확도
- 색상 모델: 89.86% 정확도
- 한국어/영어 모두 지원

**단점:**
- 첫 실행 시 1-2분 소요 (모델 학습)

**로그:**
```
🚀 개선된 모델 로딩 시작...
📊 데이터셋 로딩 중...
📈 165017개 샘플로 모델 학습 중...
✅ 모든 모델 로딩 완료!
🤖 개선된 AI 모델 로딩 성공!
```

---

### 📌 옵션 2: 기본 모델 사용 (빠른 실행)

```bash
USE_IMPROVED_MODEL=false python app.py
```

**장점:**
- 빠른 시작 (모델 학습 없음)
- 즉시 사용 가능

**단점:**
- 감정 분석 정확도 낮음
- 기본 색상 매핑만 사용

**로그:**
```
📌 기본 모델 사용 (simple_emotion_model)
```

---

## ⚠️ 주의사항

### improved_emotion_model 사용 시

#### 필수 파일 확인
```bash
# 다음 파일들이 존재해야 합니다
ls -la our_model/emotion_sentimen_dataset.csv
ls -la our_model/your_file_name.csv
```

#### 첫 실행 시 시간 소요
- 첫 실행: **약 1-2분** (모델 학습)
- 이후 실행: **약 10-20초** (모델 재로드)

#### 모델 로딩 실패 시
자동으로 `simple_emotion_model`로 폴백됩니다:
```
❌ 개선된 AI 모델 로딩 실패: ...
🔄 폴백 모델 사용 (simple_emotion_model)
```

---

## 🔧 포트 변경

포트 8080이 이미 사용 중인 경우:

```bash
# app.py의 마지막 줄 수정
# 변경 전:
app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)

# 변경 후:
app.run(host='0.0.0.0', port=8081, debug=False, use_reloader=False)
```

---

## 📊 성능 비교

| 항목 | 개선된 모델 | 기본 모델 |
|------|-----------|---------|
| 텍스트 감정 정확도 | 97% | ~70% |
| 색상 모델 정확도 | 89.86% | 기본 매핑 |
| 첫 실행 시간 | 1-2분 | 즉시 |
| 이후 실행 시간 | 10-20초 | 즉시 |
| 한국어 지원 | ✅ | ✅ |
| 영어 지원 | ✅ | ✅ |

---

## 🎨 감정 분류

| 감정 | 한국어 키워드 | 영어 키워드 | 색상 |
|------|------------|----------|------|
| Happiness | 행복, 기쁨, 사랑 | happy, joy, love | 황금색 |
| Sadness | 슬픔, 외로움, 우울 | sad, lonely, blue | 파란색 |
| Anger | 화, 짜증, 분노 | angry, mad, hate | 빨간색 |
| Fear | 무서움, 두려움 | scared, afraid, fear | 회색 |
| Disgust | 역겨움, 혐오 | disgusted, gross | 초록색 |
| Surprise | 놀람, 충격 | surprised, shocked | 핑크색 |

---

## 📝 API 사용 예시

### 감정 분석 요청
```bash
curl -X POST http://localhost:8080/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "오늘 정말 행복한 하루였어!"}'
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

---

## 🆘 문제 해결

### Q: 모듈을 찾을 수 없습니다
```
ModuleNotFoundError: No module named 'pandas'
```

**해결책:**
```bash
pip install -r requirements.txt
```

### Q: 포트가 이미 사용 중입니다
```
Address already in use
```

**해결책:**
```bash
# 기존 프로세스 종료
lsof -i :8080
kill -9 <PID>

# 또는 포트 변경
USE_PORT=8081 python app.py
```

### Q: 한국어가 깨져서 나옵니다

**해결책:** 파일 인코딩 확인
```python
# -*- coding: utf-8 -*-
```

### Q: 서버가 느립니다

**원인:** 첫 실행 시 모델 학습 (정상)

**해결책:**
- 첫 실행은 1-2분 소요
- 이후 요청은 빠르게 처리됨

---

## 📚 추가 정보

- **상세 설정 가이드**: `SETUP.md` 참고
- **프로젝트 개요**: `README.md` 참고
- **패키지 정보**: `requirements.txt` 참고

---

**마지막 업데이트:** 2025-11-16
