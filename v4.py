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
    user_choice = raw_input("Here is a list of some deals in your neighborhood. Which one would you like to see?: ")
    user_input_list.append(user_choice)
    if user_choice in rest_list3:
        print "Here is some info on %s: " % (user_choice)
        deal_title = bar_deal_info()
        print deal_title.title
        bar_info()
    else:
        "That restaurant is not on the list. Please check your spelling and try again."
        #return to raw_input

def bar_search():
    user_input = user_input_list[0]
    params = {"lang": "en", "term": user_input}
    search_connect = client.search("San Francisco", **params)
    search_results = search_connect.businesses[0].id
    return search_results

def bar_business_address():
    search_results = bar_search()
    params2 = {"lang": "en"}
    data = client.get_business(search_results, **params2)
    bar_address = str(data.business.location.address).strip("[]").replace("u'", "").replace("'", "")
    return bar_address

def bar_business_name():
    search_results = bar_search()
    params2 = {"lang": "en"}
    data = client.get_business(search_results, **params2)
    name = data.business.name
    return name

def bar_rating_info():
    search_results = bar_search()
    params = {"lang": "en"}
    data = client.get_business(search_results, **params)
    rating = data.business.rating
    return rating

def bar_phone():
    search_results = bar_search()
    params = {"lang": "en"}
    data = client.get_business(search_results, **params)
    phone = data.business.display_phone
    return phone

def bar_num_reviews():
    search_results = bar_search()
    params = {"lang": "en"}
    data = client.get_business(search_results, **params)
    num_reviews = data.business.review_count
    return num_reviews

def is_there_deal():
    search_results = bar_search()
    params = {"lang": "en"}
    data = client.get_business(search_results, **params)
    is_deal = data.business.deals
    return is_deal

def bar_deal_info():
    search_results = bar_search()
    params = {"lang": "en"}
    data = client.get_business(search_results, **params)
    deals_title = data.business.deals[0]
    return deals_title

def bar_info():
    print "\n"
    print "Rating: " , bar_rating_info()
    print "Phone Number: ", bar_phone()
    print "Number of Reviews: ", bar_num_reviews()
    print "\n"

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
                user_input = raw_input("Type name of restaurant: ")
                user_input_list.append(user_input)
                bar_address = bar_business_address()
                bar_name = bar_business_name()
                user_input2 = raw_input("Did you mean %s at %s? (Y/N): " % (bar_name, bar_address))
                if user_input2 == "Y":
                    deal_identifier = is_there_deal()
                    if deal_identifier == None:
                        print "There is currently no deal at %s. But here is some additional information: " % (bar_name)
                        del user_input_list[:]                        
                    else:
                        deal_title = bar_deal_info()
                        print deal_title.title
                        print "\n"
                        print "Here is some additional information about %s: " % (bar_name)
                        bar_info()
                        del user_input_list[:]
                    main()
                if user_input2 == "N":
                    print "..."
                else:
                    print "Please enter 'Y' or 'N'."
                    #go back to user_input2 raw input
        elif search_choice == "3":
            exit()
        else:
            print "Please enter 1, 2, or 3."
            main()

if __name__ == '__main__':
    main()