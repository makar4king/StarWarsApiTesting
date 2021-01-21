import pytest
from jsonschema import validate
from test_data import *


class TestStarWarsApi:

    # Test which checks what length of people's list is equal to field 'count'
    def test_check_count_of_all_people(self, get_all_people, get_request_and_convert_to_json):
        data = get_all_people
        people = get_request_and_convert_to_json('https://swapi.dev/api/people/')
        assert len(data) == people['count'], "Length of array is not equal to field 'count'"

    # Test which checks that all people names are unique
    def test_unique_names(self, get_all_people):
        data = get_all_people
        names_list = []
        for i in range(len(data)):
            names_list.append(data[i]['name'])
        names_list.sort()
        for i in range(1, len(names_list)):
            assert names_list[i] != names_list[i - 1], "There is same names"

    # Test which checks there are no page with number 0 for people requests
    def test_no_number_zero_page(self, get_request):
        response = get_request('https://swapi.dev/api/people/?page=0')
        assert response.status_code == 404

    # Parametrized test which checks there are 3 Skywalker's, 1 Vader, 2 Darth's
    @pytest.mark.parametrize('match,equal', search_names_test_data)
    def test_search_names(self, match, equal, get_request_and_convert_to_json):
        people = get_request_and_convert_to_json(f"https://swapi.dev/api/people/?search={match}")
        assert people['count'] == equal

    # Test which validates that all people objects contain required schema fields
    def test_validate_people_objects(self, get_all_people, json_schema_of_people):
        for i in range(len(get_all_people)):
            assert validate(get_all_people[i], schema=json_schema_of_people) is None

    # Test which validates that search for people is case insensitive
    def test_check_search_insensitive_to_upper_case(self, get_request_and_convert_to_json):
        response_base = get_request_and_convert_to_json(f"https://swapi.dev/api/people/1")
        name_upper_case = response_base['name'].upper()
        response_by_upper = get_request_and_convert_to_json(f"https://swapi.dev/api/people/?search={name_upper_case}")
        assert response_base['name'] == response_by_upper['results'][0]['name']

    # Test which validates that search for people is case insensitive
    def test_check_search_insensitive_to_lower_case(self, get_request_and_convert_to_json):
        response_base = get_request_and_convert_to_json(f"https://swapi.dev/api/people/1")
        name_lower_case = response_base['name'].upper()
        response_by_lower = get_request_and_convert_to_json(f"https://swapi.dev/api/people/?search={name_lower_case}")
        assert response_base['name'] == response_by_lower['results'][0]['name']

    # Test which validates that search for people is case insensitive
    def test_check_search_insensitive_to_swap_case(self, get_request_and_convert_to_json):
        response_base = get_request_and_convert_to_json(f"https://swapi.dev/api/people/1")
        name_swap_case = response_base['name'].swapcase()
        response_by_swap = get_request_and_convert_to_json(f"https://swapi.dev/api/people/?search={name_swap_case}")
        assert response_base['name'] == response_by_swap['results'][0]['name']

    # Test which check that search for any char in English alphabet or any number from 0
    # to 9 will return number of results >0 except cases of search by 6, 9 and 0.
    @pytest.mark.parametrize('query', check_search_result_test_data)
    def test_check_search_result(self, query, return_search_people_results):
        assert return_search_people_results(query)['count'] > 0

    # A test that checks that the ID of the object in the list and in the url match
    def test_check_ID_in_the_list_and_in_the_url_match(self, get_all_people):
        data = get_all_people
        list_of_urls = []
        for i in range(len(data)):
            list_of_urls.append(data[i]['url'])
        for i in range(1, len(list_of_urls)):
            assert list_of_urls[i-1] == f"http://swapi.dev/api/people/{i}/", f'Error in object #{i}'
