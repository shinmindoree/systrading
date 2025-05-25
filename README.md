# 시스템 트레이딩 알고리즘

이 프로젝트는 바이낸스 거래소와 연동하여 자동화된 시스템 트레이딩 알고리즘을 개발하는 것을 목표로 합니다.

## 1단계: 개발 환경 구축

1. Python 3.12.7 버전 사용
2. 가상환경 생성 및 패키지 설치
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. .env 파일에 바이낸스 API 키/시크릿 저장
   ```env
   BINANCE_API_KEY=여기에_입력
   BINANCE_API_SECRET=여기에_입력
   ``` 