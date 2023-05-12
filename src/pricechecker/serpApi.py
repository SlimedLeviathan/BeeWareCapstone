from serpapi import GoogleSearch

def search(API, item, price = None):

    try:
        return searchDict[API](item, price)
    
    except:
        raise ConnectionError()

# Done
def ebaySearch(item, price = None):
    params = {
    "engine": "ebay",
    "_nkw" : f"{item}",
    "ebay_domain": "ebay.com",
    "api_key": "7882222ae7ae04d88939b426f6170b90a4c6f8fde079a51b27b715f84aef8800"
    }

    search = GoogleSearch(params)

    try:
        results = search.get_dict()

    except:
        raise ConnectionError()
    
    resultsList = []
    # message += results['search_metadata']['ebay_url']

    for result in results['organic_results']:

        itemPrice = ebayPrices(result)

        if price == None or itemPrice == 'Price Not Found':
            makeMessage(result['title'], itemPrice, result['link'], result['thumbnail'], resultsList)

        elif itemPrice < price:
            makeMessage(result['title'], itemPrice, result['link'], result['thumbnail'], resultsList)

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

    try:
        results = search.get_dict()

    except:
        raise ConnectionError()
    
    resultsList = []
    # message += results['search_metadata']['ebay_url']

    for result in results['products']:
        
        if price == None:
            makeMessage(result['title'], result['price'], result['link'], result['thumbnails'][0], resultsList)

        elif result['price'] < price:
            makeMessage(result['title'], result['price'], result['link'], result['thumbnails'][0], resultsList)

    return resultsList

# Done
def GSSearch(item, price = None):
    params = {
    "engine": "google_shopping",
    "q" : f"{item}",
    "api_key": "7882222ae7ae04d88939b426f6170b90a4c6f8fde079a51b27b715f84aef8800"
    }

    search = GoogleSearch(params)

    try:
        results = search.get_dict()

    except:
        raise ConnectionError()
    
    resultsList = []
    # message += results['search_metadata']['ebay_url']

    for result in results['shopping_results']:

        itemPrice = result['extracted_price']
        
        if itemPrice == 0:
            itemPrice = 'Price Not Listed'

        if price == None:
            makeMessage(result['title'], itemPrice, result['link'], result['thumbnail'], resultsList)

        elif result['price'] < price and not itemPrice == 'Price Not Listed':
            makeMessage(result['title'], itemPrice, result['link'], result['thumbnail'], resultsList)

    return resultsList

# Done
def walmartSearch(item, price = None):
    params = {
    "engine": "walmart",
    "query" : f"{item}",
    "api_key": "7882222ae7ae04d88939b426f6170b90a4c6f8fde079a51b27b715f84aef8800"
    }

    search = GoogleSearch(params)

    try:
        results = search.get_dict()

    except:
        raise ConnectionError()

    resultsList = []
    # message += results['search_metadata']['ebay_url']

    for result in results['organic_results']:

        if price == None:
            makeMessage(result['title'], result['primary_offer']['offer_price'], result['product_page_url'], result['thumbnail'], resultsList)

        elif int(result['price']) < price:
            makeMessage(result['title'], result['primary_offer']['offer_price'], result['link'], result['thumbnail'], resultsList)

    return resultsList

def makeMessage(title, price, link, image, resultsList):
    
    message = ''

    message += title
    
    if type(price) == int or type(price) == float:
        message += f' ${price}'

    else:
        message += f' {price}'

    resultsList.append({'message' : message, 'link' : link, 'price' : price, 'image' : image})

def accountSearch():
    import requests

    try:
        results = requests.get(url = 'https://serpapi.com/account?api_key=7882222ae7ae04d88939b426f6170b90a4c6f8fde079a51b27b715f84aef8800').json()

    except:
        raise ConnectionError()

    return results['total_searches_left']

searchDict = {'Ebay' : ebaySearch, 'Google Shopping' : GSSearch, 'Walmart' : walmartSearch, 'Home Depot' : HDSearch}