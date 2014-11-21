Use the command `sudo yum --disablerepo="*"
--enablerepo="lantw44-gnome-restore-gtk-icons" reinstall
gnome-settings-daemon gsettings-desktop-schemas`
to replace the official packages with the patched packages.

After installing these patched packages, use the following command to enable
GTK+ icon and image support. You have to logout and re-login for the change to
take effect.

`gsettings set org.gnome.desktop.interface buttons-have-icons true`  
`gsettings set org.gnome.desktop.interface menus-have-icons true`

_WARNING: You must reinstall both `gnome-settings-daemon` and
`gsettings-desktop-schemas`. If you only reinstall one of them, your GNOME
Shell may fail to start._

