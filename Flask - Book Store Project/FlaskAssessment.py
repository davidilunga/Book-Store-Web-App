# app.py

from flask import Flask, render_template, request, redirect, url_for, session
from User import RegisteredUser, User
from Book import Book
from Hashing import PasswordHash as hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'

def getBooks():
    library = []
    try:
        file = open("static/files/library.txt", 'r')
        for x in file:
            book = x.split('/ ')
            bookself = Book(book[0], book[1], book[2], book[3], book[4], book[5])
            library.append(bookself)
        file.close()

        return library
    except Exception as e:
        print(f"Error: {type(e)} - {e}")

basket = []

def getUserList():
    while True:
        try:
            users = []
            file = open("static/files/accounts.txt", "r")
            for x in file:
                userInfo = x.split(', ')
                user = RegisteredUser(userInfo[0], userInfo[1], userInfo[2], userInfo[3], userInfo[4])
                users.append(user)
            file.close
            return users
        except FileNotFoundError as e:
            file = open("static/files/accounts.txt", 'w')
            file.close()

def getUser(userinfo):
    users = getUserList()
    for account in users:
        if userinfo == account.email:
            return account

    return None

def getBasket(user):
    personal_basket = []
    if user != '':
        while True:
            try:
                username = user.split("@")
                file = open(f"static/files/baskets/{username[0]}_basket.txt", 'r')
                for x in file:
                    book = x.split('/ ')
                    bookself = Book(book[0], book[1], book[2], book[3], book[4], book[5])
                    personal_basket.append(bookself)
                return personal_basket
            except FileNotFoundError as e:
                file = open(f"static/files/baskets/{username[0]}_basket.txt", 'w')
                file.close()
    else:
        return personal_basket

def getOrders(user):
    personal_basket = []
    if user != '':
        while True:
            try:
                username = user.split("@")
                file = open(f"static/files/orders/{username[0]}_orders.txt", 'r')
                for x in file:
                    book = x.split('/ ')
                    bookself = Book(book[0], book[1], book[2], book[3], book[4], book[5])
                    personal_basket.append(bookself)
                return personal_basket
            except FileNotFoundError as e:
                file = open(f"static/files/baskets/{username[0]}_orders.txt", 'w')
                file.close()
    else:
        return personal_basket

def updateAccounts(users):
    file = open("static/files/accounts.txt", 'w')
    for account in users:
        file.write(f'{account.fName}, {account.lName}, {account.email}, {account.salt}, {account.password}, \n')
        
    file.close()

@app.route('/')
def home():
    signed_in =  False
    if 'user' in session:
        signed_in =  True
        return render_template('index.html', title='Home', signed_in = signed_in)
    return render_template('index.html', title='Home', signed_in = signed_in)

@app.route('/add-to-basket/<rowid>', methods = ["GET" , "POST"])
def add_to_basket(rowid):
    books = getBooks()
    book = None
    for x in books:
        if x.rowid == rowid:
            book = x
    while True:
        try:
            username = session['user'].split("@")
            file = open(f"static/files/baskets/{username[0]}_basket.txt", 'a')
            file.write(f"{book.rowid}/ {book.title}/ {book.author}/ {book.genre}/ {book.price}/ {book.overview}/ \n")
            file.close()
        except FileNotFoundError as fn:
            file = open(f"static/files/baskets/{username[0]}_basket.txt", 'w')
            file.close()
        except Exception as e:
            print(f"Error: {type(e)} - {e}")
            file = open(f"static/files/baskets/{username[0]}_basket.txt", 'w')
            file.close()
        else:
            break
    return redirect(url_for('success'))

@app.route('/success', methods = ["GET"])
def success():
    return redirect(url_for('book_info'))

@app.route('/book-information/delete/<number>', methods = ["GET" , "POST"])
def delete_from_basket(number):
    number = int(number)
    basket = getBasket(session['user'])
    basket.pop(number)
    username = session['user'].split("@")
    file = open(f"static/files/baskets/{username[0]}_basket.txt", 'w')
    for x in basket:
        file.write(f"{x.rowid}/ {x.title}/ {x.author}/ {x.genre}/ {x.price}/ {x.overview}/ \n")
    file.close()
    return redirect(url_for('success'))


@app.route('/book-information', methods = ["GET" , "POST"])
def book_info():
    books = getBooks()
    signed_in =  False
    basket = []
    total = 0
    if 'user' in session:
        signed_in =  True
        basket = getBasket(session['user'])
        for x in basket:
            total += float(x.price)
    if request.method == "POST":
        available_books = []
        searched_book = request.form.get('book-search').lower()
        for x in books:
            if searched_book in x.title.lower():
                available_books.append(x)
        books = available_books
        return render_template('book_info.html', title='Book Information', content='Search Books Content', books = books, signed_in = signed_in, basket = basket, total = total)

    return render_template('book_info.html', title='Book Information', content='Search Books Content', books = books, signed_in = signed_in, basket = basket, total = total)

