from bs4 import BeautifulSoup
import requests
import json
from konlpy.tag import Okt
from collections import Counter
import os
import re
import datetime
from tqdm import tqdm
import warnings


COLOR_BLUE = "\033[94m"
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_RESET = "\033[0m"

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

def extract_text_from_url(url: str) -> dict:
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        target_divs = soup.find_all('div', id=lambda x: x and ('contents' in x or 'news' in x))
        text_content = ' '.join([div.get_text() for div in target_divs])

        return text_tokenizer(text_content)
    except Exception as e:
        error_message = f"{datetime.datetime.now()} - Error fetching content from {url}: {e}\n"
        
        with open('cache/error_log.txt', 'a', encoding='utf-8') as error_log:
            error_log.write(error_message)
        
        return None



def load_stopwords() -> set:
    with open('./cache/stopword.txt', 'r', encoding='utf-8') as f:
        stopwords = f.readlines()
    return set([word.strip() for word in stopwords])


def text_tokenizer(text: str) -> dict:
    okt = Okt()
    tokens = okt.pos(text, norm=True, stem=True)

    meaningful_tags = ['Noun', 'Adjective', 'Verb']

    stopwords = load_stopwords()
    
    filtered_tokens = [
        word for word, tag in tokens if tag in meaningful_tags and re.match("^[가-힣]+$", word) and word not in stopwords and len(word) > 1
    ]

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

    for word, freq in content.items():
        if word in cached_data:
            cached_data[word] += freq
        else:
            cached_data[word] = freq

    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(cached_data, f, ensure_ascii=False, indent=4)



def process_and_save_texts(urls: list) -> None:
    for url in tqdm(urls, desc="Processing URLs", ncols=100):
        extracted_content = extract_text_from_url(url)
        if extracted_content:
            save_extracted_text_to_cache(extracted_content)