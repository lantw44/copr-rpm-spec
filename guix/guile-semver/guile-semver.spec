%global debug_package %{nil}

# Workaround brp-strip failures on Fedora 35.
# https://github.com/rpm-software-management/rpm/issues/1765
%if 0%{?fedora} >= 35
%global __brp_strip   %{nil}
%endif

Name:           guile-semver
Version:        0.1.1
Release:        3%{?dist}
Summary:        Guile library for Semantic Versioning

License:        GPLv3+
URL:            https://ngyro.com/software/guile-semver.html
Source0:        https://files.ngyro.com/%{name}/%{name}-%{version}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/2.2
%global guile_ccache_dir %{_libdir}/guile/2.2/site-ccache

BuildRequires:  make
BuildRequires:  pkgconfig(guile-2.2)
Requires:       guile22

%description
guile-semver is a Guile library that handles Semantic Versions and NPM-style
ranges. It supports:

- reading and writing Semantic Versions;
- comparing Semantic Versions;
- reading Semantic Version ranges; and
- testing membership of Semantic Versions in ranges.


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
%doc AUTHORS ChangeLog NEWS README THANKS
%{guile_source_dir}/semver.scm
%{guile_ccache_dir}/semver.go
%dir %{guile_source_dir}/semver
%dir %{guile_ccache_dir}/semver
%{guile_source_dir}/semver/partial.scm
%{guile_ccache_dir}/semver/partial.go
%{guile_source_dir}/semver/ranges.scm
%{guile_ccache_dir}/semver/ranges.go


%changelog
* Sat Sep 25 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.1.1-3
- Disable brp-strip on Fedora 35 and later because it fails on Guile objects

* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.1.1-2
- Rebuilt for Fedora 34 and 35

* Mon Feb 15 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.1.1-1
- Initial packaging