@app.route('/log-in', methods = ["GET" , "POST"])
def log_in(): 
    if request.method == 'POST':
        email = request.form.get('username').strip()
        password = request.form.get('password').strip()
        
        users = getUserList()
        for account in users:
            if email == account.email:
                validated_password = hash.checkPassword(account.salt, account.password, password)
                if validated_password == True:
                    session['user'] = email
                    return redirect(url_for('book_info'))
                else:
                    return render_template('log_in.html', message='Invalid credentials')

    return render_template('log_in.html', title='Log In', content='Log in to your account')

@app.route('/checkout/remove/<number>', methods = ["GET" , "POST"])
def delete_from_checkout(number):
    number = int(number)
    basket = getBasket(session['user'])
    basket.pop(number)
    username = session['user'].split("@")
    file = open(f"static/files/baskets/{username[0]}_basket.txt", 'w')
    for x in basket:
        file.write(f"{x.rowid}/ {x.title}/ {x.author}/ {x.genre}/ {x.price}/ {x.overview}/ \n")
    file.close()
    return redirect(url_for('checkout'))

@app.route('/checkout', methods = ["GET" , "POST"])
def checkout():
    books = getBooks()
    signed_in =  False
    basket = []
    total = 0
    if 'user' in session:
        signed_in =  True
        basket = getBasket(session['user'])
        for x in basket:
            total += float(x.price)
        return render_template('checkout.html', title='Checkout', books = books, signed_in = signed_in, basket = basket, total = total)
    return render_template('checkout.html', title='Checkout', books = books, signed_in = signed_in, basket = basket, total = total)

@app.route('/checkout/pay-now/',  methods = ["GET" , "POST"])
def pay():
    basket = getBasket(session['user'])
    username = session['user'].split("@")
    try:
        file = open(f"static/files/orders/{username[0]}_orders.txt", 'a')
    except FileNotFoundError as f:
        file = open(f"static/files/orders/{username[0]}_orders.txt", 'w')
    except Exception as e:
        print(f"Error: {type(e)} - {e}")
    else:
        for x in basket:
            file.write(f"{x.rowid}/ {x.title}/ {x.author}/ {x.genre}/ {x.price}/ {x.overview}/ \n")
        file.close()

        file = open(f"static/files/baskets/{username[0]}_basket.txt", 'w')
        file.write('')
        file.close()
    return redirect(url_for('order_history'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')
        
        passwordSalt = hash.get_salt(16)
        password = hash.run(password, passwordSalt)
        user = RegisteredUser(first_name, last_name, email, passwordSalt, password)
        
        file = open("static/files/accounts.txt", 'a')
        file.write(f'{user.fName}, {user.lName}, {user.email}, {user.salt}, {user.password}, \n')
        file.close()
        return render_template('log_in.html', title='Log In', content='Log in to your account')
    
    else:
        return render_template('register.html', title='Register')

@app.route('/account-details', methods = ["GET" , "POST"])
def account_details():
    signed_in_user = getUser(session["user"])
    signed_in =  False
    if 'user' in session:
        signed_in =  True
        return render_template('account_details.html', title = "View Account Details", signed_in_user = signed_in_user, signed_in = signed_in) 
    
    return render_template('account_details.html', title='View Account Details', signed_in_user = signed_in_user)

@app.route('/account-details/edit-account-details', methods = ["GET" , "POST"])
def edit_account_details():
    signed_in_user = getUser(session["user"])
    if 'user' in session:
        signed_in =  True
    if request.method == 'POST':
        userList = getUserList()

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template('edit_account_details.html', error='Passwords do not match')
        
        passwordSalt = hash.get_salt(16)
        password = hash.run(password, passwordSalt)
        
        for x in userList:
            if session['user'] == x.email:
                x.fName = first_name
                x.lName = last_name
                x.email = email
                x.salt = passwordSalt
                x.password = password
                session['user'] = x.email

        updateAccounts(userList)
        return redirect(url_for('account_details'))

    return render_template('edit_account_details.html', title='View Account Details', signed_in = signed_in, signed_in_user = signed_in_user)

@app.route('/logout')
def logout():
    # Clear the session (log out the user)
    session.pop('user', None)
    return redirect(url_for('log_in'))

@app.route('/order-history',  methods = ["GET" , "POST"])
def order_history():
    signed_in_user = getUser(session["user"])
    if 'user' in session:
        signed_in =  True
        orders = getOrders(session['user'])
        return render_template('order_history.html', title='Order History', orders = orders, signed_in = signed_in, basket = basket)
    return render_template('order_history.html', title = 'Order History', signed_in = signed_in, signed_in_user = signed_in_user)

if __name__ == '__main__':
    app.run(debug=True)
