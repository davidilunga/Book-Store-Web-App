from abc import ABC, abstractmethod
from Book import Book

class User(ABC):
    def __init__(self, fName, lName, email) -> None:
        self.__fName = fName
        self.__lName = lName
        self.__email = email

    @property
    def fName(self):
        return self.__fName
    
    @fName.setter
    def fName(self, fName):
        self.__fName = fName
#--------------------------------------------
    @property
    def lName(self):
        return self.__lName
    
    @lName.setter
    def lName(self, lName):
        self.__lName = lName
#--------------------------------------------
    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, email):
        self.__email = email

    @abstractmethod
    def viewUserDetails():
        pass

    @abstractmethod
    def viewOrderHistory():
        pass


class UnregisteredUser(User):
    def __init__(self, fName, lName, email) -> None:
        super().__init__(fName, lName, email)

class RegisteredUser(User):
    def __init__(self, fName, lName, email, salt, password) -> None:
        super().__init__(fName, lName, email)
        self.__salt = salt
        self.__password = password
#-------------------------------------------- 
    @property
    def salt(self):
        return self.__salt
    
    @salt.setter
    def salt(self, salt):
        self.__salt= salt
#--------------------------------------------
    @property
    def password(self):
        return self.__password
    
    @password.setter
    def password(self, password):
        self.__password = password
#--------------------------------------------
    def viewUserDetails(self):
        print('*****************************************************************************')
        print('*                          VIEW ACCOUNT DETAILS                             *')
        print('*****************************************************************************')

        print("\nHere are your user details: \n")

        print(f"Name : {self.fName} {self.lName}")
        print(f"Email : {self.email}")

    def viewOrderHistory(self):
        try:
            history = []
            username = self.email.split("@")
            file = open(f"files/orders/{username[0]}_orders.txt", 'r')
            for x in file:
                book = x.split('/ ')
                bookself = Book(book[0], book[1], book[2], book[3], book[4])
                history.append(bookself)
            file.close()
            print('*****************************************************************************')
            print('*                          VIEW ORDER HISTORY                               *')
            print('*****************************************************************************')

            print("\nHere's your order history: \n")
            for book in history:
                print("--------------------------------------------------------------------")
                print(f"    Title: {book.title}")
                print(f"    Author: {book.author}")
                print(f"    Genre: {book.genre}")
                print(f"    Price: {book.price}")
                print(f"    Overview: {book.overview}")
                
        except FileNotFoundError as f:
            print("You have no order history.")
        except Exception as e:
            print(f"Error: {type(e)} - {e}")