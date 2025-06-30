import requests
import time

CACHE = {
    "senticrypt": None,
    "timestamp": 0
}
CACHE_DURATION = 60 * 60 * 2 # Cache for 2 hours

def get_senticrypt_data():
    now = time.time()
    if CACHE["senticrypt"] and (now - CACHE["timestamp"]) < CACHE_DURATION:
        return CACHE["senticrypt"]

    try:
        response = requests.get("https://api.senticrypt.com/v2/all.json")
        response.raise_for_status()
        data = response.json()
        CACHE["senticrypt"] = data
        CACHE["timestamp"] = now
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching SentiCrypt data: {e}")
        return None