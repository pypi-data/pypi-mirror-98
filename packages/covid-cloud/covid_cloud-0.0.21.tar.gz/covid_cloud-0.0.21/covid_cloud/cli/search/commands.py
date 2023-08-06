from .tables import commands as tables_commands
from covid_cloud.cli.utils import assert_config
from covid_cloud.client import *
from covid_cloud.cli.auth.utils import get_oauth_token


@click.group()
@click.pass_context
def search(ctx):
    assert_config(ctx, 'search-url')


@search.command()
@click.pass_context
@click.argument("q")
@click.option('-d', '--download', is_flag=True)
@click.option('-j', '--use-json', '--json', is_flag=True)
@click.option('-r', '--raw', is_flag=True)
def query(ctx, q, download, use_json, raw):
    click.echo(search_client.query(ctx.obj['search-url'], q, download, use_json, raw, get_oauth_token(ctx)))


search.add_command(tables_commands.tables)
