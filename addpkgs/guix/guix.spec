Name:       guix
Version:    0.5
Release:    1%{?dist}
Summary:    a purely functional package manager for the GNU system

Group:      System Environment/Base
License:    GPLv3+
URL:        https://www.gnu.org/software/guix
Source0:    ftp://alpha.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz

%global guile_required    2.0.5
%global sqlite_required   3.6.19
%global guix_user         guix-builder
%global guix_group        guix-builder

BuildRequires: guile-devel >= %{guile_required}
BuildRequires: sqlite-devel >= %{sqlite_required}
BuildRequires: bzip2-devel, libgcrypt-devel

Requires:   guile >= %{guile_required}
Requires:   sqlite >= %{sqlite_required}
Requires:   bzip2, libgcrypt
Requires(post):  /sbin/useradd
Requires(post):  /sbin/groupadd
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

%prep
%setup -q

%build
%configure --disable-rpath
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/nix/store
mkdir -p %{buildroot}%{_localstatedir}/log/nix
mkdir -p %{buildroot}%{_localstatedir}/nix
%find_lang %{name}

%post
/sbin/install-info %{_infodir}/guix.info.gz %{_infodir}/dir || :
if [ "$1" = 1 ]; then
    /sbin/groupadd -r %{guix_group}
    /sbin/useradd -M -N -g %{guix_group} -d /nix/store -s /sbin/nologin \
        -c "Guix build user" %{guix_user}
    /usr/bin/gpasswd -a %{guix_user} %{guix_group} >/dev/null
    chgrp %{guix_user} /nix/store
    chmod 1775 /nix/store
fi

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/guix.info.gz %{_infodir}/dir || :
fi

%files -f %{name}.lang
%{_bindir}/guix
%{_bindir}/guix-daemon
%{_sbindir}/guix-register
%{_libexecdir}/guix/list-runtime-roots
%{_libexecdir}/guix/substitute-binary
%attr(4755,root,root) %{_libexecdir}/nix-setuid-helper
%{_datadir}/guile/site/2.0/gnu/*
%{_datadir}/guile/site/2.0/guix/*
%{_datadir}/guile/site/2.0/guix.scm
%{_datadir}/guile/site/2.0/guix.go
%dir /nix/store
%dir %{_localstatedir}/log/nix
%dir %{_localstatedir}/nix
%{_infodir}/%{name}.info*
%{_infodir}/images/bootstrap-graph.png.gz
%exclude %{_infodir}/dir

%changelog
* Tue Dec 17 2013 Ting-Wei Lan <lantw44@gmail.com>
- Update to 0.5

* Mon Sep 30 2013 Ting-Wei Lan <lantw44@gmail.com>
- Initial packaging
