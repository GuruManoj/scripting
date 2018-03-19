from googleapiclient.discovery import build
import pprint

my_api_key = " AIzaSyDHrpu0KW0cZtrzt4IisEQaWtjPkxAuTtQ "
my_cse_id = "012758781286053106780:e_qc7l2z7ek"

def google_search(search_term, api_key, cse_id, count):
    service = build("customsearch", "v1", developerKey=api_key)
    #res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    res = service.cse().list(
    q= search_term,
    cx= my_cse_id,
    searchType='image',
    num=count,
    #imgType='clipart',
    fileType='png',
    safe= 'off'
).execute()
    #pprint.pprint(res)
    return res['items']

results = google_search(
    'car', my_api_key, my_cse_id, count=10)

for result in results:
    pprint.pprint(result["link"])