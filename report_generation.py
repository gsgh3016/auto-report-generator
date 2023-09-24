import openai
import os
from konlpy.tag import Okt
from collections import Counter


COLOR_RED = "\033[91m"
COLOR_RESET = "\033[0m"


def check_tokens(prompt: str, max_length: int) -> bool:
    okt = Okt()
    tokens = okt.pos(prompt, norm=True, stem=True)
    return len(tokens) <= max_length

def split_string_by_tokens(prompt: str, max_length: int) -> list:
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

def generate_report(contents_set, api_key, search_keyword):
    openai.api_key = api_key
    keywords = ", ".join(list(contents_set))
    prompt_base = f"'{search_keyword}'에 관한 주제로 웹 크롤링과 형태소 분석을 통해 얻은 주요 키워드는 {keywords}입니다. "
    prompt_base += "이 키워드들을 바탕으로 다음 항목들에 대한 상세한 보고서를 작성해주세요:"
    prompt_base += "\n1. 개요\n2. 배경 및 현황\n3. 문제점\n4. 해결방안\n5. 기대효과\n"

    MAX_TOKENS = 3500
    
    previous_response_end = ""
    if not check_tokens(prompt_base, MAX_TOKENS):
        prompt_split = split_string_by_tokens(prompt_base, MAX_TOKENS)
        for i, prompt_piece in enumerate(prompt_split):
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=prompt_piece + previous_response_end,
                max_tokens=MAX_TOKENS
            )
            res = response.choices[0].text.strip()
            previous_response_end = " ".join(res.split()[-150:])
            print(f"{COLOR_RED} prompt {i + 1} / {len(prompt_split)} {COLOR_RESET}")
            
    
    response_texts = []
    previous_response_end = ""
    
    try:
        while len(" ".join(response_texts)) < 500000:
            prompt = " - 이전 내용을 바탕으로 보고서를 계속 완성해주세요."
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=previous_response_end + prompt,
                max_tokens=MAX_TOKENS
            )
            res = response.choices[0].text.strip()
            response_texts.append(res)
            if len(res.split()) < MAX_TOKENS / 3:
                break
            previous_response_end = " ".join(res.split()[-150:])
    except:
        print(f"{COLOR_RED} davinci 호출 시 오류 {COLOR_RESET}")
    finally:
        full_report = "".join(response_texts)
        
        if not os.path.exists('output'):
            os.makedirs('output')

        with open('output/report.txt', 'w', encoding='utf-8') as f:
            f.write(full_report)
