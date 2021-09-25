%global debug_package %{nil}

# Workaround brp-strip failures on Fedora 35.
# https://github.com/rpm-software-management/rpm/issues/1765
%if 0%{?fedora} >= 35
%global __brp_strip   %{nil}
%endif

Name:           guile-zlib
Version:        0.1.0
Release:        2%{?dist}
Summary:        Guile bindings for zlib

License:        GPLv3+
URL:            https://notabug.org/guile-zlib/guile-zlib
Source0:        https://notabug.org/guile-zlib/guile-zlib/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/2.2
%global guile_ccache_dir %{_libdir}/guile/2.2/site-ccache

BuildRequires:  autoconf, automake, make
BuildRequires:  pkgconfig(guile-2.2), pkgconfig(zlib)
Requires:       guile22, zlib-devel

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
* Sat Sep 25 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-2
- Disable brp-strip on Fedora 35 and later because it fails on Guile objects

* Mon Jun 14 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-1
- Update to 0.1.0

* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.0.1-2
- Rebuilt for Fedora 34 and 35

* Mon Feb 15 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.0.1-1
- Initial packaging
