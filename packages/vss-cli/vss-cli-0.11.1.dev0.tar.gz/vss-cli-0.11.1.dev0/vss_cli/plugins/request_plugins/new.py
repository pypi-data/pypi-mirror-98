"""New VM Request Management plugin for VSS CLI (vss-cli)."""
import logging

import click

from vss_cli import autocompletion, const, rel_opts as so
from vss_cli.cli import pass_context
from vss_cli.config import Configuration
from vss_cli.helper import format_output
from vss_cli.plugins.request import cli

_LOGGING = logging.getLogger(__name__)


@cli.group('new', short_help='Manage new virtual machine deployment requests')
@pass_context
def request_mgmt_new(ctx: Configuration):
    """Manage new virtual machine deployment requests."""
    pass


@request_mgmt_new.command('ls', short_help='list vm new requests')
@so.filter_opt
@so.all_opt
@so.count_opt
@so.page_opt
@so.sort_opt
@pass_context
def request_mgmt_new_ls(
    ctx: Configuration, filter_by, page, sort, show_all, count
):
    """List requests.

    Filter list in the following format <field_name> <operator>,<value>
    where operator is eq, ne, lt, le, gt, ge, like, in.
    For example: status=eq,PROCESSED

    vss-cli request new ls -f status=eq,PROCESSED

    Sort list in the following format <field_name>=<asc|desc>. For example:

    vss-cli request new ls -s created_on=desc
    """
    columns = ctx.columns or const.COLUMNS_REQUEST_NEW_MIN
    _LOGGING.debug(f'Columns {columns}')
    params = dict(expand=1, sort='created_on,desc')
    if all(filter_by):
        params['filter'] = ';'.join(filter_by)
    if all(sort):
        params['sort'] = ';'.join(sort)
    # make request
    with ctx.spinner(disable=ctx.debug):
        _requests = ctx.get_new_requests(
            show_all=show_all, per_page=count, **params
        )

    output = format_output(ctx, _requests, columns=columns)
    # page results
    if page:
        click.echo_via_pager(output)
    else:
        ctx.echo(output)


@request_mgmt_new.command('get', short_help='New vm request')
@click.argument(
    'rid',
    type=click.INT,
    required=True,
    autocompletion=autocompletion.new_requests,
)
@pass_context
def request_mgmt_new_get(ctx: Configuration, rid):
    """Get New VM Request info."""
    # make request
    with ctx.spinner(disable=ctx.debug):
        obj = ctx.get_new_request(rid)
    columns = ctx.columns or const.COLUMNS_REQUEST_NEW
    ctx.echo(format_output(ctx, [obj], columns=columns, single=True))


@request_mgmt_new.command('retry', short_help='Retry vm new request')
@click.argument('rid', type=click.INT, required=True)
@pass_context
def request_mgmt_new_retry(ctx: Configuration, rid):
    """Retry new VM request with status 'Error Processed'."""
    # make request
    with ctx.spinner(disable=ctx.debug):
        obj = ctx.retry_new_request(rid)
    columns = ctx.columns or const.COLUMNS_REQUEST_SUBMITTED
    ctx.echo(format_output(ctx, [obj], columns=columns, single=True))
