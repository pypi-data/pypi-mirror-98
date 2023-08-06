"""Details for the auto-completion."""
import os
from typing import Callable, Dict, List, Tuple  # NOQA

from requests.exceptions import HTTPError

from vss_cli import const
from vss_cli.config import Configuration
from vss_cli.exceptions import VssError


def _init_ctx(ctx: Configuration) -> None:
    """Initialize ctx."""
    # ctx is incomplete thus need to 'hack' around it
    # see bug https://github.com/pallets/click/issues/942
    ctx.client = Configuration(tk=os.environ.get('VSS_TOKEN'))
    ctx.client.endpoint = os.environ.get('VSS_ENDPOINT', None)
    ctx.client.username = os.environ.get('VSS_USER', None)
    ctx.client.password = os.environ.get('VSS_USER_PASS', None)
    ctx.client.timeout = int(
        os.environ.get('VSS_TIMEOUT', str(const.DEFAULT_TIMEOUT))
    )
    ctx.client.config_path = os.environ.get('VSS_CONFIG', const.DEFAULT_CONFIG)
    # fallback to load configuration
    ctx.client.load_config()


def _autocomplete(
    f: Callable,
    incomplete: str,
    attrs: List[str],
    f_kwargs: Dict = None,
    sort_index: int = 0,
    complete_index: int = 0,
) -> List[Tuple[str, str]]:
    """Autocomplete main function."""
    try:
        response = f(**f_kwargs)
    except (HTTPError, VssError):
        response = []

    completions = []  # type: List[Tuple[str, str]]
    if response:
        for obj in response:
            sub_attrs = []
            # start iterating in second item (index 1)
            for attr in attrs[1:]:
                sub_attrs.append(str(obj.get(attr, 'N/A')))
            # first item (index 0) is always the key
            r = (str(obj[attrs[0]]), ' - '.join(sub_attrs))
            completions.append(r)

        completions.sort(key=lambda x: x[sort_index])

        return [c for c in completions if incomplete in c[complete_index]]
    return completions


