import logging
import getpass
import time
import os
import click
from remote_file_sync.utils import get_user_host_and_path, get_ssh_client
from remote_file_sync.handlers import FileWatcher, DirWatcher
from watchdog.observers import Observer

@click.command()
@click.argument('local_directory', type=click.Path(exists=True))
@click.argument('remote_location', type=str)
@click.option('-f', default=None, multiple=True, help='name of the files from the given directory to be synced with the remote system. e.g: file1.txt file2.py, file3')
@click.option('-r', is_flag=True, help='also sync subfolders of the given folder')
def main(local_directory, remote_location, **kwargs):
    """
    Sync a local directory with a remote system.

    :param: local_directory: unix-like paths to the directory to sync with the remote system. e.g: /path/to/dir
    :param: remote_location: scp-like remote destination. e.g: user@host: /some/path
    """

    # unwrapping optional values into more suggestive variables
    files = kwargs.get('f')
    recursive = kwargs.get('r')

    # configure logger
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    try:
        # this will raise value error if the second parameter is invalid
        user, host, remote_dir = get_user_host_and_path(remote_location)
        # the password for the user you mentioned in the second argument
        password = getpass.getpass("{}@{}'s password:".format(user, host))

        with get_ssh_client(host, user, password) as ssh:
            # check if -f argument is present
            if files:
                patterns=[]
                # check if all files exist
                for file in files:
                    full_filepath = local_directory+file
                    if os.path.isfile(full_filepath):
                        patterns.append(full_filepath)
                    else:
                        raise Exception('{} is not a file\n'.format(full_filepath))
                # instantiate PatternMatchingEventHandler
                event_handler = FileWatcher(ssh, remote_dir, patterns=patterns)
            else:
                # instantiate FileSystemEventHandler
                event_handler = DirWatcher(ssh, local_directory, remote_location)
            observer = Observer()
            observer.schedule(event_handler, local_directory, recursive)
            observer.start()
            logging.info("Watcher is now active.")
            while True:
                time.sleep(1)
                event_handler.reset_lock()
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        return 0
    except Exception as ex:
        logging.error(str(ex))
        return -1
