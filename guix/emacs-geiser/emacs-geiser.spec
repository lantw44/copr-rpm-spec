%global pkg geiser
%global pkgname Geiser

Name:           emacs-%{pkg}
Version:        0.31.1
Release:        1%{?dist}
Summary:        Geiser is a generic Emacs/Scheme interaction mode

License:        BSD
URL:            https://nongnu.org/geiser
Source0:        https://gitlab.com/emacs-geiser/geiser/-/archive/%{version}/%{pkg}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  texinfo
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
%autosetup -n %{pkg}-%{version} -p1


%build
makeinfo --no-split doc/geiser.texi


%install
install -m 755 -d %{buildroot}%{_emacs_sitelispdir}/geiser
install -m 644 elisp/*.el %{buildroot}%{_emacs_sitelispdir}/geiser/
%{_emacs_bytecompile} %{buildroot}%{_emacs_sitelispdir}/geiser/*.el
install -m 755 -d %{buildroot}%{_emacs_sitelispdir}/geiser/src
install -m 755 -d %{buildroot}%{_infodir}
gzip -9 < geiser.info > %{buildroot}%{_infodir}/geiser.info.gz


%post
/sbin/install-info %{_infodir}/geiser.info.gz %{_infodir}/dir || :


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/geiser.info.gz %{_infodir}/dir || :
fi


%files
%license license
%doc news.org readme.org
%{_emacs_sitelispdir}/geiser/geiser.el
%{_emacs_sitelispdir}/geiser/geiser.elc
%{_emacs_sitelispdir}/geiser/geiser-*.el
%{_emacs_sitelispdir}/geiser/geiser-*.elc
%dir %{_emacs_sitelispdir}/geiser/src
%{_infodir}/geiser.info.gz


%changelog
* Sat Nov 02 2024 Ting-Wei Lan <lantw44@gmail.com> - 0.31.1-1
- Update to 0.31.1
- Use the builtin transient package

* Wed Apr 19 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.28.2-2
- Rebuilt for Fedora 38 and 39

* Sun Feb 12 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.28.2-1
- Update to 0.28.2

* Sat Oct 29 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.23.2-2
- Rebuilt for Fedora 37 and 38

* Thu Apr 28 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.23.2-1
- Update to 0.23.2

* Sat Sep 25 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.17-1
- Update to 0.17

* Mon Jun 14 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.16-1
- Update to 0.16
- Move support for Scheme implementations to separate packages

* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.12-2
- Rebuilt for Fedora 34 and 35

* Mon Feb 15 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.12-1
- Update to 0.12

* Sun Nov  1 2020 Ting-Wei Lan <lantw44@gmail.com> - 0.11.2-2
- Rebuilt for Fedora 33 and 34

* Sun Apr 26 2020 Ting-Wei Lan <lantw44@gmail.com> - 0.11.2-1
- Update to 0.11.2

* Tue Sep 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.10-2
- Rebuilt for Fedora 31 and 32

* Thu May 16 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.10-1
- Update to 0.10

* Wed May 01 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.9-8
- Rebuilt for Fedora 30 and 31
- Use HTTPS in URL

* Tue Oct 23 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.9-7
- Rebuilt for Fedora 29 and 30

* Mon Feb 26 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.9-6
- Remove group tag because it is deprecated in Fedora

* Mon Dec 11 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.9-5
- Use autosetup, make_build, make_install macros

* Sat Dec 09 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.9-4
- Use HTTPS to download the source

* Mon Oct 16 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.9-3
- Rebuilt for Fedora 27 and 28

* Wed Mar 08 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.9-2
- Rebuilt for Fedora 26 and 27

* Fri Nov 04 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.9-1
- Update to 0.9

* Sat Sep 10 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.8.1-4
- Rebuilt for Fedora 25 and 26

* Fri Apr 01 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.8.1-3
- Add geiser to the load path of guile

* Thu Mar 03 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.8.1-2
- Rebuilt for Fedora 24 and 25

* Thu Nov 05 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.8.1-1
- Update to 0.8.1
- Don't clutter the system site-lisp directory

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
