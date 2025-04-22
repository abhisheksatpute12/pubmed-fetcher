# pubmed_fetcher/fetcher.py
import requests
from typing import List, Dict
from pubmed_fetcher.parser import parse_article

EMAIL = "your@email.com"
BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def fetch_papers(query: str, debug: bool = False) -> List[Dict[str, str]]:
    ids = fetch_ids(query, debug)
    articles = fetch_details(ids, debug)
    return [parse_article(article) for article in articles]

def fetch_ids(query: str, debug: bool = False) -> List[str]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 50,
        "email": EMAIL
    }
    response = requests.get(f"{BASE}/esearch.fcgi", params=params)
    response.raise_for_status()
    ids = response.json()["esearchresult"]["idlist"]
    if debug:
        print(f"Fetched IDs: {ids}")
    return ids

def fetch_details(ids: List[str], debug: bool = False) -> List[Dict]:
    id_str = ",".join(ids)
    params = {
        "db": "pubmed",
        "retmode": "xml",
        "id": id_str,
        "email": EMAIL
    }
    response = requests.get(f"{BASE}/efetch.fcgi", params=params)
    response.raise_for_status()
    return response.text.split("<PubmedArticle>")
