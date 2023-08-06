import json
import click
import requests

from schematics.exceptions import ValidationError, DataError
from shipa.client.types import (
    AddNodeRequest, UpdateFrameworkRequest, AddFrameworkRequest, AddAppRequest, DeployAppRequest, MoveAppRequest, RemoveFrameworkRequest, AddClusterRequest,
    EnvSetRequest, EnvUnsetRequest, AppExistsError
)
from shipa.commands.constant import KUBERNETES_PROVISIONER
from shipa.utils import RepositoryFolder, parse_ingress_config, parse_port, parse_step_interval

CONST_TEST_TOKEN = "test-token"
CONST_TEST_SERVER = "test-server"


class ShipaClient(object):

    def __init__(self, server, client, email=None, password=None, token=None, verbose=False):
        self.server = server
        if not server.startswith('http'):
            self.urlbase = 'http://{0}'.format(server)
        else:
            self.urlbase = server

        self.email = email
        self.password = password
        self.token = token
        self.verbose = verbose
        self.http = client

        if token is not None:
            self.headers = {"Authorization": "bearer " + self.token}
            self.json_headers = {"Authorization": "bearer " + self.token, 'Content-Type': 'application/json',
                                 'Accept': 'application/json'}

    def print_response(self, response):
        if self.verbose:
            print(response.text)
            print(response.status_code)

    def auth(self, client=None):
        if self.token is not None:
            return

        if client is not None:
            self.http = client

        if self.email is None or self.password is None:
            raise click.ClickException('Please, provide email and password')

        url = '{0}/users/{1}/tokens'.format(self.urlbase, self.email)
        params = {'password': self.password}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        try:
            r = self.http.post(url, params=params, headers=headers)
            self.print_response(r)

            if r.status_code != 200:
                raise click.ClickException('Invalid token or user/password ({0})'.format(r.text.strip("\n")))

            self.token = r.json()['token']
            self.headers = {"Authorization": "bearer " + self.token}
            self.json_headers = {"Authorization": "bearer " + self.token, 'Content-Type': 'application/json',
                                 'Accept': 'application/json'}

        except (requests.ConnectionError, IOError) as e:
            raise click.ClickException(str(e))

    def app_deploy(self, appname, image=None, directory='.', port=None, registry_secret=None, registry_user=None, steps=1,
                   step_interval=None, step_weight=None):
        files = None
        try:
            url = '{0}/apps/{1}/deploy'.format(self.urlbase, appname)

            if self.server is not CONST_TEST_SERVER:
                folder = RepositoryFolder(directory, verbose=self.verbose)
                file = folder.create_tarfile()
                files = {'file': file}



            protocol = None
            if port is not None:
                protocol, port = parse_port(port)
            

            request = DeployAppRequest({'image': image, 'port_number': port, 'port_protocol': protocol, 'steps': steps,
                                        'step_interval': parse_step_interval(step_interval), 'step_weight': step_weight})
            request.registry_secret = registry_secret
            request.registry_user = registry_user
            request.validate()

            r = self.http.post(url, files=files, headers=self.headers, data=request.to_primitive())
            self.print_response(r)
            if r.text is None:
                raise click.ClickException(r.text)

            ok = any(line.strip() == "OK" for line in r.text.split('\n'))

            if ok is False:
                raise click.ClickException(r.text)

        except (requests.ConnectionError, ValidationError, DataError) as e:
            raise click.ClickException(str(e))

    def app_create(self, appname, team, framework, platform=None, description=None, dependency_files=tuple(), tags=tuple(),
                   plan=None):
        try:
            url = '{0}/apps'.format(self.urlbase)

            if len(dependency_files) == 0:
                request = AddAppRequest({'name': appname, 'platform': platform, 'plan': plan, 'teamOwner': team,
                                         'description': description, 'pool': framework, 'tags': tags})
            else:
                request = AddAppRequest({'name': appname, 'platform': platform, 'plan': plan, 'teamOwner': team,
                                         'description': description, 'pool': framework, 'dependency_files': dependency_files,
                                         'tags': tags})
                
                
            request.validate()

            r = self.http.post(url, headers=self.json_headers, data=json.dumps(request.to_primitive()))
            self.print_response(r)

            if r.status_code == 409:
                raise AppExistsError('Could not create {0} already exists'.format(appname))

            if r.status_code != 201:
                raise click.ClickException(r.text)

            out = json.loads(r.text)
            if out['status'] != 'success':
                raise click.ClickException(out['status'])

            print('App {0} has been created!'.format(appname))
            print('Use app-info to check the status of the app and its units')
            if out.get("ip", None) is not None:
                print('Address of your app {0} is {1}'.format(appname, out['ip']))

        except (requests.ConnectionError, ValidationError, DataError) as e:
            raise click.ClickException(str(e))

    def app_remove(self, appname):
        try:
            url = '{0}/apps/{1}'.format(self.urlbase, appname)

            r = self.http.delete(url, headers=self.headers)
            self.print_response(r)
            if r.status_code != 200:
                raise click.ClickException(r.text)

            responses = r.text.split('\n')
            for response in responses:
                if response.find("Message") < 0:
                    continue
                out = json.loads(response)
                print(out['Message'].replace('\n', ''))

        except requests.ConnectionError as e:
            raise click.ClickException(str(e))
        except AttributeError:
            print('Done removing application.')

    def autoscale_check(self):
        try:
            print('running autoscale checks')
            url = '{0}/node/autoscale/run'.format(self.urlbase)

            r = self.http.post(url, headers=self.headers)
            self.print_response(r)
            if r.text is None:
                raise click.ClickException(r.text)

            if "Node Autoscaler available only" in r.text:
                raise click.ClickException(r.text)

            responses = r.text.split('\n')
            for response in responses:
                if response.find("Message") < 0:
                    continue
                out = json.loads(response)
                print(out['Message'].replace('\n', ''))

        except requests.ConnectionError as e:
            raise click.ClickException(str(e))

    def app_move(self, appname, framework):
        url = '{0}/apps/{1}/move'.format(self.urlbase, appname)

        try:
            request = MoveAppRequest({'pool': framework})
            request.validate()

            r = self.http.post(url, headers=self.headers, data=request.to_primitive())
            self.print_response(r)
            if r.text is None:
                raise click.ClickException(r.text)

            ok = any(line.strip() == "OK" for line in r.text.split('\n'))
            if ok is False:
                raise click.ClickException(r.text.replace('\n\n', ''))

        except (requests.ConnectionError, ValidationError, DataError) as e:
            raise click.ClickException(str(e))

    def framework_add(self, framework, ingress, default=False, public=False, teams=tuple(), accept_drivers=tuple(), app_quota_limit=None,
                 provisioner=None, plan=None, kubernetes_namespace=None):

        try:
            url = '{0}/pools'.format(self.urlbase)

            request = AddFrameworkRequest({'name': framework, 'router': ingress, 'public': public, 'default': default,
                                      'teams': teams, 'provisioner': provisioner, 'plan': plan, 'accept_drivers': accept_drivers,
                                      'kubernetes_namespace': kubernetes_namespace, 'app_quota_limit': app_quota_limit})
            request.validate()

            r = self.http.post(url, headers=self.headers, data=request.to_primitive())
            self.print_response(r)
            if r.status_code != 201:
                raise click.ClickException(r.text)

        except (requests.ConnectionError, ValidationError, DataError) as e:
            raise click.ClickException(str(e))

    def framework_remove(self, framework):

        try:
            url = '{0}/pools/{1}'.format(self.urlbase, framework)

            r = self.http.delete(url, headers=self.headers)
            self.print_response(r)
            if r.status_code != 200:
                raise click.ClickException(r.text)

        except requests.ConnectionError as e:
            raise click.ClickException(str(e))

    def framework_update(self, framework, default=False, public=False, accept_drivers=tuple(), app_quota_limit=None, plan=None):
        try:
            url = '{0}/pools/{1}'.format(self.urlbase, framework)
            request = UpdateFrameworkRequest({'public': public, 'default': default, 'plan': plan,
                                         'app_quota_limit': app_quota_limit, 'accept_drivers': accept_drivers})
            request.validate()

            r = self.http.put(url, headers=self.headers, data=request.to_primitive())
            self.print_response(r)
            if r.status_code != 200:
                raise click.ClickException(r.text)

        except (requests.ConnectionError, ValidationError, DataError) as e:
            raise click.ClickException(str(e))

    def file_read(self, path=None):
        try:
            if path is not None:
                with open(path, "r") as f:
                    return f.read()
            return None
        except IOError as e:
            raise click.ClickException(e)

    def node_add(self, frameworks=tuple(), iaas=None, iaasid=None, address=None, template=None, driver=None,
                 cacert=None, clientcert=None, clientkey=None, register=False):

        try:
            url = '{0}/node'.format(self.urlbase)

            request = AddNodeRequest({'register': register, 'pool': frameworks[0], 'alternative_pools': frameworks[1:],
                                      'client_key': self.file_read(clientkey),
                                      'client_cert': self.file_read(clientcert), 'ca_cert': self.file_read(cacert),
                                      'meta_data': {'driver': driver, 'address': address, 'iaas': iaas,
                                                    'iaas_id': iaasid, 'template': template}})
            request.validate()

            r = self.http.post(url, headers=self.json_headers, data=json.dumps(request.to_primitive()))
            self.print_response(r)
            if r.status_code != 201:
                raise click.ClickException(r.text)

        except (requests.ConnectionError, ValidationError, DataError) as e:
            raise click.ClickException(str(e))

    def node_remove(self, address, no_rebalance=False, destroy=False):
        try:
            url = '{0}/node'.format(self.urlbase, address)

            request = RemoveFrameworkRequest({'address': address, 'destroy': destroy, 'no_rebalance': no_rebalance})
            request.validate()

            r = self.http.delete(url, headers=self.headers, params=request.to_primitive())
            self.print_response(r)
            if r.status_code != 200:
                raise click.ClickException(r.text)

        except (requests.ConnectionError, ValidationError, DataError) as e:
            raise click.ClickException(str(e))

    def cluster_add(self, name, address=tuple(), default=None, frameworks=tuple(), teams=tuple(), token=None,
                    ingress_ip=tuple(), ingress_http_port=tuple(), ingress_https_port=tuple(), ingress_protected_port=tuple(),
                    ingress_service=tuple(), install_cert_manager=None, ca_cert=None, client_cert=None,
                    client_key=None, provisioner=KUBERNETES_PROVISIONER, custom_data=dict()):

        try:
            ingress_data = {
                "ingress_ip": ingress_ip,
                "ingress_http_port": ingress_http_port,
                "ingress_https_port": ingress_https_port,
                "ingress_protected_port": ingress_protected_port,
                "ingress_service": ingress_service
            }
            ingress_controllers = parse_ingress_config(ingress_data)

            url = '{0}/provisioner/clusters'.format(self.urlbase)

            request = AddClusterRequest({'name': name, 'address': address, 'default': default, 'teams': teams,
                                         'token': token, 'ingress_controllers': ingress_controllers,
                                         'install_cert_manager': install_cert_manager, 'ca_cert': ca_cert,
                                         'pools': frameworks, 'client_cert': client_cert, 'client_key': client_key,
                                         'provisioner': provisioner, 'custom_data': custom_data})
            request.validate()

            r = self.http.post(url, headers=self.json_headers, data=json.dumps(request.to_primitive()))
            self.print_response(r)
            if r.status_code != 201:
                raise click.ClickException(r.text)

        except (requests.ConnectionError, ValidationError, DataError) as e:
            raise click.ClickException(str(e))

    def cluster_remove(self, name):
        try:
            url = '{0}/provisioner/clusters/{1}'.format(self.urlbase, name)

            r = self.http.delete(url, headers=self.headers)
            self.print_response(r)
            if r.status_code != 200:
                raise click.ClickException(r.text)

        except requests.ConnectionError as e:
            raise click.ClickException(str(e))

    def env_set(self, app_name=None, envs=tuple(), private=False, no_restart=False):
        try:
            url = '{0}/apps/{1}/env'.format(self.urlbase, app_name)

            request = EnvSetRequest({'envs': envs, 'private': private, 'no_restart': no_restart})
            request.validate()

            r = self.http.post(url, headers=self.json_headers, data=json.dumps(request.to_primitive()))
            self.print_response(r)
            if r.status_code != 200:
                raise click.ClickException(r.text)

        except (requests.ConnectionError, ValidationError, DataError) as e:
            raise click.ClickException(str(e))

    def env_unset(self, app_name=None, envs=tuple(), no_restart=False):
        try:
            url = '{0}/apps/{1}/env'.format(self.urlbase, app_name)

            request = EnvUnsetRequest({'envs': envs, 'no_restart': no_restart})
            request.validate()

            r = self.http.delete(url, headers=self.json_headers, data=json.dumps(request.to_primitive()))
            self.print_response(r)
            if r.status_code != 200:
                raise click.ClickException(r.text)

        except (requests.ConnectionError, ValidationError, DataError) as e:
            raise click.ClickException(str(e))
