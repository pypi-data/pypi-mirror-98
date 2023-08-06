"""Compute Shared Options plugin for VSS CLI (vss-cli)."""
import click

import vss_cli.autocompletion as autocompletion
from vss_cli.plugins.compute_plugins import callbacks
from vss_cli.validators import (
    validate_admin, validate_inform, validate_json_type)

source_opt = click.option(
    '--source',
    '-s',
    help='Source virtual machine or template MOREF or UUID.',
    type=click.STRING,
    required=True,
    autocompletion=autocompletion.virtual_machines,
)
source_template_opt = click.option(
    '--source',
    '-s',
    help='Source virtual machine or template MOREF or UUID.',
    type=click.STRING,
    required=True,
    autocompletion=autocompletion.vm_templates,
)
source_image_opt = click.option(
    '--source',
    '-s',
    help='Source Virtual Machine OVA/OVF id, name or path.',
    type=click.STRING,
    required=True,
    autocompletion=autocompletion.vm_images,
)
description_opt = click.option(
    '--description',
    '-d',
    help='A brief description.',
    type=click.STRING,
    required=True,
)
client_nr_opt = click.option(
    '--client',
    '-b',
    help='Client department.',
    type=click.STRING,
    required=False,
)
client_opt = click.option(
    '--client',
    '-b',
    help='Client department.',
    type=click.STRING,
    required=True,
)
admin_opt = click.option(
    '--admin',
    '-a',
    help='Admin name, phone number and email separated by '
    '`:` i.e. "John Doe:416-123-1234:john.doe@utoronto.ca"',
    type=click.STRING,
    callback=validate_admin,
    required=False,
)
inform_opt = click.option(
    '--inform',
    '-r',
    help='Informational contact emails in comma separated',
    type=click.STRING,
    callback=validate_inform,
    required=False,
)
usage_opt = click.option(
    '--usage',
    '-u',
    help='Vm usage.',
    type=click.Choice(['Test', 'Prod', 'Dev', 'QA']),
    required=False,
    default='Test',
)
os_nr_opt = click.option(
    '--os',
    '-o',
    help='Guest operating system id.',
    type=click.STRING,
    required=False,
    autocompletion=autocompletion.operating_systems,
)
os_opt = click.option(
    '--os',
    '-o',
    help='Guest operating system id.',
    type=click.STRING,
    required=True,
    autocompletion=autocompletion.operating_systems,
)
memory_opt = click.option(
    '--memory', '-m', help='Memory in GB.', type=click.INT, required=False
)
cpu_opt = click.option(
    '--cpu', '-c', help='Cpu count.', type=click.INT, required=False
)
folder_nr_opt = click.option(
    '--folder',
    '-f',
    help='Logical folder moref name or path.',
    type=click.STRING,
    required=False,
    autocompletion=autocompletion.folders,
)
folder_opt = click.option(
    '--folder',
    '-f',
    help='Logical folder moref name or path.',
    type=click.STRING,
    required=True,
    autocompletion=autocompletion.folders,
)
networks_nr_opt = click.option(
    '--net',
    '-n',
    help='Network adapter <moref-or-name>=<nic-type>.',
    type=click.STRING,
    multiple=True,
    required=False,
    callback=callbacks.process_networks_opt,
    autocompletion=autocompletion.networks,
)
networks_opt = click.option(
    '--net',
    '-n',
    help='Network adapter <moref-or-name>=<nic-type>.',
    type=click.STRING,
    multiple=True,
    required=True,
    callback=callbacks.process_networks_opt,
    autocompletion=autocompletion.networks,
)
scsi_ctrllr_opt = click.option(
    '--scsi',
    '-s',
    help='SCSI Controller <type>=<sharing>.',
    type=click.STRING,
    multiple=True,
    required=True,
    callback=callbacks.process_scsi_opt,
    autocompletion=autocompletion.vm_controller_scsi_types,
)
disks_nr_opt = click.option(
    '--disk',
    '-i',
    help='Disk spec <capacity>=<backing_mode>=<backing_sharing>. '
    'optional: backing_mode, backing_sharing',
    type=click.STRING,
    multiple=True,
    required=False,
    callback=callbacks.process_disk_opt,
)
disk_opt = click.option(
    '--disk',
    '-i',
    help='Disk spec <capacity>=<backing_mode>=<backing_sharing>. '
    'optional: backing_mode, backing_sharing',
    type=click.STRING,
    multiple=True,
    required=True,
    callback=callbacks.process_disk_opt,
)
domain_opt = click.option(
    '--domain',
    '-t',
    help='Target fault domain name or moref.',
    type=click.STRING,
    required=False,
    autocompletion=autocompletion.domains,
)
notes_opt = click.option(
    '--notes', help='Custom notes.', type=click.STRING, required=False
)
custom_spec_opt = click.option(
    '--custom-spec',
    '-p',
    help='Guest OS custom specification in JSON format.',
    type=click.STRING,
    required=False,
    callback=validate_json_type,
)
iso_opt = click.option(
    '--iso',
    '-s',
    help='ISO image to be mounted after creation',
    type=click.STRING,
    required=False,
    autocompletion=autocompletion.isos,
)
high_io_opt = click.option(
    '--high-io',
    '-h',
    help='Use VMware Paravirtual SCSIController.',
    is_flag=True,
    required=False,
)
power_on_opt = click.option(
    '--power-on',
    help='Power on after successful deployment.',
    is_flag=True,
    required=False,
)
extra_config_opt = click.option(
    '--extra-config',
    '-e',
    help='Extra configuration key=value format.',
    type=click.STRING,
    required=False,
    multiple=True,
    callback=callbacks.process_options,
)
user_data_opt = click.option(
    '--user-data',
    help='Cloud-init user_data YAML file path to '
    'pre-configure guest os upon first boot.',
    type=click.STRING,
    callback=callbacks.process_user_data,
    required=False,
)
net_cfg_opt = click.option(
    '--network-config',
    help='Cloud-init network-config YAML file path to '
    'pre-configure guest os upon first boot.',
    type=click.STRING,
    callback=callbacks.process_user_data,
    required=False,
)
vss_service_opt = click.option(
    '--vss-service',
    help='VSS Service related to VM',
    autocompletion=autocompletion.vss_services,
    required=False,
)
instances = click.option(
    '--instances',
    help='Number of instances to deploy',
    type=click.INT,
    default=1,
    show_default=True,
)
vss_options_opt = click.option(
    '--vss-option',
    help='VSS Option to enable',
    autocompletion=autocompletion.vss_options,
    required=False,
)
firmware_nr_opt = click.option(
    '--firmware',
    '-w',
    help='Firmware type.',
    autocompletion=autocompletion.vm_firmware,
    required=False,
)
firmware_opt = click.option(
    '--firmware',
    '-w',
    help='Firmware type.',
    autocompletion=autocompletion.vm_firmware,
    required=True,
)
