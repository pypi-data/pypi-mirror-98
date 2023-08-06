import unittest
from unittest.mock import patch
import json

from tests.utils import fixtures_path, get_citations, clean_bibliography
from hestia_earth.extend_bibliography.bibliography_apis.mendeley_api.client import get_client, exec_search, \
    create_biblio


class FakeGetRequest():
    def __init__(self):
        with open(f"{fixtures_path}/mendeley-api/response.json", 'r') as f:
            self.content = json.load(f)

    def json(self):
        return self.content


class TestMendeleyApiClient(unittest.TestCase):
    @patch('requests.get', return_value=FakeGetRequest())
    def test_exec_search(self, _m):
        title = get_citations()[0]
        with get_client(api_key='api_key') as client:
            items = exec_search(client, 'title')(title)
        self.assertEqual(items[0]['title'], title)

    def test_create_biblio(self):
        with open(f"{fixtures_path}/mendeley-api/bibliography.json", 'r') as f:
            expected_biblio = json.load(f)
        with open(f"{fixtures_path}/mendeley-api/actors.json", 'r') as f:
            expected_actors = json.load(f)
        data = FakeGetRequest().json().get('results')[0]
        title = get_citations()[0]
        (biblio, actors) = create_biblio(data, 'title', title)
        self.assertEqual(clean_bibliography(biblio), expected_biblio)
        self.assertEqual(actors, expected_actors)


if __name__ == '__main__':
    unittest.main()
