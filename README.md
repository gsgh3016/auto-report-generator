# auto-web-crawling

## 개요

- 검색어에 대한 자동 보고서 생성
- 검색 API: 네이버 검색 API에서 'news' 노드 활용 &rarr; `./검색어_naver_news.json`으로 파일 생성
- 검색 결과에서 각 뉴스 기사 페이지로 접속하여 \<p> 테그 추적 및 텍스트 크롤링
- 크롤링한 데이터를 형태소 분석을 통해 빈도수 체크
- 상위 빈도 단어, 반복 명령을 통해 보고서 생성
- cache에 stopword 지정 가능

## 환경 설정

1. 파이썬(>=3.7), 자바(konlpy) 설치
2. poetry 설치
> ```bash
> pip install poetry
> ```
3. 종속성 모듈 설치
> ```bash
> poetry install
> ```
4. ./.env 파일 만들기
> ```python
> client_id = "your_naver_client_id"
> client_secret = "your_naver_client_secret"
> open_ai_key = "your_open_ai_key"
> ```

## 실행

1. poetry 쉘 생성
> ```bash
> poetry shell
> ```

2. poetry 쉘 내부에서 main.py 실행
> ```bash
> poetry run python3 main.py
> ```

## 기능

### 네이버 검색 API로 `{키워드}_naver_{카테고리}.json` 파일 생성
- `main.py`의 `node` 변수로 카테고리 선정 가능
- 실행 후 키워드 입력 시 기존 json 파일 유무에 따라 크롤링 여부 결정
- json 파일 생성 시 `./cache/` 디렉토리에 생성

### 뉴스 기사 본문 텍스트 크롤링 및 형태소 별 빈도 분석
- `./cache/extracted_text.json`파일에 `형태소 키워드:빈도수` 형식으로 저장
- `gpt-3.5-turbo-0613`모델의 프롬프팅에 사용

### `gpt-3.5-turbo-0613` 모델을 활용한 보고서 생성
- `report_generation.py` 모듈을 통해 `./output/report.txt` 파일에 보고서 생성

### (선택)
- `get_keywords()` 함수로 `./keywords/generated_keyword.txt` 파일 생성
