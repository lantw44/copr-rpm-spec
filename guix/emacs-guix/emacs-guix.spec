%global pkg guix
%global pkgname Guix

Name:           emacs-%{pkg}
Version:        0.5.2
Release:        5%{?dist}
Summary:        Emacs-Guix is an Emacs interface for GNU Guix package manager

License:        GPLv3+
URL:            https://emacs-guix.gitlab.io/website
Source0:        https://emacs-guix.gitlab.io/website/releases/%{name}-%{version}.tar.gz

# Fix crash when installing a package
# https://gitlab.com/emacs-guix/emacs-guix/-/issues/18
Patch0:         emacs-guix-0.5.2-guix-api-change.patch
Patch1:         emacs-guix-0.5.2-emacs-27.patch
Patch2:         emacs-guix-0.5.2-geiser-0.12.patch

%global debug_package    %{nil}
%global guile_source_dir %{_datadir}/guile/site/2.2
%global guile_ccache_dir %{_libdir}/guile/2.2/site-ccache

BuildRequires:  emacs, make, texinfo
BuildRequires:  guix >= 0.13.0
BuildRequires:  autoconf, automake
BuildRequires:  pkgconfig(guile-2.2), guile-gcrypt
BuildRequires:  emacs-geiser, emacs-dash, emacs-bui, emacs-edit-indirect
BuildRequires:  emacs-magit, emacs-magit-popup

Requires:       emacs(bin) >= %{_emacs_version}
Requires:       emacs-geiser, emacs-dash, emacs-bui, emacs-edit-indirect
Requires:       emacs-magit, emacs-magit-popup
Suggests:       guix

Obsoletes:      guix-emacs <= 0.8.3-1
Obsoletes:      guix-emacs-el <= 0.8.3-1
Provides:       guix-emacs <= 0.8.3-1
Provides:       guix-emacs-el <= 0.8.3-1

%description
Emacs-%{pkgname} is an add-on package for GNU Emacs. It provides various
features and tools for GNU Guix package manager.

It allows you to manage your Guix profile(s) from Emacs: to install, upgrade
and remove packages, to switch and remove profile generations, to display all
available info about packages and to do many other things.


%prep
%autosetup -p1


%build
autoreconf -fiv
%configure \
    --with-lispdir=%{_emacs_sitelispdir}/%{pkg} \
    --with-geiser-lispdir=%{_emacs_sitelispdir}/geiser \
    --with-dash-lispdir=%{_emacs_sitelispdir}/dash \
    --with-bui-lispdir=%{_emacs_sitelispdir}/bui \
    --with-editindirect-lispdir=%{_emacs_sitelispdir}/edit-indirect \
    --with-popup-lispdir=%{_emacs_sitelispdir}/magit-popup \
    GUILE=%{_bindir}/guile2.2 \
    GUILD=%{_bindir}/guild2.2
%make_build


%install
%make_install
gzip -9 %{buildroot}%{_infodir}/%{name}.info
# move the autoload script
mkdir -p %{buildroot}%{_emacs_sitestartdir}
mv %{buildroot}%{_emacs_sitelispdir}/guix/guix-autoloads.el \
    %{buildroot}%{_emacs_sitestartdir}/guix-autoloads.el


%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi


%files
%license COPYING
%doc NEWS README THANKS
%dir %{_emacs_sitelispdir}/%{pkg}
%{_emacs_sitelispdir}/%{pkg}/guix.el
%{_emacs_sitelispdir}/%{pkg}/guix.elc
%{_emacs_sitelispdir}/%{pkg}/guix-*.el
%{_emacs_sitelispdir}/%{pkg}/guix-*.elc
%{_emacs_sitestartdir}/guix-autoloads.el
%{guile_source_dir}/%{name}.scm
%{guile_ccache_dir}/%{name}.go
%dir %{guile_source_dir}/%{name}
%dir %{guile_ccache_dir}/%{name}
%{guile_source_dir}/%{name}/*.scm
%{guile_ccache_dir}/%{name}/*.go
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/images
%{_datadir}/%{name}/images/guix-logo.svg
%{_datadir}/%{name}/images/guixsd-logo.svg
%{_infodir}/%{name}.info.gz
%exclude %{_infodir}/dir


%changelog
* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.5.2-5
- Rebuilt for Fedora 34 and 35

* Mon Feb 15 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.5.2-4
- Make it compatible with Geiser 0.12

* Sun Nov  1 2020 Ting-Wei Lan <lantw44@gmail.com> - 0.5.2-3
- Fix build with Emacs 27

* Tue Jun 09 2020 Ting-Wei Lan <lantw44@gmail.com> - 0.5.2-2
- Add a patch from upstream to fix crash when installing a package

* Sun Apr 26 2020 Ting-Wei Lan <lantw44@gmail.com> - 0.5.2-1
- Update to 0.5.2

* Tue Sep 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.5.1.1-3
- Rebuilt for Fedora 31 and 32

* Wed May 15 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.5.1.1-2
- Switch to Guile 2.2
- Remove noarch because .go files are not architecture-independent

* Thu May 02 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.5.1.1-1
- Update to 0.5.1.1

* Sun Dec 02 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.5-1
- Update to 0.5

* Tue Oct 23 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.4.1.1-2
- Rebuilt for Fedora 29 and 30

* Sat Jul 07 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.4.1.1-1
- Update to 0.4.1.1
- Keep the name of autoloads script because it doesn't work when being renamed

* Mon Feb 26 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.3.4-1
- Update to 0.3.4
- Remove group tag because it is deprecated in Fedora

* Mon Dec 11 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.3.3-2
- Use autosetup and make_build macros

* Mon Oct 16 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.3.3-1
- Update to 0.3.3

* Sat May 27 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.3.1-1
- Initial packaging
