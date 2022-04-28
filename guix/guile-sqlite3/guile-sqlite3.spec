%global debug_package %{nil}

# Workaround brp-strip failures on Fedora 35.
# https://github.com/rpm-software-management/rpm/issues/1765
%if 0%{?fedora} >= 35
%global __brp_strip   %{nil}
%endif

Name:           guile-sqlite3
Version:        0.1.3
Release:        4%{?dist}
Summary:        Guile bindings for the SQLite3 database engine

License:        LGPLv3+
URL:            https://notabug.org/guile-sqlite3/guile-sqlite3
Source0:        https://notabug.org/guile-sqlite3/guile-sqlite3/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/2.2
%global guile_ccache_dir %{_libdir}/guile/2.2/site-ccache

BuildRequires:  autoconf, automake, make
BuildRequires:  pkgconfig(guile-2.2), pkgconfig(sqlite3)
Requires:       guile22, sqlite-devel

%description
Guile-SQLite3: Guile bindings for the SQLite3 database engine.


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
%license COPYING COPYING.LESSER
%doc AUTHORS ChangeLog NEWS README
%{guile_source_dir}/sqlite3.scm
%{guile_ccache_dir}/sqlite3.go


%changelog
* Thu Apr 28 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.1.3-4
- Rebuilt for Fedora 36 and 37

* Sat Sep 25 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.1.3-3
- Disable brp-strip on Fedora 35 and later because it fails on Guile objects

* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.1.3-2
- Rebuilt for Fedora 34 and 35

* Sun Nov  1 2020 Ting-Wei Lan <lantw44@gmail.com> - 0.1.3-1
- Update to 0.1.3

* Sun Apr 26 2020 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-7
- Rebuilt for Fedora 32 and 33

* Tue Sep 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-6
- Rebuilt for Fedora 31 and 32

* Wed May 15 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-5
- Switch to Guile 2.2
- Add ChangeLog to doc

* Wed May 01 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-4
- Rebuilt for Fedora 30 and 31

* Sun Dec 02 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-3
- Update upstream website and source file URL

* Tue Oct 23 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-2
- Rebuilt for Fedora 29 and 30

* Sun Jul 08 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-1
- Initial packaging
