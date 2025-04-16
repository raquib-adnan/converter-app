import requests
from datetime import datetime
import json

def convert_currency(from_currency, to_currency, amount):
    """
    Convert currency using Frankfurter API
    Returns tuple of (converted_amount, last_updated)
    """
    try:
        url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"API Error: Status code {response.status_code}")
            return None, None
            
        data = response.json()
        
        # Debug print
        print(f"API Response: {json.dumps(data, indent=2)}")
        
        if 'rates' in data and to_currency in data['rates']:
            return data['rates'][to_currency], data['date']
        else:
            print(f"API Error: Invalid response format")
            return None, None
            
    except requests.RequestException as e:
        print(f"Network Error: {str(e)}")
        return None, None
    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {str(e)}")
        return None, None
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        return None, None

def get_currency_list():
    """
    Get list of available currencies using Frankfurter API
    """
    try:
        url = "https://api.frankfurter.app/currencies"
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"API Error: Status code {response.status_code}")
            return []
            
        data = response.json()
        
        # Debug print
        print(f"Currencies API Response: {json.dumps(data, indent=2)}")
        
        # Format the currency list
        return [(code, f"{code} - {name}") for code, name in data.items()]
            
    except requests.RequestException as e:
        print(f"Network Error: {str(e)}")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {str(e)}")
        return []
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        return [] 