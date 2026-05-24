%global cross_arch      arm
%global cross_triplet   arm-linux-gnueabi
%global cross_sysroot   %{_prefix}/%{cross_triplet}/sys-root

%if 0%{?_unique_build_ids}
%global _find_debuginfo_opts --build-id-seed "%{name}-%{version}-%{release}"
%endif

%if "%{cross_arch}" == "arm"
%global lib_dir_name    lib
%elif "%{cross_arch}" == "arm64"
%global lib_dir_name    lib64
%else
%global lib_dir_name    lib
%endif

Name:       %{cross_triplet}-libxml2
Version:    2.15.3
Release:    1%{?dist}
Summary:    XML parser and toolkit (%{cross_triplet})

License:    MIT AND ISC-Veillard
URL:        https://gitlab.gnome.org/GNOME/libxml2/-/wikis/home
Source0:    https://download.gnome.org/sources/libxml2/2.15/libxml2-%{version}.tar.xz

BuildRequires: make
BuildRequires: %{cross_triplet}-filesystem
BuildRequires: %{cross_triplet}-gcc-stage2
BuildRequires: %{cross_triplet}-glibc-stage1
Requires:   %{cross_triplet}-filesystem
Requires:   %{cross_triplet}-gcc-stage2
Requires:   %{cross_triplet}-glibc-stage1

%global __provides_exclude_from ^%{cross_sysroot}
%global __requires_exclude_from ^%{cross_sysroot}

%description


%prep
%autosetup -p1 -n libxml2-%{version}


%build
# Set configure arguments.
%global _build          %{_host}
%global _host           %{cross_triplet}
%global _libdir         /usr/%{lib_dir_name}

# Set environment variables.
%global __cc            %{_bindir}/%{cross_triplet}-gcc

# Remove architecture-specific flags and the annotation plugin.
%undefine _annotated_build
%global optflags        %{__global_compiler_flags}

%configure --with-sysroot
%make_build


%install
%make_install DESTDIR=%{buildroot}%{cross_sysroot}

# find-debuginfo runs gdb-add-index, and gdb-add-index needs objcopy.
%global __find_debuginfo \\\
    OBJCOPY=%{_bindir}/%{cross_triplet}-objcopy %{__find_debuginfo}

# Don't strip anything - /usr/bin/strip does not work on other architectures.
%undefine __strip
%global __strip /bin/true


%files
%license Copyright
%doc NEWS README.md
%{cross_sysroot}/usr/bin/xml2-config
%{cross_sysroot}/usr/bin/xmlcatalog
%{cross_sysroot}/usr/bin/xmllint
%{cross_sysroot}/usr/include/libxml2
%{cross_sysroot}/usr/%{lib_dir_name}/libxml2.so
%{cross_sysroot}/usr/%{lib_dir_name}/libxml2.so.16
%{cross_sysroot}/usr/%{lib_dir_name}/libxml2.so.16.*
%{cross_sysroot}/usr/%{lib_dir_name}/cmake/libxml2
%{cross_sysroot}/usr/%{lib_dir_name}/pkgconfig/libxml-2.0.pc


%changelog
* Sun May 24 2026 Ting-Wei Lan <lantw44@gmail.com> - 2.15.3-1
- Initial packaging
