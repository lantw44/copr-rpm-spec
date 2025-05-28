%global debug_package %{nil}

Name:           guile-sqlite3
Version:        0.1.3
Release:        10%{?dist}
Summary:        Guile bindings for the SQLite3 database engine

License:        LGPL-3.0-or-later
URL:            https://notabug.org/guile-sqlite3/guile-sqlite3
Source0:        https://notabug.org/guile-sqlite3/guile-sqlite3/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/3.0
%global guile_ccache_dir %{_libdir}/guile/3.0/site-ccache

BuildRequires:  autoconf, automake, make
BuildRequires:  pkgconfig(guile-3.0), pkgconfig(sqlite3)
Requires:       guile30, sqlite-devel

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
* Sat May 24 2025 Ting-Wei Lan <lantw44@gmail.com> - 0.1.3-10
- Migrate to SPDX license

* Sun Nov 03 2024 Ting-Wei Lan <lantw44@gmail.com> - 0.1.3-9
- Rebuilt for Fedora 39, 40, 41, 42

* Sat Oct 05 2024 Ting-Wei Lan <lantw44@gmail.com> - 0.1.3-8
- Drop the brp-strip workaround

* Wed Apr 19 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.1.3-7
- Rebuilt for Fedora 38 and 39

* Sun Feb 12 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.1.3-6
- Switch to Guile 3.0

* Sat Oct 29 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.1.3-5
- Rebuilt for Fedora 37 and 38

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
