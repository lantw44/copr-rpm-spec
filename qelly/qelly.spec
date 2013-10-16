Name:       qelly
Version:    1.0
Release:    0.1.alpha2%{?dist}
Summary:    Qelly is a Qt port of Nally

%global     real_name     Qelly
%global     real_version  1.0a2

Group:      Applications/Internet
License:    GPLv3
URL:        https://github.com/uranusjr/Qelly
Source0:    https://github.com/uranusjr/Qelly/archive/v%{real_version}.tar.gz

BuildRequires: qt-devel, libqxt-devel
Requires:   qt, libqxt

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
qmake-qt4
make %{?_smp_mflags}


%install
mkdir -p %{buildroot}/usr/bin
install -m 755 "bin/Qelly" "%{buildroot}/usr/bin"

%files
%defattr(-,root,root,-)
%{_bindir}/Qelly
%doc AUTHORS CHANGES LICENSE README.md

%changelog
* Thu Oct 17 2013 Ting-Wei Lan <lantw44@gmail.com>
- Initial packaging
