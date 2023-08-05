#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

import shutil
import os
from db_sync_tool.utility import mode, system, output
from db_sync_tool.remote import utility as remote_utility


def clean_up():
    """
    Clean up
    :return:
    """
    if not mode.is_import():
        remote_utility.remove_target_database_dump()
        if mode.get_sync_mode() == mode.SyncMode.PROXY:
            remove_temporary_data_dir()


def remove_temporary_data_dir():
    """
    Remove temporary data directory for storing database dump files
    :return:
    """
    if os.path.exists(system.default_local_sync_path):
        output.message(
            output.Subject.LOCAL,
            'Cleaning up',
            True
        )
        shutil.rmtree(system.default_local_sync_path)


def clean_up_dump_dir(client, path, num=5):
    """
    Clean up the dump directory from old dump files (only affect .sql and .tar.gz files)
    :param client:
    :param path:
    :param num:
    :return:
    """
    # Distinguish stat command on os system (Darwin|Linux)
    if check_os(client).strip() == 'Darwin':
        _command = get_command(client, 'stat') + ' -f "%Sm %N" ' + path + ' | ' + get_command(client,
                                                                                              'sort') + ' -rn | ' + get_command(
            client, 'grep') + ' -E ".tar.gz|.sql"'
    else:
        _command = get_command(client, 'stat') + ' -c "%y %n" ' + path + ' | ' + get_command(client,
                                                                                             'sort') + ' -rn | ' + get_command(
            client, 'grep') + ' -E ".tar.gz|.sql"'

    # List files in directory sorted by change date
    _files = mode.run_command(
        _command,
        client,
        True
    ).splitlines()

    for i in range(len(_files)):
        _filename = _files[i].rsplit(' ', 1)[-1]

        # Remove oldest files chosen by keep_dumps count
        if not i < num:
            mode.run_command(
                'rm ' + _filename,
                client
            )


def check_os(client):
    """
    Check which system is running (Linux|Darwin)
    :param client:
    :return:
    """
    return mode.run_command(
        get_command(client, 'uname') + ' -s',
        client,
        True
    )


def get_command(client, command):
    """
    Get command helper for overriding default commands on the given client
    :param client:
    :param command:
    :return: String command
    """
    if 'console' in system.config[client]:
        if command in system.config[client]['console']:
            return system.config[client]['console'][command]
    return command


def get_dump_dir(client):
    """
    Get database dump directory by client
    :param client:
    :return: String path
    """
    if system.config[f'default_{client}_dump_dir']:
        return '/tmp/'
    else:
        return system.config[client]['dump_dir']


def check_and_create_dump_dir(client, path):
    """
    Check if a path exists on the client system and creates the given path if necessary
    :param client:
    :param path:
    :return:
    """
    mode.run_command(
        '[ ! -d "' + path + '" ] && mkdir -p "' + path + '"',
        client
    )


def get_ssh_host_name(client, with_user=False):
    """
    Format ssh host name depending on existing client name
    :param client:
    :param with_user:
    :return:
    """
    if not 'user' in system.config[client] and not 'host' in system.config[client]:
        return ''

    if with_user:
        _host = system.config[client]['user'] + '@' + system.config[client]['host']
    else:
        _host = system.config[client]['host']

    if 'name' in system.config[client]:
        return output.CliFormat.BOLD + system.config[client][
            'name'] + output.CliFormat.ENDC + output.CliFormat.BLACK + ' (' + _host + ')' + output.CliFormat.ENDC
    else:
        return _host


def create_local_temporary_data_dir():
    """
    Create local temporary data dir
    :return:
    """
    # @ToDo: Combine with check_and_create_dump_dir()
    if not os.path.exists(system.default_local_sync_path):
        os.makedirs(system.default_local_sync_path)


def dict_to_args(dict):
    """
    Convert an dictionary to a args list
    :param dict: Dictionary
    :return: List
    """
    _args = []
    for key, val in dict.items():
        if isinstance(val, bool):
            if val:
                _args.append(f'--{key}')
        else:
            _args.append(f'--{key}')
            _args.append(str(val))
    if len(_args) == 0:
        return None
    return _args


def check_file_exists(client, path):
    """
    Check if a file exists
    :param client: String
    :param path: String file path
    :return: Boolean
    """
    return mode.run_command(f'[ -f {path} ] && echo "1"', client, True) == '1'


def run_script(client=None, script='before'):
    """
    Executing script command
    :param client: String
    :param script: String
    :return:
    """
    if client is None:
        _config = system.config
        _subject = output.Subject.LOCAL
        client = mode.Client.LOCAL
    else:
        _config = system.config[client]
        _subject = output.host_to_subject(client)

    if not 'scripts' in _config:
        return

    if f'{script}' in _config['scripts']:
        output.message(
            _subject,
            f'Running script {client}',
            True
        )
        mode.run_command(
            _config['scripts'][script],
            client
        )


def confirm(prompt=None, resp=False):
    """
    https://code.activestate.com/recipes/541096-prompt-the-user-for-confirmation/

    prompts for yes or no response from the user. Returns True for yes and
    False for no.

    'resp' should be set to the default value assumed by the caller when
    user simply types ENTER.

    >>> confirm(prompt='Create Directory?', resp=True)
    Create Directory? [Y|n]:
    True
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [y|N]:
    False

    """

    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s|%s]: ' % (prompt, 'Y', 'n')
    else:
        prompt = '%s [%s|%s]: ' % (prompt, 'y', 'N')

    while True:
        ans = input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print('Please enter y or n.')
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False
