The post-install script will create an user and a group called `guix-builder`.

If you want more users for building packages, add more users to the
`guix-builder` group.

Start the `guix-daemon` by using systemd or manually running command
`guix-daemon --build-users-group=guix-builder` as root. `guix-daemon`
will create most necessary files and directories when you first using it.
