%global cross_arch      arm
%global cross_triplet   arm-linux-gnueabi
%global cross_sysroot   %{_prefix}/%{cross_triplet}/sys-root

%if 0%{?_unique_build_ids}
%global _find_debuginfo_opts --build-id-seed "%{name}-%{version}-%{release}"
%endif

%if 0%{!?cross_stage:1}
%global cross_stage     final
%endif

%if "%{cross_stage}" != "final"
%global pkg_suffix      -%{cross_stage}
%else
%global pkg_suffix      %{nil}
%endif

%if "%{cross_arch}" == "arm"
  %global lib_dir_name        lib
%else
  %if "%{cross_arch}" == "arm64"
    %global lib_dir_name      lib64
  %else
    %global lib_dir_name      lib
  %endif
%endif

%bcond_without ada

Name:       %{cross_triplet}-gcc%{pkg_suffix}
Version:    10.3.0
Release:    2%{?dist}
Summary:    The GNU Compiler Collection (%{cross_triplet})

%global major_version   %(echo %{version} | sed 's/\\..*$//')

License:    GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
URL:        https://gcc.gnu.org
Source0:    https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz

# https://gcc.gnu.org/git/gitweb.cgi?p=gcc.git;a=patch;h=2bf34b9f4e446bf9be7f04458058dd5319fb396e
Patch0:     gcc-11-libsanitizer-cyclades.patch

BuildRequires: gcc, gcc-c++, gcc-gnat
BuildRequires: texinfo, gettext, flex, bison, zlib-devel
BuildRequires: gmp-devel, mpfr-devel, libmpc-devel, isl-devel
BuildRequires: elfutils-libelf-devel, libzstd-devel
BuildRequires: %{cross_triplet}-filesystem
BuildRequires: %{cross_triplet}-binutils
Requires:   %{cross_triplet}-filesystem
Requires:   %{cross_triplet}-binutils
Provides:   %{cross_triplet}-gcc-stage1 = %{version}

%if "%{cross_stage}" == "pass2"
BuildRequires: %{cross_triplet}-glibc-stage1
Requires:   %{cross_triplet}-glibc-stage1
Provides:   %{cross_triplet}-gcc-stage2 = %{version}
%endif

%if "%{cross_stage}" == "final"
BuildRequires: %{cross_triplet}-glibc
BuildRequires: gcc-gnat, libstdc++-static
Requires:   %{cross_triplet}-glibc
Provides:   %{cross_triplet}-gcc-stage2 = %{version}
Provides:   %{cross_triplet}-gcc-stage3 = %{version}
%endif

%global shared_library_regexp  [^/]*\\.so[.0-9]*$
%global usr_lib_gcc_dir        %{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}
%global usr_lib_gcc_adalib_dir %{usr_lib_gcc_dir}/adalib

%global __provides_exclude_from ^(%{cross_sysroot}|%{usr_lib_gcc_dir}/%{shared_library_regexp}|%{usr_lib_gcc_adalib_dir}/%{shared_library_regexp})
%global __requires_exclude_from ^(%{cross_sysroot}|%{usr_lib_gcc_dir}/%{shared_library_regexp}|%{usr_lib_gcc_adalib_dir}/%{shared_library_regexp})

%description


%prep
%autosetup -p1 -Tb 0 -n gcc-%{version}


