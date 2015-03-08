`yum install chromium`

If you find that all hardware acceleration is disabled in `chrome://gpu`, it
is likely that you DRI3 support is broken. Please add `LIBGL_DRI3_DISABLE=1`
to your environment variables to workaround it.

If you get a SELinux error when running NaCl extensions, please run the command
`semanage fcontext -a -t bin_t '/home/.*/\.config/chromium/.*/Extensions/.*/.*/plugin/pnacl/.*\.nexe'`
as root and run `restorecon -R ~/.config/chromium` as your user to set correct
SELinux types.
