%global pkg bui
%global pkgname BUI

Name:           emacs-%{pkg}
Version:        1.2.1
Release:        11%{?dist}
Summary:        Buffer interface library for Emacs

License:        GPL-3.0-or-later
URL:            https://github.com/alezost/bui.el
Source0:        https://github.com/alezost/bui.el/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  emacs
BuildRequires:  emacs-dash

Requires:       emacs(bin) >= %{_emacs_version}
Requires:       emacs-dash

%description
%{pkgname} is an add-on package for GNU Emacs. It is an Emacs library that can
be used to make user interfaces to display some kind of entries (like packages,
buffers, functions, etc.).


%prep
%autosetup -n bui.el-%{version} -p1


%build


%install
mkdir -p %{buildroot}%{_emacs_sitelispdir}
install -m 755 -d %{buildroot}%{_emacs_sitelispdir}/bui
install -m 644 *.el %{buildroot}%{_emacs_sitelispdir}/bui/
%{_emacs_bytecompile} %{buildroot}%{_emacs_sitelispdir}/bui/*.el


%files
%license COPYING
%doc NEWS README.org
%dir %{_emacs_sitelispdir}/bui
%{_emacs_sitelispdir}/bui/bui.el
%{_emacs_sitelispdir}/bui/bui.elc
%{_emacs_sitelispdir}/bui/bui-*.el
%{_emacs_sitelispdir}/bui/bui-*.elc


%changelog
* Sat May 24 2025 Ting-Wei Lan <lantw44@gmail.com> - 1.2.1-11
- Migrate to SPDX license

* Sun Nov 03 2024 Ting-Wei Lan <lantw44@gmail.com> - 1.2.1-10
- Rebuilt for Fedora 39, 40, 41, 42

* Wed Apr 19 2023 Ting-Wei Lan <lantw44@gmail.com> - 1.2.1-9
- Rebuilt for Fedora 38 and 39

* Sat Oct 29 2022 Ting-Wei Lan <lantw44@gmail.com> - 1.2.1-8
- Rebuilt for Fedora 37 and 38

* Thu Apr 28 2022 Ting-Wei Lan <lantw44@gmail.com> - 1.2.1-7
- Rebuilt for Fedora 36 and 37

* Sat Sep 25 2021 Ting-Wei Lan <lantw44@gmail.com> - 1.2.1-6
- Rebuilt for Fedora 35 and 36

* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 1.2.1-5
- Rebuilt for Fedora 34 and 35

* Sun Nov  1 2020 Ting-Wei Lan <lantw44@gmail.com> - 1.2.1-4
- Rebuilt for Fedora 33 and 34

* Sun Apr 26 2020 Ting-Wei Lan <lantw44@gmail.com> - 1.2.1-3
- Rebuilt for Fedora 32 and 33

* Tue Sep 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 1.2.1-2
- Rebuilt for Fedora 31 and 32

* Thu May 02 2019 Ting-Wei Lan <lantw44@gmail.com> - 1.2.1-1
- Update to 1.2.1

* Sun Dec 02 2018 Ting-Wei Lan <lantw44@gmail.com> - 1.2.0-1
- Update to 1.2.0

* Tue Oct 23 2018 Ting-Wei Lan <lantw44@gmail.com> - 1.1.0-6
- Rebuilt for Fedora 29 and 30

* Mon Feb 26 2018 Ting-Wei Lan <lantw44@gmail.com> - 1.1.0-5
- Remove group tag because it is deprecated in Fedora

* Mon Dec 11 2017 Ting-Wei Lan <lantw44@gmail.com> - 1.1.0-4
- Use autosetup macro
- Rename the source tarball

* Mon Oct 16 2017 Ting-Wei Lan <lantw44@gmail.com> - 1.1.0-3
- Rebuilt for Fedora 27 and 28

* Fri Jun 16 2017 Ting-Wei Lan <lantw44@gmail.com> - 1.1.0-2
- Add an empty build section to avoid rpmlint warning

* Sat May 27 2017 Ting-Wei Lan <lantw44@gmail.com> - 1.1.0-1
- Initial packaging
