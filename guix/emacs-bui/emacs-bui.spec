%global pkg bui
%global pkgname BUI

Name:           emacs-%{pkg}
Version:        1.1.0
Release:        4%{?dist}
Summary:        Buffer interface library for Emacs

Group:          Applications/Editors
License:        GPLv3+
URL:            https://github.com/alezost/bui.el
Source0:        https://github.com/alezost/bui.el/archive/v%{version}.tar.gz

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
* Mon Dec 11 2017 Ting-Wei Lan <lantw44@gmail.com> - 1.1.0-4
- Use autosetup macro

* Mon Oct 16 2017 Ting-Wei Lan <lantw44@gmail.com> - 1.1.0-3
- Rebuilt for Fedora 27 and 28

* Fri Jun 16 2017 Ting-Wei Lan <lantw44@gmail.com> - 1.1.0-2
- Add an empty build section to avoid rpmlint warning

* Sat May 27 2017 Ting-Wei Lan <lantw44@gmail.com> - 1.1.0-1
- Initial packaging
