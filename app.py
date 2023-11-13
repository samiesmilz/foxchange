from flask import Flask, flash, request, render_template, jsonify, session
import requests

app = Flask("__name__", static_folder='static')
app.config["SECRET_KEY"] = "mk7638"
BASE_URL = "http://api.exchangerate.host/"
API_KEY = "5125409f04b854153066e6ee9a41f7c8"


#  Home page route
@app.route("/")
def homepage():

    currencies = session.get("currencies", get_currency_list())
    quotes = session.get("quotes", get_live_rates())

    return render_template("index.html", currencies=currencies, quotes=quotes)


@app.route("/convert", methods=["POST"])
def post_data():

    # Access form data using request form.
    amount_str = request.form.get("amount", "1")
    from_currency = request.form.get("currency-from")
    to_currency = request.form.get("currency-to")
    currencies = session.get("currencies", get_currency_list())

    try:
        amount = int(amount_str)
    except ValueError as e:
        flash("Please enter a valid amount!")
        return render_template("index.html", currencies=currencies, quotes=session.get("quotes", get_live_rates()))

    if from_currency == to_currency:
        flash("Please select a different target currency to convert to!")

    if not from_currency:
        flash("Please enter a valid from currency code!")
    elif not to_currency:
        flash("Please a valid - to currency code!")

    if from_currency not in currencies.keys():
        flash("Invalid - from currency code.")
    elif to_currency not in currencies.keys():
        flash("Invalid - currency to code!")

    #  Prepare form data for submitting to the api
    params = {'from': from_currency, 'to': to_currency,
              'amount': amount, "access_key": API_KEY}
    endpoint = f"{BASE_URL}/convert"
    response = make_api_request(endpoint, params)
    query = response.get("query")
    quotes = get_live_rates(from_currency)

    return render_template("index.html", response=response, currencies=currencies, query=query, quotes=quotes)


@app.route("/list")
def get_list():
    """ Get a list of avalible currencies from the API """

    endpoint = f"{BASE_URL}/list"
    params = {"access_key": API_KEY}
    response = make_api_request(endpoint, params)

    return response.get("currencies")


@app.route("/live")
def get_live_rates(code="USD"):

    source = code
    api_url = f"{BASE_URL}/live"
    params = {"access_key": API_KEY, "source": source}

    response = make_api_request(api_url, params)
    session["quotes"] = response.get("quotes")
    return response.get("quotes")


def get_currency_list():
    """ Get a list of available currencies from the api """
    endpoint = f"{BASE_URL}/list"
    params = {"access_key": API_KEY}

    response = make_api_request(endpoint, params)
    session["currencies"] = response.get("currencies")
    return response.get("currencies")


# Handle potential request errors once and for all.

def make_api_request(api_url, params):
    """ Handle errors and exceptions for api requests."""
    try:
        response = requests.get(api_url, params=params)
        # If the request was successful, return the JSON response
        return response.json()

    except requests.exceptions.RequestException as e:
        # Handle exceptions like connection error, timeout, HTTP error
        return {'error': f'Error making API request: {e}'}
