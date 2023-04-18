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

%global date 20230415
%global gitrev 6a24b762d3e1086dcffd002c68cb5ca3a33a5c6d
%global shortgitrev %(c=%{gitrev}; echo "${c:0:7}")

Name:       %{pkg_fullname}
Version:    0.9.28
Release:    0.5.%{date}git%{shortgitrev}%{?dist}
Summary:    Tiny C Compiler

License:    LGPLv2
URL:        https://bellard.org/tcc
Source0:    https://repo.or.cz/tinycc.git/snapshot/%{gitrev}.tar.gz#/%{pkg_name}-%{gitrev}.tar.gz

BuildRequires: %{use_cc}, glibc-devel, make, texinfo, perl-podlators

%description
Tiny C Compiler is a small C compiler, which can already compile itself.
It can also run C source code as a script.


%prep
%autosetup -n tinycc-%{shortgitrev} -p1


%build
# We cannot use configure macro here because it will pass unsupported compiler
# flags to TCC. These flags are passed to GCC with configure options instead.
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --with-selinux \
    --enable-cross \
    --cc=%{use_cc} \
%if %{use_gcc}
    --debug \
    --extra-cflags='%{optflags}' \
    --extra-ldflags='%{__global_ldflags}' \
%else
    --extra-cflags= \
    --extra-ldflags= \
%endif

%make_build


%check
# TCC linker segfault on GCC LTO objects.
sed -i 's|-flto=[^ ]*||g' config.mak
# Running tests in parallel can cause them to fail.
%ifnarch i686
%{__make} test
%endif


%install
%make_install
# Handle the file with doc macro.
rm %{buildroot}%{_datadir}/doc/tcc-doc.html
# Drop unnecessary executable bits to avoid missing build ID errors.
chmod -x \
    %{buildroot}%{_libdir}/libtcc.a \
    %{buildroot}%{_libdir}/tcc/*.a \
    %{buildroot}%{_libdir}/tcc/*.o \
    %{buildroot}%{_libdir}/tcc/win32/lib/*.a


%post
/sbin/install-info %{_infodir}/tcc-doc.info.gz %{_infodir}/dir || :


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/tcc-doc.info.gz %{_infodir}/dir || :
fi


%files
%license COPYING
%doc Changelog README TODO USES VERSION tcc-doc.html
%{_bindir}/tcc
%{_bindir}/arm-tcc
%{_bindir}/arm-wince-tcc
%{_bindir}/arm64-tcc
%{_bindir}/arm64-osx-tcc
%{_bindir}/c67-tcc
%{_bindir}/i386-tcc
%{_bindir}/i386-win32-tcc
%{_bindir}/riscv64-tcc
%{_bindir}/x86_64-tcc
%{_bindir}/x86_64-osx-tcc
%{_bindir}/x86_64-win32-tcc
%{_includedir}/libtcc.h
%{_libdir}/libtcc.a
%dir %{_libdir}/tcc
%{_libdir}/tcc/libtcc1.a
%{_libdir}/tcc/arm-libtcc1.a
%{_libdir}/tcc/arm64-libtcc1.a
%{_libdir}/tcc/arm64-osx-libtcc1.a
%{_libdir}/tcc/bcheck.o
%{_libdir}/tcc/bt-exe.o
%{_libdir}/tcc/bt-log.o
%{_libdir}/tcc/i386-libtcc1.a
%{_libdir}/tcc/riscv64-libtcc1.a
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


%changelog
* Tue Apr 18 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.9.28-0.5.20230415git6a24b76
- Update to the latest git snapshot

* Sat Oct 29 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.9.28-0.4.20221023gitdf6fd04
- Update to the latest git snapshot

* Thu Apr 28 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.9.28-0.3.20220428gitfa9c31c
- Update to the latest git snapshot
- Fix build on Fedora 36

* Mon Aug 23 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.9.28-0.2.20210821gitc7a57bf
- Update to the latest git snapshot
- Drop unnecessary executable bits to fix build on CentOS 8

* Sat Aug 14 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.9.28-0.1.20210803git675046b
- Update to a git snapshot from mob branch to fix tcc linker crash on
  Fedora 29, CentOS 8 and their later versions
- Use distribution build flags on all architectures
- Run tests on x86_64

* Sun Jul 11 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.9.27-7
- Fix tcc -run when SELinux is enforcing

* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.9.27-6
- Rebuilt for Fedora 34 and 35

* Fri Oct 30 2020 Ting-Wei Lan <lantw44@gmail.com> - 0.9.27-5
- Rebuilt for Fedora 33 and 34

* Thu Apr 23 2020 Ting-Wei Lan <lantw44@gmail.com> - 0.9.27-4
- Rebuilt for Fedora 32 and 33

* Tue Sep 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.9.27-3
- Rebuilt for Fedora 31 and 32

* Tue Apr 30 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.9.27-2
- Rebuilt for Fedora 30 and 31

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
