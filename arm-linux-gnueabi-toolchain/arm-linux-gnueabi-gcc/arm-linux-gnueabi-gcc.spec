%define cross_arch      arm
%define cross_triplet   arm-linux-gnueabi
%define cross_sysroot   %{_prefix}/%{cross_triplet}/sys-root

%if 0%{!?cross_stage:1}
%define cross_stage     final
%endif

%if %{cross_stage} != "final"
%define pkg_suffix      -%{cross_stage}
%else
%define pkg_suffix      %{nil}
%endif

%define enable_java     0
%if 0%{?fedora} >= 21
%define enable_ada      1
%else
%define enable_ada      0
%endif

%define isl_version     0.12.2
%define isl_source      %{_builddir}/isl-%{isl_version}
%define isl_build       %{_builddir}/isl-build
%define isl_install     %{_builddir}/isl-install
%define cloog_version   0.18.1
%define cloog_source    %{_builddir}/cloog-%{cloog_version}
%define cloog_build     %{_builddir}/cloog-build
%define cloog_install   %{_builddir}/cloog-install

Name:       %{cross_triplet}-gcc%{pkg_suffix}
Version:    4.9.2
Release:    3%{?dist}
Summary:    The GNU Compiler Collection (%{cross_triplet})

Group:      Development/Languages
License:    GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
URL:        https://gcc.gnu.org
Source0:    https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.bz2
Source1:    ftp://gcc.gnu.org/pub/gcc/infrastructure/isl-%{isl_version}.tar.bz2
Source2:    ftp://gcc.gnu.org/pub/gcc/infrastructure/cloog-%{cloog_version}.tar.gz

BuildRequires: texinfo, gettext, flex, bison, zlib-devel
BuildRequires: gmp-devel, mpfr-devel, libmpc-devel, elfutils-libelf-devel
BuildRequires: %{cross_triplet}-binutils
Requires:   %{cross_triplet}-binutils

%if %{cross_stage} == "pass2"
BuildRequires: %{cross_triplet}-glibc-headers
Requires:   %{cross_triplet}-glibc-headers
Provides:   %{cross_triplet}-gcc-pass1 = %{version}
Obsoletes:  %{cross_triplet}-gcc-pass1 <= %{version}
%endif

%if %{cross_stage} == "final"
BuildRequires: %{cross_triplet}-glibc
BuildRequires: gcc-gnat, libstdc++-static
Requires:   %{cross_triplet}-glibc
Provides:   %{cross_triplet}-gcc-pass1 = %{version}
Provides:   %{cross_triplet}-gcc-pass2 = %{version}
Obsoletes:  %{cross_triplet}-gcc-pass1 <= %{version}
Obsoletes:  %{cross_triplet}-gcc-pass2 <= %{version}
%endif

%description


%prep
%setup -qTb 2 -n cloog-%{cloog_version}
%setup -qTb 1 -n isl-%{isl_version}
%setup -qTb 0 -n gcc-%{version}


%build
mkdir -p %{isl_build} %{isl_install}
cd %{isl_build}
%{isl_source}/configure \
    --prefix=%{isl_install} \
    --disable-shared \

make %{?_smp_mflags}
make install

mkdir -p %{cloog_build} %{cloog_install}
cd %{cloog_build}
%{cloog_source}/configure \
    --prefix=%{cloog_install} \
    --disable-shared \
    --with-isl=system \
    --with-isl-prefix=%{isl_install} \

make %{?_smp_mflags} V=1
make install

mkdir -p %{_builddir}/gcc-build
cd %{_builddir}/gcc-build
AR_FOR_TARGET=%{_bindir}/%{cross_triplet}-ar \
AS_FOR_TARGET=%{_bindir}/%{cross_triplet}-as \
DLLTOOL_FOR_TARGET=%{_bindir}/%{cross_triplet}-dlltool \
LD_FOR_TARGET=%{_bindir}/%{cross_triplet}-ld \
NM_FOR_TARGET=%{_bindir}/%{cross_triplet}-nm \
OBJDUMP_FOR_TARGET=%{_bindir}/%{cross_triplet}-objdump \
RANLIB_FOR_TARGET=%{_bindir}/%{cross_triplet}-ranlib \
STRIP_FOR_TARGET=%{_bindir}/%{cross_triplet}-strip \
WINDRES_FOR_TARGET=%{_bindir}/%{cross_triplet}-windres \
WINDMC_FOR_TARGET=%{_bindir}/%{cross_triplet}-windmc \
../gcc-%{version}/configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --host=%{_target_platform} \
    --build=%{_target_platform} \
    --target=%{cross_triplet} \
    --with-local-prefix=%{cross_sysroot} \
    --with-sysroot=%{cross_sysroot} \
    --with-isl=%{isl_install} \
    --with-cloog=%{cloog_install} \
    --with-system-zlib \
    --disable-nls \
    --enable-lto \
    --enable-__cxa_atexit \
    --enable-linker-build-id \