%build
mkdir -p %{_builddir}/gcc-%{version}-build
cd %{_builddir}/gcc-%{version}-build
export AR_FOR_TARGET=%{_bindir}/%{cross_triplet}-ar
export AS_FOR_TARGET=%{_bindir}/%{cross_triplet}-as
export DLLTOOL_FOR_TARGET=%{_bindir}/%{cross_triplet}-dlltool
export LD_FOR_TARGET=%{_bindir}/%{cross_triplet}-ld
export NM_FOR_TARGET=%{_bindir}/%{cross_triplet}-nm
export OBJDUMP_FOR_TARGET=%{_bindir}/%{cross_triplet}-objdump
export RANLIB_FOR_TARGET=%{_bindir}/%{cross_triplet}-ranlib
export STRIP_FOR_TARGET=%{_bindir}/%{cross_triplet}-strip
export WINDRES_FOR_TARGET=%{_bindir}/%{cross_triplet}-windres
export WINDMC_FOR_TARGET=%{_bindir}/%{cross_triplet}-windmc
%global _configure ../gcc-%{version}/configure
%global _program_prefix %{cross_triplet}-
%global _hardening_ldflags \\\
    %(echo "%{_hardening_ldflags}" | \\\
        sed -e 's/-specs=[^ ]*//g')
%global __global_ldflags \\\
    %(echo "%{__global_ldflags}" | \\\
        sed -e 's/-specs=[^ ]*//g' \\\
            -e 's/-Wl,-z,defs *//g')
%global optflags \\\
    %(echo "%{optflags}" | \\\
        sed -e 's/-m[^ ]*//g' \\\
            -e 's/-specs=[^ ]*//g' \\\
            -e 's/-Werror=[^ ]*//g' \\\
            -e 's/-fstack-clash-protection *//g' \\\
            -e 's/-fcf-protection *//g')
# GCC doesn't build without dependency tracking
# https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55930
%configure \
    --libdir=%{_prefix}/lib \
    --target=%{cross_triplet} \
    --enable-dependency-tracking \
    --with-local-prefix=%{cross_sysroot} \
    --with-sysroot=%{cross_sysroot} \
    --with-gcc-major-version-only \
    --with-linker-hash-style=gnu \
    --with-system-zlib \
    --with-isl \
    --with-zstd \
    --disable-nls \
    --enable-lto \
    --enable-multilib \
    --enable-__cxa_atexit \
    --enable-initfini-array \
    --enable-linker-build-id \
    --enable-gnu-unique-object \
    --enable-gnu-indirect-function \
%if "%{cross_arch}" == "arm"
%if "%(echo %{cross_triplet} | sed 's/.*-\([a-z]*\)$/\1/')" == "gnueabihf"
    --with-tune=generic-armv7-a \
    --with-arch=armv7-a \
    --with-float=hard \
    --with-fpu=vfpv3-d16 \
    --with-abi=aapcs-linux \
%endif
%endif
%if "%{cross_stage}" == "pass1"
    --with-newlib \
    --enable-languages=c \
    --disable-shared \
    --disable-threads \
    --disable-libmudflap \

%make_build all-gcc
%endif
%if "%{cross_stage}" == "pass2"
    --enable-languages=c \
    --enable-shared \
    --disable-libgomp \
    --disable-libmudflap \

%make_build all-gcc all-target-libgcc
%endif
%if "%{cross_stage}" == "final"
%if %{with ada}
    --enable-languages=c,c++,fortran,objc,obj-c++,go,d,lto,ada \
%else
    --enable-languages=c,c++,fortran,objc,obj-c++,go,d,lto \
%endif
%if 0%{?fedora} <= 22
    --with-default-libstdcxx-abi=gcc4-compatible \
%endif
    --enable-shared \
    --enable-libmulflap \
    --enable-libgomp \
    --enable-libssp \
    --enable-libquadmath \
    --enable-libquadmath-support \
    --enable-libsanitizer \
    --enable-gold \
    --enable-plugin \
    --enable-threads=posix \

%make_build
%endif


%install
cd %{_builddir}/gcc-%{version}-build

