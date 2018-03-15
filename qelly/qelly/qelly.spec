Name:       qelly
Version:    1.0
Release:    0.11.beta%{?dist}
Summary:    Qelly is a Qt port of Nally

%global     real_name     Qelly
%global     real_version  1.0b

License:    GPLv3
URL:        https://github.com/uranusjr/Qelly
Source0:    https://github.com/uranusjr/Qelly/archive/v%{real_version}.tar.gz#/%{name}-%{real_version}.tar.gz

BuildRequires: qt-devel, libqxt-devel, chrpath

%description
Qelly (pronounced as the English name "Kelly") is a Qt port of Nally, the
open-source Telnet/SSH client for Mac OS X. Qt is chosen to be the underlying
framework of this application bacause it enables us to build a GUI-based
application with a native-looking interface for every operating system with
minimal effort. The project is currently only a Qt version of Nally (hence the
name), but more features from other Telnet/SSH clients are also planned.

%prep
%autosetup -n %{real_name}-%{real_version} -p1

%build
%{qmake_qt4}
%make_build


%install
mkdir -p %{buildroot}/usr/bin
chrpath -d "bin/Qelly"
install -m 755 "bin/Qelly" "%{buildroot}/usr/bin"

%files
%defattr(-,root,root,-)
%{_bindir}/Qelly
%license LICENSE
%doc AUTHORS CHANGES README.md

%changelog
* Mon Feb 26 2018 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.11.beta
- Remove group tag because it is deprecated in Fedora

* Mon Dec 11 2017 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.10.beta
- Use autosetup and make_build macros
- Rename the source tarball

* Mon Oct 16 2017 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.9.beta
- Use qmake_qt4 macro instead of _qt4_qmake macro
- Fix build failure on Fedora 27 and 28

* Wed Mar 08 2017 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.8.beta
- Rebuilt for Fedora 26 and 27

* Sat Sep 10 2016 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.7.beta
- Rebuilt for Fedora 25 and 26

* Thu Mar 03 2016 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.6.beta
- Rebuilt for Fedora 24 and 25

* Mon Nov 23 2015 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.5.beta
- Disable RPATH
- Use qmake macro
- Remove non-needed Requires

* Tue Jul 28 2015 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.4.beta
- Rebuilt for Fedora 23 and 24

* Sun May 17 2015 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.3.beta
- Use license marco to install the license file

* Fri Mar 20 2015 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.2.beta
- Rebuilt for Fedora 22 and 23

* Tue Dec 17 2013 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.1.beta
- Update to 1.0b (https://github.com/uranusjr/Qelly/releases/tag/v1.0b)

* Mon Oct 21 2013 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.1.alpha3
- Update to 1.0a3 (https://github.com/uranusjr/Qelly/releases/tag/v1.0a3)

* Thu Oct 17 2013 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.1.alpha2
- Initial packaging
