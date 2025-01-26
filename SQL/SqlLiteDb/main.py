import sys
from utils.db import create_tables
from crawl import get_links

from Models import Article, Category

"""
The executable code of the program stores the data in the database,

 displays it, and creates a table in the database.

"""

def run():
    links = get_links()

    cat = Category.create(name = 'Sport')
    for link in links:
        article = Article.create(url=link,category = cat)
        print(article.id)


def show():
    print(f"articles: {Article.select().count()}\t Categorys:{Category.select().count()}")

if __name__ == '__main__':
    if sys.argv[1] == 'create_tables':
        create_tables()
    elif sys.argv[1] == 'run':
        run()
    elif sys.argv[1] == 'status':
        show()
