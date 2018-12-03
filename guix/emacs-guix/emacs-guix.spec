%global pkg guix
%global pkgname Guix

Name:           emacs-%{pkg}
Version:        0.5
Release:        1%{?dist}
Summary:        Emacs-Guix is an Emacs interface for GNU Guix package manager

License:        GPLv3+
URL:            https://emacs-guix.gitlab.io/website
Source0:        https://emacs-guix.gitlab.io/website/releases/%{name}-%{version}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/2.0
%global guile_ccache_dir %{_libdir}/guile/2.0/site-ccache

BuildArch:      noarch
BuildRequires:  emacs, texinfo
BuildRequires:  guix >= 0.13.0
BuildRequires:  pkgconfig(guile-2.0), guile-gcrypt
BuildRequires:  emacs-geiser, emacs-dash, emacs-bui, emacs-magit

Requires:       emacs(bin) >= %{_emacs_version}
Requires:       emacs-geiser, emacs-dash, emacs-bui, emacs-magit
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
%configure \
    --with-lispdir=%{_emacs_sitelispdir}/%{pkg} \
    --with-guile-site-dir=%{guile_source_dir} \ \
    --with-guile-site-ccache-dir=%{guile_ccache_dir} \
    GUILE=%{_bindir}/guile \
    GUILD=%{_bindir}/guild
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
