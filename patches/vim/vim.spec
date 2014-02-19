%define patchlevel 179
%if %{?WITH_SELINUX:0}%{!?WITH_SELINUX:1}
%define WITH_SELINUX 1
%endif
%define desktop_file 1
%if %{desktop_file}
%define desktop_file_utils_version 0.2.93
%endif

%define withnetbeans 1

%define withvimspell 0
%define withhunspell 0
%define withruby 1

%define baseversion 7.4
%define vimdir vim74

Summary: The VIM editor (Copr: lantw44/patches)
URL:     http://www.vim.org/
Name: vim
Version: %{baseversion}.%{patchlevel}
Release: 1%{?dist}
License: Vim
Group: Applications/Editors
Source0: ftp://ftp.vim.org/pub/vim/unix/vim-%{baseversion}.tar.bz2
Source3: gvim.desktop
Source4: vimrc
Source5: ftp://ftp.vim.org/pub/vim/patches/README.patches
Source7: gvim16.png
Source8: gvim32.png
Source9: gvim48.png
Source10: gvim64.png
Source11: Changelog.rpm
Source12: vi_help.txt
%if %{withvimspell}
Source13: vim-spell-files.tar.bz2
%endif
Source14: spec-template
Source15: spec-template.new

Patch2002: vim-7.0-fixkeys.patch
Patch2003: vim-6.2-specsyntax.patch
%if %{withhunspell}
Patch2011: vim-7.0-hunspell.patch
BuildRequires: hunspell-devel
%endif
# If you're as lazy as me, generate the list using
# for i in `seq 1 14`; do printf "Patch%03d: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.%03d\n" $i $i; done
Patch001: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.001
Patch002: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.002
Patch003: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.003
Patch004: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.004
Patch005: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.005
Patch006: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.006
Patch007: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.007
Patch008: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.008
Patch009: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.009
Patch010: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.010
Patch011: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.011
Patch012: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.012
Patch013: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.013
Patch014: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.014
Patch015: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.015
Patch016: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.016
Patch017: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.017
Patch018: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.018
Patch019: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.019
Patch020: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.020
Patch021: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.021
Patch022: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.022
Patch023: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.023
Patch024: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.024
Patch025: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.025
Patch026: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.026
Patch027: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.027
Patch028: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.028
Patch029: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.029
Patch030: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.030
Patch031: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.031
Patch032: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.032
Patch033: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.033
Patch034: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.034
Patch035: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.035
Patch036: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.036
Patch037: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.037
Patch038: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.038
Patch039: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.039
Patch040: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.040
Patch041: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.041
Patch042: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.042
Patch043: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.043
Patch044: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.044
Patch045: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.045
Patch046: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.046
Patch047: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.047
Patch048: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.048
Patch049: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.049
Patch050: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.050
Patch051: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.051
Patch052: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.052
Patch053: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.053
Patch054: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.054
Patch055: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.055
Patch056: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.056
Patch057: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.057
Patch058: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.058
Patch059: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.059
Patch060: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.060
Patch061: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.061
Patch062: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.062
Patch063: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.063
Patch064: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.064
Patch065: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.065
Patch066: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.066
Patch067: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.067
Patch068: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.068
Patch069: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.069
Patch070: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.070
Patch071: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.071
Patch072: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.072
Patch073: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.073
Patch074: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.074
Patch075: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.075
Patch076: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.076
Patch077: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.077
Patch078: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.078
Patch079: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.079
Patch080: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.080
Patch081: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.081
Patch082: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.082
Patch083: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.083
Patch084: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.084
Patch085: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.085
Patch086: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.086
Patch087: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.087
Patch088: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.088
Patch089: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.089
Patch090: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.090
Patch091: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.091
Patch092: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.092
Patch093: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.093
Patch094: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.094
Patch095: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.095
Patch096: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.096
Patch097: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.097
Patch098: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.098
Patch099: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.099
Patch100: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.100
Patch101: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.101
Patch102: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.102
Patch103: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.103
Patch104: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.104
Patch105: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.105
Patch106: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.106
Patch107: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.107
Patch108: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.108
Patch109: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.109
Patch110: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.110
Patch111: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.111
Patch112: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.112
Patch113: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.113
Patch114: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.114
Patch115: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.115
Patch116: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.116
Patch117: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.117
Patch118: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.118
Patch119: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.119
Patch120: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.120
Patch121: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.121
Patch122: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.122
Patch123: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.123
Patch124: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.124
Patch125: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.125
Patch126: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.126
Patch127: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.127
Patch128: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.128
Patch129: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.129
Patch130: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.130
Patch131: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.131
Patch132: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.132
Patch133: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.133
Patch134: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.134
Patch135: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.135
Patch136: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.136
Patch137: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.137
Patch138: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.138
Patch139: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.139
Patch140: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.140
Patch141: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.141
Patch142: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.142
Patch143: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.143
Patch144: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.144
Patch145: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.145
Patch146: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.146
Patch147: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.147
Patch148: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.148
Patch149: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.149
Patch150: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.150
Patch151: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.151
Patch152: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.152
Patch153: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.153
Patch154: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.154
Patch155: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.155
Patch156: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.156
Patch157: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.157
Patch158: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.158
Patch159: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.159
Patch160: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.160
Patch161: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.161
Patch162: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.162
Patch163: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.163
Patch164: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.164
Patch165: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.165
Patch166: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.166
Patch167: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.167
Patch168: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.168
Patch169: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.169
Patch170: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.170
Patch171: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.171
Patch172: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.172
Patch173: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.173
Patch174: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.174
Patch175: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.175
Patch176: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.176
Patch177: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.177
Patch178: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.178
Patch179: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.179

