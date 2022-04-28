%global debug_package %{nil}

# Workaround brp-strip failures on Fedora 35.
# https://github.com/rpm-software-management/rpm/issues/1765
%if 0%{?fedora} >= 35
%global __brp_strip   %{nil}
%endif

Name:           guile-gcrypt
Version:        0.3.0
Release:        4%{?dist}
Summary:        Guile bindings to Libgcrypt

License:        GPLv3+
URL:            https://notabug.org/cwebber/guile-gcrypt
Source0:        https://notabug.org/cwebber/guile-gcrypt/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/2.2
%global guile_ccache_dir %{_libdir}/guile/2.2/site-ccache

BuildRequires:  autoconf, automake, make, texinfo
BuildRequires:  pkgconfig(guile-2.2), libgcrypt-devel
Requires:       guile22, libgcrypt-devel
Requires(post): info
Requires(preun): info

%description
Guile-Gcrypt provides a Guile 2.x interface to a subset of the GNU Libgcrypt
crytographic library, which is itself used by the GNU Privacy Guard (GPG).

Guile-Gcrypt provides modules for cryptographic hash functions, message
authentication codes (MAC), public-key crytography, strong randomness, and
more. It is implemented using the foreign function interface (FFI) of Guile.


%prep
%autosetup -n %{name} -p1


%build
./bootstrap.sh
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
%doc AUTHORS ChangeLog NEWS README
%dir %{guile_source_dir}/gcrypt
%dir %{guile_ccache_dir}/gcrypt
%{guile_source_dir}/gcrypt/*.scm
%{guile_ccache_dir}/gcrypt/*.go
%{_infodir}/%{name}.info.gz
%exclude %{_infodir}/dir


%changelog
* Thu Apr 28 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.3.0-4
- Rebuilt for Fedora 36 and 37

* Sat Sep 25 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.3.0-3
- Disable brp-strip on Fedora 35 and later because it fails on Guile objects

* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.3.0-2
- Rebuilt for Fedora 34 and 35

* Sun Nov  1 2020 Ting-Wei Lan <lantw44@gmail.com> - 0.3.0-1
- Update to 0.3.0

* Sun Apr 26 2020 Ting-Wei Lan <lantw44@gmail.com> - 0.2.1-1
- Update to 0.2.1

* Tue Sep 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.2.0-1
- Update to 0.2.0

* Wed May 15 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-3
- Switch to Guile 2.2

* Wed May 01 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-2
- Rebuilt for Fedora 30 and 31

* Sun Dec 02 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-1
- Initial packaging
