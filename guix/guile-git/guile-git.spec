Name:           guile-git
Version:        0.1.0
Release:        2%{?dist}
Summary:        Guile bindings of libgit2

License:        GPLv3+
URL:            https://gitlab.com/guile-git/guile-git
Source0:        https://gitlab.com/guile-git/guile-git/uploads/e8c218ac7ae77b745c44d1ffbe34f1dd/guile-git-%{version}.tar.gz

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
%autosetup -n %{name}-%{version} -p1


%build
%configure
%make_build


%check
%{__make} %{?_smp_mflags} check


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
* Tue Oct 23 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-2
- Rebuilt for Fedora 29 and 30

* Sat Jul 07 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-1
- Update to 0.1.0

* Sat Dec 09 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.1-0.1.20171106git951a32c
- Initial packaging
