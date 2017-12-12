%global cross_arch      arm
%global cross_triplet   arm-linux-gnueabi
%global cross_sysroot   %{_prefix}/%{cross_triplet}/sys-root

%if %{cross_arch} == "arm"
  %global lib_dir_name        lib
%else
  %if %{cross_arch} == "arm64"
    %global lib_dir_name      lib64
  %else
    %global lib_dir_name      lib
  %endif
%endif

Name:       %{cross_triplet}-filesystem
Version:    3
Release:    6%{?dist}
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
%if %{cross_arch} == "arm64"
mkdir %{buildroot}%{cross_sysroot}/lib
%endif
mkdir %{buildroot}%{cross_sysroot}/%{lib_dir_name}
mkdir %{buildroot}%{cross_sysroot}/sbin
mkdir %{buildroot}%{cross_sysroot}/usr
mkdir %{buildroot}%{cross_sysroot}/usr/bin
mkdir %{buildroot}%{cross_sysroot}/usr/include
%if %{cross_arch} == "arm64"
mkdir %{buildroot}%{cross_sysroot}/usr/lib
%endif
mkdir %{buildroot}%{cross_sysroot}/usr/%{lib_dir_name}
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
%if %{cross_arch} == "arm64"
%dir %{cross_sysroot}/lib
%endif
%dir %{cross_sysroot}/%{lib_dir_name}
%dir %{cross_sysroot}/sbin
%dir %{cross_sysroot}/usr
%dir %{cross_sysroot}/usr/bin
%dir %{cross_sysroot}/usr/include
%if %{cross_arch} == "arm64"
%dir %{cross_sysroot}/usr/lib
%endif
%dir %{cross_sysroot}/usr/%{lib_dir_name}
%dir %{cross_sysroot}/usr/libexec
%dir %{cross_sysroot}/usr/sbin
%dir %{cross_sysroot}/usr/share
%dir %{cross_sysroot}/var
%dir %{cross_sysroot}/var/db



%changelog
* Mon Dec 11 2017 Ting-Wei Lan <lantw44@gmail.com> - 3-6
- Replace define with global

* Mon Oct 16 2017 Ting-Wei Lan <lantw44@gmail.com> - 3-5
- Rebuilt for Fedora 27 and 28

* Wed Mar 08 2017 Ting-Wei Lan <lantw44@gmail.com> - 3-4
- Rebuilt for Fedora 26 and 27

* Sat Sep 10 2016 Ting-Wei Lan <lantw44@gmail.com> - 3-3
- Rebuilt for Fedora 25 and 26

* Thu Mar 03 2016 Ting-Wei Lan <lantw44@gmail.com> - 3-2
- Rebuilt for Fedora 24 and 25

* Tue Dec 29 2015 Ting-Wei Lan <lantw44@gmail.com> - 3-1
- ld needs a empty /usr/lib directory

* Tue Dec 29 2015 Ting-Wei Lan <lantw44@gmail.com> - 2-1
- Support aarch64-linux-gnu
- /usr/etc is not needed

* Tue Nov 24 2015 Ting-Wei Lan <lantw44@gmail.com> - 1-1
- Create required filesystem layout
