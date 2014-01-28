Name:           ht
Version:        2.0.22
Release:        1%{?dist}
Summary:        File editor/viewer/analyzer for executables (Copr: lantw44/patches)

Group:          Applications/Editors
License:        GPLv2
URL:            http://hte.sourceforge.net/
Source0:        http://downloads.sourceforge.net/hte/ht-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libX11-devel ncurses-devel lzo-devel
BuildRequires:  recode

%description
Copr: lantw44/patches
Note: This is a modified package. It contains updated ht with name hteditor,
which prevents file name conflict with TeXLive.

HT is a file editor/viewer/analyzer for executables. The goal is to combine
the low-level functionality of a debugger and the usability of IDEs. We plan
to implement all (hex-)editing features and support of the most important
file formats.

%prep
%setup -q
recode latin1..utf8 TODO
find . -name \*.cc -o -name \*.h | xargs chmod 0644

%build
%configure --enable-maintainermode
CXXFLAGS="%{optflags}" make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mv ${RPM_BUILD_ROOT}/usr/bin/ht ${RPM_BUILD_ROOT}/usr/bin/hteditor

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING AUTHORS NEWS README TODO KNOWNBUGS
%{_bindir}/hteditor

%changelog
* Wed Jan 08 2014 Ting-Wei Lan <lantw44@gmail.com>
- Update to version 2.0.22
- Fix conflict with TeXLive

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Feb 19 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 2.0.18-1
- version upgrade

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr  5 2009 Dan Horák <dan[AT]danny.cz>
- 2.0.16-1
- version update
- added patch for building with gcc 4.4
- remove executable permissions on source files

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Nov 11 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 2.0.15-1
- version upgrade

* Tue Nov 11 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 2.0.14-2
- recode TODO to utf8
- fix permissions on endianess.cc
- honor optflags via non standard maintainer mode

* Wed Sep 03 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 2.0.14-1
- version upgrade
- BR lzo-devel
- use opt flags

* Mon Jan 07 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 2.0.10-1
- version upgrade
- fix source location
- fix license

* Mon Jun 25 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 2.0.8-1
- initial version
