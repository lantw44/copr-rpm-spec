The post-install script will create an user and a group called `guixbuild`.

If you want more users for building packages, add more users to the
`guixbuild` group.

Start the `guix-daemon` by using systemd or manually running command
`guix-daemon --build-users-group=guixbuild` as root. `guix-daemon`
will create most necessary files and directories when you first using it.

If you want to use prebuilt packages provided by
[GNU Hydra](https://hydra.gnu.org), you should run
`guix archive --authorize --import < /usr/share/guix/hydra.gnu.org.pub`
as root before using `guix package`.
