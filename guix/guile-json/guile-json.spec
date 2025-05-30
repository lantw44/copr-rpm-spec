%global debug_package %{nil}

Name:           guile-json
Version:        4.7.3
Release:        6%{?dist}
Summary:        JSON module for Guile

License:        GPL-3.0-or-later
URL:            https://savannah.nongnu.org/projects/guile-json
Source0:        https://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/3.0
%global guile_ccache_dir %{_libdir}/guile/3.0/site-ccache

BuildRequires:  make
BuildRequires:  pkgconfig(guile-3.0)
Requires:       guile30

%description
guile-json is a JSON module for Guile. It supports parsing and building JSON
documents according to the https://json.org specification. These are the main
features:

- Strictly complies to https://json.org specification.
- Build JSON documents programmatically via macros.
- Unicode support for strings.
- Allows JSON pretty printing.


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
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{guile_source_dir}/json.scm
%{guile_ccache_dir}/json.go
%dir %{guile_source_dir}/json
%dir %{guile_ccache_dir}/json
%{guile_source_dir}/json/builder.scm
%{guile_ccache_dir}/json/builder.go
%{guile_source_dir}/json/parser.scm
%{guile_ccache_dir}/json/parser.go
%{guile_source_dir}/json/record.scm
%{guile_ccache_dir}/json/record.go


%changelog
* Sat May 24 2025 Ting-Wei Lan <lantw44@gmail.com> - 4.7.3-6
- Migrate to SPDX license

* Sun Nov 03 2024 Ting-Wei Lan <lantw44@gmail.com> - 4.7.3-5
- Rebuilt for Fedora 39, 40, 41, 42

* Sat Oct 05 2024 Ting-Wei Lan <lantw44@gmail.com> - 4.7.3-4
- Drop the brp-strip workaround

* Wed Apr 19 2023 Ting-Wei Lan <lantw44@gmail.com> - 4.7.3-3
- Rebuilt for Fedora 38 and 39

* Sun Feb 12 2023 Ting-Wei Lan <lantw44@gmail.com> - 4.7.3-2
- Switch to Guile 3.0

* Mon Dec 05 2022 Ting-Wei Lan <lantw44@gmail.com> - 4.7.3-1
- Update to 4.7.3

* Sat Oct 29 2022 Ting-Wei Lan <lantw44@gmail.com> - 4.7.2-1
- Update to 4.7.2

* Thu Apr 28 2022 Ting-Wei Lan <lantw44@gmail.com> - 4.7.1-1
- Update to 4.7.1

* Sat Sep 25 2021 Ting-Wei Lan <lantw44@gmail.com> - 4.5.2-3
- Disable brp-strip on Fedora 35 and later because it fails on Guile objects

* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 4.5.2-2
- Rebuilt for Fedora 34 and 35

* Mon Feb 15 2021 Ting-Wei Lan <lantw44@gmail.com> - 4.5.2-1
- Update to 4.5.2
- Run tests

* Sun Nov  1 2020 Ting-Wei Lan <lantw44@gmail.com> - 3.4.0-2
- Rebuilt for Fedora 33 and 34

* Sun Apr 26 2020 Ting-Wei Lan <lantw44@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Wed Sep 18 2019 Ting-Wei Lan <lantw44@gmail.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 1.3.2-4
- Rebuilt for Fedora 31 and 32

* Wed May 15 2019 Ting-Wei Lan <lantw44@gmail.com> - 1.3.2-3
- Switch to Guile 2.2

* Wed May 01 2019 Ting-Wei Lan <lantw44@gmail.com> - 1.3.2-2
- Rebuilt for Fedora 30 and 31

* Mon Dec 03 2018 Ting-Wei Lan <lantw44@gmail.com> - 1.3.2-1
- Update to 1.3.2

* Tue Oct 23 2018 Ting-Wei Lan <lantw44@gmail.com> - 1.0.1-2
- Rebuilt for Fedora 29 and 30

* Sat Jul 07 2018 Ting-Wei Lan <lantw44@gmail.com> - 1.0.1-1
- Update to 1.0.1

* Mon Dec 11 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.6.0-5
- Use autosetup and make_build macros
- Use HTTPS links in description

* Sun Dec 10 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.6.0-4
- Remove noarch because .go files are not architecture-independent

* Sat Dec 09 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.6.0-3
- Use HTTPS to download the source

* Mon Oct 16 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.6.0-2
- Rebuilt for Fedora 27 and 28

* Wed Mar 08 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.6.0-1
- Update to 0.6.0

* Sat Sep 10 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.5.0-2
- Rebuilt for Fedora 25 and 26

* Fri Apr 01 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.5.0-1
- Update to 0.5.0

* Thu Mar 03 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.4.0-2
- Rebuilt for Fedora 24 and 25

* Sat Nov 21 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.4.0-1
- Initial packaging
