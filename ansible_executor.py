from ansible import context
from ansible.cli import CLI
from ansible.module_utils.common.collections import ImmutableDict
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
import os
import time

def execute_deployment(deployment_playbook, inventory_file, cloud_credentials):
    os.environ["AWS_ACCESS_KEY_ID"] = cloud_credentials['aws_access_key']
    os.environ["AWS_SECRET_ACCESS_KEY"] = cloud_credentials['aws_secret_key']
    os.environ['region'] = 'ap-south-1'
    os.environ['ANSIBLE_HOST_KEY_CHECKING'] = "False"
    os.environ['ANSIBLE_SSH_RETRIES'] = '5'
    os.environ['node_1'] = 'EFK-Node-1'
    time.sleep(15)
    loader = DataLoader()

    context.CLIARGS = ImmutableDict(tags={}, listtags=False, listtasks=False, listhosts=False, syntax=False,
                                    connection='ssh',
                                    module_path=None, forks=100, remote_user='xxx', private_key_file=None,
                                    ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None,
                                    scp_extra_args=None, become=True,
                                    become_method='sudo', become_user='root', verbosity=True, check=False,
                                    start_at_task=None)

    inventory = InventoryManager(loader=loader,
                                 sources=(inventory_file))

    variable_manager = VariableManager(loader=loader, inventory=inventory, version_info=CLI.version_info(gitinfo=False))

    pbex = PlaybookExecutor(
        playbooks=[deployment_playbook],
        inventory=inventory, variable_manager=variable_manager, loader=loader, passwords={})

    results = pbex.run()

    return results
