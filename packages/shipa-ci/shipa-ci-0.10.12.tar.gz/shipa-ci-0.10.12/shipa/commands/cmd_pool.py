import click

from shipa.commands import constant


@click.group()
def cli_add():
    pass


@cli_add.command("add", short_help=constant.CMD_FRAMEWORK_ADD)
@click.argument("framework", required=True)
@click.option('-d', '--default', is_flag=True, help=constant.OPT_FRAMEWORK_DEFAULT)
@click.option('-p', '--public', is_flag=True, help=constant.OPT_FRAMEWORK_PUBLIC)
@click.option('--accept-drivers', help=constant.OPT_FRAMEWORK_DRIVER, multiple=True)
@click.option('--app-quota-limit', help=constant.OPT_FRAMEWORK_QUOTA_LIMIT, type=int)
@click.option('--ingress', help=constant.OPT_FRAMEWORK_INGRESS)
@click.option('--kubernetes-namespace', help=constant.OPT_FRAMEWORK_NAMESPACE)
@click.option('--provisioner', help=constant.OPT_FRAMEWORK_PROVISIONER)
@click.option('--plan', help=constant.OPT_FRAMEWORK_PLAN)
@click.option('-t', '--team', help=constant.OPT_FRAMEWORK_TEAM, multiple=True)
@click.pass_obj
def create(env, framework, ingress, default, public, team, accept_drivers, app_quota_limit, provisioner, plan, kubernetes_namespace):
    """Each docker node added by shipa engine belongs to one framework."""

    with env.client.http as http_client:
        env.client.auth(http_client)
        env.client.framework_add(framework=framework, ingress=ingress, default=default, public=public, teams=team, accept_drivers=accept_drivers,
                            app_quota_limit=app_quota_limit, provisioner=provisioner, plan=plan,
                            kubernetes_namespace=kubernetes_namespace)
        print('Framework successfully registered.')


@click.group()
def cli_remove():
    pass


@cli_remove.command("remove", short_help=constant.CMD_FRAMEWORK_REMOVE)
@click.argument("framework", required=True)
@click.pass_obj
def remove(env, framework):
    """Remove an existing framework."""

    with env.client.http as http_client:
        env.client.auth(http_client)
        env.client.framework_remove(framework=framework)
        print('Framework successfully removed.')


@click.group()
def cli_update():
    pass


@cli_update.command("update", short_help=constant.CMD_FRAMEWORK_UPDATE)
@click.argument("framework", required=True)
@click.option('-d', '--default', is_flag=True, help=constant.OPT_FRAMEWORK_DEFAULT)
@click.option('-p', '--public', is_flag=True, help=constant.OPT_FRAMEWORK_PUBLIC)
@click.option('--accept-drivers', help=constant.OPT_FRAMEWORK_DRIVER, multiple=True)
@click.option('--app-quota-limit', help=constant.OPT_FRAMEWORK_QUOTA_LIMIT, type=int)
@click.option('--plan', help=constant.OPT_FRAMEWORK_PLAN)
@click.pass_obj
def update(env, framework, default, public, accept_drivers, app_quota_limit, plan):
    """Updates attributes for a framework."""

    with env.client.http as http_client:
        env.client.auth(http_client)
        env.client.framework_update(framework=framework, default=default, public=public, accept_drivers=accept_drivers,
                               app_quota_limit=app_quota_limit, plan=plan)
        print('Framework successfully updated.')


cli = click.CommandCollection(sources=[cli_add, cli_remove, cli_update])
