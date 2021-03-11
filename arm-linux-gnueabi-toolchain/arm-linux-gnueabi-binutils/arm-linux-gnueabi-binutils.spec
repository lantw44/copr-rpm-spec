%global cross_arch      arm
%global cross_triplet   arm-linux-gnueabi
%global cross_sysroot   %{_prefix}/%{cross_triplet}/sys-root

%if 0%{?_unique_build_ids}
%global _find_debuginfo_opts --build-id-seed "%{name}-%{version}-%{release}"
%endif

Name:       %{cross_triplet}-binutils
Version:    2.36.1
Release:    1%{?dist}
Summary:    A GNU collection of binary utilities (%{cross_triplet})

License:    GPLv3+
URL:        https://www.gnu.org/software/binutils
Source0:    https://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.xz

BuildRequires: gcc, gcc-c++
BuildRequires: texinfo, gettext, flex, bison, zlib-devel
BuildRequires: %{cross_triplet}-filesystem
Requires:   %{cross_triplet}-filesystem

%description


%prep
%autosetup -n binutils-%{version} -p1


%build
%configure \
    --host=%{_target_platform} \
    --build=%{_target_platform} \
    --target=%{cross_triplet} \
    --program-prefix=%{cross_triplet}- \
    --enable-64-bit-bfd \
    --enable-ld=default \
    --enable-gold=yes \
    --enable-multilib \
    --enable-threads \
    --enable-plugins \
    --enable-lto \
    --disable-nls \
    --disable-shared \
    --disable-werror \
    --with-sysroot=%{cross_sysroot} \
    --with-system-zlib \

%make_build


%install
%make_install
rm -rf %{buildroot}%{_mandir}
rm -rf %{buildroot}%{_infodir}
rm -f %{buildroot}%{_libdir}/bfd-plugins/*.a
rmdir %{buildroot}%{_libdir}/bfd-plugins


%files
%license COPYING COPYING.LIB COPYING3 COPYING3.LIB
%doc ChangeLog MAINTAINERS README
%{_bindir}/%{cross_triplet}-addr2line
%{_bindir}/%{cross_triplet}-ar
%{_bindir}/%{cross_triplet}-as
%{_bindir}/%{cross_triplet}-c++filt
%{_bindir}/%{cross_triplet}-dwp
%{_bindir}/%{cross_triplet}-elfedit
%{_bindir}/%{cross_triplet}-gprof
%{_bindir}/%{cross_triplet}-ld
%{_bindir}/%{cross_triplet}-ld.bfd
%{_bindir}/%{cross_triplet}-ld.gold
%{_bindir}/%{cross_triplet}-nm
%{_bindir}/%{cross_triplet}-objcopy
%{_bindir}/%{cross_triplet}-objdump
%{_bindir}/%{cross_triplet}-ranlib
%{_bindir}/%{cross_triplet}-readelf
%{_bindir}/%{cross_triplet}-size
%{_bindir}/%{cross_triplet}-strings
%{_bindir}/%{cross_triplet}-strip
%{_prefix}/%{cross_triplet}/bin/ar
%{_prefix}/%{cross_triplet}/bin/as
%{_prefix}/%{cross_triplet}/bin/ld
%{_prefix}/%{cross_triplet}/bin/ld.bfd
%{_prefix}/%{cross_triplet}/bin/ld.gold
%{_prefix}/%{cross_triplet}/bin/nm
%{_prefix}/%{cross_triplet}/bin/objcopy
%{_prefix}/%{cross_triplet}/bin/objdump
%{_prefix}/%{cross_triplet}/bin/ranlib
%{_prefix}/%{cross_triplet}/bin/readelf
%{_prefix}/%{cross_triplet}/bin/strip
%{_prefix}/%{cross_triplet}/lib/ldscripts


%changelog
* Wed Mar 10 2021 Ting-Wei Lan <lantw44@gmail.com> - 2.36.1-1
- Update to 2.36.1

* Tue Oct 20 2020 Ting-Wei Lan <lantw44@gmail.com> - 2.35.1-1
- Update to 2.35.1
- Enable LTO

* Mon Jul 27 2020 Ting-Wei Lan <lantw44@gmail.com> - 2.35-1
- Update to 2.35

* Sat Apr 25 2020 Ting-Wei Lan <lantw44@gmail.com> - 2.34-2
- Rebuilt for Fedora 32 and 33

* Sun Feb 09 2020 Ting-Wei Lan <lantw44@gmail.com> - 2.34-1
- Update to 2.34
- Use xz-compressed source tarball

* Sun Oct 13 2019 Ting-Wei Lan <lantw44@gmail.com> - 2.33.1-1
- Update to 2.33.1

* Tue Sep 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 2.32-3
- Rebuilt for Fedora 31 and 32

* Wed May 01 2019 Ting-Wei Lan <lantw44@gmail.com> - 2.32-2
- Rebuilt for Fedora 30 and 31

* Fri Feb 22 2019 Ting-Wei Lan <lantw44@gmail.com> - 2.32-1
- Update to 2.32

* Mon Oct 22 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.31.1-2
- Add GCC to BuildRequires for Fedora 29 and later

* Sat Jul 28 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.31.1-1
- Update to 2.31.1

* Tue Jul 17 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.31-1
- Update to 2.31

* Mon Feb 26 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.30-2
- Remove group tag because it is deprecated in Fedora

* Sun Jan 28 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.30-1
- Update to 2.30

* Mon Dec 11 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.29.1-3
- Use autosetup, make_build, make_install macros
- Replace define with global

* Thu Dec 07 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.29.1-2
- Fix build ID conflict for Fedora 27 and later

* Mon Oct 16 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.29.1-1
- Update to 2.29.1

* Tue Jul 25 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.29-1
- Update to 2.29

* Tue Mar 07 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.28-1
- Update to 2.28

* Sat Sep 10 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.27-2
- Rebuilt for Fedora 25 and 26

* Tue Aug 16 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.27-1
- Update to 2.27

* Wed Jun 29 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.26.1-1
- Update to 2.26.1

* Thu Mar 03 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.26-2
- Rebuilt for Fedora 24 and 25

* Mon Jan 25 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.26-1
- Update to 2.26

* Mon Dec 28 2015 Ting-Wei Lan <lantw44@gmail.com> - 2.25.1-5
- Sync configure options with Fedora
- Support arm-linux-gnueabihf and aarch64-linux-gnu

* Tue Nov 24 2015 Ting-Wei Lan <lantw44@gmail.com> - 2.25.1-4
- Require the filesystem sub-package

* Sun Nov 22 2015 Ting-Wei Lan <lantw44@gmail.com> - 2.25.1-3
- Install license files and documentation

* Tue Jul 28 2015 Ting-Wei Lan <lantw44@gmail.com> - 2.25.1-2
- Rebuilt for Fedora 23 and 24

* Thu Jul 23 2015 Ting-Wei Lan <lantw44@gmail.com> - 2.25.1-1
- Update to 2.25.1

* Fri Mar 20 2015 Ting-Wei Lan <lantw44@gmail.com> - 2.25-2
- Rebuilt for Fedora 22 and 23

* Fri Dec 26 2014 Ting-Wei Lan <lantw44@gmail.com> - 2.25-1
- Update to 2.25

* Sat Dec 20 2014 Ting-Wei Lan <lantw44@gmail.com> - 2.24-1
- Initial packaging
