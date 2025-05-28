%global debug_package %{nil}

Name:           guile-zlib
Version:        0.2.2
Release:        1%{?dist}
Summary:        Guile bindings for zlib

License:        GPL-3.0-or-later
URL:            https://notabug.org/guile-zlib/guile-zlib
Source0:        https://notabug.org/guile-zlib/guile-zlib/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/3.0
%global guile_ccache_dir %{_libdir}/guile/3.0/site-ccache

BuildRequires:  autoconf, automake, make
BuildRequires:  pkgconfig(guile-3.0), pkgconfig(zlib)
Requires:       guile30, zlib-devel

%description
Guile-zlib: Guile bindings for zlib, a lossless data-compression library. The
bindings are written in pure Scheme by using Guile's foreign function interface.


%prep
%autosetup -n %{name} -p1


%build
autoreconf -fiv
%configure
%make_build


%check
# Workaround the failed 'gzip output port, error' test for zlib-ng.
sed -i 's|(random-bytevector 65536)|(random-bytevector 200000)|' tests/zlib.scm
%{__make} %{?_smp_mflags} check


%install
%make_install


%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README.org
%{guile_source_dir}/zlib.scm
%{guile_ccache_dir}/zlib.go
%dir %{guile_source_dir}/zlib
%dir %{guile_ccache_dir}/zlib
%{guile_source_dir}/zlib/config.scm
%{guile_ccache_dir}/zlib/config.go


%changelog
* Sat May 24 2025 Ting-Wei Lan <lantw44@gmail.com> - 0.2.2-1
- Update to 0.2.2
- Migrate to SPDX license

* Sat Nov 02 2024 Ting-Wei Lan <lantw44@gmail.com> - 0.2.1-1
- Update to 0.2.1

* Sat Oct 05 2024 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-7
- Drop the brp-strip workaround

* Wed Apr 19 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-6
- Rebuilt for Fedora 38 and 39

* Sun Feb 12 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-5
- Switch to Guile 3.0

* Sat Oct 29 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-4
- Rebuilt for Fedora 37 and 38

* Thu Apr 28 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-3
- Rebuilt for Fedora 36 and 37

* Sat Sep 25 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-2
- Disable brp-strip on Fedora 35 and later because it fails on Guile objects

* Mon Jun 14 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-1
- Update to 0.1.0

* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.0.1-2
- Rebuilt for Fedora 34 and 35

* Mon Feb 15 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.0.1-1
- Initial packaging
