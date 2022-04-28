%global debug_package %{nil}

# Workaround brp-strip failures on Fedora 35.
# https://github.com/rpm-software-management/rpm/issues/1765
%if 0%{?fedora} >= 35
%global __brp_strip   %{nil}
%endif

Name:           guile-git
Version:        0.5.2
Release:        2%{?dist}
Summary:        Guile bindings of libgit2

License:        GPLv3+ and LGPLv3+
URL:            https://gitlab.com/guile-git/guile-git
Source0:        https://gitlab.com/guile-git/guile-git/uploads/6450f3991aa524484038cdcea3fb248d/guile-git-%{version}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/2.2
%global guile_ccache_dir %{_libdir}/guile/2.2/site-ccache

BuildRequires:  gcc
BuildRequires:  autoconf, automake, texinfo
BuildRequires:  pkgconfig(guile-2.2), pkgconfig(libgit2), guile-bytestructures
Requires:       guile22, guile-bytestructures, libgit2-devel
Requires(post): info
Requires(preun): info

%description
Guile-Git provides Guile bindings to libgit2, a library to manipulate
repositories of the Git version control system.


%prep
%autosetup -n %{name}-%{version} -p1


%build
%configure GUILE=%{_bindir}/guile2.2 GUILD=%{_bindir}/guild2.2
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
%license COPYING COPYING.LESSER
%doc NEWS README.md
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
* Thu Apr 28 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.5.2-2
- Rebuilt for Fedora 36 and 37

* Sat Sep 25 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.5.2-1
- Update to 0.5.2
- Disable brp-strip on Fedora 35 and later because it fails on Guile objects

* Mon Jun 14 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.5.1-1
- Update to 0.5.1

* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.4.0-2
- Rebuilt for Fedora 34 and 35

* Sun Nov  1 2020 Ting-Wei Lan <lantw44@gmail.com> - 0.4.0-1
- Update to 0.4.0

* Sun Apr 26 2020 Ting-Wei Lan <lantw44@gmail.com> - 0.3.0-1
- Update to 0.3.0

* Tue Sep 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.2.0-3
- Rebuilt for Fedora 31 and 32

* Wed May 15 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.2.0-2
- Switch to Guile 2.2
- Fix license

* Thu May 02 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.2.0-1
- Update to 0.2.0

* Tue Oct 23 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-2
- Rebuilt for Fedora 29 and 30

* Sat Jul 07 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-1
- Update to 0.1.0

* Sat Dec 09 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.1-0.1.20171106git951a32c
- Initial packaging
