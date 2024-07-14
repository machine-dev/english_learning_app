import requests

def fetch_definition(word):
    response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    if response.status_code == 200:
        data = response.json()
        definition = data[0]['meanings'][0]['definitions'][0]['definition']
        return definition
    return None
