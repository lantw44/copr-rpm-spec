`dnf install chromium`

If you get a SELinux error when running NaCl extensions, please run the command

`semanage fcontext -a -t bin_t '/home/.*/\.config/chromium/.*/Extensions/.*/.*/plugin/pnacl/.*\.nexe'`

as root and run

`restorecon -R ~/.config/chromium`

as your user to set correct SELinux types.
