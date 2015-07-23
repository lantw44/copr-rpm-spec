Name:       guix
Version:    0.8.3
Release:    1%{?dist}
Summary:    a purely functional package manager for the GNU system

Group:      System Environment/Base
License:    GPLv3+
URL:        https://www.gnu.org/software/guix
Source0:    ftp://alpha.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz

%global guile_required    5:2.0.7
%global sqlite_required   3.6.19
%global guix_user         guixbuild
%global guix_group        guixbuild
%global completionsdir    %(pkg-config --variable=completionsdir bash-completion)

BuildRequires: guile-devel >= %{guile_required}
BuildRequires: sqlite-devel >= %{sqlite_required}
BuildRequires: bzip2-devel, libgcrypt-devel
BuildRequires: emacs, emacs-geiser, bash-completion

# Get _unitdir macro to install the systemd service file
BuildRequires: systemd

Requires:   guile >= %{guile_required}
Requires:   sqlite >= %{sqlite_required}
Requires:   gzip, bzip2, xz, libgcrypt
Requires(post):  /usr/sbin/useradd
Requires(post):  /usr/sbin/usermod
Requires(post):  /usr/sbin/groupadd
Requires(post):  /usr/sbin/groupmod
Requires(post):  /usr/bin/gpasswd
Requires(post):  /sbin/install-info
Requires(preun): /sbin/install-info


%description
GNU Guix is a purely functional package manager for the GNU system. In addition
to standard package management features, Guix supports transactional upgrades
and roll-backs, unprivileged package management, per-user profiles, and garbage
collection. It provides Guile Scheme APIs, including high-level embedded
domain-specific languages (EDSLs), to describe how packages are to be built and
composed.

%package emacs
Summary:    Emacs interface for GNU Guix
Requires:   %{name} = %{version}-%{release}
Requires:   emacs(bin) >= %{_emacs_version}
Requires:   emacs-geiser
BuildArch:  noarch

%description emacs
Emacs interface for GNU Guix.

%package emacs-el
Summary:    Source for Emacs interface for GNU Guix
Requires:   %{name}-emacs = %{version}-%{release}
BuildArch:  noarch

%description emacs-el
Source for Emacs interface for GNU Guix.

%prep
%setup -q

%build
%configure --disable-rpath --with-bash-completion-dir=%{completionsdir}
make %{?_smp_mflags}

%check
# Remove the check that don't work because of depending on external resources
sed -i 's|tests/builders.scm||' Makefile
# Using user namespaces in mock is not allowed
sed -i 's|tests/syscalls.scm||' Makefile
sed -i 's|tests/containers.scm||' Makefile
make %{?_smp_mflags} check

%install
make install DESTDIR=%{buildroot} systemdservicedir=%{_unitdir}
%{_emacs_bytecompile} %{buildroot}%{_emacs_sitelispdir}/guix*.el
%find_lang guix
%find_lang guix-packages

%post
/sbin/install-info %{_infodir}/guix.info.gz %{_infodir}/dir || :
if [ "$1" = 1 ]; then
    /usr/sbin/groupadd -r %{guix_group}
    /usr/sbin/useradd -M -N -g %{guix_group} -d /gnu/store -s /sbin/nologin \
        -c "Guix build user" %{guix_user}
    /usr/bin/gpasswd -a %{guix_user} %{guix_group} >/dev/null
elif [ "$1" -gt 1 ]; then
    /usr/sbin/groupmod -n %{guix_group} guix-builder 2>/dev/null || :
    /usr/sbin/usermod -l %{guix_user} -d /gnu/store guix-builder 2>/dev/null || :
fi

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/guix.info.gz %{_infodir}/dir || :
fi

