%global debug_package %{nil}

Name:           guile-gcrypt
Version:        0.4.0
Release:        5%{?dist}
Summary:        Guile bindings to Libgcrypt

License:        GPL-3.0-or-later
URL:            https://notabug.org/cwebber/guile-gcrypt
Source0:        https://notabug.org/cwebber/guile-gcrypt/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/3.0
%global guile_ccache_dir %{_libdir}/guile/3.0/site-ccache

BuildRequires:  autoconf, automake, make, texinfo
BuildRequires:  pkgconfig(guile-3.0), libgcrypt-devel
Requires:       guile30, libgcrypt-devel
Requires(post): info
Requires(preun): info

%description
Guile-Gcrypt provides a Guile 3.x/2.x interface to a subset of the GNU Libgcrypt
cryptographic library, which is itself used by the GNU Privacy Guard (GPG).

Guile-Gcrypt provides modules for cryptographic hash functions, message
authentication codes (MAC), public-key cryptography, strong randomness, and
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
* Sat May 24 2025 Ting-Wei Lan <lantw44@gmail.com> - 0.4.0-5
- Migrate to SPDX license

* Sun Nov 03 2024 Ting-Wei Lan <lantw44@gmail.com> - 0.4.0-4
- Rebuilt for Fedora 39, 40, 41, 42

* Sat Oct 05 2024 Ting-Wei Lan <lantw44@gmail.com> - 0.4.0-3
- Drop the brp-strip workaround

* Wed Apr 19 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.4.0-2
- Rebuilt for Fedora 38 and 39

* Sun Feb 12 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.4.0-1
- Update to 0.4.0
- Switch to Guile 3.0

* Sat Oct 29 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.3.0-5
- Rebuilt for Fedora 37 and 38

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
