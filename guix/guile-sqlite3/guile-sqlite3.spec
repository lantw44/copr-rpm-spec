%global debug_package %{nil}

Name:           guile-sqlite3
Version:        0.1.0
Release:        2%{?dist}
Summary:        Guile bindings for the SQLite3 database engine

License:        LGPLv3+
URL:            https://notabug.org/civodul/guile-sqlite3
Source0:        https://notabug.org/civodul/guile-sqlite3/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/2.0
%global guile_ccache_dir %{_libdir}/guile/2.0/site-ccache

BuildRequires:  autoconf, automake, pkgconfig(guile-2.0), pkgconfig(sqlite3)
Requires:       guile, sqlite-devel

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
%doc AUTHORS NEWS README
%{guile_source_dir}/sqlite3.scm
%{guile_ccache_dir}/sqlite3.go


%changelog
* Tue Oct 23 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-2
- Rebuilt for Fedora 29 and 30

* Sun Jul 08 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-1
- Initial packaging