%files -f guix.lang -f guix-packages.lang
%license COPYING
%doc AUTHORS ChangeLog NEWS README ROADMAP THANKS TODO
%{_bindir}/guix
%{_bindir}/guix-daemon
%{_sbindir}/guix-register
%{_libexecdir}/guix/list-runtime-roots
%{_libexecdir}/guix/offload
%{_libexecdir}/guix/substitute
%{_libexecdir}/guix-authenticate
%{_datadir}/guix/hydra.gnu.org.pub
%{_datadir}/guile/site/2.0/gnu.scm
%{_datadir}/guile/site/2.0/gnu.go
%{_datadir}/guile/site/2.0/gnu/artwork.scm
%{_datadir}/guile/site/2.0/gnu/artwork.go
%{_datadir}/guile/site/2.0/gnu/build/*.scm
%{_datadir}/guile/site/2.0/gnu/build/*.go
%{_datadir}/guile/site/2.0/gnu/packages.scm
%{_datadir}/guile/site/2.0/gnu/packages.go
%{_datadir}/guile/site/2.0/gnu/packages/*.scm
%{_datadir}/guile/site/2.0/gnu/packages/*.go
%{_datadir}/guile/site/2.0/gnu/packages/ld-wrapper.in
%{_datadir}/guile/site/2.0/gnu/packages/linux-libre-*.conf
%{_datadir}/guile/site/2.0/gnu/packages/patches/*.patch
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/armhf-linux/tar
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/armhf-linux/xz
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/armhf-linux/mkdir
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/armhf-linux/bash
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/armhf-linux/guile-2.0.11.tar.xz
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/mips64el-linux/tar
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/mips64el-linux/xz
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/mips64el-linux/mkdir
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/mips64el-linux/bash
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/mips64el-linux/guile-2.0.9.tar.xz
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/i686-linux/tar
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/i686-linux/xz
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/i686-linux/mkdir
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/i686-linux/bash
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/i686-linux/guile-2.0.9.tar.xz
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/x86_64-linux/tar
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/x86_64-linux/xz
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/x86_64-linux/mkdir
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/x86_64-linux/bash
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/x86_64-linux/guile-2.0.9.tar.xz
%{_datadir}/guile/site/2.0/gnu/services.scm
%{_datadir}/guile/site/2.0/gnu/services.go
%{_datadir}/guile/site/2.0/gnu/services/*.scm
%{_datadir}/guile/site/2.0/gnu/services/*.go
%{_datadir}/guile/site/2.0/gnu/system.scm
%{_datadir}/guile/site/2.0/gnu/system.go
%{_datadir}/guile/site/2.0/gnu/system/*.scm
%{_datadir}/guile/site/2.0/gnu/system/*.go
%{_datadir}/guile/site/2.0/gnu/system/examples/bare-bones.tmpl
%{_datadir}/guile/site/2.0/gnu/system/examples/desktop.tmpl
%{_datadir}/guile/site/2.0/guix.scm
%{_datadir}/guile/site/2.0/guix.go
%{_datadir}/guile/site/2.0/guix/*.scm
%{_datadir}/guile/site/2.0/guix/*.go
%{_datadir}/guile/site/2.0/guix/build/*.scm
%{_datadir}/guile/site/2.0/guix/build/*.go
%{_datadir}/guile/site/2.0/guix/emacs/guix-helper.scm
%{_datadir}/guile/site/2.0/guix/emacs/guix-main.scm
%{_datadir}/guile/site/2.0/guix/import/*.scm
%{_datadir}/guile/site/2.0/guix/import/*.go
%{_datadir}/guile/site/2.0/guix/scripts/*.scm
%{_datadir}/guile/site/2.0/guix/scripts/*.go
%{_datadir}/guile/site/2.0/guix/scripts/import/*.scm
%{_datadir}/guile/site/2.0/guix/scripts/import/*.go
%{_datadir}/guile/site/2.0/guix/build-system/*.scm
%{_datadir}/guile/site/2.0/guix/build-system/*.go
%{_infodir}/%{name}.info*
%{_infodir}/images/bootstrap-graph.png.gz
%{_infodir}/images/coreutils-size-map.png.gz
%exclude %{_infodir}/dir
%{_mandir}/man1/guix-archive.1.gz
%{_mandir}/man1/guix-build.1.gz
%{_mandir}/man1/guix-daemon.1.gz
%{_mandir}/man1/guix-download.1.gz
%{_mandir}/man1/guix-edit.1.gz
%{_mandir}/man1/guix-environment.1.gz
%{_mandir}/man1/guix-gc.1.gz
%{_mandir}/man1/guix-hash.1.gz
%{_mandir}/man1/guix-import.1.gz
%{_mandir}/man1/guix-lint.1.gz
%{_mandir}/man1/guix-package.1.gz
%{_mandir}/man1/guix-publish.1.gz
%{_mandir}/man1/guix-pull.1.gz
%{_mandir}/man1/guix-refresh.1.gz
%{_mandir}/man1/guix-size.1.gz
%{_mandir}/man1/guix-system.1.gz
%{_mandir}/man1/guix.1.gz
%{completionsdir}/guix
%{_unitdir}/guix-daemon.service

%files emacs
%{_emacs_sitelispdir}/guix*.elc

%files emacs-el
%{_emacs_sitelispdir}/guix*.el

%changelog
* Thu Jul 23 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.8.3-1
- Update to 0.8.3
- Remove checks that depend on missing remote resources
- Remove checks that are not allowed to run in mock
- Remove the systemd service file written by me. Upstream already provides a
  better systemd service file.
- Rename guix-builder group to guixbuild, which is the default of guix-daemon
  and upstream systemd service file.

* Thu May 21 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.8.2-3
- We no longer have to create /gnu/store and /var/log/guix manually. Guix can
  create and set correct permissions for these directories.

* Sun May 17 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.8.2-2
- Use license marco to install the license file

* Fri May 15 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.8.2-1
- Update to 0.8.2
- Add a %check section to run the test

* Wed Apr 15 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.8.1-3
- Use /usr/sbin/useradd and /usr/sbin/groupadd instead of /sbin/useradd and
  /sbin/groupadd to make this package work with DNF

* Fri Mar 20 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.8.1-2
- Rebuilt for Fedora 22 and 23
- Add epoch to guile dependency to prevent it from using compat-guile18

* Fri Jan 30 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.8.1-1
- Update to 0.8.1

* Sat Nov 22 2014 Ting-Wei Lan <lantw44@gmail.com> - 0.8-2
- Do not create /var/guix, which prevents guix-daemon from populating /var/guix
  and /gnu/store on the first start.

* Wed Nov 19 2014 Ting-Wei Lan <lantw44@gmail.com> - 0.8-1
- Update to 0.8

* Tue Jul 29 2014 Ting-Wei Lan <lantw44@gmail.com> - 0.7-1
- Update to 0.7

* Fri Apr 18 2014 Ting-Wei Lan <lantw44@gmail.com> - 0.6-2
- Add a systemd service file

* Thu Apr 10 2014 Ting-Wei Lan <lantw44@gmail.com> - 0.6-1
- Update to 0.6

* Tue Dec 17 2013 Ting-Wei Lan <lantw44@gmail.com> - 0.5-1
- Update to 0.5

* Mon Sep 30 2013 Ting-Wei Lan <lantw44@gmail.com> - 0.4-4
- Initial packaging
