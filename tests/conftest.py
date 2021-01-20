import pytest
import requests


# Fixture which returns list of all people
@pytest.fixture()
def return_all_people():
    number_of_page = 1
    results = []
    next_link = 'not_null'
    while next_link is not None:
        response = requests.get(f"https://swapi.dev/api/people/?page={number_of_page}")
        people = response.json()
        results += people['results']
        next_link = people['next']
        number_of_page += 1
    return results


# Fixture which returns json-schema of people object
@pytest.fixture()
def json_schema_of_people():
    schema = requests.get('https://swapi.dev/api/people/schema').json()
    return schema


# Fixture which returns search people results
@pytest.fixture()
def return_search_people_results():
    def request(query):
        response = requests.get(f"https://swapi.dev/api/people/?search={query}").json()
        return response

    return request
