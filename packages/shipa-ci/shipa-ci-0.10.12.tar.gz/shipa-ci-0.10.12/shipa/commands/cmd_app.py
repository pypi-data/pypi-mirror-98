import click

from shipa.commands import constant
from shipa.utils import validate_map
from shipa.client.types import AppExistsError


@click.group()
def cli_create():
    pass


@cli_create.command("create", short_help=constant.CMD_APP_CREATE)
@click.argument("appname", required=True)
@click.argument("platform", required=False)
@click.option('-d', '--description', help=constant.OPT_APP_CREATE_DESCRIPTION)
@click.option('-f', '--dependency-file', help=constant.OPT_APP_CREATE_DEPENDENCY, multiple=True)
@click.option('-g', '--tag', help=constant.OPT_APP_CREATE_TAG, multiple=True)
@click.option('-p', '--plan', help=constant.OPT_APP_CREATE_PLAN)
@click.option('-t', '--team', help=constant.OPT_APP_CREATE_TEAM, required=True)
@click.option('-F', '--framework', help=constant.OPT_APP_CREATE_FRAMEWORK)
@click.option('-o', '--pool', help=constant.OPT_APP_CREATE_POOL)
@click.option('--ignore-if-exists', help=constant.OPT_APP_CREATE_IGNORE_IF_EXISTS, default=False)
@click.pass_obj
def create(env, appname, platform, description, dependency_file, tag, plan, team, framework, pool, ignore_if_exists):
    """Creates a new app using the given name and platform."""

    with env.client.http as http_client:
        env.client.auth(http_client)
        try:
            if pool is not None:
                framework = pool
                
            env.client.app_create(appname, team=team, framework=framework, platform=platform, description=description,
                                dependency_files=dependency_file, tags=tag, plan=plan)
        except AppExistsError as e:
            print(e)
            if ignore_if_exists:
                pass


@click.group()
def cli_remove():
    pass


@cli_remove.command("remove", short_help=constant.CMD_APP_REMOVE)
@click.argument("appname", required=True)
@click.pass_obj
def remove(env, appname):
    """If the app is bound to any service instance, all binds will be removed before the app gets deleted"""

    with env.client.http as http_client:
        env.client.auth(http_client)
        env.client.app_remove(appname=appname)
        env.client.autoscale_check()
        print('App {0} has been removed!'.format(appname))


@click.group()
def cli_deploy():
    pass


@cli_deploy.command("deploy", short_help=constant.CMD_APP_DEPLOY)
@click.option('-a', '--app', 'appname', help=constant.OPT_APP_DEPLOY_APP, required=True)
@click.option('-d', '--directory', help=constant.OPT_APP_DEPLOY_DIRECTORY, default='.')
@click.option('-i', '--image', help=constant.OPT_APP_DEPLOY_IMAGE)
@click.option('--port', help=constant.OPT_APP_DEPLOY_PORT)
@click.option('--registry-secret', help=constant.OPT_APP_DEPLOY_REGISTRY_SECRET)
@click.option('--registry-user', help=constant.OPT_APP_DEPLOY_REGISTRY_USER)
@click.option('--steps', help=constant.OPT_APP_DEPLOY_STEPS, type=int, default=1, show_default=True)
@click.option('--step-interval', help=constant.OPT_APP_DEPLOY_STEP_INTERVAL)
@click.option('--step-weight', help=constant.OPT_APP_DEPLOY_STEP_WEIGHT)
@click.pass_obj
def deploy(env, appname, image, directory, port, registry_secret, registry_user, steps, step_interval, step_weight):
    """Deploys set of directories to shipa server."""

    with env.client.http as http_client:
        env.client.auth(http_client)
        env.client.app_deploy(appname=appname, image=image, directory=directory, port=port, registry_secret=registry_secret,
                              registry_user=registry_user, steps=steps, step_interval=step_interval,
                              step_weight=step_weight)
        env.client.autoscale_check()
        print('App {0} has been deployed!'.format(appname))


@click.group()
def cli_move():
    pass


@cli_remove.command("move", short_help=constant.CMD_APP_REMOVE)
@click.option('-a', '--app', 'appname', help=constant.OPT_APP_REMOVE_APP, required=True)
@click.option('-p', '--framework', help=constant.OPT_APP_CREATE_FRAMEWORK, required=True)
@click.pass_obj
def move(env, appname, framework):
    """ Moves app to another framework """

    with env.client.http as http_client:
        env.client.auth(http_client)
        env.client.app_move(appname=appname, framework=framework)
        env.client.autoscale_check()
        print('App {0} has been moved!'.format(appname))


cli = click.CommandCollection(sources=[cli_create, cli_remove, cli_deploy, cli_move])
