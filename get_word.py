import requests


# Api to https://www.dicolink.com/ (100 requests per hour)
target_url = "https://api.dicolink.com"
token = None

if token == None:
    api_used = False
else:
    api_used = True

# Get random word
def get_random_word():
    parameters = {
        "avecdef": True,
        "verbeconjugue": False,
        "api_key": token
    }

    random_word_responce = requests.get(
        f"{target_url}/v1/mots/motauhasard", params=parameters)

    data_word = random_word_responce.json()[0]
    return data_word["mot"]


# Get random word definition
def get_random_word_def(word):
    parameters = {
        "limite": 600,
        "api_key": token
    }

    random_word_def_responce = requests.get(
        f"{target_url}/v1/mot/{word}/definitions", params=parameters)

    data_def = random_word_def_responce.json()[0]
    return data_def["definition"]
