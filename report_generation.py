import openai
import os
from konlpy.tag import Okt
from collections import Counter
from tqdm import tqdm


COLOR_RED = "\033[91m"
COLOR_RESET = "\033[0m"
COLOR_BLUE = "\033[94m"


def check_tokens(prompt: str, max_length: int = 3500) -> bool:
    okt = Okt()
    tokens = okt.pos(prompt, norm=True, stem=True)
    return len(tokens) <= max_length

def split_string_by_tokens(prompt: str, max_length: int = 3500) -> list:
    okt = Okt()
    tokens = okt.pos(prompt, norm=True, stem=True)
    cnt = 0
    return_strings = []
    tmp_string = ""
    for token in tokens:
        tmp_string += token[0]
        cnt += 0
        if cnt >= max_length:
            return_strings.append(tmp_string)
            cnt = 0
    return return_strings

def generate_report(contents_set, api_key, search_keyword, max_attempts: int = 10):
    openai.api_key = api_key
    keywords = ", ".join(list(contents_set))
    messages = [
        {"role": "system", "content": f"너는 {search_keyword} 분야의 전문가로서 조언을 주고 있어"},
        {"role": "user", "content": f"'{search_keyword}'에 관한 주제로 웹 크롤링과 형태소 분석을 통해 얻은 주요 키워드는 {keywords}입니다. 이 키워드들을 바탕으로 보고서를 작성해주세요."}
    ]
    
    response_texts = []
    
    for idx in tqdm(range(max_attempts), desc="Generating report", ncols=100):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages
            )
            res = response['choices'][0]['message']['content']
            response_texts.append(res)
            messages.append({"role": "user", "content": "계속해서 보고서를 완성해주세요."})
        except Exception as e:
            print(f"{COLOR_RED}Error during attempt {idx + 1}: {e}{COLOR_RESET}")

    full_report = "".join(response_texts)
    
    if not os.path.exists('output'):
        os.makedirs('output')

    with open('output/report.txt', 'w', encoding='utf-8') as f:
        f.write(full_report)
