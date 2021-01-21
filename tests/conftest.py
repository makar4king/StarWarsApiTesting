import pytest
import requests


# A fixture that returns a response to a GET request
@pytest.fixture()
def get_request():
    def request(url):
        response = requests.get(url)
        return response

    return request


# A fixture that returns a response to a GET request, but converted in JSON format
@pytest.fixture()
def get_request_and_convert_to_json():
    def request(url):
        response = requests.get(url).json()
        return response

    return request


# Fixture which returns list of all people
@pytest.fixture()
def get_all_people(get_request_and_convert_to_json):
    results = []
    next_link = 'https://swapi.dev/api/people/?page=1'
    while next_link is not None:
        people = get_request_and_convert_to_json(next_link)
        results += people['results']
        next_link = people['next']
    return results


# Fixture which returns json-schema of people object
@pytest.fixture()
def json_schema_of_people(get_request_and_convert_to_json):
    schema = get_request_and_convert_to_json('https://swapi.dev/api/people/schema')
    return schema


# Fixture which returns search people results
@pytest.fixture()
def return_search_people_results(get_request_and_convert_to_json):
    def request(query):
        response = get_request_and_convert_to_json(f"https://swapi.dev/api/people/?search={query}")
        return response

    return request
