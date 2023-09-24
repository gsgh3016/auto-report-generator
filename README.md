# auto-web-crawling

## 개요

- 검색어에 대한 자동 보고서 생성
- 검색 API: 네이버 검색 API에서 'news' 노드 활용 &rarr; `./검색어_naver_news.json`으로 파일 생성
- 검색 결과에서 각 뉴스 기사 페이지로 접속하여 \<p> 테그 추적 및 텍스트 크롤링
- 크롤링한 데이터를 형태소 분석을 통해 빈도수 체크
- 상위 빈도 단어, 반복 명령을 통해 보고서 생성
- cache에 stopword 지정 가능

## 환경 설정

- 파이썬(>=3.7), 자바(konlpy) 설치

```bash
pip install poetry
```
```bash
poetry install
```

## 실행

```bash
poetry run python3 main.py
```
