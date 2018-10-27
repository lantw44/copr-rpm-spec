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
Version:    0.9.27
Release:    1%{?dist}
Summary:    Tiny C Compiler

License:    LGPLv2
URL:        https://bellard.org/tcc
Source0:    https://download.savannah.gnu.org/releases/tinycc/%{pkg_name}-%{version}.tar.bz2

BuildRequires: %{use_cc}, glibc-devel, texinfo, perl-podlators

%description
Tiny C Compiler is a small C compiler, which can already compile itself.
It can also run C source code as a script.

%prep
%autosetup -n %{pkg_name}-%{version} -p1

%build
# We cannot use configure macro here because it will pass unsupported compiler
# flags to tcc. These flags are passed to gcc with make command line instead.
./configure --prefix=%{_prefix} --libdir=%{_libdir} \
            --cc=%{use_cc} --enable-cross
%make_build \
%ifarch x86_64 amd64
%if %{use_gcc}
    CC="gcc %{optflags} %{__global_ldflags}"
%endif
%endif

%install
%make_install
rm %{buildroot}%{_datadir}/doc/tcc-doc.html

%post
/sbin/install-info %{_infodir}/tcc-doc.info.gz %{_infodir}/dir || :

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/tcc-doc.info.gz %{_infodir}/dir || :
fi

%files
%{_bindir}/tcc
%{_bindir}/arm-tcc
%{_bindir}/arm-wince-tcc
%{_bindir}/arm64-tcc
%{_bindir}/c67-tcc
%{_bindir}/i386-tcc
%{_bindir}/i386-win32-tcc
%{_bindir}/x86_64-tcc
%{_bindir}/x86_64-osx-tcc
%{_bindir}/x86_64-win32-tcc
%{_includedir}/libtcc.h
%{_libdir}/libtcc.a
%dir %{_libdir}/tcc
%{_libdir}/tcc/libtcc1.a
%{_libdir}/tcc/arm-libtcc1.a
%{_libdir}/tcc/arm64-libtcc1.a
%{_libdir}/tcc/i386-libtcc1.a
%{_libdir}/tcc/x86_64-libtcc1.a
%{_libdir}/tcc/x86_64-osx-libtcc1.a
%dir %{_libdir}/tcc/include
%{_libdir}/tcc/include/*.h
%dir %{_libdir}/tcc/win32
%dir %{_libdir}/tcc/win32/include
%dir %{_libdir}/tcc/win32/include/sec_api
%dir %{_libdir}/tcc/win32/include/sec_api/sys
%dir %{_libdir}/tcc/win32/include/sys
%dir %{_libdir}/tcc/win32/include/tcc
%dir %{_libdir}/tcc/win32/include/winapi
%{_libdir}/tcc/win32/include/*.h
%{_libdir}/tcc/win32/include/sec_api/*.h
%{_libdir}/tcc/win32/include/sec_api/sys/*.h
%{_libdir}/tcc/win32/include/sys/*.h
%{_libdir}/tcc/win32/include/tcc/*.h
%{_libdir}/tcc/win32/include/winapi/*.h
%dir %{_libdir}/tcc/win32/lib
%{_libdir}/tcc/win32/lib/arm-wince-libtcc1.a
%{_libdir}/tcc/win32/lib/i386-win32-libtcc1.a
%{_libdir}/tcc/win32/lib/x86_64-win32-libtcc1.a
%{_libdir}/tcc/win32/lib/*.def
%{_mandir}/man1/tcc.1.gz
%{_infodir}/tcc-doc.info.gz
%license COPYING
%doc Changelog README TODO VERSION tcc-doc.html

%changelog
* Sat Oct 27 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.9.27-1
- Update to 0.9.27

* Mon Oct 22 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.9.26-16
- Rebuilt for Fedora 29 and 30

* Mon Feb 26 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.9.26-15
- Remove group tag because it is deprecated in Fedora

* Mon Dec 11 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.9.26-14
- Use autosetup, make_build, make_install macros
- Use HTTPS to download the source

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
