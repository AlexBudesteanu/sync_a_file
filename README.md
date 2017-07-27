# sync_files

command line tool used for syncronizing a directory with a remote system

## Prerequisites

This tool has an external dependency to rsync [rsync](https://linux.die.net/man/1/rsync) in order to do the initial mapping of the folders with the remote system.
rsync is bundled with the vast majority of linux distributions but if somehow it is missing from your system, you can manually install it using the corresponding package manager of the linux distribution.

For instance, for debian distributions of linux you can install rsync by typing:

```
sudo apt-get install rsync
```

## Installing

To install this tool you must first download the sources and then run the following command in the root directory of the project

```
sudo pip3 install .
```
The tool must be installed with escalated privileges because it places a binary file in the /usr/local/bin protected directory so that the tool can be used from command line

## Usage

You can use this tool as any other command line tool.
Here is an example:

```
sync-files /path/to/dir user@host:/path/to/synced/dir
```

For more information on how to use this tool you can type:

```
sync-files --help
```