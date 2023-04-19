Name:           disarchive
Version:        0.5.0
Release:        2%{?dist}
Summary:        Disassembler of software archives for long-term preservation

License:        GPLv3+
URL:            https://ngyro.com/software/disarchive.html
Source0:        https://files.ngyro.com/%{name}/%{name}-%{version}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/3.0
%global guile_ccache_dir %{_libdir}/guile/3.0/site-ccache

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(guile-3.0), pkgconfig(zlib)
BuildRequires:  guile-gcrypt, guile-lzma, guile-quickcheck
Requires:       guile30, guile-gcrypt, guile-lzma
Requires:       tar, gzip, xz

%description
Disarchive can disassemble software archives into data and metadata. The goal is
to create a small amount of metadata that can be used to recreate a software
archive bit-for-bit from the original files. For example, a software archive
made using tar and Gzip will need to describe the order of files in the tarball
and the compression parameters used by Gzip. 


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
%license COPYING
%doc ChangeLog NEWS README
%{_bindir}/disarchive
%{_libexecdir}/disarchive-zgz
%{guile_source_dir}/disarchive.scm
%{guile_ccache_dir}/disarchive.go
%dir %{guile_source_dir}/disarchive
%dir %{guile_ccache_dir}/disarchive
%{guile_source_dir}/disarchive/*.scm
%{guile_ccache_dir}/disarchive/*.go
%dir %{guile_source_dir}/disarchive/assemblers
%dir %{guile_ccache_dir}/disarchive/assemblers
%{guile_source_dir}/disarchive/assemblers/*.scm
%{guile_ccache_dir}/disarchive/assemblers/*.go
%dir %{guile_source_dir}/disarchive/formats
%dir %{guile_ccache_dir}/disarchive/formats
%{guile_source_dir}/disarchive/formats/*.scm
%{guile_ccache_dir}/disarchive/formats/*.go
%dir %{guile_source_dir}/disarchive/kinds
%dir %{guile_ccache_dir}/disarchive/kinds
%{guile_source_dir}/disarchive/kinds/*.scm
%{guile_ccache_dir}/disarchive/kinds/*.go
%dir %{guile_source_dir}/disarchive/resolvers
%dir %{guile_ccache_dir}/disarchive/resolvers
%{guile_source_dir}/disarchive/resolvers/*.scm
%{guile_ccache_dir}/disarchive/resolvers/*.go
%dir %{guile_source_dir}/disarchive/scripts
%dir %{guile_ccache_dir}/disarchive/scripts
%{guile_source_dir}/disarchive/scripts/*.scm
%{guile_ccache_dir}/disarchive/scripts/*.go


%changelog
* Wed Apr 19 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.5.0-2
- Rebuilt for Fedora 38 and 39

* Sun Feb 12 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.5.0-1
- Initial packaging
