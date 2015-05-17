Name:       guix
Version:    0.8.2
Release:    2%{?dist}
Summary:    a purely functional package manager for the GNU system

Group:      System Environment/Base
License:    GPLv3+
URL:        https://www.gnu.org/software/guix
Source0:    ftp://alpha.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
Source1:    guix.service

%global guile_required    5:2.0.5
%global sqlite_required   3.6.19
%global guix_user         guix-builder
%global guix_group        guix-builder
%global completionsdir    %(pkg-config --variable=completionsdir bash-completion)

BuildRequires: guile-devel >= %{guile_required}
BuildRequires: sqlite-devel >= %{sqlite_required}
BuildRequires: bzip2-devel, libgcrypt-devel
BuildRequires: emacs, emacs-geiser, bash-completion

# Get _unitdir macro to install the systemd service file
BuildRequires: systemd

Requires:   guile >= %{guile_required}
Requires:   sqlite >= %{sqlite_required}
Requires:   bzip2, libgcrypt
Requires(post):  /usr/sbin/useradd
Requires(post):  /usr/sbin/groupadd
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
make %{?_smp_mflags} check

%install
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/gnu/store
mkdir -p %{buildroot}%{_localstatedir}/log/guix
mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/guix.service
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
fi
chgrp %{guix_user} /gnu/store
chmod 1775 /gnu/store

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/guix.info.gz %{_infodir}/dir || :
    rmdir --ignore-fail-on-non-empty /gnu/store
    rmdir --ignore-fail-on-non-empty /gnu
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
%dir /gnu/store
%dir %{_localstatedir}/log/guix
%{_infodir}/%{name}.info*
%{_infodir}/images/bootstrap-graph.png.gz
%exclude %{_infodir}/dir
%{completionsdir}/guix
%{_unitdir}/guix.service

%files emacs
%{_emacs_sitelispdir}/guix*.elc

%files emacs-el
%{_emacs_sitelispdir}/guix*.el

%changelog
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
