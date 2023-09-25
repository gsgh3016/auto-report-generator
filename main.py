from naver_api import load_api_keys, getNaverSearch
from data_extraction import process_and_save_texts
from data_extraction import initialize_cache_file
from report_generation import generate_report
import os
import datetime
import json
import warnings
# if necessary
# from keyword_generation import get_keywords

COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_RESET = "\033[0m"

warnings.simplefilter(action='ignore', category=Warning)


def getPostData(post, jsonResult, cnt):
    title = post['title']
    description = post['description']
    org_link = post['originallink']
    link = post['link']

    pDate = datetime.datetime.strptime(
        post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
    pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')

    jsonResult.append({
        'cnt': cnt,
        'title': title,
        'description': description,
        'org_link': org_link,
        'link': link,
        'pDate': pDate
    })


if __name__ == "__main__":
    print(f"{COLOR_BLUE}API 키 로딩 중...{COLOR_RESET}")
    client_id, client_secret = load_api_keys()
    open_ai_key = os.environ.get('open_ai_key')

    node = 'news'   # 크롤링 대상 선택 가능
    srcText = input('검색어를 입력하세요: ')
    json_file_path = f"./cache/{srcText}_naver_{node}.json"
    initialize_cache_file()

    if os.path.exists(json_file_path):
        print(f"{COLOR_BLUE}캐시에서 데이터 로딩 중...{COLOR_RESET}")
        with open(json_file_path, 'r', encoding='utf8') as f:
            jsonResult = json.load(f)
            cnt = len(jsonResult)
            total = cnt
    else:
        print(f"{COLOR_BLUE}네이버 검색 중...{COLOR_RESET}")
        cnt = 0
        jsonResult = []
        jsonResponse = getNaverSearch(
            node, srcText, 1, 100, client_id, client_secret)
        total = jsonResponse['total']

        while (jsonResponse is not None) and (jsonResponse['display'] != 0):
            for post in jsonResponse['items']:
                cnt += 1
                getPostData(post, jsonResult, cnt)

            start = jsonResponse['start'] + jsonResponse['display']
            jsonResponse = getNaverSearch(
                node, srcText, start, 100, client_id, client_secret)

        with open(json_file_path, 'w', encoding='utf8') as outfile:
            jsonFile = json.dumps(jsonResult, indent=4,
                                  sort_keys=True, ensure_ascii=False)
            outfile.write(jsonFile)

        print(f"{COLOR_GREEN}전체 검색: {total} 건{COLOR_RESET}")
        print(f"{COLOR_GREEN}가져온 데이터: {cnt} 건{COLOR_RESET}")
        print(f"{COLOR_GREEN}{srcText}_naver_{node}.json 저장 완료!{COLOR_RESET}")

    print(f"{COLOR_BLUE}내용 추출 중...{COLOR_RESET}")
    urls = [item['link'] for item in jsonResult]
    process_and_save_texts(urls)

    print(f"{COLOR_BLUE}보고서 생성 중...{COLOR_RESET}")
    contents = {}
    extracted_text_file_path = './cache/extracted_text.json'
    if not os.path.exists(extracted_text_file_path):
        with open(extracted_text_file_path, 'w', encoding='utf-8') as f:
            f.write('{}')

    with open('./cache/extracted_text.json', 'r', encoding='utf-8') as f:
        cached_data = json.load(f)

    for url in urls:
        content_freq = cached_data.get(url, {})
        for word, freq in content_freq.items():
            if word in contents:
                contents[word] += freq
            else:
                contents[word] = freq

    sorted_contents_tuple = sorted(contents.items(), key=lambda item: item[1], reverse=True)[:20]
    contents_word_freqs = [tp[0] for tp in sorted_contents_tuple]
    generate_report(contents_word_freqs, open_ai_key, srcText)
    print(f"{COLOR_GREEN}보고서 생성 완료!{COLOR_RESET}")
