import requests


# Api to https://www.dicolink.com/
target_url = "https://api.dicolink.com"
token = "_0QSsKMBBuylQL-wFwdxNsuk5ozVU7tm"


# Get random word
parameters_word = {
    "avecdef": True,
    "verbeconjugue": False,
    "api_key": token
}


def get_random_word():
    random_word_responce = requests.get(
        f"{target_url}/v1/mots/motauhasard", params=parameters_word)

    data_word = random_word_responce.json()[0]
    return data_word["mot"]


# Get random word definition
parameters_def = {
    "limite": 600,
    "api_key": token
}


def get_random_word_def(word):
    random_word_def_responce = requests.get(
        f"{target_url}/v1/mot/{word}/definitions", params=parameters_def)

    data_def = random_word_def_responce.json()[0]
    return data_def["definition"]
