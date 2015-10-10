%global pkg geiser
%global pkgname Geiser

Name:           emacs-%{pkg}
Version:        0.7
Release:        3%{?dist}
Summary:        Geiser is an Emacs environment to hack and have fun in Scheme

License:        BSD
URL:            http://nongnu.org/geiser
Source0:        http://download.sv.gnu.org/releases/geiser/%{version}/%{pkg}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  emacs
Requires:       emacs(bin) >= %{_emacs_version}
Requires(post): info
Requires(preun): info

Obsoletes:      emacs-%{pkg}-el <= 0.7-2
Provides:       emacs-%{pkg}-el <= 0.7-2

%description
%{pkgname} is an add-on package for GNU Emacs. It is a collection of Emacs
major and minor modes that conspire with one or more Scheme interpreters to
keep the Lisp Machine Spirit alive.


%prep
%setup -q -n %{pkg}-%{version}


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%post
/sbin/install-info %{_infodir}/geiser.info.gz %{_infodir}/dir || :


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/geiser.info.gz %{_infodir}/dir || :
fi


%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README THANKS
%{_bindir}/geiser-racket
%{_infodir}/geiser.info.gz
%{_datadir}/geiser/
%{_emacs_sitelispdir}/geiser.el
%{_emacs_sitelispdir}/geiser.elc
%{_emacs_sitelispdir}/geiser-*.el
%{_emacs_sitelispdir}/geiser-*.elc
%exclude %{_infodir}/dir



%changelog
* Sat Oct 10 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.7-3
- Add the missing emacs(bin) Requires
- Use info instead of /sbin/install-info in Requires
- Merge elisp source sub-packages back into the main package

* Sun May 17 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.7-2
- Use license marco to install the license file

* Fri Mar 20 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.7-1
- Rebuilt for Fedora 22 and 23
- Update to 0.7

* Sat Nov 22 2014 Ting-Wei Lan <lantw44@gmail.com> - 0.6-1
- Initial packaging
