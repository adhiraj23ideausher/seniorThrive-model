import requests
import os
from dotenv import load_dotenv
load_dotenv()

rapid_api_key=os.getenv("RAPID_API_KEY")
rapid_api_host=os.getenv('RAPID_API_HOST')
url = "https://amazon-product-data6.p.rapidapi.com/product-by-text"


headers = {
    'X-RapidAPI-Key': rapid_api_key,
    'X-RapidAPI-Host': rapid_api_host
}

def get_products(product):
    querystring = {
    "keyword": product,
    "page": "1",
    "country": "US",
    "sort_by": "feature"
    }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        res=response.json()
        return res['data'][:5]
    except Exception as e:
        print("Error:", e)



