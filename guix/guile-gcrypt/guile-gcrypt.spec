%global debug_package %{nil}

Name:           guile-gcrypt
Version:        0.1.0
Release:        1%{?dist}
Summary:        Guile bindings to Libgcrypt

License:        GPLv3+
URL:            https://notabug.org/cwebber/guile-gcrypt
Source0:        https://notabug.org/cwebber/guile-gcrypt/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/2.0
%global guile_ccache_dir %{_libdir}/guile/2.0/site-ccache

BuildRequires:  autoconf, automake, texinfo
BuildRequires:  pkgconfig(guile-2.0), libgcrypt-devel
Requires:       guile, libgcrypt-devel
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
* Sun Dec 02 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.1.0-1
- Initial packaging
