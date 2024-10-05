%global debug_package %{nil}

Name:           guile-lzma
Version:        0.1.1
Release:        3%{?dist}
Summary:        Guile bindings for liblzma

License:        GPLv3+
URL:            https://ngyro.com/software/guile-lzma.html
Source0:        https://files.ngyro.com/%{name}/%{name}-%{version}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/3.0
%global guile_ccache_dir %{_libdir}/guile/3.0/site-ccache

BuildRequires:  make
BuildRequires:  pkgconfig(guile-3.0), pkgconfig(liblzma), guile-bytestructures
Requires:       guile30, guile-bytestructures, xz-devel

%description
Guile-LZMA is a Guile wrapper for the liblzma (XZ) library. It exposes an
interface similar to other Guile compression libraries, like Guile-zlib.


%prep
%autosetup -p1


%build
%configure
%make_build


%check
%{__make} %{?_smp_mflags} check


%install
%make_install


%files
%license COPYING COPYING.CC0
%doc AUTHORS ChangeLog NEWS README
%{guile_source_dir}/lzma.scm
%{guile_ccache_dir}/lzma.go
%dir %{guile_source_dir}/lzma
%dir %{guile_ccache_dir}/lzma
%{guile_source_dir}/lzma/config.scm
%{guile_ccache_dir}/lzma/config.go
%{guile_source_dir}/lzma/stream.scm
%{guile_ccache_dir}/lzma/stream.go


%changelog
* Sat Oct 05 2024 Ting-Wei Lan <lantw44@gmail.com> - 0.1.1-3
- Drop the brp-strip workaround

* Wed Apr 19 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.1.1-2
- Rebuilt for Fedora 38 and 39

* Sun Feb 12 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.1.1-1
- Initial packaging
