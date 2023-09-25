import openai
import os
import re

def get_keywords(input_keyword: str, api_key: str, max_attempts: int = 10) -> None:
    if not os.path.exists('keywords'):
        os.makedirs('keywords')
        
    openai.api_key = api_key
    keywords = ""
    attempts = 0
    
    while attempts < max_attempts:
        try:
            prompt_base = f"주제 '{input_keyword}'와 관련하여 연관된 주요 키워드나 구문을 나열해주세요. 가장 중요한 키워드부터 시작해주세요."
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo-0613',
                messages=[
                    {"role": "system", "content": f"너는 {input_keyword} 분야의 전문가로서 조언을 주고 있어"},
                    {"role": "user", "content": prompt_base},
                ]
            )
            response_raw = response['choices'][0]['message']['content']
            keywords += response_raw
            
            input_keyword = " ".join(response_raw.split()[-10:])
            attempts += 1

            if len(response_raw.split()) < 10:
                break

        except Exception as e:
            print(f"API 호출 중 오류 발생: {e}")
            break
    
    with open('keywords/generated_keyword.txt', 'w', encoding='utf-8') as f:
        f.write(keywords)
