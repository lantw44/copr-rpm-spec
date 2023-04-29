The post-install script will create an user and a group called `guixbuild`.

If you want more users for building packages, add more users to the
`guixbuild` group.

Start the `guix-daemon` by using systemd or manually running command
`guix-daemon --build-users-group=guixbuild` as root. `guix-daemon`
will create most necessary files and directories when you first using it.

If you want to use prebuilt packages, you should run
`for i in /usr/share/guix/*.pub; do guix archive --authorize < "$i"; done`
as root before using `guix package`.