%if "%{cross_stage}" == "pass1"
%{__make} install-gcc DESTDIR=%{buildroot}
%endif
%if "%{cross_stage}" == "pass2"
%{__make} install-gcc install-target-libgcc DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{cross_sysroot}/%{lib_dir_name}
mv %{buildroot}%{_prefix}/%{cross_triplet}/%{lib_dir_name}/* \
    %{buildroot}%{cross_sysroot}/%{lib_dir_name}
rmdir %{buildroot}%{_prefix}/%{cross_triplet}/%{lib_dir_name}
%endif
%if "%{cross_stage}" == "final"
%make_install
mkdir -p %{buildroot}%{cross_sysroot}/%{lib_dir_name}
mv %{buildroot}%{_prefix}/%{cross_triplet}/%{lib_dir_name}/* \
    %{buildroot}%{cross_sysroot}/%{lib_dir_name}
rmdir %{buildroot}%{_prefix}/%{cross_triplet}/%{lib_dir_name}
%endif

find %{buildroot} -name '*.la' -delete
rm -rf %{buildroot}%{_mandir}
rm -rf %{buildroot}%{_infodir}
rm -rf %{buildroot}%{_datadir}/gcc-%{major_version}/python
rm -f %{buildroot}%{_bindir}/%{cross_triplet}-gcc-%{major_version}
rm -f %{buildroot}%{_libdir}/libcc1.so*
rm -f %{buildroot}%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include-fixed/pthread.h
rm -rf %{buildroot}%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include-fixed/bits
rm -rf %{buildroot}%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/install-tools
rm -f %{buildroot}%{_libexecdir}/gcc/%{cross_triplet}/%{major_version}/install-tools/fixincl
rm -f %{buildroot}%{_libexecdir}/gcc/%{cross_triplet}/%{major_version}/install-tools/fixinc.sh
rm -f %{buildroot}%{_libexecdir}/gcc/%{cross_triplet}/%{major_version}/install-tools/mkheaders
rm -f %{buildroot}%{_libexecdir}/gcc/%{cross_triplet}/%{major_version}/install-tools/mkinstalldirs
rmdir --ignore-fail-on-non-empty %{buildroot}%{_libexecdir}/gcc/%{cross_triplet}/%{major_version}/install-tools

# Don't strip anything - /usr/bin/strip does not work on other architectures
%undefine __strip
%global __strip /bin/true


%files
%license COPYING COPYING.LIB COPYING.RUNTIME COPYING3 COPYING3.LIB
%doc ChangeLog ChangeLog.jit ChangeLog.tree-ssa MAINTAINERS NEWS README
%{_bindir}/%{cross_triplet}-cpp
%{_bindir}/%{cross_triplet}-gcc
%{_bindir}/%{cross_triplet}-gcc-ar
%{_bindir}/%{cross_triplet}-gcc-nm
%{_bindir}/%{cross_triplet}-gcc-ranlib
%{_bindir}/%{cross_triplet}-gcov
%{_bindir}/%{cross_triplet}-gcov-dump
%{_bindir}/%{cross_triplet}-gcov-tool
%{_bindir}/%{cross_triplet}-lto-dump
%dir %{_prefix}/lib/gcc/%{cross_triplet}
%dir %{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}
%dir %{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include-fixed
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include-fixed/README
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include-fixed/limits.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include-fixed/syslimits.h
%dir %{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/stddef.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/stdarg.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/stdfix.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/varargs.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/float.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/stdbool.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/iso646.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/stdint.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/stdint-gcc.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/stdalign.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/stdnoreturn.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/stdatomic.h
%if "%{cross_arch}" == "arm"
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/unwind-arm-common.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/mmintrin.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/arm_cmse.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/arm_cde.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/arm_mve.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/arm_mve_types.h
%endif
%if "%{cross_arch}" == "arm64"
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/arm_sve.h
%endif
%if "%{cross_arch}" == "arm" || "%{cross_arch}" == "arm64"
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/arm_neon.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/arm_acle.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/arm_fp16.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/arm_bf16.h
%endif
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/plugin
%dir %{_libexecdir}/gcc/%{cross_triplet}
%dir %{_libexecdir}/gcc/%{cross_triplet}/%{major_version}
%{_libexecdir}/gcc/%{cross_triplet}/%{major_version}/cc1
%{_libexecdir}/gcc/%{cross_triplet}/%{major_version}/collect2
%{_libexecdir}/gcc/%{cross_triplet}/%{major_version}/lto1
%{_libexecdir}/gcc/%{cross_triplet}/%{major_version}/lto-wrapper
%{_libexecdir}/gcc/%{cross_triplet}/%{major_version}/liblto_plugin.so*
%dir %{_libexecdir}/gcc/%{cross_triplet}/%{major_version}/plugin
%{_libexecdir}/gcc/%{cross_triplet}/%{major_version}/plugin/gengtype
%if "%{cross_stage}" != "pass1"
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/gcov.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/unwind.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/crtbegin*.o
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/crtend*.o
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/crtfastmath.o
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/libgcc.a
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/libgcc_eh.a
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/libgcov.a
%{cross_sysroot}/%{lib_dir_name}/libgcc_s.so
%{cross_sysroot}/%{lib_dir_name}/libgcc_s.so.1
%endif
%if "%{cross_stage}" == "final"
%{_bindir}/%{cross_triplet}-c++
%{_bindir}/%{cross_triplet}-g++
%{_bindir}/%{cross_triplet}-gccgo
%{_bindir}/%{cross_triplet}-gdc
%{_bindir}/%{cross_triplet}-gfortran
%dir %{_prefix}/%{cross_triplet}
%dir %{_prefix}/%{cross_triplet}/include
%dir %{_prefix}/%{cross_triplet}/include/c++
%{_prefix}/%{cross_triplet}/include/c++/%{major_version}
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/ISO_Fortran_binding.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/omp.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/openacc.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/acc_prof.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/d
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/objc
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/ssp
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/include/sanitizer
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/finclude
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/libcaf_single.a
%{_libexecdir}/gcc/%{cross_triplet}/%{major_version}/cc1plus
%{_libexecdir}/gcc/%{cross_triplet}/%{major_version}/cc1obj
%{_libexecdir}/gcc/%{cross_triplet}/%{major_version}/cc1objplus
%{_libexecdir}/gcc/%{cross_triplet}/%{major_version}/d21
%{_libexecdir}/gcc/%{cross_triplet}/%{major_version}/f951
%{_libexecdir}/gcc/%{cross_triplet}/%{major_version}/go1
%dir %{cross_sysroot}/%{lib_dir_name}/go
%{cross_sysroot}/%{lib_dir_name}/go/%{major_version}
%{cross_sysroot}/%{lib_dir_name}/libasan.a
%{cross_sysroot}/%{lib_dir_name}/libasan_preinit.o
%{cross_sysroot}/%{lib_dir_name}/libasan.so*
%{cross_sysroot}/%{lib_dir_name}/libatomic.a
%{cross_sysroot}/%{lib_dir_name}/libatomic.so*
%{cross_sysroot}/%{lib_dir_name}/libgfortran.a
%{cross_sysroot}/%{lib_dir_name}/libgfortran.so*
%{cross_sysroot}/%{lib_dir_name}/libgfortran.spec
%{cross_sysroot}/%{lib_dir_name}/libgdruntime.a
%{cross_sysroot}/%{lib_dir_name}/libgdruntime.so*
%{cross_sysroot}/%{lib_dir_name}/libgo.a
%{cross_sysroot}/%{lib_dir_name}/libgo.so*
%{cross_sysroot}/%{lib_dir_name}/libgobegin.a
%{cross_sysroot}/%{lib_dir_name}/libgolibbegin.a
%{cross_sysroot}/%{lib_dir_name}/libgomp.a
%{cross_sysroot}/%{lib_dir_name}/libgomp.so*
%{cross_sysroot}/%{lib_dir_name}/libgomp.spec
%{cross_sysroot}/%{lib_dir_name}/libgphobos.a
%{cross_sysroot}/%{lib_dir_name}/libgphobos.so*
%{cross_sysroot}/%{lib_dir_name}/libgphobos.spec
%{cross_sysroot}/%{lib_dir_name}/libitm.a
%{cross_sysroot}/%{lib_dir_name}/libitm.so*
%{cross_sysroot}/%{lib_dir_name}/libitm.spec
%{cross_sysroot}/%{lib_dir_name}/libobjc.a
%{cross_sysroot}/%{lib_dir_name}/libobjc.so*
%{cross_sysroot}/%{lib_dir_name}/libsanitizer.spec
%{cross_sysroot}/%{lib_dir_name}/libssp.a
%{cross_sysroot}/%{lib_dir_name}/libssp_nonshared.a
%{cross_sysroot}/%{lib_dir_name}/libssp.so
%{cross_sysroot}/%{lib_dir_name}/libssp.so.0*
%{cross_sysroot}/%{lib_dir_name}/libstdc++fs.a
%{cross_sysroot}/%{lib_dir_name}/libstdc++.a
%{cross_sysroot}/%{lib_dir_name}/libstdc++.so
%{cross_sysroot}/%{lib_dir_name}/libstdc++.so.6
%{cross_sysroot}/%{lib_dir_name}/libstdc++.so.6.*.*
%{cross_sysroot}/%{lib_dir_name}/libsupc++.a
%{cross_sysroot}/%{lib_dir_name}/libubsan.a
%{cross_sysroot}/%{lib_dir_name}/libubsan.so*
%if "%{cross_arch}" == "arm64"
%{cross_sysroot}/%{lib_dir_name}/liblsan.a
%{cross_sysroot}/%{lib_dir_name}/liblsan_preinit.o
%{cross_sysroot}/%{lib_dir_name}/liblsan.so*
%{cross_sysroot}/%{lib_dir_name}/libtsan.a
%{cross_sysroot}/%{lib_dir_name}/libtsan_preinit.o
%{cross_sysroot}/%{lib_dir_name}/libtsan.so*
%endif
%if %{with ada}
%{_bindir}/%{cross_triplet}-gnat
%{_bindir}/%{cross_triplet}-gnatbind
%{_bindir}/%{cross_triplet}-gnatchop
%{_bindir}/%{cross_triplet}-gnatclean
%{_bindir}/%{cross_triplet}-gnatfind
%{_bindir}/%{cross_triplet}-gnatkr
%{_bindir}/%{cross_triplet}-gnatlink
%{_bindir}/%{cross_triplet}-gnatls
%{_bindir}/%{cross_triplet}-gnatmake
%{_bindir}/%{cross_triplet}-gnatname
%{_bindir}/%{cross_triplet}-gnatprep
%{_bindir}/%{cross_triplet}-gnatxref
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/adainclude
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/adalib
%{_prefix}/lib/gcc/%{cross_triplet}/%{major_version}/ada_target_properties
%{_libexecdir}/gcc/%{cross_triplet}/%{major_version}/gnat1
%endif
%endif


%changelog
* Fri Jul 02 2021 Ting-Wei Lan <lantw44@gmail.com> - 10.3.0-2
- Fix build failure with Linux 5.13

* Fri Apr 09 2021 Ting-Wei Lan <lantw44@gmail.com> - 10.3.0-1
- Update to new stable release 10.3.0

* Wed Mar 10 2021 Ting-Wei Lan <lantw44@gmail.com> - 10.2.0-3
- Remove pthread.h from include-fixed directory

* Tue Oct 20 2020 Ting-Wei Lan <lantw44@gmail.com> - 10.2.0-2
- Use versioned build directory
- Add LTO to the list of enabled languages

* Sat Jul 25 2020 Ting-Wei Lan <lantw44@gmail.com> - 10.2.0-1
- Update to new stable release 10.2.0

* Sat May 09 2020 Ting-Wei Lan <lantw44@gmail.com> - 10.1.0-1
- Update to new stable release 10.1.0

* Tue Apr 28 2020 Ting-Wei Lan <lantw44@gmail.com> - 10.0.1-2.20200425git8fc8bf8
- Quote strings in if conditionals for RPM 4.16
- Remove __ar_no_strip and define __strip to a dummy command

* Sun Apr 26 2020 Ting-Wei Lan <lantw44@gmail.com> - 10.0.1-1.20200425git8fc8bf8
- Update to GCC 10 snapshot for Fedora 32

* Sat Mar 21 2020 Ting-Wei Lan <lantw44@gmail.com> - 9.3.0-1
- Update to new stable release 9.3.0

* Mon Feb 10 2020 Ting-Wei Lan <lantw44@gmail.com> - 9.2.0-3
- Fix build failure with GLIBC 2.31

* Tue Sep 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 9.2.0-2
- Rebuilt for Fedora 31 and 32

* Mon Aug 19 2019 Ting-Wei Lan <lantw44@gmail.com> - 9.2.0-1
- Update to new stable release 9.2.0
- Remove bits from include-fixed directory

* Sat May 25 2019 Ting-Wei Lan <lantw44@gmail.com> - 9.1.0-2
- Sync --with-tune argument with the official Fedora package

* Fri May 03 2019 Ting-Wei Lan <lantw44@gmail.com> - 9.1.0-1
- Update to new stable release 9.1.0

* Wed May 01 2019 Ting-Wei Lan <lantw44@gmail.com> - 9.0.1-1.20190501svn270762
- Update to GCC 9 snapshot for Fedora 30
- Enable D support

* Sat Feb 23 2019 Ting-Wei Lan <lantw44@gmail.com> - 8.3.0-1
- Update to new stable release 8.3.0

* Mon Oct 22 2018 Ting-Wei Lan <lantw44@gmail.com> - 8.2.0-2
- Add GCC to BuildRequires for Fedora 29 and later

* Thu Jul 26 2018 Ting-Wei Lan <lantw44@gmail.com> - 8.2.0-1
- Update to new stable release 8.2.0

* Thu Jul 19 2018 Ting-Wei Lan <lantw44@gmail.com> - 8.1.0-2
- Enable Go support

* Wed May 02 2018 Ting-Wei Lan <lantw44@gmail.com> - 8.1.0-1
- Update to new stable release 8.1.0

* Sun Apr 29 2018 Ting-Wei Lan <lantw44@gmail.com> - 8.0.1-1.20180429svn259748
- Update to GCC 8 snapshot for Fedora 28

* Mon Feb 26 2018 Ting-Wei Lan <lantw44@gmail.com> - 7.3.0-2
- Remove -fcf-protection from compiler flags because it needs -m options
- Remove -specs from _hardening_ldflags because it is now used directly
- Remove group tag because it is deprecated in Fedora

* Thu Jan 25 2018 Ting-Wei Lan <lantw44@gmail.com> - 7.3.0-1
- Update to new stable release 7.3.0
- Remove -fstack-clash-protection from compiler flags to fix Fortran build
- Remove -Wl,-z,defs from linker flags to prevent plugins from being disabled

* Mon Dec 11 2017 Ting-Wei Lan <lantw44@gmail.com> - 7.2.0-4
- Use configure, make_build, make_install macros
- Replace define with global

* Thu Dec 07 2017 Ting-Wei Lan <lantw44@gmail.com> - 7.2.0-3
- Fix build ID conflict for Fedora 27 and later

* Mon Oct 16 2017 Ting-Wei Lan <lantw44@gmail.com> - 7.2.0-2
- Rebuilt for Fedora 27 and 28

* Mon Aug 14 2017 Ting-Wei Lan <lantw44@gmail.com> - 7.2.0-1
- Update to new stable release 7.2.0

* Tue Aug 08 2017 Ting-Wei Lan <lantw44@gmail.com> - 7.1.0-4
- Fix build failure with GLIBC 2.26

* Wed Aug 02 2017 Ting-Wei Lan <lantw44@gmail.com> - 7.1.0-3
- Filter provides and requires in adalib directory to sync with GCC 6 branch
- Own include, include-fixed, plugin and versioned gcc directories

* Mon Jul 03 2017 Ting-Wei Lan <lantw44@gmail.com> - 7.1.0-2
- Filter provides and requires in cross_sysroot

* Wed May 03 2017 Ting-Wei Lan <lantw44@gmail.com> - 7.1.0-1
- Update to new stable release 7.1.0
- Use bcond_without macro to conditionally enable Ada support
- Use only major version number in filesystem paths

* Wed Mar 08 2017 Ting-Wei Lan <lantw44@gmail.com> - 6.3.0-2
- Fix wrong string check caught by GCC 7

* Thu Dec 22 2016 Ting-Wei Lan <lantw44@gmail.com> - 6.3.0-1
- Update to new stable release 6.3.0

* Sat Sep 10 2016 Ting-Wei Lan <lantw44@gmail.com> - 6.2.0-2
- Rebuilt for Fedora 25 and 26

* Thu Aug 25 2016 Ting-Wei Lan <lantw44@gmail.com> - 6.2.0-1
- Update to new stable release 6.2.0

* Sun May 08 2016 Ting-Wei Lan <lantw44@gmail.com> - 6.1.0-1
- Update to new stable release 6.1.0
- Drop support for Fedora 23 and older versions

* Thu Mar 03 2016 Ting-Wei Lan <lantw44@gmail.com> - 5.3.0-3
- Rebuilt for Fedora 24 and 25

* Mon Dec 28 2015 Ting-Wei Lan <lantw44@gmail.com> - 5.3.0-2
- Sync configure options with Fedora
- Support arm-linux-gnueabihf and aarch64-linux-gnu

* Sat Dec 05 2015 Ting-Wei Lan <lantw44@gmail.com> - 5.3.0-1
- Update to new stable release 5.3.0
- Fix glibc build with dnf on Fedora 24

* Tue Nov 24 2015 Ting-Wei Lan <lantw44@gmail.com> - 5.2.0-5
- Own the directory of C++ headers
- Require the filesystem sub-package

* Sun Nov 22 2015 Ting-Wei Lan <lantw44@gmail.com> - 5.2.0-4
- Install license files and documentation

* Sat Nov 21 2015 Ting-Wei Lan <lantw44@gmail.com> - 5.2.0-3
- Rebuilt for hardening flags

* Tue Jul 28 2015 Ting-Wei Lan <lantw44@gmail.com> - 5.2.0-2
- Rebuilt for Fedora 23 and 24

* Fri Jul 17 2015 Ting-Wei Lan <lantw44@gmail.com> - 5.2.0-1
- Update to new stable release 5.2.0

* Thu Apr 23 2015 Ting-Wei Lan <lantw44@gmail.com> - 5.1.0-2
- Fix the usage of Fedora macro

* Wed Apr 22 2015 Ting-Wei Lan <lantw44@gmail.com> - 5.1.0-1
- Update to new stable release 5.1.0
- Drop untested and possibly non-working Java support.
- Drop bundled CLooG because it is no longer required in GCC 5.
- Drop bundled ISL because it is now available in Fedora repository.
- Remove libcc1.so to prevent conflict with gcc-gdb-plugin.

* Fri Mar 20 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.9.2-4
- Rebuilt for Fedora 22 and 23
- Ada support cannot be built using GCC 5, so we disable it until GCC 5
  become a stable release.

* Fri Jan 02 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.9.2-3
- Enable Ada support on Fedora 21 or later.

* Sun Dec 21 2014 Ting-Wei Lan <lantw44@gmail.com> - 4.9.2-2
- Disable automatic requirements finding in %{cross_sysroot} instead of
  disabling it in all directories.
- Remove the %{cross_triplet}-kernel-headers dependency. It should be pulled
  in by %{cross_triplet}-glibc or %{cross_triplet}-glibc-headers.

* Fri Dec 19 2014 Ting-Wei Lan <lantw44@gmail.com> - 4.9.2-1
- Initial packaging
