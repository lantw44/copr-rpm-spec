%define cross_arch      arm
%define cross_triplet   arm-linux-gnueabi
%define cross_sysroot   %{_prefix}/%{cross_triplet}/sys-root

Name:       %{cross_triplet}-binutils
Version:    2.25
Release:    2%{?dist}
Summary:    A GNU collection of binary utilities (%{cross_triplet})

Group:      Development/Tools
License:    GPLv3+
URL:        https://www.gnu.org/software/binutils
Source0:    https://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.bz2

BuildRequires: texinfo, gettext, flex, bison, zlib-devel

%description


%prep
%setup -qn binutils-%{version}


%build
%configure \
    --host=%{_target_platform} \
    --build=%{_target_platform} \
    --target=%{cross_triplet} \
    --program-prefix=%{cross_triplet}- \
    --enable-ld=default \
    --enable-gold=yes \
    --enable-multilib \
    --enable-threads \
    --enable-plugins \
    --disable-nls \
    --disable-shared \
    --disable-werror \
    --with-sysroot=%{cross_sysroot} \

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_mandir}
rm -rf %{buildroot}%{_infodir}


%files
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
%{_prefix}/%{cross_triplet}/bin/strip
%{_prefix}/%{cross_triplet}/lib/ldscripts


%changelog
* Fri Mar 20 2015 Ting-Wei Lan <lantw44@gmail.com> - 2.25-2
- Rebuilt for Fedora 22 and 23

* Fri Dec 26 2014 Ting-Wei Lan <lantw44@gmail.com> - 2.25-1
- Update to 2.25

* Sat Dec 20 2014 Ting-Wei Lan <lantw44@gmail.com> - 2.24-1
- Initial packaging
