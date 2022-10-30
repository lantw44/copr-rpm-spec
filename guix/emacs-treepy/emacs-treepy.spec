%global pkg treepy
%global pkgname treepy

Name:           emacs-%{pkg}
Version:        0.1.2
Release:        5%{?dist}
Summary:        Functions for traversing tree-like data

License:        GPLv3+
URL:            https://github.com/volrath/treepy.el
Source0:        https://github.com/volrath/treepy.el/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  emacs

Requires:       emacs(bin) >= %{_emacs_version}

%description
%{pkgname} is an add-on package for GNU Emacs. It includes a set of generic
functions for traversing tree-like data structures recursively and/or
iteratively, ported from clojure.walk and clojure.zip respectively.


%prep
%autosetup -n treepy.el-%{version} -p1


%build


%install
mkdir -p %{buildroot}%{_emacs_sitelispdir}
install -m 755 -d %{buildroot}%{_emacs_sitelispdir}/treepy
install -m 644 *.el %{buildroot}%{_emacs_sitelispdir}/treepy/
%{_emacs_bytecompile} %{buildroot}%{_emacs_sitelispdir}/treepy/*.el


%files
%license LICENSE
%doc README.md
%dir %{_emacs_sitelispdir}/treepy
%{_emacs_sitelispdir}/treepy/treepy.el
%{_emacs_sitelispdir}/treepy/treepy.elc


%changelog
* Sat Oct 29 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.1.2-5
- Rebuilt for Fedora 37 and 38

* Thu Apr 28 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.1.2-4
- Rebuilt for Fedora 36 and 37

* Sat Sep 25 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.1.2-3
- Rebuilt for Fedora 35 and 36

* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.1.2-2
- Rebuilt for Fedora 34 and 35

* Sun Nov  1 2020 Ting-Wei Lan <lantw44@gmail.com> - 0.1.2-1
- Update to 0.1.2

* Sun Apr 26 2020 Ting-Wei Lan <lantw44@gmail.com> - 0.1.1-4
- Rebuilt for Fedora 32 and 33

* Tue Sep 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.1.1-3
- Rebuilt for Fedora 31 and 32

* Wed May 01 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.1.1-2
- Rebuilt for Fedora 30 and 31

* Sun Dec 02 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.1.1-1
- Initial packaging
