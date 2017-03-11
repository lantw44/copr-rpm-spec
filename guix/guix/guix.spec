Name:           guix
Version:        0.12.0
Release:        2%{?dist}
Summary:        A purely functional package manager for the GNU system

License:        GPLv3+
URL:            https://www.gnu.org/software/guix
Source0:        ftp://alpha.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz

%global guix_user         guixbuild
%global guix_group        guixbuild
%global completionsdir    %(pkg-config --variable=completionsdir bash-completion)

BuildRequires:  pkgconfig(guile-2.0)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  zlib-devel, bzip2-devel, libgcrypt-devel
BuildRequires:  gettext, help2man, graphviz
BuildRequires:  emacs, emacs-geiser, emacs-magit, bash-completion
BuildRequires:  guile-json, guile-ssh, gnutls-guile
BuildRequires:  systemd

Requires:       gzip, bzip2, xz
Requires:       %{_bindir}/dot
Requires:       %{_libdir}/libgcrypt.so
Requires:       emacs-filesystem >= %{_emacs_version}
Requires(post): /usr/sbin/useradd
Requires(post): /usr/sbin/usermod
Requires(post): /usr/sbin/groupadd
Requires(post): /usr/sbin/groupmod
Requires(post): /usr/bin/gpasswd
Requires(post): info
Requires(post): systemd
Requires(preun): info
Requires(preun): systemd
Requires(postun): systemd

Recommends:     guile-json, guile-ssh, gnutls-guile
Suggests:       emacs, emacs-geiser, emacs-magit

Obsoletes:      %{name}-emacs <= 0.8.3-1
Obsoletes:      %{name}-emacs-el <= 0.8.3-1
Provides:       %{name}-emacs <= 0.8.3-1
Provides:       %{name}-emacs-el <= 0.8.3-1

%description
GNU Guix is a purely functional package manager for the GNU system. In addition
to standard package management features, Guix supports transactional upgrades
and roll-backs, unprivileged package management, per-user profiles, and garbage
collection. It provides Guile Scheme APIs, including high-level embedded
domain-specific languages (EDSLs), to describe how packages are to be built and
composed.


%prep
%autosetup -p1


%build
%configure --disable-rpath \
    --with-bash-completion-dir=%{completionsdir} \
    --with-lispdir=%{_emacs_sitelispdir}/guix
make %{?_smp_mflags}


%check
# user namespace is not supported in chroot
if unshare -Ur true; then :; else
    sed -i 's|tests/syscalls.scm||' Makefile
    sed -i 's|tests/containers.scm||' Makefile
    sed -i 's|tests/guix-environment-container.sh||' Makefile
fi

make %{?_smp_mflags} check


%install
make install DESTDIR=%{buildroot} systemdservicedir=%{_unitdir}
# drop useless upstart service file
rm %{buildroot}%{_libdir}/upstart/system/guix-daemon.conf
rm %{buildroot}%{_libdir}/upstart/system/guix-publish.conf
rmdir %{buildroot}%{_libdir}/upstart/system
rmdir %{buildroot}%{_libdir}/upstart
# move the autoload script
mkdir -p %{buildroot}%{_emacs_sitestartdir}
%{_emacs_bytecompile} %{buildroot}%{_emacs_sitelispdir}/guix/guix*.el
mv %{buildroot}%{_emacs_sitelispdir}/guix/guix-autoloads.el \
    %{buildroot}%{_emacs_sitestartdir}/guix.el
# own the configuration directory
mkdir -p %{buildroot}%{_sysconfdir}/guix
%find_lang guix
%find_lang guix-packages


%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
if [ "$1" = 1 ]; then
    /usr/sbin/groupadd -r %{guix_group}
    /usr/sbin/useradd -r -M -N -g %{guix_group} -d /gnu/store -s /sbin/nologin \
        -c "Guix build user" %{guix_user}
    /usr/bin/gpasswd -a %{guix_user} %{guix_group} >/dev/null
elif [ "$1" -gt 1 ]; then
    /usr/sbin/groupmod -n %{guix_group} guix-builder 2>/dev/null || :
    /usr/sbin/usermod -l %{guix_user} -d /gnu/store guix-builder 2>/dev/null || :
fi
%systemd_post guix-daemon.service guix-publish.service


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi
%systemd_preun guix-daemon.service guix-publish.service


%postun
%systemd_postun_with_restart guix-daemon.service guix-publish.service


