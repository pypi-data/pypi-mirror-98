#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

import sys
from db_sync_tool.utility import mode, output, helper
from db_sync_tool.remote import client as remote_client


def run_ssh_command_by_client(client, command):
    """
    Running origin ssh command
    :param client: String
    :param command: String
    :return:
    """
    if client == mode.Client.ORIGIN:
        return run_ssh_command(command, remote_client.ssh_client_origin, client)
    elif client == mode.Client.TARGET:
        return run_ssh_command(command, remote_client.ssh_client_target, client)


def run_ssh_command(command, ssh_client=remote_client.ssh_client_origin, client=None):
    """
    Running ssh command
    :param command: String
    :param ssh_client:
    :param client: String
    :return:
    """
    stdin, stdout, stderr = ssh_client.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()

    err = stderr.read().decode()

    if err and 0 != exit_status:
        helper.run_script(client=client, script='error')
        sys.exit(output.message(output.Subject.ERROR, err, False))
    elif err:
        output.message(output.Subject.WARNING, err, True)

    return stdout