%global pkg dash
%global pkgname Dash

Name:           emacs-%{pkg}
Version:        2.20.0
Release:        1%{?dist}
Summary:        Dash is a modern list library for Emacs

License:        GPL-3.0-or-later
URL:            https://github.com/magnars/dash.el
Source0:        https://github.com/magnars/dash.el/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  emacs, make, texinfo
Requires:       emacs(bin) >= %{_emacs_version}

%description
%{pkgname} is an add-on package for GNU Emacs. It is a modern list library for
Emacs. No cl required.


%prep
%autosetup -n dash.el-%{version} -p1


%build
%make_build WERROR="'(setq byte-compile-error-on-warn nil)'"
makeinfo --no-split dash.texi


%check
%{__make} %{?_smp_mflags} check


%install
mkdir -p %{buildroot}%{_emacs_sitelispdir}
install -m 755 -d %{buildroot}%{_emacs_sitelispdir}/dash
install -m 644 dash.el dash.elc dash-functional.el \
    %{buildroot}%{_emacs_sitelispdir}/dash/
%{_emacs_bytecompile} %{buildroot}%{_emacs_sitelispdir}/dash/dash-functional.el
mkdir -p %{buildroot}%{_infodir}
gzip -9 < dash.info > %{buildroot}%{_infodir}/dash.info.gz


%post
/sbin/install-info %{_infodir}/dash.info.gz %{_infodir}/dir || :


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/dash.info.gz %{_infodir}/dir || :
fi


%files
%license LICENSE
%doc NEWS.md README.md
%dir %{_emacs_sitelispdir}/dash
%{_emacs_sitelispdir}/dash/dash.el
%{_emacs_sitelispdir}/dash/dash.elc
%{_emacs_sitelispdir}/dash/dash-functional.el
%{_emacs_sitelispdir}/dash/dash-functional.elc
%{_infodir}/dash.info.gz



%changelog
* Sat May 24 2025 Ting-Wei Lan <lantw44@gmail.com> - 2.20.0-1
- Update to 2.20.0
- Migrate to SPDX license

* Sat Nov 02 2024 Ting-Wei Lan <lantw44@gmail.com> - 2.19.1-5
- Disable byte-compile-error-on-warn for Emacs 29

* Wed Apr 19 2023 Ting-Wei Lan <lantw44@gmail.com> - 2.19.1-4
- Rebuilt for Fedora 38 and 39

* Sat Oct 29 2022 Ting-Wei Lan <lantw44@gmail.com> - 2.19.1-3
- Fix build with Emacs 28

* Thu Apr 28 2022 Ting-Wei Lan <lantw44@gmail.com> - 2.19.1-2
- Rebuilt for Fedora 36 and 37

* Sat Sep 25 2021 Ting-Wei Lan <lantw44@gmail.com> - 2.19.1-1
- Update to 2.19.1

* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 2.18.1-1
- Update to 2.18.1

* Sun Nov  1 2020 Ting-Wei Lan <lantw44@gmail.com> - 2.17.0-2
- Rebuilt for Fedora 33 and 34

* Sat Apr 25 2020 Ting-Wei Lan <lantw44@gmail.com> - 2.17.0-1
- Update to 2.17.0

* Tue Sep 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 2.16.0-2
- Rebuilt for Fedora 31 and 32

* Tue May 14 2019 Ting-Wei Lan <lantw44@gmail.com> - 2.16.0-1
- Update to 2.16.0

* Wed May 01 2019 Ting-Wei Lan <lantw44@gmail.com> - 2.14.1-3
- Rebuilt for Fedora 30 and 31

* Tue Oct 23 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.14.1-2
- Rebuilt for Fedora 29 and 30

* Sat Jul 07 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.14.1-1
- Update to 2.14.1

* Mon Feb 26 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.13.0-5
- Remove group tag because it is deprecated in Fedora

* Mon Dec 11 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.13.0-4
- Use autosetup macro
- Rename the source tarball

* Mon Oct 16 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.13.0-3
- Rebuilt for Fedora 27 and 28

* Wed Mar 08 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.13.0-2
- Rebuilt for Fedora 26 and 27

* Fri Nov 04 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.13.0-1
- Update to 2.13.0

* Sat Sep 10 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.12.1-3
- Rebuilt for Fedora 25 and 26

* Thu Mar 03 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.12.1-2
- Rebuilt for Fedora 24 and 25

* Sat Nov 21 2015 Ting-Wei Lan <lantw44@gmail.com> - 2.12.1-1
- Initial packaging
