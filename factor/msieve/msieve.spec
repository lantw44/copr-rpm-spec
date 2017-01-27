Name:       msieve
Version:    1.53
Release:    1%{?dist}
Summary:    Msieve is a C library to factor large integers.

Group:      Applications/Engineering
License:    Public Domain
URL:        https://sourceforge.net/projects/msieve
Source0:    https://downloads.sourceforge.net/project/msieve/msieve/Msieve v1.53/msieve153_src.tar.gz

BuildRequires: gmp-ecm-devel, zlib-devel
Requires:   zlib-devel

%description
Msieve is a C library implementing a suite of algorithms to factor large
integers. It contains an implementation of the SIQS and GNFS algorithms; the
latter has helped complete some of the largest public factorizations known.

%prep
%setup -qn %{name}-%{version}


%build
sed -i 's|-march=native||' Makefile
make %{?_smp_mflags} all ECM=1 CC="gcc %{optflags} %{__global_ldflags}"


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
