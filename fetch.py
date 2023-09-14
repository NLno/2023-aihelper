import requests
from bs4 import BeautifulSoup

def fetch(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        paragraphs = soup.find_all('p')
        all_paragraphs = ''.join([paragraph.text for paragraph in paragraphs])
        print("all paragraphs: ", all_paragraphs)
        return "Now act as a summarizer. You should summarize the article from url="+url+", and the contents are: "+all_paragraphs
    return


if __name__ == "__main__":
    fetch("https://dev.qweather.com/en/help")