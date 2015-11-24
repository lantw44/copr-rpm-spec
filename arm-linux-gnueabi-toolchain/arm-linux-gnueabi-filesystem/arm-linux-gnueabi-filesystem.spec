%define cross_arch      arm
%define cross_triplet   arm-linux-gnueabi
%define cross_sysroot   %{_prefix}/%{cross_triplet}/sys-root

Name:       %{cross_triplet}-filesystem
Version:    1
Release:    1%{?dist}
Summary:    Cross compilation toolchain filesystem layout (%{cross_triplet})

Group:      Development/System
License:    Public Domain
URL:        https://copr.fedoraproject.org/coprs/lantw44/arm-linux-gnueabi-toolchain

BuildArch:  noarch

%description


%prep


%build


%install
mkdir -p %{buildroot}%{_prefix}/%{cross_triplet}
mkdir %{buildroot}%{_prefix}/%{cross_triplet}/bin
mkdir %{buildroot}%{_prefix}/%{cross_triplet}/lib
mkdir -p %{buildroot}%{cross_sysroot}
mkdir %{buildroot}%{cross_sysroot}/etc
mkdir %{buildroot}%{cross_sysroot}/lib
mkdir %{buildroot}%{cross_sysroot}/sbin
mkdir %{buildroot}%{cross_sysroot}/usr
mkdir %{buildroot}%{cross_sysroot}/usr/bin
mkdir %{buildroot}%{cross_sysroot}/usr/etc
mkdir %{buildroot}%{cross_sysroot}/usr/include
mkdir %{buildroot}%{cross_sysroot}/usr/lib
mkdir %{buildroot}%{cross_sysroot}/usr/libexec
mkdir %{buildroot}%{cross_sysroot}/usr/sbin
mkdir %{buildroot}%{cross_sysroot}/usr/share
mkdir %{buildroot}%{cross_sysroot}/var
mkdir %{buildroot}%{cross_sysroot}/var/db


%files
%dir %{_prefix}/%{cross_triplet}
%dir %{_prefix}/%{cross_triplet}/bin
%dir %{_prefix}/%{cross_triplet}/lib
%dir %{cross_sysroot}
%dir %{cross_sysroot}/etc
%dir %{cross_sysroot}/lib
%dir %{cross_sysroot}/sbin
%dir %{cross_sysroot}/usr
%dir %{cross_sysroot}/usr/bin
%dir %{cross_sysroot}/usr/etc
%dir %{cross_sysroot}/usr/include
%dir %{cross_sysroot}/usr/lib
%dir %{cross_sysroot}/usr/libexec
%dir %{cross_sysroot}/usr/sbin
%dir %{cross_sysroot}/usr/share
%dir %{cross_sysroot}/var
%dir %{cross_sysroot}/var/db



%changelog
* Tue Nov 24 2015 Ting-Wei Lan <lantw44@gmail.com> - 1-1
- Create required filesystem layout
