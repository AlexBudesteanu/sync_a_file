import logging
import os
from scp import SCPClient
from watchdog.events import FileSystemEventHandler, PatternMatchingEventHandler, FileModifiedEvent
from subprocess import check_call, DEVNULL
from functools import reduce

class DirWatcher(FileSystemEventHandler):

    def __init__(self, ssh, root_directory, remote_location):
        super(DirWatcher, self).__init__()
        self._can_send = True
        self._root_directory = root_directory
        self._remote_location = remote_location
        self._sftp = ssh.open_sftp()
        # map folders and files here so that when a file
        # will modify you will not get a file doesn't exist error
        self._map_structure()

    def reset_lock(self):
        self._can_send = True

    def _map_structure(self):
        # for simplicity, we will use rsync.
        rsync_command = "rsync -a {} {}".format(self._root_directory, self._remote_location)
        check_call(rsync_command, stdout=DEVNULL, stderr=DEVNULL, shell=True)

    def _sync(self, path):
        # if the remote_location contains a / we must map a remote root, otherwise the root will be ~ (user home)
        remote_root_folder = self._remote_location.split('/')[-1] if '/' in self._remote_location else None
        partial_path = reduce(lambda final_path, partial_path: final_path + '/' + partial_path, path.split('/')[1:])
        remote_path = remote_root_folder + '/' + partial_path if remote_root_folder else partial_path
        logging.info(remote_path)
        self._sftp.put(path, remote_path)
        logging.info("{} synced successfully".format(path))

    def on_modified(self, event):
        # 'and' clause added because of the way some editors handle file edits
        if isinstance(event, FileModifiedEvent) and os.path.isfile(event.src_path):
            super(DirWatcher, self).on_modified(event)
            if self._can_send:
                self._sync(event.src_path)
                self._can_send = False

class FileWatcher(PatternMatchingEventHandler):

    def __init__(self, ssh_client, destination, **kwargs):
        super(FileWatcher, self).__init__(**kwargs)
        self._can_send = True
        self._ssh_client = ssh_client
        self._destination = destination

    def reset_lock(self):
        self._can_send = True

    def _sync(self, file):
        with SCPClient(self._ssh_client.get_transport()) as scp:
            scp.put(file, self._destination)
        logging.info("{} synced successfully".format(file))

    def on_modified(self, event):
        super(FileWatcher, self).on_modified(event)
        if self._can_send:
            self._sync(event.src_path)
            self._can_send = False