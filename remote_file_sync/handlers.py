import logging
import os
import shlex
from scp import SCPClient
from watchdog.events import FileSystemEventHandler, PatternMatchingEventHandler, FileModifiedEvent
from subprocess import check_call, DEVNULL

class DirWatcher(FileSystemEventHandler):

    def __init__(self, ssh, root_directory, destination):
        super(DirWatcher, self).__init__()
        self._can_send = True
        self._root_directory = root_directory
        self._destination = destination
        self._sftp = ssh.open_sftp()

    def reset_lock(self):
        self._can_send = True

    def _sync(self, path):
        directory, file = os.path.split(path)
        subdirs = directory.split("/")[1:] if "/" in directory else ['']
        print("dirname: {}".format(subdirs))
        print("filename: {}".format(file))
        f_path = None
        for dir in subdirs:
            f_path = "/".join(dir)
        f_path += "/"+file
        print(f_path)
        self._sftp.put(path, self._destination+f_path)
        logging.info("Folder synced successfully")

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
        logging.info("File synced successfully")

    def on_modified(self, event):
        super(FileWatcher, self).on_modified(event)
        if self._can_send:
            self._sync(event.src_path)
            self._can_send = False