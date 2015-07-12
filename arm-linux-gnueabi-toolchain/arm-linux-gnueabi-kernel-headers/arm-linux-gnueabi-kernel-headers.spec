%define cross_arch      arm
%define cross_triplet   arm-linux-gnueabi
%define cross_sysroot   %{_prefix}/%{cross_triplet}/sys-root

Name:       %{cross_triplet}-kernel-headers
Version:    4.1.2
Release:    1%{?dist}
Summary:    Header files for the Linux kernel (%{cross_triplet})

%define kversion        %(echo %{version} | sed 's/\.0$//')

Group:      Development/System
License:    GPLv2
URL:        https://www.kernel.org/
Source0:    https://www.kernel.org/pub/linux/kernel/v4.x/linux-%{kversion}.tar.xz

%description


%prep
%setup -qn linux-%{kversion}


%build
make ARCH=%{cross_arch} mrproper
make ARCH=%{cross_arch} headers_check


%install
install -d %{buildroot}%{cross_sysroot}
make headers_install ARCH=%{cross_arch} \
    INSTALL_HDR_PATH=%{buildroot}%{cross_sysroot}/usr
find %{buildroot}%{cross_sysroot} -name .install -delete
find %{buildroot}%{cross_sysroot} -name ..install.cmd -delete


%files
%{cross_sysroot}/usr/include/asm-generic/*.h
%{cross_sysroot}/usr/include/drm/*.h
%{cross_sysroot}/usr/include/linux/android/binder.h
%{cross_sysroot}/usr/include/linux/byteorder/*.h
%{cross_sysroot}/usr/include/linux/caif/*.h
%{cross_sysroot}/usr/include/linux/can/*.h
%{cross_sysroot}/usr/include/linux/dvb/*.h
%{cross_sysroot}/usr/include/linux/hdlc/*.h
%{cross_sysroot}/usr/include/linux/hsi/*.h
%{cross_sysroot}/usr/include/linux/iio/*.h
%{cross_sysroot}/usr/include/linux/isdn/*.h
%{cross_sysroot}/usr/include/linux/mmc/*.h
%{cross_sysroot}/usr/include/linux/netfilter/ipset/*.h
%{cross_sysroot}/usr/include/linux/netfilter/*.h
%{cross_sysroot}/usr/include/linux/netfilter_arp/*.h
%{cross_sysroot}/usr/include/linux/netfilter_bridge/*.h
%{cross_sysroot}/usr/include/linux/netfilter_ipv4/*.h
%{cross_sysroot}/usr/include/linux/netfilter_ipv6/*.h
%{cross_sysroot}/usr/include/linux/nfsd/*.h
%{cross_sysroot}/usr/include/linux/raid/*.h
%{cross_sysroot}/usr/include/linux/spi/*.h
%{cross_sysroot}/usr/include/linux/sunrpc/*.h
%{cross_sysroot}/usr/include/linux/tc_act/*.h
%{cross_sysroot}/usr/include/linux/tc_ematch/*.h
%{cross_sysroot}/usr/include/linux/usb/*.h
%{cross_sysroot}/usr/include/linux/wimax/*.h
%{cross_sysroot}/usr/include/linux/*.h
%{cross_sysroot}/usr/include/misc/*.h
%{cross_sysroot}/usr/include/mtd/*.h
%{cross_sysroot}/usr/include/rdma/*.h
%{cross_sysroot}/usr/include/scsi/fc/*.h
%{cross_sysroot}/usr/include/scsi/*.h
%{cross_sysroot}/usr/include/sound/*.h
%{cross_sysroot}/usr/include/video/*.h
%{cross_sysroot}/usr/include/xen/*.h
%{cross_sysroot}/usr/include/asm/*.h


%changelog
* Wed Jul 12 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.1.2-1
- Update to 4.1.2

* Wed Jul 01 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.1.1-1
- Update to 4.1.1

* Tue Jun 23 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.1.0-1
- Update to 4.1

* Sun Jun 07 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.0.5-1
- Update to 4.0.5

* Tue May 19 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.0.4-1
- Update to 4.0.4

* Thu May 14 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.0.3-1
- Update to 4.0.3

* Thu May 07 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.0.2-1
- Update to 4.0.2

* Thu Apr 30 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.0.1-1
- Update to 4.0.1

* Mon Apr 13 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.0.0-1
- Update to 4.0

* Thu Mar 26 2015 Ting-Wei Lan <lantw44@gmail.com> - 3.19.3-1
- Update to 3.19.3

* Fri Mar 20 2015 Ting-Wei Lan <lantw44@gmail.com> - 3.19.2-2
- Update to 3.19.2

* Sun Mar 15 2015 Ting-Wei Lan <lantw44@gmail.com> - 3.19.1-1
- Update to 3.19.1

* Thu Dec 18 2014 Ting-Wei Lan <lantw44@gmail.com> - 3.18.1-1
- Initial packaging
