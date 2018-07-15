Name:           guile-bytestructures
Version:        1.0.3
Release:        1%{?dist}
Summary:        Structured access library to bytevector contents for Guile

License:        GPLv3+
URL:            https://github.com/TaylanUB/scheme-bytestructures
Source0:        https://github.com/TaylanUB/scheme-bytestructures/releases/download/v%{version}/bytestructures-%{version}.tar.gz

%global debug_package    %{nil}
%global guile_source_dir %{_datadir}/guile/site/2.0
%global guile_ccache_dir %{_libdir}/guile/2.0/site-ccache

BuildRequires:  autoconf, automake, pkgconfig(guile-2.0)
Requires:       guile

%description
This library offers a system imitating the type system of the C programming
language, to be used on bytevectors. C's type system works on raw memory, and
ours works on bytevectors which are an abstraction over raw memory in Scheme.
The system is in fact more powerful than the C type system, elevating types to
first-class status.


%prep
%autosetup -n bytestructures-%{version} -p1


%build
%configure
%make_build


%install
%make_install


%files
%license COPYING
%doc README.md
%dir %{guile_source_dir}/bytestructures
%dir %{guile_ccache_dir}/bytestructures
%{guile_source_dir}/bytestructures/body/*.scm
%{guile_source_dir}/bytestructures/guile.scm
%{guile_ccache_dir}/bytestructures/guile.go
%dir %{guile_source_dir}/bytestructures/guile
%dir %{guile_ccache_dir}/bytestructures/guile
%{guile_source_dir}/bytestructures/guile/*.scm
%{guile_ccache_dir}/bytestructures/guile/*.go
%dir %{guile_source_dir}/bytestructures/r6
%dir %{guile_ccache_dir}/bytestructures/r6
%{guile_source_dir}/bytestructures/r6/bytevectors.scm
%{guile_ccache_dir}/bytestructures/r6/bytevectors.go
%exclude %{guile_source_dir}/bytestructures/body
%exclude %{guile_source_dir}/bytestructures/r7
%exclude %{guile_source_dir}/run-tests.*.scm


%changelog
* Sat Jul 07 2018 Ting-Wei Lan <lantw44@gmail.com> - 1.0.3-1
- Update to 1.0.3

* Sat Dec 09 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.1-0.1.20171209git7ed31b1
- Initial packaging