Patch3000: vim-7.4-syntax.patch
Patch3002: vim-7.1-nowarnings.patch
Patch3004: vim-7.0-rclocation.patch
Patch3006: vim-6.4-checkhl.patch
Patch3007: vim-7.4-fstabsyntax.patch
Patch3008: vim-7.0-warning.patch
Patch3009: vim-7.0-syncolor.patch
Patch3010: vim-7.0-specedit.patch
Patch3011: vim72-rh514717.patch
Patch3012: vim-7.3-manpage-typo-668894-675480.patch
Patch3013: vim-7.3-xsubpp-path.patch
Patch3014: vim-manpagefixes-948566.patch

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: python-devel ncurses-devel gettext perl-devel lua-devel
BuildRequires: perl(ExtUtils::Embed) perl(ExtUtils::ParseXS)
BuildRequires: libacl-devel gpm-devel autoconf
%if %{WITH_SELINUX}
BuildRequires: libselinux-devel
%endif
%if "%{withruby}" == "1"
Buildrequires: ruby-devel ruby
%endif
%if %{desktop_file}
# for /usr/bin/desktop-file-install
Requires: desktop-file-utils
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
%endif
Epoch: 2
Conflicts: filesystem < 3

%description
Copr: lantw44/patches
Note: This is a modified package. Install it if you want Lua intepreter
support in Vim.

VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.

%package common
Summary: The common files needed by any version of the VIM editor (Copr: lantw44/patches)
Group: Applications/Editors
Conflicts: man-pages-fr < 0.9.7-14
Conflicts: man-pages-it < 0.3.0-17
Conflicts: man-pages-pl < 0.24-2
Requires: %{name}-filesystem

%description common
Copr: lantw44/patches
Note: This is a modified package. Install it if you want Lua intepreter
support in Vim.

VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-common package contains files which every VIM binary will need in
order to run.

If you are installing vim-enhanced or vim-X11, you'll also need
to install the vim-common package.

%package spell
Summary: The dictionaries for spell checking. This package is optional (Copr: lantw44/patches)
Group: Applications/Editors
Requires: vim-common = %{epoch}:%{version}-%{release}

%description spell
Copr: lantw44/patches
Note: This is a modified package. Install it if you want Lua intepreter
support in Vim.

This subpackage contains dictionaries for vim spell checking in
many different languages.

%package minimal
Summary: A minimal version of the VIM editor (Copr: lantw44/patches)
Group: Applications/Editors
Provides: vi = %{version}-%{release}
Provides: /bin/vi

%description minimal
Copr: lantw44/patches
Note: This is a modified package. Install it if you want Lua intepreter
support in Vim.

VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more. The
vim-minimal package includes a minimal version of VIM, which is
installed into /bin/vi for use when only the root partition is
present. NOTE: The online help is only available when the vim-common
package is installed.

%package enhanced
Summary: A version of the VIM editor which includes recent enhancements (Copr: lantw44/patches)
Group: Applications/Editors
Requires: vim-common = %{epoch}:%{version}-%{release} which
Provides: vim = %{version}-%{release}
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description enhanced
Copr: lantw44/patches
Note: This is a modified package. Install it if you want Lua intepreter
support in Vim.

VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-enhanced package contains a version of VIM with extra, recently
introduced features like Python and Perl interpreters.

Install the vim-enhanced package if you'd like to use a version of the
VIM editor which includes recently added enhancements like
interpreters for the Python and Perl scripting languages.  You'll also
need to install the vim-common package.

%package filesystem
Summary: VIM filesystem layout (Copr: lantw44/patches)
Group: Applications/Editors

%Description filesystem
This package provides some directories which are required by other
packages that add vim files, p.e.  additional syntax files or filetypes.

%package X11
Summary: The VIM version of the vi editor for the X Window System (Copr: lantw44/patches)
Group: Applications/Editors
Requires: vim-common = %{epoch}:%{version}-%{release} libattr >= 2.4 gtk2 >= 2.6
Provides: gvim = %{version}-%{release}
BuildRequires: gtk2-devel libSM-devel libXt-devel libXpm-devel
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires: hicolor-icon-theme

%description X11
Copr: lantw44/patches
Note: This is a modified package. Install it if you want Lua intepreter
support in Vim.

VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and
more. VIM-X11 is a version of the VIM editor which will run within the
X Window System.  If you install this package, you can run VIM as an X
application with a full GUI interface and mouse support.

Install the vim-X11 package if you'd like to try out a version of vi
with graphics and mouse capabilities.  You'll also need to install the
vim-common package.

%prep
%setup -q -b 0 -n %{vimdir}
# fix rogue dependencies from sample code
chmod -x runtime/tools/mve.awk
%patch2002 -p1
%patch2003 -p1
%if %{withhunspell}
%patch2011 -p1
%endif
perl -pi -e "s,bin/nawk,bin/awk,g" runtime/tools/mve.awk

