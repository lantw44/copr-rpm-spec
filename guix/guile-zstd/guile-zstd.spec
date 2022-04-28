%global debug_package %{nil}

# Workaround brp-strip failures on Fedora 35.
# https://github.com/rpm-software-management/rpm/issues/1765
%if 0%{?fedora} >= 35
%global __brp_strip   %{nil}
%endif

Name:           guile-zstd
Version:        0.1.1
Release:        4%{?dist}
Summary:        GNU Guile bindings to the zstd compression library

License:        GPLv3+
URL:            https://notabug.org/guile-zstd/guile-zstd
Source0:        https://notabug.org/guile-zstd/guile-zstd/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/2.2
%global guile_ccache_dir %{_libdir}/guile/2.2/site-ccache

BuildRequires:  autoconf, automake, make
BuildRequires:  pkgconfig(guile-2.2), pkgconfig(libzstd)
Requires:       guile22, libzstd-devel

%description
Guile-zstd: GNU Guile bindings to the zstd compression library.


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
%doc AUTHORS ChangeLog NEWS README
%{guile_source_dir}/zstd.scm
%{guile_ccache_dir}/zstd.go
%dir %{guile_source_dir}/zstd
%dir %{guile_ccache_dir}/zstd
%{guile_source_dir}/zstd/config.scm
%{guile_ccache_dir}/zstd/config.go


%changelog
* Thu Apr 28 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.1.1-4
- Rebuilt for Fedora 36 and 37

* Sat Sep 25 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.1.1-3
- Disable brp-strip on Fedora 35 and later because it fails on Guile objects

* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.1.1-2
- Rebuilt for Fedora 34 and 35

* Mon Feb 15 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.1.1-1
- Initial packaging
