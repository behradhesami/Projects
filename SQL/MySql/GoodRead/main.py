from importer import AuthorImporter, BookAuthorImporter, BookImporter,\
      BookShelfImporter, ShelfImporter, UserImporter


"""
GoodRead Simulation

"""
from Model import *


def create_tables():
    database.create_tables(
        [User, Book, Author, Shelf, BookShelf
        , UserRealation, UserAuthorRealation,BookAuthor,
         BookTranslator]
         )


def load_data():
    importer_classes = [
        UserImporter, BookImporter, AuthorImporter,
        BookAuthorImporter, ShelfImporter, BookShelfImporter
    ]
    for _class in importer_classes:
        print(_class.load())







if __name__ == '__main__':
    load_data()
    #create_tables()