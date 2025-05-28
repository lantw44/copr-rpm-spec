%global debug_package %{nil}

Name:           guile-bytestructures
Version:        1.0.10
Release:        9%{?dist}
Summary:        Structured access library to bytevector contents for Guile

License:        GPL-3.0-or-later
URL:            https://github.com/TaylanUB/scheme-bytestructures
Source0:        https://github.com/TaylanUB/scheme-bytestructures/releases/download/v%{version}/bytestructures-%{version}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/3.0
%global guile_ccache_dir %{_libdir}/guile/3.0/site-ccache

BuildRequires:  make
BuildRequires:  pkgconfig(guile-3.0)
Requires:       guile30

%description
This library offers a system imitating the type system of the C programming
language, to be used on bytevectors. C's type system works on raw memory, and
ours works on bytevectors which are an abstraction over raw memory in Scheme.
The system is in fact more powerful than the C type system, elevating types to
first-class status.


%prep
%autosetup -n bytestructures-%{version} -p1


%build
%configure
%make_build


%install
%make_install


%files
%license COPYING
%doc README.md
%dir %{guile_source_dir}/bytestructures
%dir %{guile_ccache_dir}/bytestructures
%{guile_source_dir}/bytestructures/body
%{guile_source_dir}/bytestructures/guile.scm
%{guile_ccache_dir}/bytestructures/guile.go
%dir %{guile_source_dir}/bytestructures/guile
%dir %{guile_ccache_dir}/bytestructures/guile
%{guile_source_dir}/bytestructures/guile/*.scm
%{guile_ccache_dir}/bytestructures/guile/*.go
%dir %{guile_source_dir}/bytestructures/r6
%dir %{guile_ccache_dir}/bytestructures/r6
%{guile_source_dir}/bytestructures/r6/bytevectors.scm
%{guile_ccache_dir}/bytestructures/r6/bytevectors.go
%{guile_source_dir}/bytestructures/r7


%changelog
* Sat May 24 2025 Ting-Wei Lan <lantw44@gmail.com> - 1.0.10-9
- Migrate to SPDX license

* Sun Nov 03 2024 Ting-Wei Lan <lantw44@gmail.com> - 1.0.10-8
- Rebuilt for Fedora 39, 40, 41, 42

* Sat Oct 05 2024 Ting-Wei Lan <lantw44@gmail.com> - 1.0.10-7
- Drop the brp-strip workaround

* Wed Apr 19 2023 Ting-Wei Lan <lantw44@gmail.com> - 1.0.10-6
- Rebuilt for Fedora 38 and 39

* Sun Feb 12 2023 Ting-Wei Lan <lantw44@gmail.com> - 1.0.10-5
- Switch to Guile 3.0

* Sat Oct 29 2022 Ting-Wei Lan <lantw44@gmail.com> - 1.0.10-4
- Rebuilt for Fedora 37 and 38

* Thu Apr 28 2022 Ting-Wei Lan <lantw44@gmail.com> - 1.0.10-3
- Rebuilt for Fedora 36 and 37

* Sat Sep 25 2021 Ting-Wei Lan <lantw44@gmail.com> - 1.0.10-2
- Disable brp-strip on Fedora 35 and later because it fails on Guile objects

* Mon Mar 15 2021 Ting-Wei Lan <lantw44@gmail.com> - 1.0.10-1
- Update to 1.0.10

* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 1.0.7-3
- Rebuilt for Fedora 34 and 35

* Sun Nov  1 2020 Ting-Wei Lan <lantw44@gmail.com> - 1.0.7-2
- Rebuilt for Fedora 33 and 34

* Sun Apr 26 2020 Ting-Wei Lan <lantw44@gmail.com> - 1.0.7-1
- Update to 1.0.7

* Tue Sep 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 1.0.6-1
- Update to 1.0.6

* Wed May 15 2019 Ting-Wei Lan <lantw44@gmail.com> - 1.0.5-2
- Switch to Guile 2.2

* Thu May 02 2019 Ting-Wei Lan <lantw44@gmail.com> - 1.0.5-1
- Update to 1.0.5

* Tue Oct 23 2018 Ting-Wei Lan <lantw44@gmail.com> - 1.0.3-2
- Rebuilt for Fedora 29 and 30

* Sat Jul 07 2018 Ting-Wei Lan <lantw44@gmail.com> - 1.0.3-1
- Update to 1.0.3

* Sat Dec 09 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.1-0.1.20171209git7ed31b1
- Initial packaging
