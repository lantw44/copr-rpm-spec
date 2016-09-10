Name:       qelly
Version:    1.0
Release:    0.7.beta%{?dist}
Summary:    Qelly is a Qt port of Nally

%global     real_name     Qelly
%global     real_version  1.0b

Group:      Applications/Internet
License:    GPLv3
URL:        https://github.com/uranusjr/Qelly
Source0:    https://github.com/uranusjr/Qelly/archive/v%{real_version}.tar.gz

BuildRequires: qt-devel, libqxt-devel, chrpath

%description
Qelly (pronounced as the English name "Kelly") is a Qt port of Nally, the
open-source Telnet/SSH client for Mac OS X. Qt is chosen to be the underlying
framework of this application bacause it enables us to build a GUI-based
application with a native-looking interface for every operating system with
minimal effort. The project is currently only a Qt version of Nally (hence the
name), but more features from other Telnet/SSH clients are also planned.

%prep
%setup -q -n %{real_name}-%{real_version}

%build
%{_qt4_qmake}
make %{?_smp_mflags}


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
