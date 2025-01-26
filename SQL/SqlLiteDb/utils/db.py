from Models import database, Article, Category


def create_tables():
    database.create_tables([Article, Category])
