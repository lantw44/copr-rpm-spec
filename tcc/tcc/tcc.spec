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
Release:    5%{?dist}
Summary:    Tiny C Compiler

Group:      Development/Languages
License:    LGPL
URL:        http://bellard.org/tcc
Source0:    http://download.savannah.gnu.org/releases/tinycc/%{pkg_name}-%{version}.tar.bz2

BuildRequires: %{use_cc}, glibc-devel, texinfo, perl-podlators

%description
Tiny C Compiler is a small C compiler, which can already compile itself.
It can also run C source code as a script.

%prep
%setup -q -n %{pkg_name}-%{version}

%build
./configure --prefix=%{_prefix} --libdir=%{_libdir} \
            --cc=%{use_cc} --enable-cross
make %{?_smp_mflags}

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
%{_libdir}/libtcc.a
%{_libdir}/tcc/include/*.h
%{_libdir}/tcc/libtcc1.a
%ifnarch i386 i486 i586 i686
%{_libdir}/tcc/i386/include/*.h
%{_libdir}/tcc/i386/libtcc1.a
%endif
%{_libdir}/tcc/win32/include/*.h
%{_libdir}/tcc/win32/include/sec_api/*.h
%{_libdir}/tcc/win32/include/sec_api/sys/*.h
%{_libdir}/tcc/win32/include/sys/*.h
%{_libdir}/tcc/win32/include/winapi/*.h
%{_libdir}/tcc/win32/lib/32/libtcc1.a
%{_libdir}/tcc/win32/lib/64/libtcc1.a
%{_libdir}/tcc/win32/lib/*.def
%{_mandir}/man1/tcc.1.gz
%{_infodir}/tcc-doc.info.gz
%doc Changelog COPYING README TODO VERSION tcc-doc.html

%changelog
* Fri Mar 20 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.9.26-5
- Rebuilt for Fedora 22 and 23

* Mon Nov 04 2013 Ting-Wei Lan <lantw44@gmail.com> - 0.9.26-4
- Initial packaging
