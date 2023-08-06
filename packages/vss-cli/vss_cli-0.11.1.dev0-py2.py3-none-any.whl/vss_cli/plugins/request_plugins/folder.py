"""Folder Request Management plugin for VSS CLI (vss-cli)."""
import logging

import click

from vss_cli import const, rel_opts as so
import vss_cli.autocompletion as autocompletion
from vss_cli.cli import pass_context
from vss_cli.config import Configuration
from vss_cli.helper import format_output
from vss_cli.plugins.request import cli

_LOGGING = logging.getLogger(__name__)


@cli.group('folder', short_help='Manage logical folder requests.')
@pass_context
def request_mgmt_folder(ctx: Configuration):
    """Manage logical Folders.

    Logical Folders are containers for storing and organizing
    inventory objects, in this case virtual machines.
    """
    pass


@request_mgmt_folder.command('ls', short_help='list logical folder requests')
@so.filter_opt
@so.sort_opt
@so.all_opt
@so.count_opt
@so.page_opt
@pass_context
def request_mgmt_folder_ls(ctx, filter_by, page, sort, show_all, count):
    """List requests.

    Filter list in the following format <field_name>=<operator>,<value>
    where operator is eq, ne, lt, le, gt, ge, like, in.
    For example: status=eq,PROCESSED

    vss-cli request folder ls -f status=eq,PROCESSED -f name,Dev

    Sort list in the following format <field_name>=<asc|desc>. For example:

    vss-cli request folder ls -s created_on=desc
    """
    columns = ctx.columns or const.COLUMNS_REQUEST_FOLDER_MIN
    params = dict(expand=1, sort='created_on,desc')
    if all(filter_by):
        params['filter'] = ';'.join(filter_by)
    if all(sort):
        params['sort'] = ';'.join(sort)
    # make request
    with ctx.spinner(disable=ctx.debug):
        _requests = ctx.get_folder_requests(
            show_all=show_all, per_page=count, **params
        )

    output = format_output(ctx, _requests, columns=columns)
    # page results
    if page:
        click.echo_via_pager(output)
    else:
        ctx.echo(output)


@request_mgmt_folder.command('get', short_help='Folder request')
@click.argument(
    'rid',
    type=click.INT,
    required=True,
    autocompletion=autocompletion.folder_requests,
)
@pass_context
def request_mgmt_folder_get(ctx, rid):
    """Get Folder info."""
    # make request
    with ctx.spinner(disable=ctx.debug):
        obj = ctx.get_folder_request(rid)
    columns = ctx.columns or const.COLUMNS_REQUEST_FOLDER
    ctx.echo(format_output(ctx, [obj], columns=columns, single=True))
