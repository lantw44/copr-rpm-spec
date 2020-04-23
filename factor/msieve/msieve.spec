Name:       msieve
Version:    1.53
Release:    9%{?dist}
Summary:    Msieve is a C library to factor large integers.

License:    Public Domain
URL:        https://sourceforge.net/projects/msieve
Source0:    https://downloads.sourceforge.net/project/msieve/msieve/Msieve v1.53/msieve153_src.tar.gz

BuildRequires: gcc
BuildRequires: gmp-ecm-devel, zlib-devel
Requires:   zlib-devel

%description
Msieve is a C library implementing a suite of algorithms to factor large
integers. It contains an implementation of the SIQS and GNFS algorithms; the
latter has helped complete some of the largest public factorizations known.

%prep
%autosetup -n %{name}-%{version} -p1


%build
sed -i 's|-march=native||' Makefile
%make_build all ECM=1 CC="gcc %{build_cflags} %{build_ldflags} -fcommon"


%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
install -m 755 msieve %{buildroot}%{_bindir}
install -m 644 libmsieve.a %{buildroot}%{_libdir}


%files
%{_bindir}/msieve
%{_libdir}/libmsieve.a
%doc Changes Readme Readme.nfs Readme.qs



%changelog
* Thu Apr 23 2020 Ting-Wei Lan <lantw44@gmail.com> - 1.53-9
- Fix GCC 10 linking failure with -fcommon
- Use build_* flags instead of the old optflags and __global_ldflags

* Tue Sep 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 1.53-8
- Rebuilt for Fedora 31 and 32

* Tue Apr 30 2019 Ting-Wei Lan <lantw44@gmail.com> - 1.53-7
- Rebuilt for Fedora 30 and 31

* Mon Oct 22 2018 Ting-Wei Lan <lantw44@gmail.com> - 1.53-6
- Add GCC to BuildRequires for Fedora 29 and later

* Mon Feb 26 2018 Ting-Wei Lan <lantw44@gmail.com> - 1.53-5
- Remove group tag because it is deprecated in Fedora

* Mon Dec 11 2017 Ting-Wei Lan <lantw44@gmail.com> - 1.53-4
- Use autosetup and make_build macros

* Mon Oct 16 2017 Ting-Wei Lan <lantw44@gmail.com> - 1.53-3
- Rebuilt for Fedora 27 and 28

* Wed Mar 08 2017 Ting-Wei Lan <lantw44@gmail.com> - 1.53-2
- Rebuilt for Fedora 26 and 27

* Mon Jan 23 2017 Ting-Wei Lan <lantw44@gmail.com> - 1.53-1
- Update to 1.53
- Remove -march=native set in OPT_FLAGS

* Sat Sep 10 2016 Ting-Wei Lan <lantw44@gmail.com> - 1.52-7
- Rebuilt for Fedora 25 and 26

* Tue Jun 21 2016 Ting-Wei Lan <lantw44@gmail.com> - 1.52-6
- Rebuilt for gmp-ecm-libs soname bump

* Thu Mar 03 2016 Ting-Wei Lan <lantw44@gmail.com> - 1.52-5
- Rebuilt for Fedora 24 and 25

* Fri Nov 20 2015 Ting-Wei Lan <lantw44@gmail.com> - 1.52-4
- Rebuilt for hardening flags

* Tue Jul 28 2015 Ting-Wei Lan <lantw44@gmail.com> - 1.52-3
- Rebuilt for Fedora 23 and 24

* Fri Mar 20 2015 Ting-Wei Lan <lantw44@gmail.com> - 1.52-2
- Rebuilt for Fedora 22 and 23
- Use HTTPS to download the source

* Thu Dec 25 2014 Ting-Wei Lan <lantw44@gmail.com> - 1.52-1
- Initial packaging
