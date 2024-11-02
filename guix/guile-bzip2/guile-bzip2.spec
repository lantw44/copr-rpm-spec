%global debug_package %{nil}

Name:           guile-bzip2
Version:        0.1.0
Release:        1%{?dist}
Summary:        Guile bindings for libbzip2

License:        GPLv3+
URL:            https://ngyro.com/software/guile-bzip2.html
Source0:        https://files.ngyro.com/%{name}/%{name}-%{version}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/3.0
%global guile_ccache_dir %{_libdir}/guile/3.0/site-ccache

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(guile-3.0), pkgconfig(bzip2), guile-bytestructures
Requires:       guile30, guile-bytestructures, bzip2-devel

%description
Guile-bzip2 is a Guile wrapper for the libbzip2 (bzip2) library. It exposes an
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
%{guile_source_dir}/bzip2.scm
%{guile_ccache_dir}/bzip2.go
%dir %{guile_source_dir}/bzip2
%dir %{guile_ccache_dir}/bzip2
%{guile_source_dir}/bzip2/config.scm
%{guile_ccache_dir}/bzip2/config.go
%{guile_source_dir}/bzip2/stream.scm
%{guile_ccache_dir}/bzip2/stream.go


%changelog
* Sat Nov 02 2024 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-1
- Initial packaging
