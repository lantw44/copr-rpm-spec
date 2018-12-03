%global pkg magit-popup
%global pkgname Magit-Popup

Name:           emacs-%{pkg}
Version:        2.12.4
Release:        1%{?dist}
Summary:        Define prefix-infix-suffix command combos for Emacs

License:        GPLv3+
URL:            https://magit.vc
Source0:        https://github.com/magit/magit-popup/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  emacs, texinfo
BuildRequires:  emacs-dash
Requires:       emacs(bin) >= %{_emacs_version}
Requires:       emacs-dash

%description
%{pkgname} is an add-on package for GNU Emacs. It implements a generic interface
for toggling switches and setting options and then invoking an Emacs command
which does something with these arguments.


%prep
%autosetup -n magit-popup-%{version} -p1


%build
%make_build LOAD_PATH='-L %{_emacs_sitelispdir}/dash'


%install
mkdir -p %{buildroot}%{_emacs_sitelispdir} %{buildroot}%{_emacs_sitestartdir}
install -m 755 -d %{buildroot}%{_emacs_sitelispdir}/magit-popup
install -m 644 magit-popup.el magit-popup.elc \
    %{buildroot}%{_emacs_sitelispdir}/magit-popup/
install -m 644 magit-popup-autoloads.el \
    %{buildroot}%{_emacs_sitelispdir}/magit-popup/
ln -rs %{buildroot}%{_emacs_sitelispdir}/magit-popup/magit-popup-autoloads.el \
    %{buildroot}%{_emacs_sitestartdir}
mkdir -p %{buildroot}%{_infodir}
gzip -9 < magit-popup.info > %{buildroot}%{_infodir}/magit-popup.info.gz


%post
/sbin/install-info %{_infodir}/magit-popup.info.gz %{_infodir}/dir || :


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/magit-popup.info.gz %{_infodir}/dir || :
fi


%files
%license LICENSE
%doc AUTHORS.md README.md magit-popup.org
%dir %{_emacs_sitelispdir}/magit-popup
%{_emacs_sitelispdir}/magit-popup/magit-popup.el
%{_emacs_sitelispdir}/magit-popup/magit-popup.elc
%{_emacs_sitelispdir}/magit-popup/magit-popup-autoloads.el
%{_emacs_sitestartdir}/magit-popup-autoloads.el
%{_infodir}/magit-popup.info.gz



%changelog
* Sun Dec 02 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.12.4-1
- Update to 2.12.4

* Tue Oct 23 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.12.3-2
- Rebuilt for Fedora 29 and 30

* Sat Jul 07 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.12.3-1
- Update to 2.12.3
- Fix autoloads by creating a symlink instead of moving the script itself

* Tue Mar 13 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.12.2-1
- Initial packaging
