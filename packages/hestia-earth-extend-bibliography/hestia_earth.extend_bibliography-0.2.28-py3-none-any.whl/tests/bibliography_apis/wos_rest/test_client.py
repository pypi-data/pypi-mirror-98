import unittest
from unittest.mock import patch
import json

from tests.utils import fixtures_path, get_citations, clean_bibliography
from hestia_earth.extend_bibliography.bibliography_apis.wos_rest.client import get_client, exec_search, create_biblio


class FakePostRequest():
    def __init__(self):
        with open(f"{fixtures_path}/wos-rest/response.json", 'r') as f:
            self.content = json.load(f)

    def json(self):
        return self.content


class TestWosRestClient(unittest.TestCase):
    def test_get_client(self):
        wos_api_key = 'wos_api_key'
        args = {'wos_api_key': wos_api_key}
        with get_client(**args) as client:
            self.assertEqual(client, wos_api_key)

    @patch('requests.post', return_value=FakePostRequest())
    def test_exec_search(self, _m):
        title = get_citations()[2]
        items = exec_search('api_key')(title)
        self.assertEqual(items[0]['title'], title)

    def test_create_biblio(self):
        with open(f"{fixtures_path}/wos-rest/bibliography.json", 'r') as f:
            expected_biblio = json.load(f)
        data = FakePostRequest().json().get('data').get('matchResponse')[0].get('matches')[0]
        title = get_citations().pop()
        (biblio, _a) = create_biblio(title, data)
        self.assertEqual(clean_bibliography(biblio), expected_biblio)


if __name__ == '__main__':
    unittest.main()
