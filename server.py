from flask import Flask
from flask import request
from flask import render_template

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import io
import json

with io.open('config_secret.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    client = Client(auth)

rest_list = []
rest_list2 = []
rest_list3 = []
user_input_list = []

app = Flask(__name__)

################ Functions for Option 1

def zip_search(zip_entry):
    params = {"lang": "en", "term": "food", "deals_filter": True}
    search_connect = client.search(zip_entry, **params)
    search_results = search_connect.businesses[0:]
    for item in search_results:
        rest_list.append(item.id)

def zip_convert():
    parsed_rest_list = str(rest_list).strip("[]").split(",")
    for item in parsed_rest_list:
        new_item = item.replace("u'", "").replace("'", "").strip()
        rest_list2.append(new_item)

def name_choice():
    for item in rest_list2:
        params2 = {"lang": "en"}
        data = client.get_business(item, **params2)
        name = data.business.name
        rest_list3.append(name)

def bar_search_1(user_choice):
    params = {"lang": "en", "term": user_choice}
    search_connect = client.search("San Francisco", **params)
    search_results = search_connect.businesses[0].id
    return search_results

def bar_deal_info(user_choice):
    search_results = bar_search_1(user_choice)
    params = {"lang": "en"}
    data = client.get_business(search_results, **params)
    deals_title = data.business.deals[0]
    return deals_title.title

def bar_rating_info(user_choice):
    search_results = bar_search_1(user_choice)
    params = {"lang": "en"}
    data = client.get_business(search_results, **params)
    rating = data.business.rating
    return rating

def bar_num_reviews(user_choice):
    search_results = bar_search_1(user_choice)
    params = {"lang": "en"}
    data = client.get_business(search_results, **params)
    num_reviews = data.business.review_count
    return num_reviews

# def bar_description():

def bar_business_address_1(user_choice):
    search_results = bar_search_1(user_choice)
    params2 = {"lang": "en"}
    data = client.get_business(search_results, **params2)
    bar_address = str(data.business.location.address).strip("[]").replace("u'", "").replace("'", "")
    return bar_address

def bar_phone(user_choice):
    search_results = bar_search_1(user_choice)
    params = {"lang": "en"}
    data = client.get_business(search_results, **params)
    phone = data.business.display_phone
    return phone

def deal_link(user_choice):
    search_results = bar_search_1(user_choice)
    params = {"lang": "en"}
    data = client.get_business(search_results, **params)
    link = data.business.deals[0]
    return link.url

################ Functions for Option 2


def bar_search_2(user_choice):
    params = {"lang": "en", "term": user_choice}
    search_connect = client.search("San Francisco", **params)
    search_results = search_connect.businesses[0].id
    return search_results

def bar_business_address_2(user_choice):
    search_results = bar_search_2(user_choice)
    params2 = {"lang": "en"}
    data = client.get_business(search_results, **params2)
    bar_address = str(data.business.location.address).strip("[]").replace("u'", "").replace("'", "")
    return bar_address

def bar_business_name(user_choice):
    search_results = bar_search_2(user_choice)
    params2 = {"lang": "en"}
    data = client.get_business(search_results, **params2)
    name = data.business.name
    return name

def is_there_deal(user_choice):
    search_results = bar_search_2(user_choice)
    params = {"lang": "en"}
    data = client.get_business(search_results, **params)
    is_deal = data.business.deals
    return is_deal

#####################################

@app.route('/')
def my_form():
    return render_template("app.html")

@app.route('/zipsearch')
def zip_question():
    zip_entry = request.args.get("zip")
    if len(zip_entry) == 5:
        zip_search(zip_entry)
        zip_convert()
        name_choice()
        response = render_template("template1.html", rest_list0=rest_list3[0], rest_list1=rest_list3[1], rest_list2=rest_list3[2], rest_list3=rest_list3[3], rest_list4=rest_list3[4], rest_list5=rest_list3[5], rest_list6=rest_list3[6], rest_list7=rest_list3[7], rest_list8=rest_list3[8], rest_list9=rest_list3[9])
    else:
        response = render_template("template7.html")
    return response

@app.route('/zipselect')
def zip_select():
    user_choice = request.args.get("select")
    if user_choice in rest_list3:
        deal_info = bar_deal_info(user_choice)
        link = deal_link(user_choice)
        rating_info = bar_rating_info(user_choice)
        review_info = bar_num_reviews(user_choice)
        address_info = bar_business_address_1(user_choice)
        phone_info = bar_phone(user_choice)
        response = render_template("template3.html", rest_list0=rest_list3[0], rest_list1=rest_list3[1], rest_list2=rest_list3[2], rest_list3=rest_list3[3], rest_list4=rest_list3[4], rest_list5=rest_list3[5], rest_list6=rest_list3[6], rest_list7=rest_list3[7], rest_list8=rest_list3[8], rest_list9=rest_list3[9], choice=user_choice, deal=deal_info, link=link, rating=rating_info, review = review_info, address=address_info, phone=phone_info)
    else:
        response = render_template("template8.html", rest_list0=rest_list3[0], rest_list1=rest_list3[1], rest_list2=rest_list3[2], rest_list3=rest_list3[3], rest_list4=rest_list3[4], rest_list5=rest_list3[5], rest_list6=rest_list3[6], rest_list7=rest_list3[7], rest_list8=rest_list3[8], rest_list9=rest_list3[9])
    return response

@app.route('/restsearch')
def rest_question():
    user_choice = request.args.get("rest")
    user_input_list.append(user_choice)
    bar_address = bar_business_address_2(user_choice)
    bar_name = bar_business_name(user_choice)
    return render_template("template2.html", name=bar_name, address=bar_address)

@app.route('/restanswer')
def rest_answer():
    user_input = request.args.get("yesno")
    user_choice = user_input_list[0]
    if user_input == "Y":
        rating_info = bar_rating_info(user_choice)
        review_info = bar_num_reviews(user_choice)
        address_info = bar_business_address_1(user_choice)
        phone_info = bar_phone(user_choice)
        deal_identifier = is_there_deal(user_choice)
        if deal_identifier == None:
            response = render_template("template4.html", choice=user_choice, rating=rating_info, review=review_info, address=address_info, phone=phone_info)
        else:
            deal_info = bar_deal_info(user_choice)
            link = deal_link(user_choice)
            response = render_template("template5.html", choice=user_choice, deal=deal_info, link=link, rating=rating_info, review=review_info, address=address_info, phone=phone_info)
    else:
        response = render_template("template6.html")
    return response

if __name__ == '__main__':
    app.run()
