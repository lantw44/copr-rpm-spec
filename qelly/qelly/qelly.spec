%global commit 354e0b7b37655c327a6f7ddd283d3069b4cf1b8d
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:       qelly
Version:    1.0
Release:    0.24.20160403git%{shortcommit}%{?dist}
Summary:    Qelly is a Qt port of Nally

License:    GPLv3
URL:        https://github.com/uranusjr/Qelly
Source0:    https://github.com/uranusjr/Qelly/archive/%{commit}/Qelly-%{commit}.tar.gz
Patch0:     qelly-qt-5.15.patch

BuildRequires: gcc-c++
BuildRequires: qt5-qtbase-devel, qt5-linguist, libqxt-qt5-devel, chrpath

%description
Qelly (pronounced as the English name "Kelly") is a Qt port of Nally, the
open-source Telnet/SSH client for Mac OS X. Qt is chosen to be the underlying
framework of this application bacause it enables us to build a GUI-based
application with a native-looking interface for every operating system with
minimal effort. The project is currently only a Qt version of Nally (hence the
name), but more features from other Telnet/SSH clients are also planned.

%prep
%autosetup -n Qelly-%{commit} -p1

%build
%{qmake_qt5}
%make_build qmake_all
sed -i 's| -lQxt\([^ ]*\)| -lQxt\1-qt5|g' src/Makefile
%make_build


%install
mkdir -p %{buildroot}/usr/bin
chrpath -d bin/Qelly
install -m 755 bin/Qelly %{buildroot}/usr/bin

%files
%{_bindir}/Qelly
%license LICENSE
%doc AUTHORS CHANGES README.md

%changelog
* Wed Oct 02 2024 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.24.20160403git354e0b7
- Rebuilt for Fedora 40, 41, 42

* Sat Oct 14 2023 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.23.20160403git354e0b7
- Rebuilt for Fedora 39 and 40

* Tue Apr 18 2023 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.22.20160403git354e0b7
- Rebuilt for Fedora 38 and 39

* Sat Oct 29 2022 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.21.20160403git354e0b7
- Rebuilt for Fedora 37 and 38

* Thu Apr 28 2022 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.20.20160403git354e0b7
- Rebuilt for Fedora 36 and 37

* Mon Aug 23 2021 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.19.20160403git354e0b7
- Rebuilt for Fedora 35 and 36

* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.18.20160403git354e0b7
- Rebuilt for Fedora 34 and 35

* Fri Oct 30 2020 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.17.20160403git354e0b7
- Update to the latest git snapshot
- Remove unnecessary quotes in install script
- Fix build with Qt 5.15

* Thu Apr 23 2020 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.16.beta
- Fix BuildRequires for Fedora 33

* Thu Apr 23 2020 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.15.beta
- Rebuilt for Fedora 32 and 33

* Tue Sep 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.14.beta
- Rebuilt for Fedora 31 and 32

* Tue Apr 30 2019 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.13.beta
- Rebuilt for Fedora 30 and 31
- Remove defattr
- Switch to Qt 5

* Mon Oct 22 2018 Ting-Wei Lan <lantw44@gmail.com> - 1.0-0.12.beta
- Add GCC to BuildRequires for Fedora 29 and later

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
