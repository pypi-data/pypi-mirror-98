import unittest

from shipa.client.client import CONST_TEST_TOKEN, CONST_TEST_SERVER, ShipaClient
from shipa.client.http import MockResponse, MockClient


class ShipaClusterTestCase(unittest.TestCase):

    def test_cluster_create(self):
        try:
            response = MockResponse(code=201)
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.cluster_add('test', frameworks=tuple("test"))

        except Exception as e:
            assert e is None, str(e)

    def test_cluster_create_with_ingress_options(self):
        try:
            response = MockResponse(code=201)
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)

            client.cluster_add('test', frameworks=tuple("test"), ingress_ip=("istio:0.0.0.0", "traefik:1.1.1.1"),
                               ingress_http_port=("istio:8080", "traefik:8081"),
                               ingress_https_port=("istio:443", "traefik:444"),
                               ingress_protected_port=("istio:9001", "traefik:9002"),
                               ingress_service=("istio:ClusterIP", "traefik:LoadBalancer"),
                               install_cert_manager=True)

        except Exception as e:
            assert e is None, str(e)

    def test_cluster_create_failed(self):
        response = MockResponse(code=400, text='failed to create a cluster')
        http = MockClient(response=response)
        client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)

        with self.assertRaises(Exception):
            client.cluster_add('test', frameworks=tuple("test"))
