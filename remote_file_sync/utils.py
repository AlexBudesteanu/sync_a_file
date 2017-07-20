from paramiko import SSHClient, AutoAddPolicy
import argparse
import os


def get_ssh_client(host=None, user=None, password=None):
    """
        Method that returns a ssh connection to the remote
        system.

        Args:
            host (string): the remote hostname or ip address;
            user (string): the user to use when trying to log in
                           to the remote host;
            password (string): the password for the given user;

        Returns:
            SSHClient: a SSHClient object which can be used as a context manager

        Raises:
            any exception raised by the SSHClient object's connect method.
    """
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(host, username=user, password=password)
    return ssh


# def get_directory_and_file(local_filepath=None):
#     """
#         Method that parses a filepath and extracts a filename
#         and its coresponding directory.
#
#         Args:
#             local_filepath (string): a unix filepath.
#             e.g: ~/Desktop/file.txt
#
#         Returns:
#             tuple: A tuple with a unlix directory path and
#                    the file to be synced with the remote system.
#
#         Raises:
#             ArgumentTypeError: if the given path is invalid.
#     """
#     if '/' in local_filepath and os.path.isfile(local_filepath):
#         file_dir, filename = local_filepath.split('/')
#         # append a / character to file_dir to define a valid directory path
#         file_dir += '/'
#         return (file_dir, filename)
#     else:
#         raise argparse.ArgumentTypeError('Invalid argument {}\n'.format(local_filepath))


def get_user_host_and_path(remote_location=None):
    """
        Method that parses a scp-like remote path and extracts
        the remote user, the remote host and the path where the synced
        file will be placed if it doesn't exist.

        Args:
            remote_location (string): a scp-like remote location.
            e.g: user@host:~/Desktop/

        Returns:
            tuple: A tuple with the remote user, the remote host
                   and the path to the directory in which the synced
                   file will be placed.

        Raises:
            ArgumentTypeError: if the given remote location is invalid.
    """
    try:
        remote_user_host, remote_path = remote_location.split(':')
        user, host = remote_user_host.split("@")
        return (user, host, remote_path)
    except ValueError:
        # catching a value error means that the split failed,
        # therefore the second arg is invalid
        raise argparse.ArgumentTypeError('Invalid argument {}\n'.format(remote_location))

def determine_common_dir(paths):
    pass