def table_formats(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Provide table Formats."""
    _init_ctx(ctx)

    completions = [
        ("plain", "Plain tables, no pseudo-graphics to draw lines"),
        ("simple", "Simple table with --- as header/footer (default)"),
        ("github", "Github flavored Markdown table"),
        ("grid", "Formatted as Emacs 'table.el' package"),
        ("fancy_grid", "Draws a fancy grid using box-drawing characters"),
        ("pipe", "PHP Markdown Extra"),
        ("orgtbl", "org-mode table"),
        ("jira", "Atlassian Jira Markup"),
        ("presto", "Formatted as PrestoDB cli"),
        ("psql", "Formatted as Postgres psql cli"),
        ("rst", "reStructuredText"),
        ("mediawiki", "Media Wiki as used in Wikpedia"),
        ("moinmoin", "MoinMain Wiki"),
        ("youtrack", "Youtrack format"),
        ("html", "HTML Markup"),
        ("pretty", "HTML escaping."),
        ("latex", "LaTeX markup, replacing special characters"),
        ("latex_raw", "LaTeX markup, no replacing of special characters"),
        (
            "latex_booktabs",
            "LaTex markup using spacing and style from `booktabs",
        ),
        ("textile", "Textile"),
        ("tsv", "Tab Separated Values"),
        ("csv", "Comma Separated Values"),
    ]

    completions.sort()

    return [c for c in completions if incomplete in c[0]]


def vm_templates(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete VM templates."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_templates,
        incomplete,
        ['moref', 'name'],
        complete_index=1,
        sort_index=1,
        f_kwargs={"short": 1, "show_all": True, "per_page": 2000},
    )


def virtual_machines(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete VMs."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_vms,
        incomplete,
        ['moref', 'name'],
        complete_index=1,
        sort_index=1,
        f_kwargs={"show_all": True, "short": 1, "per_page": 2000},
    )


def vm_controller_scsi_sharing(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete VM controller SCSI types."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_supported_scsi_sharing,
        incomplete,
        ['type', 'description'],
        f_kwargs={'only_type': False},
    )


def vm_controller_scsi_types(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete VM controller SCSI types."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_supported_scsi_controllers,
        incomplete,
        ['type', 'description'],
        f_kwargs={'only_type': False},
    )


def vm_disk_backing_modes(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete VM Disk Backing Modes."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_supported_disk_backing_modes,
        incomplete,
        ['type', 'description'],
        f_kwargs={'only_type': False},
    )


def vm_disk_sharing(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete VM Disk Backing Modes."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_supported_disk_sharing,
        incomplete,
        ['type', 'description'],
        f_kwargs={'only_type': False},
    )


def domains(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete Domains."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_domains,
        incomplete,
        ['moref', 'name'],
        complete_index=1,
        sort_index=1,
        f_kwargs={"short": 1, "show_all": True, "per_page": 2000},
    )


def folders(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete VM folders."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_folders,
        incomplete,
        ['moref', 'path'],
        sort_index=1,
        complete_index=1,
        f_kwargs={
            "show_all": True,
            "sort": "path,desc",
            "per_page": 500,
            "short": 1,
        },
    )


def networks(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete Networks."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_networks,
        incomplete,
        ['moref', 'label'],
        sort_index=1,
        complete_index=1,
        f_kwargs={"show_all": True, "sort": "label,desc", "per_page": 500},
    )


def operating_systems(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete VM operating systems."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_os,
        incomplete,
        ['guest_id', 'full_name'],
        f_kwargs={"show_all": True, "sort": "guest_id,desc", "per_page": 500},
    )


def vss_services(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete VSS Services."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_vss_services,
        incomplete,
        ['id', 'label'],
        sort_index=1,
        complete_index=1,
        f_kwargs={"show_all": True, "sort": "label,desc", "per_page": 500},
    )


def isos(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete ISO images."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_isos,
        incomplete,
        attrs=['id', 'path'],
        sort_index=1,
        complete_index=1,
        f_kwargs={"show_all": True, "sort": "path,desc", "per_page": 500},
    )


def vm_images(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete VM images."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_images,
        incomplete,
        attrs=['id', 'path'],
        sort_index=1,
        complete_index=1,
        f_kwargs={"show_all": True, "sort": "path,desc", "per_page": 500},
    )


def floppies(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete VM Floppies."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_floppies,
        incomplete,
        attrs=['id', 'path'],
        sort_index=1,
        complete_index=1,
        f_kwargs={"show_all": True, "sort": "path,desc", "per_page": 500},
    )


def inventory_properties(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete VM Inventory Properties."""
    _init_ctx(ctx)
    try:
        response = ctx.client.request('/inventory/options')
        if response:
            response = response.get('data')
    except (HTTPError, VssError):
        response = []

    completions = []  # type: List[Tuple[str, str]]
    if response:
        for obj in response:
            completions.append((obj['key'], obj['value']))

        completions.sort()

        return [c for c in completions if incomplete in c[0]]
    return completions


def inventory_requests(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete VM Inventory Requests."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_inventory_requests,
        incomplete,
        attrs=['id', 'created_on', 'name'],
        f_kwargs={"sort": "created_on,desc", "per_page": 500},
    )


def new_requests(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete New VM Requests."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_new_requests,
        incomplete,
        attrs=['id', 'vm_moref', 'vm_name'],
        f_kwargs={"sort": "created_on,desc", "per_page": 500},
    )


def change_requests(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete Change VM Requests."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_change_requests,
        incomplete,
        attrs=['id', 'vm_moref', 'vm_name', 'attribute'],
        f_kwargs={"sort": "created_on,desc", "per_page": 500},
    )


def export_requests(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete Export VM Requests."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_export_requests,
        incomplete,
        attrs=['id', 'vm_moref', 'vm_name'],
        f_kwargs={"sort": "created_on,desc", "per_page": 500},
    )


def folder_requests(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete Folder Requests."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_folder_requests,
        incomplete,
        attrs=['id', 'moref', 'action'],
        f_kwargs={"sort": "created_on,desc", "per_page": 500},
    )


def image_sync_requests(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete Image Sync Requests."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_folder_requests,
        incomplete,
        attrs=['id', 'type'],
        f_kwargs={"sort": "created_on,desc", "per_page": 500},
    )


def snapshot_requests(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete VM Snapshot Requests."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_snapshot_requests,
        incomplete,
        attrs=['id', 'vm_moref', 'vm_name'],
        f_kwargs={"sort": "created_on,desc", "per_page": 500},
    )


def account_messages(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete Account Messages."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_user_messages,
        incomplete,
        attrs=['id', 'kind', 'subject'],
        f_kwargs={"sort": "created_on,desc", "per_page": 500},
    )


def virtual_nic_types(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete VM NIC Types."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_supported_nic_types,
        incomplete,
        attrs=['type', 'description'],
        f_kwargs={"only_type": False},
    )


def virtual_hw_types(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete VM Virtual Hardware Types."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_supported_vmx_types,
        incomplete,
        attrs=['type', 'description'],
        f_kwargs={"only_type": False},
    )


def vss_options(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete VSS Options."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_supported_vss_options,
        incomplete,
        attrs=['option', 'description'],
        f_kwargs={"only_option": False},
    )


def groups(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete User Groups."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_groups,
        incomplete,
        attrs=['id', 'name'],
        f_kwargs={"sort": "created_on,desc", "per_page": 500},
    )


def vm_firmware(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Autocomplete VM firmware types."""
    _init_ctx(ctx)
    return _autocomplete(
        ctx.client.get_supported_firmware_types,
        incomplete,
        attrs=['type', 'description'],
        f_kwargs={"only_type": False},
    )
