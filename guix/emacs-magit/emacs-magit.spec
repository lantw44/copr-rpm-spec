%define pkg magit
%define pkgname Magit

%if %($(pkg-config emacs) ; echo $?)
%define emacs_version 22.1
%define emacs_lispdir %{_datadir}/emacs/site-lisp
%define emacs_startdir %{_datadir}/emacs/site-lisp/site-start.d
%else
%define emacs_version %(pkg-config emacs --modversion)
%define emacs_lispdir %(pkg-config emacs --variable sitepkglispdir)
%define emacs_startdir %(pkg-config emacs --variable sitestartdir)
%endif

Name:           emacs-%{pkg}
Version:        2.7.0
Release:        1%{?dist}
Summary:        Emacs interface to the most common Git operations

Group:          Applications/Editors
License:        GPLv3+
URL:            http://magit.vc

Source0:        https://github.com/magit/magit/releases/download/%{version}/magit-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  emacs, emacs-dash, emacs-with-editor, git-core, texinfo
Requires:       emacs(bin) >= %{emacs_version}
Requires:       emacs-dash, emacs-with-editor

Obsoletes:      emacs-%{pkg}-el < 2.3.1-1
Provides:       emacs-%{pkg}-el < 2.3.1-1

%description
%{pkgname} is an add-on package for GNU Emacs. It is an interface to
the Git source-code management system that aims to make the most
common operations convenient.

%prep
%setup -q -n magit-%{version}

%build
make \
    MAKEINFO='makeinfo --no-split' \
    LOAD_PATH='-L %{emacs_lispdir}/dash -L %{emacs_lispdir}/with-editor -L %{_builddir}/magit-%{version}/lisp -L .'

%install
%make_install \
    PREFIX=%{_prefix} docdir=%{_pkgdocdir} \
    LOAD_PATH='-L %{emacs_lispdir}/dash -L %{emacs_lispdir}/with-editor -L %{_builddir}/magit-%{version}/lisp -L .'

# clean up after magit's installer's assumptions
mkdir -p $RPM_BUILD_ROOT%{emacs_startdir}
mv $RPM_BUILD_ROOT%{emacs_lispdir}/magit/magit-autoloads.el \
    $RPM_BUILD_ROOT%{emacs_startdir}/emacs-magit-mode.el
gzip -9 $RPM_BUILD_ROOT%{_infodir}/magit.info
gzip -9 $RPM_BUILD_ROOT%{_infodir}/magit-popup.info


%post
/sbin/install-info /usr/share/info/magit.info.gz /usr/share/info/dir
/sbin/install-info /usr/share/info/magit-popup.info.gz /usr/share/info/dir


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete /usr/share/info/magit.info.gz /usr/share/info/dir
    /sbin/install-info --delete /usr/share/info/magit-popup.info.gz /usr/share/info/dir
fi


%files
%license COPYING
%doc README.md
%{emacs_lispdir}/%{pkg}/*.el
%{emacs_lispdir}/%{pkg}/*.elc
%{emacs_startdir}/emacs-magit-mode.el
%{_infodir}/magit.info.gz
%{_infodir}/magit-popup.info.gz
%dir %{emacs_lispdir}/%{pkg}
%{_pkgdocdir}/AUTHORS.md


%changelog
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
