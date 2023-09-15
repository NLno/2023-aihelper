import requests
from bs4 import BeautifulSoup

def fetch(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        p_elems = soup.find_all('p')
        paragraph = p_elems[1].text
        print("paragraph: ", paragraph)
        return "Now act as a summarizer. You should summarize the article from url="+url+", and the contents are: "+ paragraph
    return

if __name__ == "__main__":
    fetch("https://dev.qweather.com/en/help")