# Base patches...
# for i in `seq 1 14`; do printf "%%patch%03d -p0 \n" $i; done
%patch001 -p0
%patch002 -p0
%patch003 -p0
%patch004 -p0
%patch005 -p0
%patch006 -p0
%patch007 -p0
%patch008 -p0
%patch009 -p0
%patch010 -p0
%patch011 -p0
%patch012 -p0
%patch013 -p0
%patch014 -p0
%patch015 -p0
%patch016 -p0
%patch017 -p0
%patch018 -p0
%patch019 -p0
%patch020 -p0
%patch021 -p0
%patch022 -p0
%patch023 -p0
%patch024 -p0
%patch025 -p0
%patch026 -p0
%patch027 -p0
%patch028 -p0
%patch029 -p0
%patch030 -p0
%patch031 -p0
%patch032 -p0
%patch033 -p0
%patch034 -p0
%patch035 -p0
%patch036 -p0
%patch037 -p0
%patch038 -p0
%patch039 -p0
%patch040 -p0
%patch041 -p0
%patch042 -p0
%patch043 -p0
%patch044 -p0
%patch045 -p0
%patch046 -p0
%patch047 -p0
%patch048 -p0
%patch049 -p0
%patch050 -p0
%patch051 -p0
%patch052 -p0
%patch053 -p0
%patch054 -p0
%patch055 -p0
%patch056 -p0
%patch057 -p0
%patch058 -p0
%patch059 -p0
%patch060 -p0
%patch061 -p0
%patch062 -p0
%patch063 -p0
%patch064 -p0
%patch065 -p0
%patch066 -p0
%patch067 -p0
%patch068 -p0
%patch069 -p0
%patch070 -p0
%patch071 -p0
%patch072 -p0
%patch073 -p0
%patch074 -p0
%patch075 -p0
%patch076 -p0
%patch077 -p0
%patch078 -p0
%patch079 -p0
%patch080 -p0
%patch081 -p0
%patch082 -p0
%patch083 -p0
%patch084 -p0
%patch085 -p0
%patch086 -p0
%patch087 -p0
%patch088 -p0
%patch089 -p0
%patch090 -p0
%patch091 -p0
%patch092 -p0
%patch093 -p0
%patch094 -p0
%patch095 -p0
%patch096 -p0
%patch097 -p0
%patch098 -p0
%patch099 -p0
%patch100 -p0
%patch101 -p0
%patch102 -p0
%patch103 -p0
%patch104 -p0
%patch105 -p0
%patch106 -p0
%patch107 -p0
%patch108 -p0
%patch109 -p0
%patch110 -p0
%patch111 -p0
%patch112 -p0
%patch113 -p0
%patch114 -p0
%patch115 -p0
%patch116 -p0
%patch117 -p0
%patch118 -p0
%patch119 -p0
%patch120 -p0
%patch121 -p0
%patch122 -p0
%patch123 -p0
%patch124 -p0
%patch125 -p0
%patch126 -p0
%patch127 -p0
%patch128 -p0
%patch129 -p0
%patch130 -p0
%patch131 -p0
%patch132 -p0
%patch133 -p0
%patch134 -p0
%patch135 -p0
%patch136 -p0
%patch137 -p0
%patch138 -p0
%patch139 -p0
%patch140 -p0
%patch141 -p0
%patch142 -p0
%patch143 -p0
%patch144 -p0
%patch145 -p0
%patch146 -p0
%patch147 -p0
%patch148 -p0
%patch149 -p0
%patch150 -p0
%patch151 -p0
%patch152 -p0
%patch153 -p0
%patch154 -p0
%patch155 -p0
%patch156 -p0
%patch157 -p0
%patch158 -p0
%patch159 -p0
%patch160 -p0
%patch161 -p0
%patch162 -p0
%patch163 -p0
%patch164 -p0
%patch165 -p0
%patch166 -p0
%patch167 -p0
%patch168 -p0
%patch169 -p0
%patch170 -p0
%patch171 -p0
%patch172 -p0
%patch173 -p0
%patch174 -p0
%patch175 -p0
%patch176 -p0
%patch177 -p0
%patch178 -p0
%patch179 -p0

# install spell files
%if %{withvimspell}
%{__tar} xjf %{SOURCE13}
%endif

%patch3000 -p1
%patch3002 -p1
%patch3004 -p1
%patch3006 -p1
%patch3007 -p1
%patch3008 -p1
%patch3009 -p1
%patch3010 -p1
%patch3011 -p1
%patch3012 -p1

%if %{?fedora}%{!?fedora:0} >= 20 || %{?rhel}%{!?rhel:0} >= 7
%patch3013 -p1
%endif
%patch3014 -p1

%build
cp -f %{SOURCE5} .
cd src
autoconf

sed -e "s+VIMRCLOC	= \$(VIMLOC)+VIMRCLOC	= /etc+" Makefile > Makefile.tmp
mv -f Makefile.tmp Makefile

export CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2"
export CXXFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2"

%configure --with-features=huge \
  --enable-pythoninterp=dynamic \
  --enable-perlinterp \
  --disable-tclinterp --with-x=yes \
  --enable-xim --enable-multibyte \
  --with-tlib=ncurses \
  --enable-gtk2-check --enable-gui=gtk2 \
  --with-compiledby="<bugzilla@redhat.com>" --enable-cscope \
  --with-modified-by="<bugzilla@redhat.com>" \
  --enable-luainterp \
%if "%{withnetbeans}" == "1"
  --enable-netbeans \
%else
  --disable-netbeans \
%endif
%if %{WITH_SELINUX}
  --enable-selinux \
%else
  --disable-selinux \
%endif
%if "%{withruby}" == "1"
  --enable-rubyinterp=dynamic \
%else
  --disable-rubyinterp \
%endif

make VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir} %{?_smp_mflags}
cp vim gvim
make clean

%configure --prefix=%{_prefix} --with-features=huge \
 --enable-pythoninterp=dynamic \
 --enable-perlinterp \
 --disable-tclinterp \
 --with-x=no \
 --enable-gui=no --exec-prefix=%{_prefix} --enable-multibyte \
 --enable-cscope --with-modified-by="<bugzilla@redhat.com>" \
 --with-tlib=ncurses \
 --with-compiledby="<bugzilla@redhat.com>" \
 --enable-luainterp \
%if "%{withnetbeans}" == "1"
  --enable-netbeans \
%else
  --disable-netbeans \
%endif
%if %{WITH_SELINUX}
  --enable-selinux \
%else
  --disable-selinux \
%endif
%if "%{withruby}" == "1"
  --enable-rubyinterp=dynamic \
%else
  --disable-rubyinterp \
%endif

make VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir} %{?_smp_mflags}
cp vim enhanced-vim
make clean

perl -pi -e "s/help.txt/vi_help.txt/"  os_unix.h ex_cmds.c
perl -pi -e "s/\/etc\/vimrc/\/etc\/virc/"  os_unix.h
%configure --prefix=%{_prefix} --with-features=small --with-x=no \
  --enable-multibyte \
  --disable-netbeans \
%if %{WITH_SELINUX}
  --enable-selinux \
%else
  --disable-selinux \
%endif
  --disable-pythoninterp --disable-perlinterp --disable-tclinterp \
  --with-tlib=ncurses --enable-gui=no --disable-gpm --exec-prefix=/ \
  --with-compiledby="<bugzilla@redhat.com>" \
  --with-modified-by="<bugzilla@redhat.com>"

make VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir} %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_datadir}/%{name}/vimfiles/{after,autoload,colors,compiler,doc,ftdetect,ftplugin,indent,keymap,lang,plugin,print,spell,syntax,tutor}
mkdir -p %{buildroot}/%{_datadir}/%{name}/vimfiles/after/{autoload,colors,compiler,doc,ftdetect,ftplugin,indent,keymap,lang,plugin,print,spell,syntax,tutor}
cp -f %{SOURCE11} .
%if %{?fedora}%{!?fedora:0} >= 16 || %{?rhel}%{!?rhel:0} >= 6
cp -f %{SOURCE15} %{buildroot}/%{_datadir}/%{name}/vimfiles/template.spec
%else
cp -f %{SOURCE14} %{buildroot}/%{_datadir}/%{name}/vimfiles/template.spec
%endif
cp runtime/doc/uganda.txt LICENSE
# Those aren't Linux info files but some binary files for Amiga:
rm -f README*.info


cd src
make install DESTDIR=%{buildroot} BINDIR=%{_bindir} VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir}
make installgtutorbin  DESTDIR=%{buildroot} BINDIR=%{_bindir} VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{16x16,32x32,48x48,64x64}/apps
install -m755 vim %{buildroot}%{_bindir}/vi
install -m755 enhanced-vim %{buildroot}%{_bindir}/vim
install -m755 gvim %{buildroot}%{_bindir}/gvim
install -p -m644 %{SOURCE7} \
   %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/gvim.png
install -p -m644 %{SOURCE8} \
   %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/gvim.png
install -p -m644 %{SOURCE9} \
   %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/gvim.png
install -p -m644 %{SOURCE10} \
   %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/gvim.png

( cd %{buildroot}
  ln -sf vi ./%{_bindir}/rvi
  ln -sf vi ./%{_bindir}/rview
  ln -sf vi ./%{_bindir}/view
  ln -sf vi ./%{_bindir}/ex
  ln -sf vim ./%{_bindir}/rvim
  ln -sf vim ./%{_bindir}/vimdiff
  perl -pi -e "s,%{buildroot},," .%{_mandir}/man1/vim.1 .%{_mandir}/man1/vimtutor.1
  rm -f .%{_mandir}/man1/rvim.1
  ln -sf vim.1.gz .%{_mandir}/man1/vi.1.gz
  ln -sf vim.1.gz .%{_mandir}/man1/rvi.1.gz
  ln -sf vim.1.gz .%{_mandir}/man1/vimdiff.1.gz
  ln -sf gvim ./%{_bindir}/gview
  ln -sf gvim ./%{_bindir}/gex
  ln -sf gvim ./%{_bindir}/evim
  ln -sf gvim ./%{_bindir}/gvimdiff
  ln -sf gvim ./%{_bindir}/vimx
  %if "%{desktop_file}" == "1"
    mkdir -p %{buildroot}/%{_datadir}/applications
    desktop-file-install \
    %if 0%{?fedora} && 0%{?fedora} < 19
        --vendor fedora \
    %endif
        --dir %{buildroot}/%{_datadir}/applications \
        %{SOURCE3}
        # --add-category "Development;TextEditor;X-Red-Hat-Base" D\
  %else
    mkdir -p ./%{_sysconfdir}/X11/applnk/Applications
    cp %{SOURCE3} ./%{_sysconfdir}/X11/applnk/Applications/gvim.desktop
  %endif
  # ja_JP.ujis is obsolete, ja_JP.eucJP is recommended.
  ( cd ./%{_datadir}/%{name}/%{vimdir}/lang; \
    ln -sf menu_ja_jp.ujis.vim menu_ja_jp.eucjp.vim )
)

pushd %{buildroot}/%{_datadir}/%{name}/%{vimdir}/tutor
mkdir conv
   iconv -f CP1252 -t UTF8 tutor.ca > conv/tutor.ca
   iconv -f CP1252 -t UTF8 tutor.it > conv/tutor.it
   #iconv -f CP1253 -t UTF8 tutor.gr > conv/tutor.gr
   iconv -f CP1252 -t UTF8 tutor.fr > conv/tutor.fr
   iconv -f CP1252 -t UTF8 tutor.es > conv/tutor.es
   iconv -f CP1252 -t UTF8 tutor.de > conv/tutor.de
   #iconv -f CP737 -t UTF8 tutor.gr.cp737 > conv/tutor.gr.cp737
   #iconv -f EUC-JP -t UTF8 tutor.ja.euc > conv/tutor.ja.euc
   #iconv -f SJIS -t UTF8 tutor.ja.sjis > conv/tutor.ja.sjis
   iconv -f UTF8 -t UTF8 tutor.ja.utf-8 > conv/tutor.ja.utf-8
   iconv -f UTF8 -t UTF8 tutor.ko.utf-8 > conv/tutor.ko.utf-8
   iconv -f CP1252 -t UTF8 tutor.no > conv/tutor.no
   iconv -f ISO-8859-2 -t UTF8 tutor.pl > conv/tutor.pl
   iconv -f ISO-8859-2 -t UTF8 tutor.sk > conv/tutor.sk
   iconv -f KOI8R -t UTF8 tutor.ru > conv/tutor.ru
   iconv -f CP1252 -t UTF8 tutor.sv > conv/tutor.sv
   mv -f tutor.ja.euc tutor.ja.sjis tutor.ko.euc tutor.pl.cp1250 tutor.zh.big5 tutor.ru.cp1251 tutor.zh.euc conv/
   rm -f tutor.ca tutor.de tutor.es tutor.fr tutor.gr tutor.it tutor.ja.utf-8 tutor.ko.utf-8 tutor.no tutor.pl tutor.sk tutor.ru tutor.sv
