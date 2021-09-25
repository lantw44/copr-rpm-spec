%global debug_package %{nil}

# Workaround brp-strip failures on Fedora 35.
# https://github.com/rpm-software-management/rpm/issues/1765
%if 0%{?fedora} >= 35
%global __brp_strip   %{nil}
%endif

Name:           guile-lib
Version:        0.2.7
Release:        2%{?dist}
Summary:        Guile-Lib is a repository of useful code written in Guile Scheme

License:        GPLv3+
URL:            https://www.nongnu.org/guile-lib
Source0:        https://download.savannah.nongnu.org/releases/%{name}/%{name}-%{version}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/2.2
%global guile_ccache_dir %{_libdir}/guile/2.2/site-ccache

BuildRequires:  gcc
BuildRequires:  pkgconfig(guile-2.2)
Requires:       guile22

%description
Guile-Lib is intended as an accumulation place for pure-scheme Guile modules,
allowing for people to cooperate integrating their generic Guile modules into a
coherent library.

Guile-Lib modules are well-documented and well-supported. Particularly good
modules might migrate from Guile-Lib into Guile itself, at some point.

Think "a down-scaled, limited-scope CPAN for Guile".


%prep
%autosetup -p1
sed -i 's|"guile"|"guile2.2"|g' unit-tests/os.process.scm


%build
%configure GUILE=%{_bindir}/guile2.2 GUILD=%{_bindir}/guild2.2
%make_build moddir=%{guile_source_dir} godir=%{guile_ccache_dir}


%check
%{__make} %{?_smp_mflags} check


%install
%make_install moddir=%{guile_source_dir} godir=%{guile_ccache_dir}


%post
/sbin/install-info %{_infodir}/guile-library.info.gz %{_infodir}/dir || :


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/guile-library.info.gz %{_infodir}/dir || :
fi


%files
%license COPYING COPYING.GPL COPYING.LGPL
%doc AUTHORS ChangeLog NEWS README TODO
%{guile_source_dir}/apicheck.scm
%{guile_ccache_dir}/apicheck.go
%dir %{guile_source_dir}/compat
%dir %{guile_ccache_dir}/compat
%{guile_source_dir}/compat/*.scm
%{guile_ccache_dir}/compat/*.go
%dir %{guile_source_dir}/config
%dir %{guile_ccache_dir}/config
%{guile_source_dir}/config/*.scm
%{guile_ccache_dir}/config/*.go
%dir %{guile_source_dir}/container
%dir %{guile_ccache_dir}/container
%{guile_source_dir}/container/*.scm
%{guile_ccache_dir}/container/*.go
%dir %{guile_source_dir}/debugging
%dir %{guile_ccache_dir}/debugging
%{guile_source_dir}/debugging/*.scm
%{guile_ccache_dir}/debugging/*.go
%dir %{guile_source_dir}/graph
%dir %{guile_ccache_dir}/graph
%{guile_source_dir}/graph/*.scm
%{guile_ccache_dir}/graph/*.go
%{guile_source_dir}/htmlprag.scm
%{guile_ccache_dir}/htmlprag.go
%dir %{guile_source_dir}/io
%dir %{guile_ccache_dir}/io
%{guile_source_dir}/io/*.scm
%{guile_ccache_dir}/io/*.go
%dir %{guile_source_dir}/logging
%dir %{guile_ccache_dir}/logging
%{guile_source_dir}/logging/*.scm
%{guile_ccache_dir}/logging/*.go
%{guile_source_dir}/match-bind.scm
%{guile_ccache_dir}/match-bind.go
%dir %{guile_source_dir}/math
%dir %{guile_ccache_dir}/math
%{guile_source_dir}/math/*.scm
%{guile_ccache_dir}/math/*.go
%{guile_source_dir}/md5.scm
%{guile_ccache_dir}/md5.go
%dir %{guile_source_dir}/os
%dir %{guile_ccache_dir}/os
%{guile_source_dir}/os/*.scm
%{guile_ccache_dir}/os/*.go
%dir %{guile_source_dir}/scheme
%dir %{guile_ccache_dir}/scheme
%{guile_source_dir}/scheme/*.scm
%{guile_ccache_dir}/scheme/*.go
%dir %{guile_source_dir}/search
%dir %{guile_ccache_dir}/search
%{guile_source_dir}/search/*.scm
%{guile_ccache_dir}/search/*.go
%dir %{guile_source_dir}/string
%dir %{guile_ccache_dir}/string
%{guile_source_dir}/string/*.scm
%{guile_ccache_dir}/string/*.go
%dir %{guile_source_dir}/term
%dir %{guile_ccache_dir}/term
%{guile_source_dir}/term/*.scm
%{guile_ccache_dir}/term/*.go
%dir %{guile_source_dir}/texinfo
%dir %{guile_ccache_dir}/texinfo
%{guile_source_dir}/texinfo/*.scm
%{guile_ccache_dir}/texinfo/*.go
%dir %{guile_source_dir}/text
%dir %{guile_ccache_dir}/text
%{guile_source_dir}/text/*.scm
%{guile_ccache_dir}/text/*.go
%{guile_source_dir}/unit-test.scm
%{guile_ccache_dir}/unit-test.go
%{_libdir}/pkgconfig/guile-lib-1.0.pc
%{_infodir}/guile-library.info.gz
%exclude %{_infodir}/dir


%changelog
* Sat Sep 25 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.2.7-2
- Disable brp-strip on Fedora 35 and later because it fails on Guile objects

* Mon Jun 14 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.2.7-1
- Initial packaging
