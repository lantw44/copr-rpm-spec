`yum install chromium`

If you find that all hardware acceleration is disabled in `chrome://gpu`, it
is likely that you DRI3 support is broken. Please add `LIBGL_DRI3_DISABLE=1`
to your environment variables to workaround it.
