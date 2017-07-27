# sync-files

command line tool used for synchronizing a directory with a remote system

## Prerequisites

This tool has an external dependency to [rsync](https://linux.die.net/man/1/rsync) in order to do the initial mapping of the folders with the remote system.

[rsync](https://linux.die.net/man/1/rsync) is bundled with the vast majority of linux distributions but if somehow it is missing from your system, you can manually install it using the corresponding package manager of the linux distribution.

For instance, for debian distributions of linux you can install it by typing:

```
sudo apt-get install rsync
```

## Install

To install this tool you must first download the sources and then run the following command in the root directory of the project;

```
sudo pip3 install .
```
The tool must be installed with escalated privileges because it places a binary file in the /usr/local/bin protected directory so that the tool can be used from command line;

## Usage

If the installation was successful you can use this tool as any other command line tool.
Here is an example:

```
sync-files /path/to/dir user@host:/path/to/synced/dir
```

For more information on how to use this, you can type:

```
sync-files --help
```