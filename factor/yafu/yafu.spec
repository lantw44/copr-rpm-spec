Name:       yafu
Version:    1.34
Release:    18%{?dist}
Summary:    Automated integer factorization

License:    Public Domain
URL:        https://sourceforge.net/projects/yafu
Source0:    https://downloads.sourceforge.net/project/yafu/%{version}/%{name}-%{version}-src.zip

BuildRequires: gcc
BuildRequires: msieve, gmp-ecm-devel

%description
YAFU (with assistance from other free software) uses the most powerful modern
algorithms (and implementations of them) to factor input integers in a
completely automated way. The automation within YAFU is state-of-the-art,
combining factorization algorithms in an intelligent and adaptive methodology
that minimizes the time to find the factors of arbitrary input integers.
Most algorithm implementations are multi-threaded, allowing YAFU to fully
utilize multi- or many-core processors (including SNFS, GNFS, SIQS, and ECM).


%prep
%autosetup -n %{name}-%{version}.3 -p1


%build
sed -i 's|-lmsieve|-lmsieve -lz|' Makefile

%ifarch x86_64
%make_build x86_64 NFS=1 USE_SSE41=1 \
    CC="gcc %{build_cflags} %{build_ldflags} -fcommon"
%else
false
%endif


%install
mkdir -p %{buildroot}%{_bindir}
install -m 755 yafu %{buildroot}%{_bindir}


%files
%{_bindir}/yafu
%doc CHANGES docfile.txt README yafu.ini



%changelog
* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 1.34-18
- Rebuilt for Fedora 34 and 35

* Fri Oct 30 2020 Ting-Wei Lan <lantw44@gmail.com> - 1.34-17
- Rebuilt for Fedora 33 and 34

* Thu Apr 23 2020 Ting-Wei Lan <lantw44@gmail.com> - 1.34-16
- Fix GCC 10 linking failure with -fcommon
- Use build_* flags instead of the old optflags and __global_ldflags

* Tue Sep 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 1.34-15
- Rebuilt for Fedora 31 and 32

* Tue Apr 30 2019 Ting-Wei Lan <lantw44@gmail.com> - 1.34-14
- Rebuilt for Fedora 30 and 31

* Mon Oct 22 2018 Ting-Wei Lan <lantw44@gmail.com> - 1.34-13
- Add GCC to BuildRequires for Fedora 29 and later

* Mon Feb 26 2018 Ting-Wei Lan <lantw44@gmail.com> - 1.34-12
- Remove group tag because it is deprecated in Fedora

* Mon Dec 11 2017 Ting-Wei Lan <lantw44@gmail.com> - 1.34-11
- Use autosetup and make_build macros

* Mon Oct 16 2017 Ting-Wei Lan <lantw44@gmail.com> - 1.34-10
- Rebuilt for Fedora 27 and 28

* Wed Mar 08 2017 Ting-Wei Lan <lantw44@gmail.com> - 1.34-9
- Rebuilt for Fedora 26 and 27

* Mon Jan 23 2017 Ting-Wei Lan <lantw44@gmail.com> - 1.34-8
- Rebuilt for msieve 1.53 update

* Sat Sep 10 2016 Ting-Wei Lan <lantw44@gmail.com> - 1.34-7
- Rebuilt for Fedora 25 and 26

* Tue Jun 21 2016 Ting-Wei Lan <lantw44@gmail.com> - 1.34-6
- Rebuilt for gmp-ecm-libs soname bump

* Thu Mar 03 2016 Ting-Wei Lan <lantw44@gmail.com> - 1.34-5
- Rebuilt for Fedora 24 and 25

* Fri Nov 20 2015 Ting-Wei Lan <lantw44@gmail.com> - 1.34-4
- Rebuilt for hardening flags

* Tue Jul 28 2015 Ting-Wei Lan <lantw44@gmail.com> - 1.34-3
- Rebuilt for Fedora 23 and 24

* Fri Mar 20 2015 Ting-Wei Lan <lantw44@gmail.com> - 1.34-2
- Rebuilt for Fedora 22 and 23
- Use HTTPS to download the source

* Thu Dec 25 2014 Ting-Wei Lan <lantw44@gmail.com> - 1.34-1
- Initial packaging
