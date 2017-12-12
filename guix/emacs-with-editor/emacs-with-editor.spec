%global pkg with-editor
%global pkgname With-Editor

Name:           emacs-%{pkg}
Version:        2.7.0
Release:        3%{?dist}
Summary:        Use the Emacsclient as the editor of child processes

Group:          Applications/Editors
License:        GPLv3+
URL:            https://magit.vc
Source0:        https://github.com/magit/with-editor/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  emacs, emacs-dash, texinfo
Requires:       emacs(bin) >= %{_emacs_version}
Requires:       emacs-dash

%description
%{pkgname} is an add-on package for GNU Emacs. It makes it easy to use the
Emacsclient as the editor of child processes, making sure they know how to
call home.


%prep
%autosetup -n with-editor-%{version} -p1


%build
make MAKEINFO='makeinfo --no-split' INSTALL_INFO='true' \
    EFLAGS='-L %{_emacs_sitelispdir}/dash' all


%install
mkdir -p %{buildroot}%{_emacs_sitelispdir}
install -m 755 -d %{buildroot}%{_emacs_sitelispdir}/with-editor
install -m 644 with-editor.el \
    %{buildroot}%{_emacs_sitelispdir}/with-editor/
%{_emacs_bytecompile} %{buildroot}%{_emacs_sitelispdir}/with-editor/with-editor*.el
mkdir -p %{buildroot}%{_infodir}
gzip -9 < with-editor.info > %{buildroot}%{_infodir}/with-editor.info.gz


%post
/sbin/install-info %{_infodir}/with-editor.info.gz %{_infodir}/dir || :


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/with-editor.info.gz %{_infodir}/dir || :
fi


%files
%license COPYING
%doc AUTHORS.md README.md with-editor.org
%dir %{_emacs_sitelispdir}/with-editor
%{_emacs_sitelispdir}/with-editor/with-editor.el
%{_emacs_sitelispdir}/with-editor/with-editor.elc
%{_infodir}/with-editor.info.gz



%changelog
* Mon Dec 11 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.7.0-3
- Use autosetup macro
- Rename the source tarball

* Sat Dec 09 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.7.0-2
- Use HTTPS in URL

* Mon Oct 16 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.7.0-1
- Update to 2.7.0

* Fri Jun 16 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.5.11-1
- Update to 2.5.11

* Wed Mar 08 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.5.10-1
- Update to 2.5.10

* Sat Dec 31 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.5.8-1
- Update to 2.5.8

* Fri Nov 04 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.5.5-1
- Update to 2.5.5

* Sat Sep 10 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.5.1-2
- Rebuilt for Fedora 25 and 26

* Tue Jun 21 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.5.1-1
- Update to 2.5.1
- Include license file and all documents
- Disable Texinfo dir file generation in Makefile, which is useless

* Fri Mar 04 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.5.0-1
- Initial packaging
