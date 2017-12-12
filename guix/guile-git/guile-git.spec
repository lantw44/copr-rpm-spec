%global commit 951a32c56cc4d80f8836e3c7394783e69c1fcbad
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           guile-git
Version:        0.1
Release:        0.1.20171106git%{shortcommit}%{?dist}
Summary:        Guile bindings of libgit2

License:        GPLv3+
URL:            https://gitlab.com/guile-git/guile-git
Source0:        https://gitlab.com/guile-git/guile-git/repository/%{commit}/archive.tar.bz2#/%{name}-%{commit}.tar.bz2

%global debug_package    %{nil}
%global guile_source_dir %{_datadir}/guile/site/2.0
%global guile_ccache_dir %{_libdir}/guile/2.0/site-ccache

BuildRequires:  autoconf, automake, texinfo
BuildRequires:  pkgconfig(guile-2.0), pkgconfig(libgit2), guile-bytestructures
Requires:       guile, guile-bytestructures, libgit2-devel
Requires(post): info
Requires(preun): info

%description
Guile-Git provides Guile bindings to libgit2, a library to manipulate
repositories of the Git version control system.


%prep
%autosetup -n %{name}-%{commit}-%{commit} -p1


%build
./bootstrap
%configure
%make_build


%check
# segfault on i686
%ifnarch %{ix86}
%{__make} %{?_smp_mflags} check
%endif


%install
%make_install


%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi


%files
%license COPYING
%doc README.md
%{guile_source_dir}/git.scm
%{guile_ccache_dir}/git.go
%dir %{guile_source_dir}/git
%dir %{guile_ccache_dir}/git
%{guile_source_dir}/git/*.scm
%{guile_ccache_dir}/git/*.go
%dir %{guile_source_dir}/git/web
%dir %{guile_ccache_dir}/git/web
%{guile_source_dir}/git/web/*.scm
%{guile_ccache_dir}/git/web/*.go
%{_infodir}/%{name}.info.gz
%exclude %{_infodir}/dir


%changelog
* Sat Dec 09 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.1-0.1.20171106git951a32c
- Initial packaging
