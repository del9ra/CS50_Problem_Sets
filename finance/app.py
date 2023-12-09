import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)
app.config["DEBUG"] = True

# Custom filter. function (defined in helpers.py)
app.jinja_env.filters["usd"] = usd

# this is how we enable sessions in web app
# ensures that we're storing session info on the server itself
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    user_cash = cash[0]["cash"]
    # SUM(shares) AS total_shares is to sum up shares number of each stock
    # группирует и суммирует акции по символу компании, тк select возвращает отдельные list of dicts.
    # where each row is a dict of different symbols, shares and we need to group them by symbol for our convenience
    stocks = db.execute(
        "SELECT symbol, price, SUM(shares) AS total_shares FROM transactions WHERE user_id = ? GROUP BY symbol",
        user_id)
    grand_total = user_cash
    for stock in stocks:
        grand_total += stock["price"] * stock["total_shares"]
    return render_template(
        "index.html", stocks=stocks, cash=user_cash, grand_total=grand_total)




@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        s = request.form.get("symbol")
        shares = request.form.get("shares")    # its datatype is text in html
        if not s:       # if blank
            return apology("must provide a symbol")
        if not shares.isdigit():        # checks if it's a digit, not a string/float; without any puctuation
            return apology("invalid shared")

        shares = int(shares)    # typecast to work with it now
        if shares < 0:  # if negative
            return apology("must provide a positive number")
        quote = lookup(s) # call lookup func
        if quote:
            symbol = quote["symbol"]
            price = quote["price"]
            # store currently logged-in user in this variable
            user_id = session["user_id"]       # a way to access the currently logged-in user's ID.
            # pass their id to db.execute to retrieve cash
            cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
            user_cash = cash[0]["cash"] # cash looks like a list with dict [{'cash': 10000}]
            total_shares_price = shares * price     # 2 stocks x price for one

            if user_cash < total_shares_price:
                return apology("you can't afford this number of shares")
            # how much cash left after we buy shares
            cash_left = user_cash - total_shares_price
            # paste two values to update cash
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash_left, user_id)
            time = datetime.datetime.now()     # get the current date
            # insert values into new table 'transactions'
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price, type, time) VALUES (?, ?, ?, ?, ?, ?)", user_id, symbol, shares, price, 'buy', time)
            flash("You bought it!")
            return redirect("/")    # go to homepage
        else:
            return apology("This stock does not exist")
    else:
        return render_template("buy.html")  # if 'get' - go to buy page


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    # don't group by here as you need to display each transaction separately
    stocks = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)
    return render_template("history.html", stocks=stocks)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # means user submitted the form
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # after user entered username and password, check if it's valid username and password combination in DB
        # Query database for username and we get list of rows with usernames
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # check that we get back one row representing the user
        # and check whether the password was correct
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # use 'session' to keep track of info about the current user
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]          # сохраняем ID текущего пользака

        # после того как зарегили пользака, redirect to homepage
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # Submit the user’s input via POST to /quote
    if request.method == "POST":
        # look up the stock symbol by calling lookup func and display the results
        sym = request.form.get("symbol")
        if not sym:     # check if there's a symbol
            return apology("must provide a symbol")
        quote = lookup(sym)
        # if smth wrong with passed symbol
        if not quote:
            return apology("This stock does not exist")
        # if a company exists
        # get access to the values of these keys and pass them as params to quoted.html
        return render_template("quoted.html", name=quote["name"], symbol=quote["symbol"], price=quote["price"])
    else:
        # display form to request a stock quote
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Submit the user’s input via POST to /register
    if request.method == "POST":    # login user -> redirect to login page
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # Check if username already exists in the database
        # select returns list of dicts
        db_username = db.execute("SELECT * FROM users WHERE username = ?", username)
        if not username:
            return apology("must provide username", 400)
        elif db_username:
            return apology("username already exists", 400)
        elif not password:
            return apology("must provide password", 400)
        elif password != confirmation:
            return apology("passwords do not match", 400)
        hashed_password = generate_password_hash(password, method='pbkdf2')     # to encrypt password for security
        # add a new user and hashed password in DB
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hashed_password)
        # log the user in
        # session["user_id"] = registered_user       # keeps the track of which user is logged in
        return redirect("/")
    else:
        #if "GET", display registration form
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    user_id = session["user_id"]
    """Sell shares of stock"""
    if request.method == "POST":
        # get user_id, shares and symbol for lookup
        sym = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        if shares < 0:
            return apology("Must provide a positive integer")
        shares_owned = db.execute("SELECT shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id, sym)[0]["shares"]
        print(shares)
        print(shares_owned)
        if shares_owned < shares:
                return apology("User does not own that many shares of the stock")
        quote = lookup(sym)
        # if not quote:
        #     return apology("Please select a stock's symbol")
        symbol, price = quote["symbol"], quote["price"]
        total_value = price * shares
        # get cash and cash left to update it in users db
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        old_cash = cash[0]["cash"]
        cash_left = old_cash + total_value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash_left, user_id)
        # add this new data to transactions table
        time = datetime.datetime.now()    # get the current date
        # - shares as we want subtract it from total shares number
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, type, time) VALUES (?, ?, ?, ?, ?, ?)", user_id, symbol, -shares, price, 'sell', time)
        flash("You sold it!")
        return redirect("/")

    else:
        #if "GET", display registration form
        # get symbols to loop through them in sell.html
        # group by тк иначе вернется несколько строк say с nflx, а так все nflx будут сгруппированы в одной
        # due to GROUP by your dropdown menu displays grouped symbols, а не символы одной компании, добавленные в разное время
        # symbols без duplicates in select dropdown menu in sell page
        symbols = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
        # symbols is a list of dicts, we'll loop through in html
        return render_template("sell.html", symbols=symbols)


@app.route("/password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == 'POST':
        user_id = session["user_id"]
        new_password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not new_password:
            return apology("must provide password")
        elif not confirmation:
            return apology("must confirm password")
        elif new_password != confirmation:
            return apology("passwords do not match")
        elif len(new_password) < 6:
            return apology("Too short. Must be at least 6 characters")
        new_hash = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", new_hash, user_id)
        return redirect("/login")
    else:
        return render_template("password.html")