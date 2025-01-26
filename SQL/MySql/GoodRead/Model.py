"""
GoodRead Simulation

"""

from datetime import datetime
from peewee import MySQLDatabase,Model,CharField,\
    ForeignKeyField,DateField,DateTimeField,SmallIntegerField,TextField

from playhouse.db_url import connect


database = connect('mysql://behrad:123@127.0.0.1:3306/goodRead')

#database = MySQLDatabase('mysql://root:@127.0.0.1:3306/goodRead')


class BaseModel(Model):
    
    class Meta():
        database = database

    def __str__(self):
        return str(self.id)
    



class User(BaseModel):
    username = CharField(max_length=32)
    password = CharField(max_length=32)



class Author(BaseModel):
    name = CharField(max_length=32)



class Book(BaseModel):
    name = CharField(max_length=32)
    isbn = CharField(max_length=32)


class Shelf(BaseModel):
    name = CharField(max_length=32)
    user = ForeignKeyField(User, backref='Shelves')


class BookShelf(BaseModel):
    user = ForeignKeyField(User, backref='book_shelves')
    book = ForeignKeyField(Book, backref='book_shelves')
    shelf = ForeignKeyField(Shelf, backref='book_shelves')
    start_date = DateField(null = True)
    end_date = DateField(null = True)
    rate = SmallIntegerField()
    comment = TextField()


    create_time = DateTimeField(default = datetime.now())



class BookAuthor(BaseModel):
    book = ForeignKeyField(Book, backref='Author')
    author = ForeignKeyField(Author, backref='books')



class BookTranslator(BaseModel):

    book = ForeignKeyField(Book, backref='Author')
    translator = ForeignKeyField(Author, backref='translator_books')



class UserRealation(BaseModel):
    follower =ForeignKeyField(User, backref='follower')
    following = ForeignKeyField(User, backref='following')



class UserAuthorRealation(BaseModel):
    user_followed = ForeignKeyField(User, backref='followed_authors')
    author = ForeignKeyField(Author, backref='following_users')