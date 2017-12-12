%global use_gcc       1
%global pkg_name      tcc

%if %{use_gcc}
%global use_cc        gcc
%global pkg_fullname  %{pkg_name}
%else
%global use_cc        tcc
%global pkg_fullname  %{pkg_name}-self
%global debug_package %{nil}
%endif

Name:       %{pkg_fullname}
Version:    0.9.26
Release:    14%{?dist}
Summary:    Tiny C Compiler

Group:      Development/Languages
License:    LGPLv2
URL:        http://bellard.org/tcc
Source0:    http://download.savannah.gnu.org/releases/tinycc/%{pkg_name}-%{version}.tar.bz2

BuildRequires: %{use_cc}, glibc-devel, texinfo, perl-podlators

%description
Tiny C Compiler is a small C compiler, which can already compile itself.
It can also run C source code as a script.

%prep
%autosetup -n %{pkg_name}-%{version} -p1

%build
./configure --prefix=%{_prefix} --libdir=%{_libdir} \
            --cc=%{use_cc} --enable-cross
make %{?_smp_mflags} \
%ifarch x86_64 amd64
%if %{use_gcc}
    CC="gcc %{optflags} %{__global_ldflags}"
%endif
%endif

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_datadir}/doc/tcc/tcc-doc.html

%post
/sbin/install-info %{_infodir}/tcc-doc.info.gz %{_infodir}/dir || :

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/tcc-doc.info.gz %{_infodir}/dir || :
fi

%files
%{_bindir}/arm-eabi-tcc
%{_bindir}/arm-fpa-ld-tcc
%{_bindir}/arm-fpa-tcc
%{_bindir}/arm-vfp-tcc
%{_bindir}/c67-tcc
%ifnarch i386 i486 i586 i686
%{_bindir}/i386-tcc
%endif
%{_bindir}/i386-win32-tcc
%{_bindir}/tcc
%ifnarch x86_64 amd64
%{_bindir}/x86_64-tcc
%endif
%{_bindir}/x86_64-win32-tcc
%{_includedir}/libtcc.h
%attr(644, -, -) %{_libdir}/libtcc.a
%dir %{_libdir}/tcc
%dir %{_libdir}/tcc/include
%{_libdir}/tcc/include/*.h
%attr(644, -, -) %{_libdir}/tcc/libtcc1.a
%ifnarch i386 i486 i586 i686
%dir %{_libdir}/tcc/i386
%dir %{_libdir}/tcc/i386/include
%{_libdir}/tcc/i386/include/*.h
%attr(644, -, -) %{_libdir}/tcc/i386/libtcc1.a
%endif
%dir %{_libdir}/tcc/win32
%dir %{_libdir}/tcc/win32/include
%dir %{_libdir}/tcc/win32/include/sec_api
%dir %{_libdir}/tcc/win32/include/sys
%dir %{_libdir}/tcc/win32/include/sec_api/sys
%dir %{_libdir}/tcc/win32/include/winapi
%{_libdir}/tcc/win32/include/*.h
%{_libdir}/tcc/win32/include/sec_api/*.h
%{_libdir}/tcc/win32/include/sec_api/sys/*.h
%{_libdir}/tcc/win32/include/sys/*.h
%{_libdir}/tcc/win32/include/winapi/*.h
%dir %{_libdir}/tcc/win32/lib
%dir %{_libdir}/tcc/win32/lib/32
%dir %{_libdir}/tcc/win32/lib/64
%attr(644, -, -) %{_libdir}/tcc/win32/lib/32/libtcc1.a
%attr(644, -, -) %{_libdir}/tcc/win32/lib/64/libtcc1.a
%{_libdir}/tcc/win32/lib/*.def
%attr(644, -, -) %{_mandir}/man1/tcc.1.gz
%attr(644, -, -) %{_infodir}/tcc-doc.info.gz
%license COPYING
%doc Changelog README TODO VERSION tcc-doc.html

%changelog
* Mon Dec 11 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.9.26-14
- Use autosetup macro

* Mon Oct 16 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.9.26-13
- Rebuilt for Fedora 27 and 28

* Wed Mar 08 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.9.26-12
- Rebuilt for Fedora 26 and 27

* Sat Sep 10 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.9.26-11
- Rebuilt for Fedora 25 and 26

* Thu Mar 03 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.9.26-10
- Rebuilt for Fedora 24 and 25

* Tue Nov 24 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.9.26-9
- Own directories under /usr/lib{,64}/tcc

* Sat Nov 21 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.9.26-8
- Fix the license tag
- Enable hardening flags on x86_64
- Don't set executable permissions on static libraries, man pages,
  info pages

* Tue Jul 28 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.9.26-7
- Rebuilt for Fedora 23 and 24

* Sun May 17 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.9.26-6
- Use license marco to install the license file

* Fri Mar 20 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.9.26-5
- Rebuilt for Fedora 22 and 23

* Mon Nov 04 2013 Ting-Wei Lan <lantw44@gmail.com> - 0.9.26-4
- Initial packaging
