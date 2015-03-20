Name:       msieve
Version:    1.52
Release:    2%{?dist}
Summary:    Msieve is a C library to factor large integers.

Group:      Applications/Engineering
License:    Public Domain
URL:        https://sourceforge.net/projects/msieve
Source0:    https://downloads.sourceforge.net/project/msieve/msieve/Msieve v1.52/msieve152.tar.gz

BuildRequires: gmp-ecm-devel, zlib-devel
Requires:   zlib-devel

%description
Msieve is a C library implementing a suite of algorithms to factor large
integers. It contains an implementation of the SIQS and GNFS algorithms; the
latter has helped complete some of the largest public factorizations known.

%prep
%setup -qn %{name}-%{version}


%build
make %{?_smp_mflags} all ECM=1


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
* Fri Mar 20 2015 Ting-Wei Lan <lantw44@gmail.com> - 1.52-2
- Rebuilt for Fedora 22 and 23
- Use HTTPS to download the source

* Thu Dec 25 2014 Ting-Wei Lan <lantw44@gmail.com> - 1.52-1
- Initial packaging
