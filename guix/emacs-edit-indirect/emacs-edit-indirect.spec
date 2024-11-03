%global pkg edit-indirect
%global pkgname edit-indirect

Name:           emacs-%{pkg}
Version:        0.1.13
Release:        1%{?dist}
Summary:        Edit regions in separate buffers

License:        BSD
URL:            https://github.com/Fanael/edit-indirect
Source0:        https://github.com/Fanael/edit-indirect/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  emacs

Requires:       emacs(bin) >= %{_emacs_version}

%description
%{pkgname} is an add-on package for GNU Emacs. It allows editing regions in
%separate buffers.


%prep
%autosetup -n edit-indirect-%{version} -p1


%build


%install
mkdir -p %{buildroot}%{_emacs_sitelispdir}
install -m 755 -d %{buildroot}%{_emacs_sitelispdir}/edit-indirect
install -m 644 *.el %{buildroot}%{_emacs_sitelispdir}/edit-indirect/
%{_emacs_bytecompile} %{buildroot}%{_emacs_sitelispdir}/edit-indirect/*.el


%files
%dir %{_emacs_sitelispdir}/edit-indirect
%{_emacs_sitelispdir}/edit-indirect/edit-indirect.el
%{_emacs_sitelispdir}/edit-indirect/edit-indirect.elc


%changelog
* Sat Nov 02 2024 Ting-Wei Lan <lantw44@gmail.com> - 0.1.13-1
- Update to 0.1.13

* Wed Apr 19 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.1.10-2
- Rebuilt for Fedora 38 and 39

* Sat Oct 29 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.1.10-1
- Update to 0.1.10

* Thu Apr 28 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.1.8-1
- Update to 0.1.8

* Sat Sep 25 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.1.6-3
- Rebuilt for Fedora 35 and 36

* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.1.6-2
- Rebuilt for Fedora 34 and 35

* Sun Nov  1 2020 Ting-Wei Lan <lantw44@gmail.com> - 0.1.6-1
- Update to 0.1.6

* Sun Apr 26 2020 Ting-Wei Lan <lantw44@gmail.com> - 0.1.5-3
- Rebuilt for Fedora 32 and 33

* Tue Sep 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.1.5-2
- Rebuilt for Fedora 31 and 32

* Thu May 16 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.1.5-1
- Initial packaging
