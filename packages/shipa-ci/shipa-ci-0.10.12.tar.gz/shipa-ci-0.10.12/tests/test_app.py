import unittest

from shipa.client.client import ShipaClient, CONST_TEST_TOKEN, CONST_TEST_SERVER
from shipa.client.http import MockResponse, MockClient
from shipa.client.types import AppExistsError


class ShipaAppTestCase(unittest.TestCase):

    def test_app_create_app_exists_failed(self):
        response = MockResponse(code=409, text='{"status": "failed"}')
        http = MockClient(response=response)
        client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)

        with self.assertRaises(AppExistsError):
            client.app_create(appname='test-app', framework="test", team="admin", platform="python")

    def test_app_create(self):
        try:
            response = MockResponse(code=201, text='{"status": "success", "repository_url": "repository_url"}')
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.app_create(appname='test-app', framework="test", team="admin", platform="python")

        except Exception as e:
            assert e is None, str(e)

    def test_app_create_with_deps(self):
        try:
            response = MockResponse(code=201, text='{"status": "success", "repository_url": "repository_url"}')
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.app_create(appname='test-app', framework="test", team="admin", platform="python",
                              dependency_files=('config.yaml', 'data.bin'))

        except Exception as e:
            assert e is None, str(e)

    def test_app_create_failed_with_error_code(self):
        response = MockResponse(code=400, text='{"status": "success", "repository_url": "repository_url"}')
        http = MockClient(response=response)
        client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)

        with self.assertRaises(Exception):
            client.app_create(appname='test-app', framework="test", team="admin", platform="python")

    def test_app_create_failed_with_error_status(self):
        response = MockResponse(code=201, text='{"status": "failed", "repository_url": "repository_url"}')
        http = MockClient(response=response)
        client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)

        with self.assertRaises(Exception):
            client.app_create(appname='test-app', framework="test", team="admin", platform="python")

    def test_app_remove(self):
        try:
            response = MockResponse(code=200, text='{"Message": "removed a shipa app"}')
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.app_remove(appname='test-app')

        except Exception as e:
            assert e is None, str(e)

    def test_app_remove_failed(self):
        response = MockResponse(code=400, text='{"Message": "failed to remove a shipa app"}')
        http = MockClient(response=response)
        client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)

        with self.assertRaises(Exception):
            client.app_remove(appname='test-app')

    def test_app_deploy(self):
        try:
            response = MockResponse(code=200, text="deployed a app\n OK\n")
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.app_deploy(appname='test-app', image="test", port="UDP/1111")

        except Exception as e:
            assert e is None, str(e)

    def test_app_deploy_failed(self):
        response = MockResponse(code=200, text="deployed a app\n FAIL\n")
        http = MockClient(response=response)
        client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)

        with self.assertRaises(Exception):
            client.app_deploy(appname='test-app')

    def test_app_deploy_failed_without_response_text(self):
        response = MockResponse(code=200)
        http = MockClient(response=response)
        client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)

        with self.assertRaises(Exception):
            client.app_deploy(appname='test-app')

    def test_app_move(self):
        try:
            response = MockResponse(code=200, text="moved a app\n OK\n")
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.app_move(appname='test-app', framework='test-framework')

        except Exception as e:
            assert e is None, str(e)

    def test_app_move_failed(self):
        response = MockResponse(code=200, text="moved a app\n FAIL\n")
        http = MockClient(response=response)
        client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)

        with self.assertRaises(Exception):
            client.app_move(appname='test-app', framework='test-framework')

    def test_app_move_failed_without_response_text(self):
        response = MockResponse(code=200)
        http = MockClient(response=response)
        client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)

        with self.assertRaises(Exception):
            client.app_move(appname='test-app', framework='test-framework')
