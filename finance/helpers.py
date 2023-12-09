import csv
import datetime
import pytz
import requests
import subprocess
import urllib
import uuid

from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters. replaces special characters in the error message with their encoded equivalents
        It ensures that the error message can be safely displayed on a web page without causing issues
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    # inserts apology meme pic
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    # requires to login before accessing a given route
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    # This is a built-in decorator in Python that helps to preserve the metadata of the decorated function f.
    @wraps(f)
    def decorated_function(*args, **kwargs):
    # This is the new function that will replace f. It takes the same arguments as f.
        if session.get("user_id") is None:
            return redirect("/login")
        # If the user is logged in, the original function f is called with its original arguments, and its result is returned.
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    # takes stock symbol and returns a stock quote
    # uses an API to get a current stock quote
    """Look up quote for symbol."""

    # Prepare API request
    symbol = symbol.upper() # NFLX for Netflix
    end = datetime.datetime.now(pytz.timezone("US/Eastern"))
    start = end - datetime.timedelta(days=7)

    # Yahoo Finance API
    url = (
        f"https://query1.finance.yahoo.com/v7/finance/download/{urllib.parse.quote_plus(symbol)}"
        f"?period1={int(start.timestamp())}"
        f"&period2={int(end.timestamp())}"
        f"&interval=1d&events=history&includeAdjustedClose=true"
    )

    # Query API
    try:
        response = requests.get(url, cookies={"session": str(uuid.uuid4())}, headers={"User-Agent": "python-requests", "Accept": "*/*"})
        response.raise_for_status()

        # CSV header: Date,Open,High,Low,Close,Adj Close,Volume
        quotes = list(csv.DictReader(response.content.decode("utf-8").splitlines()))
        quotes.reverse()
        price = round(float(quotes[0]["Adj Close"]), 2)
        return {
            "name": symbol,
            "price": price,
            "symbol": symbol
        }
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"