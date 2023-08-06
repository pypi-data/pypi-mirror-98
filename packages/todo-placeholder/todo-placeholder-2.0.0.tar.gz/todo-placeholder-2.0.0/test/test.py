import todo
import requests

def get_data(url):
    r = requests.get(url)
    # How do I get the response code here? TODO via placeholder
    if r.status_code != 200:
        raise RuntimeError(f'Error: server responded with error code {r.status_code}')
    return r.text

get_data('http://www.example.com/probably_404')