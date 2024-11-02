%global debug_package %{nil}

Name:           guile-lzlib
Version:        0.3.0
Release:        1%{?dist}
Summary:        Guile bindings for lzlib

License:        GPLv3+
URL:            https://notabug.org/guile-lzlib/guile-lzlib
Source0:        https://notabug.org/guile-lzlib/guile-lzlib/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/3.0
%global guile_ccache_dir %{_libdir}/guile/3.0/site-ccache

BuildRequires:  gcc
BuildRequires:  autoconf, automake, pkgconfig(guile-3.0), lzlib-devel
Requires:       guile30, lzlib-devel

%description
Guile-lzlib: Guile bindings for lzlib, a C library for in-memory LZMA
compression and decompression. The bindings are written in pure Scheme by using
Guile's foreign function interface.


%prep
%autosetup -n %{name} -p1


%build
autoreconf -fiv
%configure
%make_build


%check
%{__make} %{?_smp_mflags} check


%install
%make_install


%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README.org
%{guile_source_dir}/lzlib.scm
%{guile_ccache_dir}/lzlib.go
%dir %{guile_source_dir}/lzlib
%dir %{guile_ccache_dir}/lzlib
%{guile_source_dir}/lzlib/config.scm
%{guile_ccache_dir}/lzlib/config.go


%changelog
* Sat Nov 02 2024 Ting-Wei Lan <lantw44@gmail.com> - 0.3.0-1
- Update to 0.3.0

* Sat Oct 05 2024 Ting-Wei Lan <lantw44@gmail.com> - 0.0.2-8
- Drop the brp-strip workaround

* Wed Apr 19 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.0.2-7
- Rebuilt for Fedora 38 and 39

* Sun Feb 12 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.0.2-6
- Switch to Guile 3.0

* Sat Oct 29 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.0.2-5
- Rebuilt for Fedora 37 and 38

* Thu Apr 28 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.0.2-4
- Rebuilt for Fedora 36 and 37

* Sat Sep 25 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.0.2-3
- Disable brp-strip on Fedora 35 and later because it fails on Guile objects

* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.0.2-2
- Rebuilt for Fedora 34 and 35

* Mon Feb 15 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.0.2-1
- Initial packaging
