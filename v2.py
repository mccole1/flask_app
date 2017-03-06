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

def zip_search():
    user_input = raw_input("Please enter your zip code: ")
    params = {"lang": "en", "term": "food", "deals_filter": True}
    search_connect = client.search(user_input, **params)
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
        print name

def deal_info_by_zip():
    user_choice = raw_input("Here is a list of bars and restaurants that are running deals in your neighborhood. Which one would you like to see?: ")
    if user_choice in rest_list3:
        print "Here is some info: "
        #Access deal information here
    else:
        "Please check your spelling and try again."

def bar_search():
    user_input = raw_input("Type name of restaurant: ")
    params = {"lang": "en", "term": user_input}
    search_connect = client.search('San Francisco', **params)
    search_results = search_connect.businesses[0].id
    return search_results

def bar_business(search_results):
    search_results = bar_search()
    params2 = {"lang": "en"}
    data = client.get_business(search_results, **params2)
    
    bar_address = str(data.business.location.address).strip("[]").replace("u'", "").replace("'", "")
    name = data.business.name
    user_input2 = raw_input("Did you mean %s at %s? (Y/N): " % (name, bar_address))
    return user_input2

def main():
    while(True):
        search_choice = raw_input("Please select from the following options:\n 1) Search by zip code\n 2) Search by restaurant name\n 3) Exit\n Please enter 1, 2, or 3: ")
        if search_choice == "1":
            zip_search()
            zip_convert()
            name_choice()
            deal_info_by_zip()
        elif search_choice == "2":
            while(True):
                correct_bar = bar_business(" ")
                if correct_bar == "Y":
                    print "Here is some info:"
                    #Access deal information here
                if correct_bar == "N":
                    main()
                else:
                    print "Please enter 'Y' or 'N'."
                    bar_business(" ")
                    #go back to user_input2 raw input
        elif search_choice == "3":
            exit()
        else:
            print "Please enter 1, 2, or 3."
            main()

if __name__ == '__main__':
    main()










