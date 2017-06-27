
from googleapiclient.discovery import build
import pprint
import json
from packages import *

my_api_key = "****"
my_cse_id = "****"

def google_search(search_term, api_key, cse_id, **kwargs):
    wt = random.uniform(1,1)
    time.sleep(wt)
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    if res['queries']['request'][0]['totalResults'] == '0':
        return "Not found"
    else:
        return res['items']








