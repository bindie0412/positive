#!/bin/zsh

# 가상 환경 활성화
source .venv/bin/activate

# 필요한 패키지 설치 (이미 설치되어 있어도 안전하게 다시 실행)
pip install -r requirements.txt

# Flask 애플리케이션 실행
/Users/jiseung/Desktop/positive/.venv/bin/python app.py
