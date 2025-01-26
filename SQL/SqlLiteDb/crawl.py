"""

    This code is a simple web scraper that takes the links from the specified website,
    prints their titles, and stores them in the database.
    It also updates the status of each article in the database.
   
   """



import requests
from bs4 import BeautifulSoup
from Models import Article

def crawl_page(url):
    response = requests.get(url)
    print(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        header_div = soup.find('div', attrs={'class': "container"})
        title = header_div.find('h1')
        print(title.text)


def get_links():
    response = requests.get('https://www.trthaber.com/haber/spor/')
    links = list()
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            href = link.attrs.get('href')
            if href is not None and href.startswith(''):
                links.append('https://www.trthaber.com/' + href)

    return( links)


if __name__ == "__main__":

    #get_links()
    articles = Article.select().where(Article.is_completed == False)
    for article in articles:

        try:
            crawl_page(article.url)
        except:
            article.is_completed ==True
            article.save()