%if %{cross_stage} == "pass1"
    --with-newlib \
    --enable-languages=c \
    --disable-shared \
    --disable-threads \
    --disable-libmudflap \

make %{?_smp_mflags} all-gcc
%endif
%if %{cross_stage} == "pass2"
    --enable-languages=c \
    --enable-shared \
    --disable-libgomp \
    --disable-libmudflap \

make %{?_smp_mflags} all-gcc all-target-libgcc
%endif
%if %{cross_stage} == "final"
%if %{enable_ada}
    --enable-languages=c,c++,fortran,objc,obj-c++,ada \
%else
    --enable-languages=c,c++,fortran,objc,obj-c++ \
%endif
    --enable-libmulflap \
    --enable-libgomp \
    --enable-libssp \
    --enable-libquadmath \
    --enable-libquadmath-support \
    --enable-libsanitizer \
    --enable-gold \
    --enable-plugin \
    --enable-threads=posix \

make %{?_smp_mflags}
%endif


%install
cd %{_builddir}/gcc-build

%if %{cross_stage} == "pass1"
make install-gcc DESTDIR=%{buildroot}
%endif
%if %{cross_stage} == "pass2"
make install-gcc install-target-libgcc DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{cross_sysroot}/lib
mv %{buildroot}%{_prefix}/%{cross_triplet}/lib/* %{buildroot}%{cross_sysroot}/lib
rmdir %{buildroot}%{_prefix}/%{cross_triplet}/lib
%endif
%if %{cross_stage} == "final"
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{cross_sysroot}/lib
mv %{buildroot}%{_prefix}/%{cross_triplet}/lib/* %{buildroot}%{cross_sysroot}/lib
rmdir %{buildroot}%{_prefix}/%{cross_triplet}/lib
%endif

find %{buildroot} -name '*.la' -delete
rm -rf %{buildroot}%{_mandir}
rm -rf %{buildroot}%{_infodir}
rm -rf %{buildroot}%{_datadir}/gcc-%{version}/python
rm -f %{buildroot}%{_bindir}/%{cross_triplet}-gcc-%{version}
rm -rf %{buildroot}%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/install-tools
rm -f %{buildroot}%{_libexecdir}/gcc/%{cross_triplet}/%{version}/install-tools/fixincl
rm -f %{buildroot}%{_libexecdir}/gcc/%{cross_triplet}/%{version}/install-tools/fixinc.sh
rm -f %{buildroot}%{_libexecdir}/gcc/%{cross_triplet}/%{version}/install-tools/mkheaders
rm -f %{buildroot}%{_libexecdir}/gcc/%{cross_triplet}/%{version}/install-tools/mkinstalldirs
rmdir --ignore-fail-on-non-empty %{buildroot}%{_libexecdir}/gcc/%{cross_triplet}/%{version}/install-tools

# Don't strip libgcc.a and libgcov.a - based on Fedora Project cross-gcc.spec
%define __ar_no_strip $RPM_BUILD_DIR/gcc-%{version}/ar-no-strip
cat > %{__ar_no_strip} << EOF
#!/bin/sh
f=\$2
case \$(basename \$f) in
    *.a)
        ;;
    *)
        %{__strip} \$@
        ;;
esac
EOF
chmod +x %{__ar_no_strip}
%undefine __strip
%define __strip %{__ar_no_strip}

# Disable automatic requirements finding in %{cross_sysroot}
%define _use_internal_dependency_generator 0
%define __rpmdeps_command %{__find_requires}
%define __rpmdeps_skip_sysroot %{_builddir}/gcc-%{version}/rpmdeps-skip-sysroot
cat > %{__rpmdeps_skip_sysroot} << EOF
#!/bin/sh
while read oneline; do
    case \$oneline in
        %{buildroot}%{cross_sysroot}*)
            ;;
        *)
            echo \$oneline | %{__rpmdeps_command}
    esac
done
EOF
chmod +x %{__rpmdeps_skip_sysroot}
%undefine __find_requires
%define __find_requires %{__rpmdeps_skip_sysroot}


%files
%{_bindir}/%{cross_triplet}-cpp
%{_bindir}/%{cross_triplet}-gcc
%{_bindir}/%{cross_triplet}-gcc-ar
%{_bindir}/%{cross_triplet}-gcc-nm
%{_bindir}/%{cross_triplet}-gcc-ranlib
%{_bindir}/%{cross_triplet}-gcov
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include-fixed/README
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include-fixed/limits.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include-fixed/syslimits.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/stddef.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/stdarg.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/stdfix.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/varargs.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/float.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/stdbool.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/iso646.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/stdint.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/stdint-gcc.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/stdalign.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/stdnoreturn.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/stdatomic.h
%if %{cross_arch} == "arm"
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/unwind-arm-common.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/mmintrin.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/arm_neon.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/arm_acle.h
%endif
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/plugin
%{_libexecdir}/gcc/%{cross_triplet}/%{version}/cc1
%{_libexecdir}/gcc/%{cross_triplet}/%{version}/collect2
%{_libexecdir}/gcc/%{cross_triplet}/%{version}/lto1
%{_libexecdir}/gcc/%{cross_triplet}/%{version}/lto-wrapper
%{_libexecdir}/gcc/%{cross_triplet}/%{version}/liblto_plugin.so*
%{_libexecdir}/gcc/%{cross_triplet}/%{version}/plugin/gengtype
%if %{cross_stage} != "pass1"
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/unwind.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/crtbegin*.o
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/crtend*.o
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/libgcc.a
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/libgcc_eh.a
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/libgcov.a
%{cross_sysroot}/lib/libgcc_s.so
%{cross_sysroot}/lib/libgcc_s.so.1
%endif
%if %{cross_stage} == "final"
%{_bindir}/%{cross_triplet}-c++
%{_bindir}/%{cross_triplet}-g++
%{_bindir}/%{cross_triplet}-gfortran
%{_prefix}/%{cross_triplet}/include/c++/%{version}
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/omp.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/objc
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/ssp
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/sanitizer
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/finclude
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/libcaf_single.a
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/libgfortranbegin.a
%{_libexecdir}/gcc/%{cross_triplet}/%{version}/cc1plus
%{_libexecdir}/gcc/%{cross_triplet}/%{version}/cc1obj
%{_libexecdir}/gcc/%{cross_triplet}/%{version}/cc1objplus
%{_libexecdir}/gcc/%{cross_triplet}/%{version}/f951
%{cross_sysroot}/lib/libasan.a
%{cross_sysroot}/lib/libasan_preinit.o
%{cross_sysroot}/lib/libasan.so*
%{cross_sysroot}/lib/libatomic.a
%{cross_sysroot}/lib/libatomic.so*
%{cross_sysroot}/lib/libgfortran.a
%{cross_sysroot}/lib/libgfortran.so*
%{cross_sysroot}/lib/libgfortran.spec
%{cross_sysroot}/lib/libgomp.a
%{cross_sysroot}/lib/libgomp.so*
%{cross_sysroot}/lib/libgomp.spec
%{cross_sysroot}/lib/libitm.a
%{cross_sysroot}/lib/libitm.so*
%{cross_sysroot}/lib/libitm.spec
%{cross_sysroot}/lib/libobjc.a
%{cross_sysroot}/lib/libobjc.so*
%{cross_sysroot}/lib/libsanitizer.spec
%{cross_sysroot}/lib/libssp.a
%{cross_sysroot}/lib/libssp_nonshared.a
%{cross_sysroot}/lib/libssp.so
%{cross_sysroot}/lib/libssp.so.0*
%{cross_sysroot}/lib/libstdc++.a
%{cross_sysroot}/lib/libstdc++.so
%{cross_sysroot}/lib/libstdc++.so.6
%{cross_sysroot}/lib/libstdc++.so.6.*.*
%{cross_sysroot}/lib/libsupc++.a
%{cross_sysroot}/lib/libubsan.a
%{cross_sysroot}/lib/libubsan.so*
%if %{enable_java}
%{_bindir}/%{cross_triplet}-aot-compile
%{_bindir}/%{cross_triplet}-gcj
%{_bindir}/%{cross_triplet}-jcf-dump
%{_bindir}/%{cross_triplet}-rebuild-gcj-db
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/gcj
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/jawt.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/jawt_md.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/jni.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/jni_md.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/jvmpi.h
%{_libexecdir}/gcc/%{cross_triplet}/%{version}/jc1
%{_libexecdir}/gcc/%{cross_triplet}/%{version}/jvgenmain
%{cross_sysroot}/lib/gcj-%{version}-15/libjvm.so
%{cross_sysroot}/lib/libgcj.so
%{cross_sysroot}/lib/libgcj.so.15*
%{cross_sysroot}/lib/libgcj.spec
%{cross_sysroot}/lib/libgcj_bc.so*
%{cross_sysroot}/lib/libgij.so
%{cross_sysroot}/lib/libgij.so.15*
%{cross_sysroot}/lib/logging.properties
%{cross_sysroot}/lib/pkgconfig/libgcj-4.9.pc
%{cross_sysroot}/lib/security/classpath.security
%endif
%if %{enable_ada}
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
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/adainclude
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/adalib
%{_libexecdir}/gcc/%{cross_triplet}/%{version}/gnat1
%endif
%endif


%changelog
* Fri Jan 02 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.9.2-3
- Enable Ada support on Fedora 21 or later.

* Sun Dec 21 2014 Ting-Wei Lan <lantw44@gmail.com> - 4.9.2-2
- Disable automatic requirements finding in %{cross_sysroot} instead of
  disabling it in all directories.
- Remove the %{cross_triplet}-kernel-headers dependency. It should be pulled
  in by %{cross_triplet}-glibc or %{cross_triplet}-glibc-headers.

* Fri Dec 19 2014 Ting-Wei Lan <lantw44@gmail.com> - 4.9.2-1
- Initial packaging