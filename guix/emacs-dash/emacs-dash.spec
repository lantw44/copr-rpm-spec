%global pkg dash
%global pkgname Dash

Name:           emacs-%{pkg}
Version:        2.13.0
Release:        4%{?dist}
Summary:        Dash is a modern list library for Emacs

Group:          Applications/Editors
License:        GPLv3+
URL:            https://github.com/magnars/dash.el
Source0:        https://github.com/magnars/dash.el/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  emacs, texinfo
Requires:       emacs(bin) >= %{_emacs_version}

%description
%{pkgname} is an add-on package for GNU Emacs. It is a modern list library for
Emacs. No cl required.


%prep
%autosetup -n dash.el-%{version} -p1


%build
./create-docs.sh


%install
mkdir -p %{buildroot}%{_emacs_sitelispdir}
install -m 755 -d %{buildroot}%{_emacs_sitelispdir}/dash
install -m 644 dash.el dash-functional.el \
    %{buildroot}%{_emacs_sitelispdir}/dash/
%{_emacs_bytecompile} %{buildroot}%{_emacs_sitelispdir}/dash/dash*.el
mkdir -p %{buildroot}%{_infodir}
gzip -9 < dash.info > %{buildroot}%{_infodir}/dash.info.gz


%post
/sbin/install-info %{_infodir}/dash.info.gz %{_infodir}/dir || :


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/dash.info.gz %{_infodir}/dir || :
fi


%files
%doc README.md
%dir %{_emacs_sitelispdir}/dash
%{_emacs_sitelispdir}/dash/dash.el
%{_emacs_sitelispdir}/dash/dash.elc
%{_emacs_sitelispdir}/dash/dash-functional.el
%{_emacs_sitelispdir}/dash/dash-functional.elc
%{_infodir}/dash.info.gz



%changelog
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
