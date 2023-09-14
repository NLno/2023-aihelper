import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch

def search(content: str):
    url = "https://serpapi.com/bing-search-api" # Bing Search API
    headers = {"Content-Type": "application/json"}
    data = {
    "engine": "bing", 
    "q": content,
    "cc": "us",
    "api_key": "ef4afab69662b5f1c7b0c44d85f03d0484faabf9cc8f6cb8f20d983a989b5460"
    }
    search = GoogleSearch(data)
    results = search.get_dict()
    organic_results = results['organic_results']
    search_result = organic_results[0]['snippet']
    print("search result: ", search_result)
    search_result = "Now explain what is " + content + ", according to the following search result: " + search_result
    return search_result
    
    
if __name__ == "__main__":
    search("Sun Wukong")