%files -f guix.lang -f guix-packages.lang
%license COPYING
%doc AUTHORS ChangeLog CODE-OF-CONDUCT NEWS README ROADMAP THANKS TODO
%{_bindir}/guix
%{_bindir}/guix-daemon
%{_sbindir}/guix-register
%{_libexecdir}/guix/download
%{_libexecdir}/guix/list-runtime-roots
%{_libexecdir}/guix/offload
%{_libexecdir}/guix/substitute
%{_libexecdir}/guix-authenticate
%dir %{_datadir}/guix
%{_datadir}/guix/hydra.gnu.org.pub
%{_datadir}/guile/site/2.0/gnu.scm
%{_datadir}/guile/site/2.0/gnu.go
%dir %{_datadir}/guile/site/2.0/gnu
%{_datadir}/guile/site/2.0/gnu/artwork.scm
%{_datadir}/guile/site/2.0/gnu/artwork.go
%dir %{_datadir}/guile/site/2.0/gnu/build
%{_datadir}/guile/site/2.0/gnu/build/*.scm
%{_datadir}/guile/site/2.0/gnu/build/*.go
%{_datadir}/guile/site/2.0/gnu/packages.scm
%{_datadir}/guile/site/2.0/gnu/packages.go
%dir %{_datadir}/guile/site/2.0/gnu/packages
%{_datadir}/guile/site/2.0/gnu/packages/*.scm
%{_datadir}/guile/site/2.0/gnu/packages/*.go
%{_datadir}/guile/site/2.0/gnu/packages/ld-wrapper.in
%{_datadir}/guile/site/2.0/gnu/packages/linux-libre-*.conf
%dir %{_datadir}/guile/site/2.0/gnu/packages/patches
%{_datadir}/guile/site/2.0/gnu/packages/patches/*.patch
%dir %{_datadir}/guile/site/2.0/gnu/packages/bootstrap
%dir %{_datadir}/guile/site/2.0/gnu/packages/bootstrap/armhf-linux
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/armhf-linux/tar
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/armhf-linux/xz
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/armhf-linux/mkdir
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/armhf-linux/bash
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/armhf-linux/guile-2.0.11.tar.xz
%dir %{_datadir}/guile/site/2.0/gnu/packages/bootstrap/mips64el-linux
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/mips64el-linux/tar
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/mips64el-linux/xz
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/mips64el-linux/mkdir
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/mips64el-linux/bash
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/mips64el-linux/guile-2.0.9.tar.xz
%dir %{_datadir}/guile/site/2.0/gnu/packages/bootstrap/i686-linux
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/i686-linux/tar
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/i686-linux/xz
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/i686-linux/mkdir
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/i686-linux/bash
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/i686-linux/guile-2.0.9.tar.xz
%dir %{_datadir}/guile/site/2.0/gnu/packages/bootstrap/x86_64-linux
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/x86_64-linux/tar
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/x86_64-linux/xz
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/x86_64-linux/mkdir
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/x86_64-linux/bash
%{_datadir}/guile/site/2.0/gnu/packages/bootstrap/x86_64-linux/guile-2.0.9.tar.xz
%{_datadir}/guile/site/2.0/gnu/services.scm
%{_datadir}/guile/site/2.0/gnu/services.go
%dir %{_datadir}/guile/site/2.0/gnu/services
%{_datadir}/guile/site/2.0/gnu/services/*.scm
%{_datadir}/guile/site/2.0/gnu/services/*.go
%{_datadir}/guile/site/2.0/gnu/system.scm
%{_datadir}/guile/site/2.0/gnu/system.go
%dir %{_datadir}/guile/site/2.0/gnu/system
%{_datadir}/guile/site/2.0/gnu/system/*.scm
%{_datadir}/guile/site/2.0/gnu/system/*.go
%dir %{_datadir}/guile/site/2.0/gnu/system/examples
%{_datadir}/guile/site/2.0/gnu/system/examples/bare-bones.tmpl
%{_datadir}/guile/site/2.0/gnu/system/examples/desktop.tmpl
%{_datadir}/guile/site/2.0/gnu/system/examples/lightweight-desktop.tmpl
%{_datadir}/guile/site/2.0/gnu/tests.scm
%{_datadir}/guile/site/2.0/gnu/tests.go
%dir %{_datadir}/guile/site/2.0/gnu/tests
%{_datadir}/guile/site/2.0/gnu/tests/*.scm
%{_datadir}/guile/site/2.0/gnu/tests/*.go
%{_datadir}/guile/site/2.0/guix.scm
%{_datadir}/guile/site/2.0/guix.go
%dir %{_datadir}/guile/site/2.0/guix
%{_datadir}/guile/site/2.0/guix/*.scm
%{_datadir}/guile/site/2.0/guix/*.go
%dir %{_datadir}/guile/site/2.0/guix/build
%{_datadir}/guile/site/2.0/guix/build/*.scm
%{_datadir}/guile/site/2.0/guix/build/*.go
%dir %{_datadir}/guile/site/2.0/guix/build-system
%{_datadir}/guile/site/2.0/guix/build-system/*.scm
%{_datadir}/guile/site/2.0/guix/build-system/*.go
%dir %{_datadir}/guile/site/2.0/guix/emacs
%{_datadir}/guile/site/2.0/guix/emacs/guix-helper.scm
%{_datadir}/guile/site/2.0/guix/emacs/guix-main.scm
%dir %{_datadir}/guile/site/2.0/guix/import
%{_datadir}/guile/site/2.0/guix/import/*.scm
%{_datadir}/guile/site/2.0/guix/import/*.go
%dir %{_datadir}/guile/site/2.0/guix/scripts
%{_datadir}/guile/site/2.0/guix/scripts/*.scm
%{_datadir}/guile/site/2.0/guix/scripts/*.go
%dir %{_datadir}/guile/site/2.0/guix/scripts/container
%{_datadir}/guile/site/2.0/guix/scripts/container/*.scm
%{_datadir}/guile/site/2.0/guix/scripts/container/*.go
%dir %{_datadir}/guile/site/2.0/guix/scripts/import
%{_datadir}/guile/site/2.0/guix/scripts/import/*.scm
%{_datadir}/guile/site/2.0/guix/scripts/import/*.go
%dir %{_datadir}/guile/site/2.0/guix/tests
%{_datadir}/guile/site/2.0/guix/tests/*.go
%{_infodir}/%{name}.info*
%dir %{_infodir}/images
%{_infodir}/images/bootstrap-graph.png.gz
%{_infodir}/images/bootstrap-packages.png.gz
%{_infodir}/images/coreutils-bag-graph.png.gz
%{_infodir}/images/coreutils-graph.png.gz
%{_infodir}/images/coreutils-size-map.png.gz
%{_infodir}/images/service-graph.png.gz
%{_infodir}/images/shepherd-graph.png.gz
%exclude %{_infodir}/dir
%{_mandir}/man1/guix-archive.1*
%{_mandir}/man1/guix-build.1*
%{_mandir}/man1/guix-challenge.1*
%{_mandir}/man1/guix-daemon.1*
%{_mandir}/man1/guix-download.1*
%{_mandir}/man1/guix-edit.1*
%{_mandir}/man1/guix-environment.1*
%{_mandir}/man1/guix-gc.1*
%{_mandir}/man1/guix-hash.1*
%{_mandir}/man1/guix-import.1*
%{_mandir}/man1/guix-lint.1*
%{_mandir}/man1/guix-package.1*
%{_mandir}/man1/guix-publish.1*
%{_mandir}/man1/guix-pull.1*
%{_mandir}/man1/guix-refresh.1*
%{_mandir}/man1/guix-size.1*
%{_mandir}/man1/guix-system.1*
%{_mandir}/man1/guix.1*
%{completionsdir}/guix
%{_datadir}/zsh/site-functions/_guix
%dir %{_emacs_sitelispdir}/guix
%{_emacs_sitelispdir}/guix/guix*.elc
%{_emacs_sitelispdir}/guix/guix*.el
%{_emacs_sitestartdir}/guix.el
%dir %{_sysconfdir}/guix
%{_unitdir}/guix-daemon.service
%{_unitdir}/guix-publish.service



%changelog
* Wed Mar 08 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.12.0-2
- Rebuilt for Fedora 26 and 27

* Sat Dec 31 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.12.0-1
- Update to 0.12.0

* Fri Nov 04 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.11.0-3
- Use autosetup macro
- Fix build failure on Guile 2.0.13

* Sat Sep 10 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.11.0-2
- Rebuilt for Fedora 25 and 26

* Thu Aug 04 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.11.0-1
- Update to 0.11.0

* Fri Apr 01 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.10.0-1
- Update to 0.10.0
- Add help2man to BuildRequires
- Add dot to both BuildRequires and Requires

* Thu Mar 03 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.9.0-3
- Rebuilt for Fedora 24 and 25

* Tue Nov 24 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.9.0-2
- Own /usr/share/info/images because no other packages use it
- Use _libdir macro instead of hard-coding /usr/lib64

* Sun Nov 22 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.9.0-1
- Update to 0.9.0
- Don't clutter the system site-lisp directory
- The build user of guix-daemon should be a system account

* Sat Oct 10 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.8.3-2
- Remove group tag, which is not required
- Use pkgconfig in BuildRequires
- Use info instead of /sbin/install-info in Requires
- Handle systemd service files
- Don't hard-code .gz when listing man pages
- Merge emacs sub-packages back into the main package

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
- Add a check section to run the test

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
