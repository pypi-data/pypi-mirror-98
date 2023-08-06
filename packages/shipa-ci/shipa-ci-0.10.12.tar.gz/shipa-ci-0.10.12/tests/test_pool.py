import unittest

from shipa.client.client import ShipaClient, CONST_TEST_SERVER, CONST_TEST_TOKEN
from shipa.client.http import MockResponse, MockClient


class ShipaFrameworkTestCase(unittest.TestCase):

    def test_framework_create(self):
        try:
            response = MockResponse(code=201)
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.framework_add(framework="test", ingress="istio")

        except Exception as e:
            assert e is None, str(e)

    def test_framework_create_with_teams(self):
        try:
            response = MockResponse(code=201)
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.framework_add(framework="test", ingress="istio", teams=("admin", "gaga"))

        except Exception as e:
            assert e is None, str(e)

    def test_framework_create_failed(self):
        response = MockResponse(code=400, text='failed to create a framework')
        http = MockClient(response=response)
        client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)

        with self.assertRaises(Exception):
            client.framework_add(framework="test", ingress="istio")

    def test_framework_remove(self):
        try:
            response = MockResponse(code=200)
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.framework_remove(framework="test")

        except Exception as e:
            assert e is None, str(e)

    def test_framework_remove_failed(self):
        response = MockResponse(code=400, text='failed to remove a framework')
        http = MockClient(response=response)
        client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)

        with self.assertRaises(Exception):
            client.framework_remove(framework="test")

    def test_framework_update(self):
        try:
            response = MockResponse(code=200)
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.framework_update(framework="test")

        except Exception as e:
            assert e is None, str(e)

    def test_framework_update_failed(self):
        response = MockResponse(code=400, text='failed to update a framework')
        http = MockClient(response=response)
        client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)

        with self.assertRaises(Exception):
            client.framework_update(framework="test")
