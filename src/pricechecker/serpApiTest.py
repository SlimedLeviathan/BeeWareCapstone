from serpapi import GoogleSearch

def search(item, price = None):
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

        if price == None:
            makeMessage(result, resultsList)

        else:
            try:
                if result["price"]["from"]["extracted"] < price:
                    makeMessage(result, resultsList)

            except:
                try:
                    if result["price"]["extracted"] < price:
                        makeMessage(result, resultsList)

                except:
                    makeMessage(result, resultsList)

    return resultsList

def makeMessage(result, resultsList):
    
    message = ''

    try:
        message += f'\n{result["title"]} '
        # message += result['condition']

        try:
            message += f'${result["price"]["from"]["extracted"]} to ${result["price"]["to"]["extracted"]}'
            resultsList.append({'message' : message, 'link' : result['link'], 'price' : result['price']['to']['extracted']})

        except:
            message += f'${result["price"]["extracted"]}'
            resultsList.append({'message' : message, 'link' : result['link'], 'price' : result['price']['extracted']})

    except:
        message += "Price Not Found"
        resultsList.append({'message' : message, 'link' : result['link'], 'price' : 'Price Not Found'})