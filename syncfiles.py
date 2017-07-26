import argparse
import logging
import getpass
import time
import os
import sys
from remote_file_sync.utils import get_user_host_and_path, get_ssh_client
from remote_file_sync.handlers import FileWatcher, DirWatcher
from watchdog.observers import Observer


def _init():
    # instantiate parser
    parser = argparse.ArgumentParser(description='Sync a local file with a remote system.')
    parser.add_argument('local_directory', type=str,
                        help='unix-like paths to the directory to sync with the remote system. e.g: /path/to/dir')
    parser.add_argument('-r', dest='recursive', action='store_true',
                        help='also sync subfolders of the given folder')
    parser.add_argument('-f', dest='files', nargs='+',
                        help='name of files from the given directory to be synced with the remote system. e.g: file1.txt file2.py, file3')
    parser.add_argument('remote_location', type=str,
                        help='scp-like remote destination. e.g: user@host:/some/path')
    parser.set_defaults(recursive=False, files=None)

    # configure logger
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    return parser


def main():
    try:
        local_directory = args.local_directory
        remote_location = args.remote_location
        recursive = args.recursive
        files = args.files
        # validate the directory argument
        if not os.path.isdir:
            raise argparse.ArgumentTypeError('{} is not a directory\n'.format(local_directory))
        # this will raise argument error if the second paramter is invalid
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
                        raise argparse.ArgumentTypeError('{} is not a file\n'.format(full_filepath))
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
    except argparse.ArgumentTypeError as arg_err:
        args_parser.error(str(arg_err))
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
    except Exception as ex:
        logging.error(str(ex))
        sys.exit(-1)


if __name__ == '__main__':
    args_parser = _init()
    args = args_parser.parse_args()

    main(args)