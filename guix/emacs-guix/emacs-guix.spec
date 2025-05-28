%global commit 21e8ade02858fe633afb5dad11c59e0a779baea2
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global debug_package %{nil}

%global pkg guix
%global pkgname Guix

Name:           emacs-%{pkg}
Version:        0.5.2
Release:        14.20250520git%{shortcommit}%{?dist}
Summary:        Emacs-Guix is an Emacs interface for GNU Guix package manager

License:        GPL-3.0-or-later
URL:            https://guix.gnu.org
Source0:        https://codeberg.org/guix/%{name}/archive/%{commit}.tar.gz#/%{name}-%{commit}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/3.0
%global guile_ccache_dir %{_libdir}/guile/3.0/site-ccache

BuildRequires:  emacs, make, texinfo
BuildRequires:  guix >= 0.13.0
BuildRequires:  autoconf, automake
BuildRequires:  pkgconfig(guile-3.0), guile-gcrypt
BuildRequires:  emacs-dash, emacs-bui, emacs-edit-indirect, emacs-magit-popup
BuildRequires:  (emacs-geiser-guile >= 0.13 or emacs-geiser < 0.13)

Requires:       emacs(bin) >= %{_emacs_version}
Requires:       emacs-dash, emacs-bui, emacs-edit-indirect, emacs-magit-popup
Requires:       (emacs-geiser-guile >= 0.13 or emacs-geiser < 0.13)
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
%autosetup -p1 -n %{name}


%build
autoreconf -fiv
%configure \
    --with-lispdir=%{_emacs_sitelispdir}/%{pkg} \
    --with-geiser-lispdir=%{_emacs_sitelispdir}/geiser \
    --with-dash-lispdir=%{_emacs_sitelispdir}/dash \
    --with-bui-lispdir=%{_emacs_sitelispdir}/bui \
    --with-editindirect-lispdir=%{_emacs_sitelispdir}/edit-indirect \
    --with-popup-lispdir=%{_emacs_sitelispdir}/magit-popup \
    GUILE=%{_bindir}/guile3.0 \
    GUILD=%{_bindir}/guild3.0

# Fedora 40 has Guile 3.0.7, but cross-module-inlining is added in Guile 3.0.8.
%if 0%{?fedora} < 41
sed -i 's|-Ono-cross-module-inlining||g' scheme/Makefile
%endif

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
%{_infodir}/%{name}.info.gz
%exclude %{_infodir}/dir


%changelog
* Sat May 24 2025 Ting-Wei Lan <lantw44@gmail.com> - 0.5.2-14.20250520git21e8ade
- Update to the latest git snapshot
- Migrate to SPDX license

* Sat Nov 02 2024 Ting-Wei Lan <lantw44@gmail.com> - 0.5.2-13.20231206git455272c
- Update to the latest git snapshot
- Fix build with Guile 3.0.7 for Fedora 40

* Sat Oct 05 2024 Ting-Wei Lan <lantw44@gmail.com> - 0.5.2-12.20221011gitcf5b7a4
- Drop the brp-strip workaround

* Wed Apr 19 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.5.2-11.20221011gitcf5b7a4
- Rebuilt for Fedora 38 and 39

* Sun Feb 12 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.5.2-10.20221011gitcf5b7a4
- Update to the latest git snapshot
- Switch to Guile 3.0

* Sat Oct 29 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.5.2-9
- Rebuilt for Fedora 37 and 38

* Thu Apr 28 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.5.2-8
- Include the path to emacs-transient because emacs-geiser needs it

* Sat Sep 25 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.5.2-7
- Disable brp-strip on Fedora 35 and later because it fails on Guile objects

* Mon Jun 14 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.5.2-6
- Drop dependency on emacs-magit because it only needs emacs-magit-popup
- Update dependency for Geiser 0.13 package split

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
