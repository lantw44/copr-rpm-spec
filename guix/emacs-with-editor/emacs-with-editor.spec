%global pkg with-editor
%global pkgname With-Editor

Name:           emacs-%{pkg}
Version:        2.9.1
Release:        1%{?dist}
Summary:        Use the Emacsclient as the editor of child processes

License:        GPLv3+
URL:            https://magit.vc
Source0:        https://github.com/magit/with-editor/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  emacs, texinfo
Requires:       emacs(bin) >= %{_emacs_version}

%description
%{pkgname} is an add-on package for GNU Emacs. It makes it easy to use the
Emacsclient as the editor of child processes, making sure they know how to
call home.


%prep
%autosetup -n with-editor-%{version} -p1


%build
%make_build


%install
mkdir -p %{buildroot}%{_emacs_sitelispdir} %{buildroot}%{_emacs_sitestartdir}
install -m 755 -d %{buildroot}%{_emacs_sitelispdir}/with-editor
install -m 644 with-editor.el with-editor.elc \
    %{buildroot}%{_emacs_sitelispdir}/with-editor/
install -m 644 with-editor-autoloads.el \
    %{buildroot}%{_emacs_sitelispdir}/with-editor/
ln -rs %{buildroot}%{_emacs_sitelispdir}/with-editor/with-editor-autoloads.el \
    %{buildroot}%{_emacs_sitestartdir}
mkdir -p %{buildroot}%{_infodir}
gzip -9 < with-editor.info > %{buildroot}%{_infodir}/with-editor.info.gz


%post
/sbin/install-info %{_infodir}/with-editor.info.gz %{_infodir}/dir || :


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/with-editor.info.gz %{_infodir}/dir || :
fi


%files
%license LICENSE
%doc AUTHORS.md README.md with-editor.org
%dir %{_emacs_sitelispdir}/with-editor
%{_emacs_sitelispdir}/with-editor/with-editor.el
%{_emacs_sitelispdir}/with-editor/with-editor.elc
%{_emacs_sitelispdir}/with-editor/with-editor-autoloads.el
%{_emacs_sitestartdir}/with-editor-autoloads.el
%{_infodir}/with-editor.info.gz



%changelog
* Sun Apr 26 2020 Ting-Wei Lan <lantw44@gmail.com> - 2.9.1-1
- Update to 2.9.1

* Tue Sep 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 2.8.3-2
- Rebuilt for Fedora 31 and 32

* Tue May 14 2019 Ting-Wei Lan <lantw44@gmail.com> - 2.8.3-1
- Update to 2.8.3

* Thu May 02 2019 Ting-Wei Lan <lantw44@gmail.com> - 2.8.1-1
- Update to 2.8.1

* Sun Dec 02 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.8.0-1
- Update to 2.8.0

* Tue Oct 23 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.7.3-2
- Rebuilt for Fedora 29 and 30

* Sat Jul 07 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.7.3-1
- Update to 2.7.3
- Fix autoloads by creating a symlink instead of moving the script itself

* Mon Feb 26 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.7.1-1
- Update to 2.7.1
- Install the generated autoloads file
- Remove group tag because it is deprecated in Fedora

* Mon Dec 11 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.7.0-3
- Use autosetup and make_build macros
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
