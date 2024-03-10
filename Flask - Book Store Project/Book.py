class Book:
    def __init__(self, rowid,title, author, genre, price, overview) -> None:
        self.__rowid = rowid
        self.__title = title
        self.__author = author
        self.__genre = genre
        self.__price = price
        self.__overview = overview

    @property
    def rowid(self):
        return self.__rowid
    
    @rowid.setter
    def rowid(self, rowid):
        self.__rowid = rowid
#--------------------------------------------
    @property
    def title(self):
        return self.__title
    
    @title.setter
    def title(self, title):
        self.__title = title
#--------------------------------------------
    @property
    def author(self):
        return self.__author
    
    @author.setter
    def author(self, author):
        self.__author = author
#--------------------------------------------
    @property
    def genre(self):
        return self.__genre
    
    @genre.setter
    def genre(self, genre):
        self.__genre = genre
#--------------------------------------------
    @property
    def price(self):
        return self.__price
    
    @price.setter
    def price(self, price):
        self.__price = price
#--------------------------------------------
    @property
    def overview(self):
        return self.__overview
    
    @overview.setter
    def overview(self, overview):
        self.__overview = overview
