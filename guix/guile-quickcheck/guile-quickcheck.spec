%global debug_package %{nil}

Name:           guile-quickcheck
Version:        0.1.0
Release:        5%{?dist}
Summary:        Randomized property-based testing for Guile

License:        GPL-3.0-or-later
URL:            https://ngyro.com/software/guile-quickcheck.html
Source0:        https://files.ngyro.com/%{name}/%{name}-%{version}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/3.0
%global guile_ccache_dir %{_libdir}/guile/3.0/site-ccache

BuildRequires:  make
BuildRequires:  pkgconfig(guile-3.0)
Requires:       guile30

%description
This Guile library provides tools for randomized, property-based testing. It
follows closely the QuickCheck library written in Haskell, with inspiration from
the Racket version. You can use it to define a property (a predicate with
specifications for its inputs) and test it by generating many random inputs and
seeing if it holds.


%prep
%autosetup -p1


%build
%configure
%make_build


%check
%{__make} %{?_smp_mflags} check


%install
%make_install


%files
%license COPYING COPYING.CC0
%doc README
%{guile_source_dir}/quickcheck.scm
%{guile_ccache_dir}/quickcheck.go
%dir %{guile_source_dir}/quickcheck
%dir %{guile_ccache_dir}/quickcheck
%{guile_source_dir}/quickcheck/*.scm
%{guile_ccache_dir}/quickcheck/*.go


%changelog
* Sat May 24 2025 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-5
- Migrate to SPDX license

* Sun Nov 03 2024 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-4
- Rebuilt for Fedora 39, 40, 41, 42

* Sat Oct 05 2024 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-3
- Drop the brp-strip workaround

* Wed Apr 19 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-2
- Rebuilt for Fedora 38 and 39

* Sun Feb 12 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-1
- Initial packaging
