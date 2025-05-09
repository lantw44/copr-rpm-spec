Name:           guile30-gnutls
Version:        4.0.0
Release:        1%{?dist}
Summary:        Guile bindings for the GnuTLS library

License:        GPL-3.0-or-later AND LGPL-2.1-or-later
URL:            https://gitlab.com/gnutls/guile
Source0:        https://ftpmirror.gnu.org/gnutls/guile-gnutls-%{version}.tar.gz

# https://gitlab.com/gnutls/guile/-/issues/25
Patch0:         guile30-gnutls-4.0.0-tests-list-pk-algorithms.patch

%global guile_source_dir     %{_datadir}/guile/site/3.0
%global guile_ccache_dir     %{_libdir}/guile/3.0/site-ccache
%global guile_extensions_dir %{_libdir}/guile/3.0/extensions

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(guile-3.0), pkgconfig(gnutls)
Requires:       guile30

%description
Guile-GnuTLS provides Guile bindings for the GnuTLS library.


%prep
%autosetup -p1 -n guile-gnutls-%{version}


%build
%configure \
    --disable-rpath \
    --disable-static \
%if 0%{?fedora} >= 38
    --disable-srp-authentication \
%endif
    GUILE=%{_bindir}/guile3.0 \
    GUILD=%{_bindir}/guild3.0 \
    guile_snarf=%{_bindir}/guile-snarf3.0
%make_build


%check
%{__make} %{?_smp_mflags} check


%install
%make_install
rm %{buildroot}%{_infodir}/dir
rm %{buildroot}%{_infodir}/gnutls-guile.info
rm %{buildroot}%{guile_extensions_dir}/guile-gnutls-v-2.la


%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{guile_source_dir}/gnutls.scm
%{guile_ccache_dir}/gnutls.go
%dir %{guile_source_dir}/gnutls
%dir %{guile_ccache_dir}/gnutls
%{guile_source_dir}/gnutls/extra.scm
%{guile_ccache_dir}/gnutls/extra.go
%{guile_extensions_dir}/guile-gnutls-v-2.so*


%changelog
* Sat Nov 02 2024 Ting-Wei Lan <lantw44@gmail.com> - 4.0.0-1
- Update to 4.0.0

* Sat May 13 2023 Ting-Wei Lan <lantw44@gmail.com> - 3.7.12-1
- Update to 3.7.12

* Wed Apr 19 2023 Ting-Wei Lan <lantw44@gmail.com> - 3.7.11-3
- Disable SRP authentication on Fedora 38 and later

* Tue Feb 28 2023 Ting-Wei Lan <lantw44@gmail.com> - 3.7.11-2
- Switch to Guile 3.0

* Wed Feb 22 2023 Zoltan Fridrich <zfridric@redhat.com> - 3.7.11-1
- Initial import (fedora#2172108).
