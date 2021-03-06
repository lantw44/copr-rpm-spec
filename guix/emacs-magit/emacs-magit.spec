%global pkg magit
%global pkgname Magit

%if %($(pkg-config emacs) ; echo $?)
%global emacs_version 22.1
%global emacs_lispdir %{_datadir}/emacs/site-lisp
%global emacs_startdir %{_datadir}/emacs/site-lisp/site-start.d
%else
%global emacs_version %(pkg-config emacs --modversion)
%global emacs_lispdir %(pkg-config emacs --variable sitepkglispdir)
%global emacs_startdir %(pkg-config emacs --variable sitestartdir)
%endif

Name:           emacs-%{pkg}
Version:        2.13.1
Release:        6%{?dist}
Summary:        Emacs interface to the most common Git operations

License:        GPLv3+
URL:            https://magit.vc

# Source0:        https://github.com/magit/magit/releases/download/%{version}/magit-%{version}.tar.gz
Source0:        https://github.com/magit/magit/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  emacs, git-core, make, texinfo
BuildRequires:  emacs-dash, emacs-ghub, emacs-magit-popup, emacs-with-editor
Requires:       emacs(bin) >= %{emacs_version}
Requires:       emacs-dash, emacs-ghub, emacs-magit-popup, emacs-with-editor

Obsoletes:      emacs-%{pkg}-el < 2.3.1-1
Provides:       emacs-%{pkg}-el < 2.3.1-1

%description
%{pkgname} is an add-on package for GNU Emacs. It is an interface to
the Git source-code management system that aims to make the most
common operations convenient.

%prep
%autosetup -n magit-%{version} -p1

%build
%make_build \
    DASH_DIR=%{emacs_lispdir}/dash \
    GHUB_DIR=%{emacs_lispdir}/ghub \
    GRAPHQL_DIR=%{emacs_lispdir}/graphql \
    MAGIT_POPUP_DIR=%{emacs_lispdir}/magit-popup \
    TREEPY_DIR=%{emacs_lispdir}/treepy \
    WITH_EDITOR_DIR=%{emacs_lispdir}/with-editor

%install
%make_install PREFIX=%{_prefix} docdir=%{_pkgdocdir}

# clean up after magit's installer's assumptions
mkdir -p $RPM_BUILD_ROOT%{emacs_startdir}
ln -rs $RPM_BUILD_ROOT%{emacs_lispdir}/magit/magit-autoloads.el \
    $RPM_BUILD_ROOT%{emacs_startdir}
gzip -9 $RPM_BUILD_ROOT%{_infodir}/magit.info


%post
/sbin/install-info /usr/share/info/magit.info.gz /usr/share/info/dir


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete /usr/share/info/magit.info.gz /usr/share/info/dir
fi


%files
%license LICENSE
%doc README.md
%{emacs_lispdir}/%{pkg}/*.el
%{emacs_lispdir}/%{pkg}/*.elc
%{emacs_startdir}/magit-autoloads.el
%{_infodir}/magit.info.gz
%dir %{emacs_lispdir}/%{pkg}
%{_pkgdocdir}/AUTHORS.md


%changelog
* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 2.13.1-6
- Rebuilt for Fedora 34 and 35

* Sun Nov  1 2020 Ting-Wei Lan <lantw44@gmail.com> - 2.13.1-5
- Rebuilt for Fedora 33 and 34

* Sun Apr 26 2020 Ting-Wei Lan <lantw44@gmail.com> - 2.13.1-4
- Rebuilt for Fedora 32 and 33

* Tue Sep 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 2.13.1-3
- Rebuilt for Fedora 31 and 32

* Wed May 01 2019 Ting-Wei Lan <lantw44@gmail.com> - 2.13.1-2
- Rebuilt for Fedora 30 and 31

* Sun Dec 02 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.13.1-1
- Update to upstream version 2.13.1

* Tue Oct 23 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.13.0-2
- Rebuilt for Fedora 29 and 30

* Sat Jul 07 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.13.0-1
- Update to upstream version 2.13.0
- Fix autoloads by creating a symlink instead of moving the script itself

* Mon Feb 26 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.11.0-4
- Add dependency on emacs-ghub and emacs-magit-popup
- Remove magit-popup.info because it is already provided by emacs-magit-popup
- Remove group tag because it is deprecated in Fedora

* Mon Dec 11 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.11.0-3
- Use autosetup and make_build macros
- Replace define with global

* Sat Dec 09 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.11.0-2
- Use HTTPS in URL

* Mon Oct 16 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.11.0-1
- Update to upstream version 2.11.0

* Wed Mar 08 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.10.3-1
- Update to upstream version 2.10.3

* Sat Dec 31 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.9.0-1
- Update to upstream version 2.9.0

* Fri Nov 04 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.8.0-1
- Update to upstream version 2.8.0

* Sat Sep 10 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.7.0-2
- Rebuilt for Fedora 25 and 26

* Tue Jun 21 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.7.0-1
- Update to upstream version 2.7.0

* Fri Apr 01 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.6.0-1
- Update to upstream version 2.6.0

* Thu Mar 03 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.5.0-1
- Update to upstream version 2.5.0

* Sat Nov 21 2015 Ting-Wei Lan <lantw44@gmail.com> - 2.3.1-1
- Update to upstream version 2.3.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jan  4 2015 Jens Petersen <petersen@redhat.com> - 1.2.2-1
- update to 1.2.2 which works with emacs-24.4 (#1172690)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 10 2013 Tom Moertel <tom@moertel.com> - 1.2.0-1
- Update to upstream version 1.2.0

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jan 25 2012 Tom Moertel <tom@moertel.com> - 1.1.1-1
- Update to upstream 1.1.1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri May 13 2011 Tom Moertel <tom@moertel.com> - 1.0.0-1
- Updated to upstream 1.0.0

* Wed Aug  4 2010 Tom Moertel <tom@moertel.com> - 0.8.2-1
- Updated to upstream 0.8.2

* Wed Aug 26 2009 Tom Moertel <tom@moertel.com> - 0.7-6
- Updated for Magit 0.7 final release (note: upstream removed FDL from tarball)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-5.20090122git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-4.20090122git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 29 2009  <tom@moertel.com> - 0.7-3.20090122git
- Added missing build dependency: texinfo

* Tue Jan 27 2009  <tom@moertel.com> - 0.7-2.20090122git
- Made fixes per Fedora packaging review (thanks Jerry James)

* Fri Jan 23 2009  <tom@moertel.com> - 0.7-1.20090122git
- Initial packaging.
