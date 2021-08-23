%global cross_arch      arm
%global cross_triplet   arm-linux-gnueabi
%global cross_sysroot   %{_prefix}/%{cross_triplet}/sys-root

%if "%{cross_arch}" == "arm"
  %global lib_dir_name        lib
%else
  %if "%{cross_arch}" == "arm64"
    %global lib_dir_name      lib64
  %else
    %global lib_dir_name      lib
  %endif
%endif

Name:       %{cross_triplet}-filesystem
Version:    3
Release:    15%{?dist}
Summary:    Cross compilation toolchain filesystem layout (%{cross_triplet})

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
%if "%{cross_arch}" == "arm64"
mkdir %{buildroot}%{cross_sysroot}/lib
%endif
mkdir %{buildroot}%{cross_sysroot}/%{lib_dir_name}
mkdir %{buildroot}%{cross_sysroot}/sbin
mkdir %{buildroot}%{cross_sysroot}/usr
mkdir %{buildroot}%{cross_sysroot}/usr/bin
mkdir %{buildroot}%{cross_sysroot}/usr/include
%if "%{cross_arch}" == "arm64"
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
%if "%{cross_arch}" == "arm64"
%dir %{cross_sysroot}/lib
%endif
%dir %{cross_sysroot}/%{lib_dir_name}
%dir %{cross_sysroot}/sbin
%dir %{cross_sysroot}/usr
%dir %{cross_sysroot}/usr/bin
%dir %{cross_sysroot}/usr/include
%if "%{cross_arch}" == "arm64"
%dir %{cross_sysroot}/usr/lib
%endif
%dir %{cross_sysroot}/usr/%{lib_dir_name}
%dir %{cross_sysroot}/usr/libexec
%dir %{cross_sysroot}/usr/sbin
%dir %{cross_sysroot}/usr/share
%dir %{cross_sysroot}/var
%dir %{cross_sysroot}/var/db



%changelog
* Mon Aug 23 2021 Ting-Wei Lan <lantw44@gmail.com> - 3-15
- Rebuilt for Fedora 35 and 36

* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 3-14
- Rebuilt for Fedora 34 and 35

* Tue Oct 20 2020 Ting-Wei Lan <lantw44@gmail.com> - 3-13
- Rebuilt for Fedora 33 and 34

* Sun Apr 26 2020 Ting-Wei Lan <lantw44@gmail.com> - 3-12
- Quote strings in if conditionals for RPM 4.16

* Sat Apr 25 2020 Ting-Wei Lan <lantw44@gmail.com> - 3-11
- Rebuilt for Fedora 32 and 33

* Tue Sep 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 3-10
- Rebuilt for Fedora 31 and 32

* Wed May 01 2019 Ting-Wei Lan <lantw44@gmail.com> - 3-9
- Rebuilt for Fedora 30 and 31

* Mon Oct 22 2018 Ting-Wei Lan <lantw44@gmail.com> - 3-8
- Rebuilt for Fedora 29 and 30

* Mon Feb 26 2018 Ting-Wei Lan <lantw44@gmail.com> - 3-7
- Remove group tag because it is deprecated in Fedora

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
