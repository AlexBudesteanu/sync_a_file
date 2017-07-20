import logging
import os
from scp import SCPClient
from watchdog.events import FileSystemEventHandler, PatternMatchingEventHandler, FileModifiedEvent

class DirWatcher(FileSystemEventHandler):

    def __init__(self, ssh_client, root_directory, destination):
        super(DirWatcher, self).__init__()
        self._can_send = True
        self._ssh_client = ssh_client
        self._destination = destination
        self._root_directory = root_directory

    def reset_lock(self):
        self._can_send = True

    def _upload(self, file):
        with SCPClient(self._ssh_client.get_transport()) as scp:
            scp.put(file, self._destination)
        logging.info("File synced successfully")

    def on_modified(self, event):
        if isinstance(event, FileModifiedEvent) and os.path.isfile(event.src_path):
            logging.info(event.src_path)
            super(DirWatcher, self).on_modified(event)
            if self._can_send:
                self._upload(event.src_path)
                self._can_send = False

class FileWatcher(PatternMatchingEventHandler):

    def __init__(self, ssh_client, destination, **kwargs):
        super(FileWatcher, self).__init__(**kwargs)
        self._can_send = True
        self._ssh_client = ssh_client
        self._destination = destination

    def reset_lock(self):
        self._can_send = True

    def _upload(self, file):
        with SCPClient(self._ssh_client.get_transport()) as scp:
            scp.put(file, self._destination)
        logging.info("File synced successfully")

    def on_modified(self, event):
        super(FileWatcher, self).on_modified(event)
        if self._can_send:
            self._upload(event.src_path)
            self._can_send = False