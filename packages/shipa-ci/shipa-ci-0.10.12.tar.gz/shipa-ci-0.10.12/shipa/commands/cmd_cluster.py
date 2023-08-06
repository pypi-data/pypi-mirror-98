import click

from shipa.commands import constant
from shipa.commands.constant import KUBERNETES_PROVISIONER
from shipa.utils import validate_map


@click.group()
def cli_add():
    pass


@cli_add.command("add", short_help=constant.CMD_CLUSTER_ADD)
@click.argument("name", required=True)
@click.option('-a', '--address', help=constant.CMD_CLUSTER_ADDRESS, multiple=True)
@click.option('-d', '--default', is_flag=True, help=constant.OPT_CLUSTER_DEFAULT)
@click.option('-p', '--frameworks', help=constant.OPT_CLUSTER_FRAMEWORK, multiple=True)
@click.option('-t', '--teams', help=constant.OPT_CLUSTER_TEAM, multiple=True)
@click.option('--token', help=constant.CMD_CLUSTER_TOKEN)
@click.option('--ingress-service', help=constant.OPT_CLUSTER_INGRESS_SERVICE, multiple=True)
@click.option('--ingress-ip', help=constant.OPT_CLUSTER_INGRESS_IP, multiple=True)
@click.option('--ingress-http-port', help=constant.OPT_CLUSTER_INGRESS_HTTP_PORT, multiple=True)
@click.option('--ingress-https-port', help=constant.OPT_CLUSTER_INGRESS_HTTPS_PORT, multiple=True)
@click.option('--ingress-protected-port', help=constant.OPT_CLUSTER_INGRESS_PROTECTED_PORT, multiple=True)
@click.option('--install-cert-manager', is_flag=True, help=constant.OPT_CLUSTER_INSTALL_CERT_MANAGER)
@click.option('--cacert', help=constant.OPT_NODE_CA_CERT)
@click.option('--clientcert', help=constant.OPT_NODE_CLIENT_CERT)
@click.option('--clientkey', help=constant.OPT_NODE_CLIENT_KEY)
@click.option('--provisioner', help=constant.OPT_CLUSTER_PROVISIONER, default=KUBERNETES_PROVISIONER, show_default=True)
@click.option('--custom-data', help=constant.OPT_CLUSTER_CUSTOM, callback=validate_map, multiple=True)
@click.pass_obj
def add(env, name, address, default, frameworks, teams, token, ingress_service, ingress_ip, ingress_http_port, ingress_https_port,
        ingress_protected_port, install_cert_manager, cacert, clientcert, clientkey, provisioner, custom_data):
    """Creates a kubernetes cluster definition."""

    with env.client.http as http_client:
        env.client.auth(http_client)
        env.client.cluster_add(name=name, address=address, default=default, frameworks=frameworks, teams=teams, token=token,
                               ingress_service=ingress_service, ingress_ip=ingress_ip, ingress_http_port=ingress_http_port,
                               ingress_https_port=ingress_https_port, ingress_protected_port=ingress_protected_port,
                               install_cert_manager=install_cert_manager, ca_cert=cacert, client_cert=clientcert,
                               client_key=clientkey, provisioner=provisioner, custom_data=custom_data)
        print('Cluster successfully added.')


@click.group()
def cli_remove():
    pass


@cli_remove.command("remove", short_help=constant.OPT_CLUSTER_REMOVE)
@click.argument("name", required=True)
@click.pass_obj
def remove(env, name):
    """Removes a kubernetes cluster definition."""

    with env.client.http as http_client:
        env.client.auth(http_client)
        env.client.cluster_remove(name=name)
        print('Cluster {0} has been removed!'.format(name))


cli = click.CommandCollection(sources=[cli_add, cli_remove])
