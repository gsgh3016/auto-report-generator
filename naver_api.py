import os
import urllib.request
import datetime
import json
from dotenv import load_dotenv


def load_api_keys():
    load_dotenv()
    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')
    return client_id, client_secret


def getRequestUrl(url, client_id, client_secret):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s]Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None


def getNaverSearch(node, srcText, start, display, client_id, client_secret):
    # Check if the file exists, if it does, skip the API call
    file_name = f"./cache/{srcText}_naver_{node}.json"
    if os.path.exists(file_name):
        print(f"{file_name} already exists. Skipping the API call.")
        return None

    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % node
    parameters = "?query=%s&start=%s&display=%s" % (
        urllib.parse.quote(srcText), start, display)

    url = base + node + parameters
    responseDecode = getRequestUrl(url, client_id, client_secret)
    if responseDecode is None:
        return None
    else:
        return json.loads(responseDecode)
