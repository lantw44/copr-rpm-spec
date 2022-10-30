%global pkg geiser-guile
%global pkgname Geiser-Guile

Name:           emacs-%{pkg}
Version:        0.23.2
Release:        2%{?dist}
Summary:        Support for Guile in Geiser

License:        BSD
URL:            https://nongnu.org/geiser
Source0:        https://gitlab.com/emacs-geiser/guile/-/archive/%{version}/guile-%{version}.tar.gz#/%{pkg}-%{version}.tar.gz

# Use guile2.2 instead of guile because Guile 2.0 support has been dropped.
Patch0:         emacs-geiser-guile-default-guile-2.2.patch

BuildArch:      noarch
BuildRequires:  emacs
BuildRequires:  emacs-geiser >= 0.13
Requires:       emacs(bin) >= %{_emacs_version}
Requires:       emacs-geiser >= 0.13
Suggests:       guile22

%description
%{pkgname} is an add-on package for GNU Emacs. It provides support for using
GNU Guile in Emacs with Geiser.


%prep
%autosetup -n guile-%{version} -p1


%build


%install
install -m 755 -d %{buildroot}%{_emacs_sitelispdir}/geiser
install -m 644 *.el %{buildroot}%{_emacs_sitelispdir}/geiser/
%{_emacs_bytecompile} %{buildroot}%{_emacs_sitelispdir}/geiser/*.el
install -m 755 -d %{buildroot}%{_emacs_sitelispdir}/geiser/src/geiser
install -m 644 src/geiser/*.scm %{buildroot}%{_emacs_sitelispdir}/geiser/src/geiser/


%files
%license license
%doc readme.org
%{_emacs_sitelispdir}/geiser/geiser-guile.el
%{_emacs_sitelispdir}/geiser/geiser-guile.elc
%dir %{_emacs_sitelispdir}/geiser/src/geiser
%{_emacs_sitelispdir}/geiser/src/geiser/*.scm


%changelog
* Sat Oct 29 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.23.2-2
- Rebuilt for Fedora 37 and 38

* Thu Apr 28 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.23.2-1
- Update to 0.23.2

* Sat Sep 25 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.17-2
- Rebuilt for Fedora 35 and 36

* Mon Jun 14 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.17-1
- Initial packaging
