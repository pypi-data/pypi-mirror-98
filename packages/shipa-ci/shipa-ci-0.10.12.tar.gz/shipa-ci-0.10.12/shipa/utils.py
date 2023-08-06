import os
import tarfile
import tempfile
from collections import defaultdict

import click

from shipa.gitignore import GitIgnore
from shipa.client.types import IngressControllerConfig


class RepositoryFolder(object):
    IGNORE_FILENAME = '.shipaignore'

    def __init__(self, directory, verbose=False):
        assert directory is not None
        assert verbose is not None

        self.directory = directory
        self.verbose = verbose

        ignore_path = os.path.join(directory, self.IGNORE_FILENAME)
        lines = None
        if os.path.isfile(ignore_path) is True:
            with open(ignore_path, 'r') as f:
                lines = f.readlines()
        self.shipa_ignore = GitIgnore(lines or [])

    def create_tarfile(self):

        os.chdir(self.directory)
        if self.verbose:
            print('Create tar archive:')

        def filter(info):
            if info.name.startswith('./.git'):
                return

            filename = info.name[2:]

            if self.shipa_ignore.match(filename):
                if self.verbose:
                    print('IGNORE: ', filename)
                return

            if self.verbose:
                print('OK', filename)
            return info

        f = tempfile.TemporaryFile(suffix='.tar.gz')
        tar = tarfile.open(fileobj=f, mode="w:gz")
        tar.add(name='.',
                recursive=True,
                filter=filter)
        tar.close()
        f.seek(0)
        return f


def parse_step_interval(step_interval):
    if step_interval is None or step_interval == '':
        return 1
    elif step_interval.endswith('s'):
        return int(step_interval[:len(step_interval) - 1])
    elif step_interval.endswith('m'):
        return int(step_interval[:len(step_interval) - 1]) * 60
    elif step_interval.endswith('h'):
        return int(step_interval[:len(step_interval) - 1]) * 60 * 60
    else:
        return step_interval


def parse_port(port):
    port_with_protocol = port.split(":")
    if len(port_with_protocol) == 2:
        return port[0], port[1]

    return "TCP", port


def parse_ingress_config(parameters):
    """parse_ingress_config takes a dict of parameters, groups them by ingress controller name and returns config for
    each controller.

    Args:
        parameters: ...

    Returns:
        A map with IngressControllerConfig for each controller.

    Examples:

        >>> parse_ingress_config({'ingress_ip': ('traefk:10.10.10.10', 'istio:10.10.10.20'), 'ingress_http_port': (
        'traefik:80', 'istio:8080')}) {"traefik": IngressControllerConfig({"ingress_ip":"10.10.10.10",
        "ingress_http_port":"80"),"istio": IngressControllerConfig({"ingress_ip":"10.10.10.20",
        "ingress_http_port":"8080")}
    """

    configs = defaultdict(IngressControllerConfig)
    for name, tuple in parameters.items():
        for value in tuple:
            parsed = value.split(":")
            if len(parsed) != 2:
                raise click.ClickException("invalid %s: %s" % (name, value))
            ingress_name, v = parsed[0], parsed[1]
            configs[ingress_name][name] = v
    return configs


def validate_map(ctx, param, values):
    try:
        map_data = dict()
        for value in values:
            k, v = value.split('=')
            map_data[k] = v
        return map_data
    except ValueError:
        raise click.BadParameter('need to be in format KEY=VALUE')


def validate_env(ctx, param, values):
    try:
        envs = []
        for value in values:
            k, v = value.split('=')
            env = {'name': k, 'value': v}
            envs.append(env)
        return envs
    except ValueError:
        raise click.BadParameter('need to be in format NAME=VALUE')
