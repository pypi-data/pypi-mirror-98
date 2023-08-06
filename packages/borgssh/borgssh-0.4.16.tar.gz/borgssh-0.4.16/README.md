# Project borgssh

This package simplifies the **borgbackup** use with a ssh server
on a (remote) computer.

## Usage

```
NAME
    sshborg

SYNOPSIS
    sshborg COMMAND

COMMANDS
    COMMAND is one of the following:

     list
       FIRST of the global commands: borg list ssh://borg@***:2222/config/borg

     create_and_prune_defaults
       SECOND of the global commands, use: sshborg create_and_prune_defaults --configfile ~/.borgssh.conf

     check
       borg check --info ssh://borg@***:2222/config/borg borg info ssh://borg@***:2222/config/borg

     create
       borg create ssh://borg@***:2222/config/borg::host_folder

     extract
       borg extract --dry-run --list ssh://borg@***:2222/config/borg::host_folder_***
```

## Remarks
   - port 2222 is hardcoded
   - username borg is hardcoded
   - prune is hardcoded (7 days, some weeks (8?), every month)

## Configuration

 The config is in `~/.borgssh.conf` by default, but can be in another file
 and sshborg is run with `-c configfile` option.

 The example of the config:
 ```
 {
 "config": "~/.borgssh.conf",
 "remote": "192.168.0.200",
 "default_folders": [
  "~/x_Lectures",
  "~/x_DATA_ANALYSIS"
 ],
 "quit": false
}
```

## Server

In general, it is ok to use a prepared docker with ssh server:

```
docker run -d  --name=openssh-server   --hostname=openssh-server  -e  PUID=1000   -e PGID=1000   -e TZ=Europe/London     -e SUDO_ACCESS=true   -e PASSWORD_ACCESS=true   -e USER_PASSWORD=mysecretpassword   -e USER_NAME=borg   -p 2222:2222   -v /media/raiddisks:/config   --restart unless-stopped   ghcr.io/linuxserver/openssh-server
```

and install borgbackup inside.
```
ssh borg@127.0.0.1 -p 2222
sudo borg
apk update && apk add borgbackup --upgrade
```

then
 - commit the docker with a new name like `openssh-server-borg`, setup
the `authorized_keys` to restrict ssh

```
command="/usr/bin/borg serve --restrict-to-path /config/borg" ssh-rsa AAAAB @giga
```

and the final docker can be run...

```
docker run -d  --name=openssh-server-borg   --hostname=openssh-server-borg  -e  PUID=1000   -e PGID=1000   -e TZ=Europe/London    -e SUDO_ACCESS=false   -e PASSWORD_ACCESS=false   -e USER_PASSWORD=mysecretpassword   -e USER_NAME=borg   -p 2222:2222   -v /mnt/raiddisks/borgssh:/config   --restart unless-stopped   openssh-server-borg
```

Borgbackup must be probably init-ed like: `borg init ssh://borg@127.0.0.1:2222/config/borg -e none`


## gitlab:

https://gitlab.com/jaromrax/sshborg
