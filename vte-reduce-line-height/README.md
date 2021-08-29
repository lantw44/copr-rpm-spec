Reduce the minimum line height in VTE, so you are not forced to waste vertical
space if VTE 0.64 decides the line height should be larger than previous
versions for your environment. This issue has been reported to VTE as
[#347](https://gitlab.gnome.org/GNOME/vte/-/issues/347) and it is known to
affect some users of Noto CJK fonts. This patch works around the issue by
disabling the new way to calculate line height introduced in VTE 0.64.
