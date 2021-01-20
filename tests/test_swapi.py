import requests
import pytest
from jsonschema import validate
from test_data import *


class TestStarWarsApi:

    # Test which checks what length of people's list is equal to field 'count'
    def test_check_count_of_all_people(self, return_all_people):
        data = return_all_people
        response = requests.get('https://swapi.dev/api/people/')
        people = response.json()
        assert len(data) == people['count'], "Length of array is not equal to field 'count'"

    # Test which checks that all people names are unique
    def test_unique_names(self, return_all_people):
        data = return_all_people
        names_list = []
        for i in range(len(data)):
            names_list.append(data[i]['name'])
        names_list.sort()
        for i in range(1, len(names_list)):
            assert names_list[i] != names_list[i - 1], "There is same names"

    # Test which checks there are no page with number 0 for people requests
    def test_no_number_zero_page(self):
        response = requests.get('https://swapi.dev/api/people/?page=0')
        assert response.status_code == 404

    # Parametrized test which checks there are 3 Skywalker's, 1 Vader, 2 Darth's
    @pytest.mark.parametrize('match,equal', search_names_test_data)
    def test_search_names(self, match, equal):
        response = requests.get(f"https://swapi.dev/api/people/?search={match}")
        people = response.json()
        assert people['count'] == equal

    # Test which validates that all people objects contain required schema fields
    def test_validate_people_objects(self, return_all_people, json_schema_of_people):
        for i in range(len(return_all_people)):
            assert validate(return_all_people[i], schema=json_schema_of_people) is None

    # Test which validates that search for people is case insensitive
    def test_check_search_insensitive_to_upper_case(self):
        response_base = requests.get(f"https://swapi.dev/api/people/1").json()
        name_upper_case = response_base['name'].upper()
        response_by_upper = requests.get(f"https://swapi.dev/api/people/?search={name_upper_case}").json()
        assert response_base['name'] == response_by_upper['results'][0]['name']

    # Test which validates that search for people is case insensitive
    def test_check_search_insensitive_to_lower_case(self):
        response_base = requests.get(f"https://swapi.dev/api/people/1").json()
        name_lower_case = response_base['name'].upper()
        response_by_lower = requests.get(f"https://swapi.dev/api/people/?search={name_lower_case}").json()
        assert response_base['name'] == response_by_lower['results'][0]['name']

    # Test which validates that search for people is case insensitive
    def test_check_search_insensitive_to_swap_case(self):
        response_base = requests.get(f"https://swapi.dev/api/people/1").json()
        name_swap_case = response_base['name'].swapcase()
        response_by_swap = requests.get(f"https://swapi.dev/api/people/?search={name_swap_case}").json()
        assert response_base['name'] == response_by_swap['results'][0]['name']

    # Test which check that search for any char in English alphabet or any number from 0
    # to 9 will return number of results >0 except cases of search by 6, 9 and 0.
    @pytest.mark.parametrize('query', check_search_result_test_data)
    def test_check_search_result(self, query, return_search_people_results):
        assert return_search_people_results(query)['count'] > 0
