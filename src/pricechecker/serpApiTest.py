from serpapi import GoogleSearch

def search(API, item, price = None):

    return searchDict[API](item, price)

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
            return f'${result["price"]["from"]["extracted"]} to ${result["price"]["to"]["extracted"]}'

        except:
            return f'${result["price"]["extracted"]}'

    except:
        return "Price Not Found"

def HDSearch(item, price = None):
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

def GSSearch(item, price = None):
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

def GPSearch(item, price = None):
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

        itemPrice = result['primary_offer']['offer_price']

        if price == None or itemPrice == 'Price Not Found':
            makeMessage(result['title'], itemPrice, result['product_page_url'], resultsList)

        elif itemPrice < price:
            makeMessage(result['title'], itemPrice, result['product_page_url'], resultsList)

    return resultsList

def makeMessage(title, price, link, resultsList):
    
    message = ''

    message += title
        
    message += f' {price}'

    resultsList.append({'message' : message, 'link' : link, 'price' : price})

searchDict = {'Ebay' : ebaySearch, 'Google Shopping' : GSSearch, 'Google Products' : GPSearch, 'Walmart' : walmartSearch, 'Home Depot' : HDSearch}