mv -f conv/* .
rmdir conv
popd

# Dependency cleanups
chmod 644 %{buildroot}/%{_datadir}/%{name}/%{vimdir}/doc/vim2html.pl \
 %{buildroot}/%{_datadir}/%{name}/%{vimdir}/tools/*.pl \
 %{buildroot}/%{_datadir}/%{name}/%{vimdir}/tools/vim132
chmod 644 ../runtime/doc/vim2html.pl

mkdir -p %{buildroot}/%{_sysconfdir}/profile.d
cat >%{buildroot}/%{_sysconfdir}/profile.d/vim.sh <<EOF
if [ -n "\$BASH_VERSION" -o -n "\$KSH_VERSION" -o -n "\$ZSH_VERSION" ]; then
  [ -x %{_bindir}/id ] || return
  ID=\`/usr/bin/id -u\`
  [ -n "\$ID" -a "\$ID" -le 200 ] && return
  # for bash and zsh, only if no alias is already set
  alias vi >/dev/null 2>&1 || alias vi=vim
fi
EOF
cat >%{buildroot}/%{_sysconfdir}/profile.d/vim.csh <<EOF
if ( -x /usr/bin/id ) then
    if ( "\`/usr/bin/id -u\`" > 200 ) then
        alias vi vim
    endif
endif
EOF
chmod 0644 %{buildroot}/%{_sysconfdir}/profile.d/*
install -p -m644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/vimrc
install -p -m644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/virc
(cd %{buildroot}/%{_datadir}/%{name}/%{vimdir}/doc;
 gzip -9 *.txt
 gzip -d help.txt.gz version7.txt.gz sponsor.txt.gz
 cp %{SOURCE12} .
 cat tags | sed -e 's/\t\(.*.txt\)\t/\t\1.gz\t/;s/\thelp.txt.gz\t/\thelp.txt\t/;s/\tversion7.txt.gz\t/\tversion7.txt\t/;s/\tsponsor.txt.gz\t/\tsponsor.txt\t/' > tags.new; mv -f tags.new tags
cat >> tags << EOF
vi_help.txt	vi_help.txt	/*vi_help.txt*
vi-author.txt	vi_help.txt	/*vi-author*
vi-Bram.txt	vi_help.txt	/*vi-Bram*
vi-Moolenaar.txt	vi_help.txt	/*vi-Moolenaar*
vi-credits.txt	vi_help.txt	/*vi-credits*
EOF
LANG=C sort tags > tags.tmp; mv tags.tmp tags
 )
(cd ../runtime; rm -rf doc; ln -svf ../../vim/%{vimdir}/doc docs;) 
rm -f %{buildroot}/%{_datadir}/vim/%{vimdir}/macros/maze/maze*.c
rm -rf %{buildroot}/%{_datadir}/vim/%{vimdir}/tools
rm -rf %{buildroot}/%{_datadir}/vim/%{vimdir}/doc/vim2html.pl
rm -f %{buildroot}/%{_datadir}/vim/%{vimdir}/tutor/tutor.gr.utf-8~
( cd %{buildroot}/%{_mandir}
  for i in `find ??/ -type f`; do
    bi=`basename $i`
    iconv -f latin1 -t UTF8 $i > %{buildroot}/$bi
    mv -f %{buildroot}/$bi $i
  done
)

# Remove not UTF-8 manpages
for i in pl.ISO8859-2 it.ISO8859-1 ru.KOI8-R fr.ISO8859-1; do
  rm -rf %{buildroot}/%{_mandir}/$i
done

# use common man1/ru directory
mv %{buildroot}/%{_mandir}/ru.UTF-8 %{buildroot}/%{_mandir}/ru

# Remove duplicate man pages
for i in fr.UTF-8 it.UTF-8 pl.UTF-8; do
  rm -rf %{buildroot}/%{_mandir}/$i
done

for i in rvim.1 gvim.1 gex.1 gview.1 vimx.1; do 
  echo ".so man1/vim.1" > %{buildroot}/%{_mandir}/man1/$i
done
echo ".so man1/vimdiff.1" > %{buildroot}/%{_mandir}/man1/gvimdiff.1
echo ".so man1/vimtutor.1" > %{buildroot}/%{_mandir}/man1/gvimtutor.1
mkdir -p %{buildroot}/%{_mandir}/man5
for i in virc.5 vimrc.5; do 
  echo ".so man1/vim.1" > %{buildroot}/%{_mandir}/man5/$i
done
touch %{buildroot}/%{_datadir}/%{name}/vimfiles/doc/tags

%post X11
touch --no-create %{_datadir}/icons/hicolor
if [ -x /%{_bindir}/gtk-update-icon-cache ]; then
  gtk-update-icon-cache --ignore-theme-index -q %{_datadir}/icons/hicolor
fi
update-desktop-database &> /dev/null ||:

%postun X11
touch --no-create %{_datadir}/icons/hicolor
if [ -x /%{_bindir}/gtk-update-icon-cache ]; then
  gtk-update-icon-cache --ignore-theme-index -q %{_datadir}/icons/hicolor
fi
update-desktop-database &> /dev/null ||:

%clean
rm -rf %{buildroot}

%files common
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/vimrc
%doc README* LICENSE 
%doc runtime/docs
%doc Changelog.rpm
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/vimfiles/template.spec
%dir %{_datadir}/%{name}/%{vimdir}
%{_datadir}/%{name}/%{vimdir}/autoload
%{_datadir}/%{name}/%{vimdir}/colors
%{_datadir}/%{name}/%{vimdir}/compiler
%{_datadir}/%{name}/%{vimdir}/doc
%{_datadir}/%{name}/%{vimdir}/*.vim
%{_datadir}/%{name}/%{vimdir}/ftplugin
%{_datadir}/%{name}/%{vimdir}/indent
%{_datadir}/%{name}/%{vimdir}/keymap
%{_datadir}/%{name}/%{vimdir}/lang/*.vim
%{_datadir}/%{name}/%{vimdir}/lang/*.txt
%dir %{_datadir}/%{name}/%{vimdir}/lang
%{_datadir}/%{name}/%{vimdir}/macros
%{_datadir}/%{name}/%{vimdir}/plugin
%{_datadir}/%{name}/%{vimdir}/print
%{_datadir}/%{name}/%{vimdir}/syntax
%{_datadir}/%{name}/%{vimdir}/tutor
%if ! %{withvimspell}
%{_datadir}/%{name}/%{vimdir}/spell
%endif
%lang(af) %{_datadir}/%{name}/%{vimdir}/lang/af
%lang(ca) %{_datadir}/%{name}/%{vimdir}/lang/ca
%lang(cs) %{_datadir}/%{name}/%{vimdir}/lang/cs
%lang(cs.cp1250) %{_datadir}/%{name}/%{vimdir}/lang/cs.cp1250
%lang(de) %{_datadir}/%{name}/%{vimdir}/lang/de
%lang(en_GB) %{_datadir}/%{name}/%{vimdir}/lang/en_GB
%lang(eo) %{_datadir}/%{name}/%{vimdir}/lang/eo
%lang(es) %{_datadir}/%{name}/%{vimdir}/lang/es
%lang(fi) %{_datadir}/%{name}/%{vimdir}/lang/fi
%lang(fr) %{_datadir}/%{name}/%{vimdir}/lang/fr
%lang(ga) %{_datadir}/%{name}/%{vimdir}/lang/ga
%lang(it) %{_datadir}/%{name}/%{vimdir}/lang/it
%lang(ja) %{_datadir}/%{name}/%{vimdir}/lang/ja
%lang(ja.euc-jp) %{_datadir}/%{name}/%{vimdir}/lang/ja.euc-jp
%lang(ja.sjis) %{_datadir}/%{name}/%{vimdir}/lang/ja.sjis
%lang(ko) %{_datadir}/%{name}/%{vimdir}/lang/ko
%lang(ko) %{_datadir}/%{name}/%{vimdir}/lang/ko.UTF-8
%lang(nb) %{_datadir}/%{name}/%{vimdir}/lang/nb
%lang(nl) %{_datadir}/%{name}/%{vimdir}/lang/nl
%lang(no) %{_datadir}/%{name}/%{vimdir}/lang/no
%lang(pl) %{_datadir}/%{name}/%{vimdir}/lang/pl
%lang(pl.UTF-8) %{_datadir}/%{name}/%{vimdir}/lang/pl.UTF-8
%lang(pl.cp1250) %{_datadir}/%{name}/%{vimdir}/lang/pl.cp1250
%lang(pt_BR) %{_datadir}/%{name}/%{vimdir}/lang/pt_BR
%lang(ru) %{_datadir}/%{name}/%{vimdir}/lang/ru
%lang(ru.cp1251) %{_datadir}/%{name}/%{vimdir}/lang/ru.cp1251
%lang(sk) %{_datadir}/%{name}/%{vimdir}/lang/sk
%lang(sk.cp1250) %{_datadir}/%{name}/%{vimdir}/lang/sk.cp1250
%lang(sv) %{_datadir}/%{name}/%{vimdir}/lang/sv
%lang(uk) %{_datadir}/%{name}/%{vimdir}/lang/uk
%lang(uk.cp1251) %{_datadir}/%{name}/%{vimdir}/lang/uk.cp1251
%lang(vi) %{_datadir}/%{name}/%{vimdir}/lang/vi
%lang(zh_CN) %{_datadir}/%{name}/%{vimdir}/lang/zh_CN
%lang(zh_CN.cp936) %{_datadir}/%{name}/%{vimdir}/lang/zh_CN.cp936
%lang(zh_TW) %{_datadir}/%{name}/%{vimdir}/lang/zh_TW
%lang(zh_CN.UTF-8) %{_datadir}/%{name}/%{vimdir}/lang/zh_CN.UTF-8
%lang(zh_TW.UTF-8) %{_datadir}/%{name}/%{vimdir}/lang/zh_TW.UTF-8
/%{_bindir}/xxd
%{_mandir}/man1/ex.*
%{_mandir}/man1/gex.*
%{_mandir}/man1/gview.*
%{_mandir}/man1/gvim*
%{_mandir}/man1/rvi.*
%{_mandir}/man1/rview.*
%{_mandir}/man1/rvim.*
%{_mandir}/man1/vi.*
%{_mandir}/man1/view.*
%{_mandir}/man1/vim.*
%{_mandir}/man1/vimdiff.*
%{_mandir}/man1/vimtutor.*
%{_mandir}/man1/vimx.*
%{_mandir}/man1/xxd.*
%{_mandir}/man5/vimrc.*
%lang(fr) %{_mandir}/fr/man1/*
%lang(it) %{_mandir}/it/man1/*
%lang(ja) %{_mandir}/ja/man1/*
%lang(pl) %{_mandir}/pl/man1/*
%lang(ru) %{_mandir}/ru/man1/*

%if %{withvimspell}
%files spell
%defattr(-,root,root)
%dir %{_datadir}/%{name}/%{vimdir}/spell
%{_datadir}/%{name}/vim70/spell/cleanadd.vim
%lang(af) %{_datadir}/%{name}/%{vimdir}/spell/af.*
%lang(am) %{_datadir}/%{name}/%{vimdir}/spell/am.*
%lang(bg) %{_datadir}/%{name}/%{vimdir}/spell/bg.*
%lang(ca) %{_datadir}/%{name}/%{vimdir}/spell/ca.*
%lang(cs) %{_datadir}/%{name}/%{vimdir}/spell/cs.*
%lang(cy) %{_datadir}/%{name}/%{vimdir}/spell/cy.*
%lang(da) %{_datadir}/%{name}/%{vimdir}/spell/da.*
%lang(de) %{_datadir}/%{name}/%{vimdir}/spell/de.*
%lang(el) %{_datadir}/%{name}/%{vimdir}/spell/el.*
%lang(en) %{_datadir}/%{name}/%{vimdir}/spell/en.*
%lang(eo) %{_datadir}/%{name}/%{vimdir}/spell/eo.*
%lang(es) %{_datadir}/%{name}/%{vimdir}/spell/es.*
%lang(fo) %{_datadir}/%{name}/%{vimdir}/spell/fo.*
%lang(fr) %{_datadir}/%{name}/%{vimdir}/spell/fr.*
%lang(ga) %{_datadir}/%{name}/%{vimdir}/spell/ga.*
%lang(gd) %{_datadir}/%{name}/%{vimdir}/spell/gd.*
%lang(gl) %{_datadir}/%{name}/%{vimdir}/spell/gl.*
%lang(he) %{_datadir}/%{name}/%{vimdir}/spell/he.*
%lang(hr) %{_datadir}/%{name}/%{vimdir}/spell/hr.*
%lang(hu) %{_datadir}/%{name}/%{vimdir}/spell/hu.*
%lang(id) %{_datadir}/%{name}/%{vimdir}/spell/id.*
%lang(it) %{_datadir}/%{name}/%{vimdir}/spell/it.*
%lang(ku) %{_datadir}/%{name}/%{vimdir}/spell/ku.*
%lang(la) %{_datadir}/%{name}/%{vimdir}/spell/la.*
%lang(lt) %{_datadir}/%{name}/%{vimdir}/spell/lt.*
%lang(lv) %{_datadir}/%{name}/%{vimdir}/spell/lv.*
%lang(mg) %{_datadir}/%{name}/%{vimdir}/spell/mg.*
%lang(mi) %{_datadir}/%{name}/%{vimdir}/spell/mi.*
%lang(ms) %{_datadir}/%{name}/%{vimdir}/spell/ms.*
%lang(nb) %{_datadir}/%{name}/%{vimdir}/spell/nb.*
%lang(nl) %{_datadir}/%{name}/%{vimdir}/spell/nl.*
%lang(nn) %{_datadir}/%{name}/%{vimdir}/spell/nn.*
%lang(ny) %{_datadir}/%{name}/%{vimdir}/spell/ny.*
%lang(pl) %{_datadir}/%{name}/%{vimdir}/spell/pl.*
%lang(pt) %{_datadir}/%{name}/%{vimdir}/spell/pt.*
%lang(ro) %{_datadir}/%{name}/%{vimdir}/spell/ro.*
%lang(ru) %{_datadir}/%{name}/%{vimdir}/spell/ru.*
%lang(rw) %{_datadir}/%{name}/%{vimdir}/spell/rw.*
%lang(sk) %{_datadir}/%{name}/%{vimdir}/spell/sk.*
%lang(sl) %{_datadir}/%{name}/%{vimdir}/spell/sl.*
%lang(sv) %{_datadir}/%{name}/%{vimdir}/spell/sv.*
%lang(sw) %{_datadir}/%{name}/%{vimdir}/spell/sw.*
%lang(tet) %{_datadir}/%{name}/%{vimdir}/spell/tet.*
%lang(th) %{_datadir}/%{name}/%{vimdir}/spell/th.*
%lang(tl) %{_datadir}/%{name}/%{vimdir}/spell/tl.*
%lang(tn) %{_datadir}/%{name}/%{vimdir}/spell/tn.*
%lang(uk) %{_datadir}/%{name}/%{vimdir}/spell/uk.*
%lang(yi) %{_datadir}/%{name}/%{vimdir}/spell/yi.*
%lang(yi-tr) %{_datadir}/%{name}/%{vimdir}/spell/yi-tr.*
%lang(zu) %{_datadir}/%{name}/%{vimdir}/spell/zu.*
%endif

%files minimal
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/virc
%{_bindir}/ex
%{_bindir}/vi
%{_bindir}/view
%{_bindir}/rvi
%{_bindir}/rview
%{_mandir}/man1/vim.*
%{_mandir}/man1/vi.*
%{_mandir}/man1/ex.*
%{_mandir}/man1/rvi.*
%{_mandir}/man1/rview.*
%{_mandir}/man1/view.*
%{_mandir}/man5/virc.*

%files enhanced
%defattr(-,root,root)
%{_bindir}/vim
%{_bindir}/rvim
%{_bindir}/vimdiff
%{_bindir}/vimtutor
%config(noreplace) %{_sysconfdir}/profile.d/vim.*

%files filesystem
%defattr(-,root,root)
%dir %{_datadir}/%{name}/vimfiles
%dir %{_datadir}/%{name}/vimfiles/after
%dir %{_datadir}/%{name}/vimfiles/after/*
%dir %{_datadir}/%{name}/vimfiles/autoload
%dir %{_datadir}/%{name}/vimfiles/colors
%dir %{_datadir}/%{name}/vimfiles/compiler
%dir %{_datadir}/%{name}/vimfiles/doc
%ghost %{_datadir}/%{name}/vimfiles/doc/tags
%dir %{_datadir}/%{name}/vimfiles/ftdetect
%dir %{_datadir}/%{name}/vimfiles/ftplugin
%dir %{_datadir}/%{name}/vimfiles/indent
%dir %{_datadir}/%{name}/vimfiles/keymap
%dir %{_datadir}/%{name}/vimfiles/lang
%dir %{_datadir}/%{name}/vimfiles/plugin
%dir %{_datadir}/%{name}/vimfiles/print
%dir %{_datadir}/%{name}/vimfiles/spell
%dir %{_datadir}/%{name}/vimfiles/syntax
%dir %{_datadir}/%{name}/vimfiles/tutor

%files X11
%defattr(-,root,root)
%if "%{desktop_file}" == "1"
/%{_datadir}/applications/*
%else
/%{_sysconfdir}/X11/applnk/*/gvim.desktop
%endif
%{_bindir}/gvimtutor
%{_bindir}/gvim
%{_bindir}/gvimdiff
%{_bindir}/gview
%{_bindir}/gex
%{_bindir}/vimx
%{_bindir}/evim
%{_mandir}/man1/evim.*
%{_datadir}/icons/hicolor/*/apps/*

%changelog
* Wed Feb 19 2014 Ting-Wei Lan <lantw44@gmail.com> 7.4.179-1
- modified from Fedora official repo, version 7.4.179-1
- add Lua interpreter support

* Sat Feb 15 2014 Karsten Hopp <karsten@redhat.com> 7.4.179-1
- patchlevel 179

* Wed Jan 29 2014 Karsten Hopp <karsten@redhat.com> 7.4.160-1
- patchlevel 160

* Tue Dec 17 2013 Karsten Hopp <karsten@redhat.com> 7.4.131-1
- patchlevel 131

* Wed Nov 20 2013 Karsten Hopp <karsten@redhat.com> 7.4.094-1
- patchlevel 094

* Tue Oct 15 2013 Karsten Hopp <karsten@redhat.com> 7.4.052-1
- patchlevel 052

* Wed Sep 11 2013 Karsten Hopp <karsten@redhat.com> 7.4.027-2
- update vim icons (#1004788)
- check if 'id -u' returns empty string (vim.sh)

* Wed Sep 11 2013 Karsten Hopp <karsten@redhat.com> 7.4.027-1
- patchlevel 027

* Wed Sep 04 2013 Karsten Hopp <karsten@redhat.com> 7.4.016-1
- patchlevel 016

* Wed Aug 28 2013 Karsten Hopp <karsten@redhat.com> 7.4.009-1
- patchlevel 009
  mkdir("foo/bar/", "p") gives an error message
  creating a preview window on startup messes up the screen
  new regexp engine can't be interrupted
  too easy to write a file was not decrypted (yet)

* Wed Aug 21 2013 Karsten Hopp <karsten@redhat.com> 7.4.5-1
- patchlevel 5
- when closing a window fails ":bwipe" may hang
- "vaB" while 'virtualedit' is set selects the wrong area

* Wed Aug 21 2013 Karsten Hopp <karsten@redhat.com> 7.4.3-1
- patchlevel 3, memory access error in Ruby syntax highlighting

* Wed Aug 21 2013 Karsten Hopp <karsten@redhat.com> 7.4.2-1
- patchlevel 2, pattern with two alternative look-behind matches doesn't match

* Wed Aug 21 2013 Karsten Hopp <karsten@redhat.com> 7.4.1-1
- patchlevel 1, 'ic' doesn't work for patterns such as [a-z]

* Mon Aug 12 2013 Karsten Hopp <karsten@redhat.com> 7.4.0-1
- update to vim-7.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:7.3.1314-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 26 2013 Karsten Hopp <karsten@redhat.com> 7.3.1314-2
- document gex and vimx in man page
- fix gvimdiff and gvimtutor man page redirects

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2:7.3.1314-2
- Perl 5.18 rebuild

* Tue Jul 09 2013 Karsten Hopp <karsten@redhat.com> 7.3.1314-1
- patchlevel 1314

* Thu Jul 04 2013 Karsten Hopp <karsten@redhat.com> 7.3.1293-1
- patchlevel 1293

* Fri Jun 14 2013 Karsten Hopp <karsten@redhat.com> 7.3.1189-1
- patchlevel 1189

* Tue Jun 04 2013 Karsten Hopp <karsten@redhat.com> 7.3.1109-1
- patchlevel 1109

* Wed May 22 2013 Karsten Hopp <karsten@redhat.com> 7.3.1004-1
- patchlevel 1004

* Wed May 22 2013 Karsten Hopp <karsten@redhat.com> 7.3.1000-1
- patchlevel 1000 !

* Tue May 21 2013 Karsten Hopp <karsten@redhat.com> 7.3.987-1
- patchlevel 987

* Tue May 21 2013 Karsten Hopp <karsten@redhat.com> 7.3.944-2
- consistent use of macros in spec file
- add some links to man pages

* Tue May 14 2013 Karsten Hopp <karsten@redhat.com> 7.3.944-1
- patchlevel 944

* Mon May 13 2013 Karsten Hopp <karsten@redhat.com> 7.3.943-2
- add BR perl(ExtUtils::ParseXS)

* Mon May 13 2013 Karsten Hopp <karsten@redhat.com> 7.3.943-1
- patchlevel 943

* Wed May 08 2013 Karsten Hopp <karsten@redhat.com> 7.3.931-1
- patchlevel 931

* Wed May 08 2013 Karsten Hopp <karsten@redhat.com> 7.3.903-1
- fix ruby version check

* Fri Apr 19 2013 Karsten Hopp <karsten@redhat.com> 7.3.903-1
- drop crv patch
- update 7.3.838 patch, it was broken upstream

* Mon Apr 15 2013 Karsten Hopp <karsten@redhat.com> 7.3.903-1
- patchlevel 903

* Mon Feb 18 2013 Karsten Hopp <karsten@redhat.com> 7.3.822-1
- patchlevel 822

* Fri Feb 15 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 7.3.797-2
- Only use --vendor for desktop-file-install on F18 or less

* Thu Jan 31 2013 Karsten Hopp <karsten@redhat.com> 7.3.797-1
- patchlevel 797

* Mon Jan 28 2013 Karsten Hopp <karsten@redhat.com> 7.3.785-1
- patchlevel 785

* Tue Nov 20 2012 Karsten Hopp <karsten@redhat.com> 7.3.715-1
- patchlevel 715

* Mon Nov 12 2012 Karsten Hopp <karsten@redhat.com> 7.3.712-1
- patchlevel 712

* Mon Nov 12 2012 Karsten Hopp <karsten@redhat.com> 7.3.682-2
- fix vim.csh syntax

* Tue Oct 23 2012 Karsten Hopp <karsten@redhat.com> 7.3.712-1
- patchlevel 712

* Mon Oct 15 2012 Karsten Hopp <karsten@redhat.com> 7.3.691-1
- patchlevel 691

* Fri Oct 05 2012 Karsten Hopp <karsten@redhat.com> 7.3.682-1
- patchlevel 682
- use --enable-rubyinterp=dynamic and --enable-pythoninterp=dynamic

* Mon Sep 03 2012 Karsten Hopp <karsten@redhat.com> 7.3.646-1
- patchlevel 646

* Tue Aug 28 2012 Karsten Hopp <karsten@redhat.com> 7.3.638-2
- fix some man page typos (#668894, #675480)
- own usr/share/vim/vimfiles/doc/tags (#845564)
- add path to csope database (#844843)

* Tue Aug 28 2012 Karsten Hopp <karsten@redhat.com> 7.3.638-1
- patchlevel 638

# vim:nrformats-=octal
