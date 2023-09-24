from bs4 import BeautifulSoup
import requests
import json
from konlpy.tag import Okt
from collections import Counter
import os
import re

COLOR_BLUE = "\033[94m"
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_RESET = "\033[0m"

def extract_text_from_url(url: str) -> dict:
    try:
        print(f"{COLOR_BLUE}Fetching content from {url} ... {COLOR_RESET}")  # 진행 상황 메시지 추가
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        target_divs = soup.find_all(
            'div', id=lambda x: x and ('contents' in x or 'news' in x))
        text_content = ' '.join([div.get_text() for div in target_divs])

        print(f"{COLOR_GREEN}Successfully fetched content from {url} {COLOR_RESET}")  # 완료 메시지 추가
        return text_tokenizer(text_content)
    except Exception as e:
        print(f"{COLOR_RED}Error fetching content from {url}: {e} {COLOR_RESET}")
        return None


def load_stopwords() -> set:
    with open('./cache/stopword.txt', 'r', encoding='utf-8') as f:
        stopwords = f.readlines()
    # 각 단어의 앞뒤 공백 제거 후 set으로 반환
    return set([word.strip() for word in stopwords])


def text_tokenizer(text: str) -> dict:
    okt = Okt()
    tokens = okt.pos(text, norm=True, stem=True)  # 토큰화 및 품사 태깅

    # 유의미한 형태소 품사 리스트
    meaningful_tags = ['Noun', 'Adjective', 'Verb']

    stopwords = load_stopwords()
    
    # 순수한 한글만 포함하는 토큰만 선택
    filtered_tokens = [word for word, tag in tokens if tag in meaningful_tags and re.match("^[가-힣]+$", word) and word not in stopwords and len(word) > 1]

    counter = Counter(filtered_tokens)
    return dict(counter.most_common(20))



def initialize_cache_file() -> None:
    cache_path = "./cache/extracted_text.json"
    empty_data = {}
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(empty_data, f, ensure_ascii=False, indent=4)


def load_cached_data() -> dict:
    cache_path = "./cache/extracted_text.json"
    if os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_extracted_text_to_cache(content: dict) -> None:
    cache_path = "./cache/extracted_text.json"
    cached_data = load_cached_data()

    # Update the cached_data with new content
    for word, freq in content.items():
        if word in cached_data:
            cached_data[word] += freq
        else:
            cached_data[word] = freq

    # Save updated data
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(cached_data, f, ensure_ascii=False, indent=4)



def process_and_save_texts(urls: list) -> None:
    total_urls = len(urls)
    for index, url in enumerate(urls):
        print(f"{COLOR_BLUE}Processing URL {index + 1} of {total_urls} {COLOR_RESET}")  # 진행 상황 메시지 추가
        extracted_content = extract_text_from_url(url)
        if extracted_content:
            save_extracted_text_to_cache(extracted_content)
        print(f"{COLOR_GREEN}successed URL {index + 1} of {total_urls} {COLOR_RESET}")