from serpapi import GoogleSearch

def search(API, item, price = None):

    return searchDict[API](item, price)

# Done
def ebaySearch(item, price = None):
    params = {
    "engine": "ebay",
    "_nkw" : f"{item}",
    "ebay_domain": "ebay.com",
    "api_key": "7882222ae7ae04d88939b426f6170b90a4c6f8fde079a51b27b715f84aef8800"
    }

    search = GoogleSearch(params)
    results = search.get_dict()


    resultsList = []
    # message += results['search_metadata']['ebay_url']

    for result in results['organic_results']:

        itemPrice = ebayPrices(result)

        if price == None or itemPrice == 'Price Not Found':
            makeMessage(result['title'], itemPrice, result['link'], resultsList)

        elif itemPrice < price:
            makeMessage(result['title'], itemPrice, result['link'], resultsList)

    return resultsList

def ebayPrices(result):

    try:
        try:
            return result["price"]["to"]["extracted"]

        except:
            return result["price"]["extracted"]

    except:
        return "Price Not Found"

# In-Progress
def HDSearch(item, price = None):
    params = {
    "engine": "home_depot",
    "q" : f"{item}",
    "api_key": "7882222ae7ae04d88939b426f6170b90a4c6f8fde079a51b27b715f84aef8800"
    }

    search = GoogleSearch(params)
    results = search.get_dict()


    resultsList = []
    # message += results['search_metadata']['ebay_url']

    for result in results['products']:


        makeMessage(result['title'], result['price'], result['link'], resultsList)

    return resultsList

# Done
def GSSearch(item, price = None):
    params = {
    "engine": "google_shopping",
    "q" : f"{item}",
    "api_key": "7882222ae7ae04d88939b426f6170b90a4c6f8fde079a51b27b715f84aef8800"
    }

    search = GoogleSearch(params)
    results = search.get_dict()


    resultsList = []
    # message += results['search_metadata']['ebay_url']

    for result in results['inline_shopping_results']:

        itemPrice = result['extracted_price']
        
        if itemPrice == 0:
            itemPrice = 'Price Not Listed'

        makeMessage(result['title'], itemPrice, result['link'], resultsList)

    return resultsList

# Done
def walmartSearch(item, price = None):
    params = {
    "engine": "walmart",
    "query" : f"{item}",
    "api_key": "7882222ae7ae04d88939b426f6170b90a4c6f8fde079a51b27b715f84aef8800"
    }

    search = GoogleSearch(params)
    results = search.get_dict()


    resultsList = []
    # message += results['search_metadata']['ebay_url']

    for result in results['organic_results']:

        makeMessage(result['title'], result['primary_offer']['offer_price'], result['product_page_url'], resultsList)

    return resultsList

def makeMessage(title, price, link, resultsList):
    
    message = ''

    message += title
    
    if type(price) == int or type(price) == float:
        message += f' ${price}'

    else:
        message += f' {price}'

    resultsList.append({'message' : message, 'link' : link, 'price' : price})

def accountSearch():
    import requests

    results = requests.get(url = 'https://serpapi.com/account?api_key=7882222ae7ae04d88939b426f6170b90a4c6f8fde079a51b27b715f84aef8800').json()

    return results['total_searches_left']

searchDict = {'Ebay' : ebaySearch, 'Google Shopping' : GSSearch, 'Walmart' : walmartSearch, 'Home Depot' : HDSearch}