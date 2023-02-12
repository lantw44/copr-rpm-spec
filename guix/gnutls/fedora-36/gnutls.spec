## START: Set by rpmautospec
## (rpmautospec version 0.3.0)
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%define srpmhash() %{lua:
local files = rpm.expand("%_specdir/gnutls.spec")
for i, p in ipairs(patches) do
   files = files.." "..p
end
for i, p in ipairs(sources) do
   files = files.." "..p
end
local sha256sum = assert(io.popen("cat "..files.."| sha256sum"))
local hash = sha256sum:read("*a")
sha256sum:close()
print(string.sub(hash, 0, 16))
}

%global with_mingw 0
%if 0%{?fedora}
%global with_mingw 0%{!?_without_mingw:1}
%endif 

Version: 3.7.8
Release: %{?autorelease}%{!?autorelease:1%{?dist}}
Patch: fedora-36_gnutls-3.6.7-no-now-guile.patch
Patch: fedora-36_gnutls-3.2.7-rpath.patch

%bcond_without bootstrap
%bcond_without dane
%if 0%{?rhel}
%bcond_with guile
%bcond_without fips
%else
%bcond_without guile
%bcond_without fips
%endif
%bcond_with tpm12
%bcond_without tpm2
%bcond_without gost
%bcond_with certificate_compression
%bcond_without tests

Summary: A TLS protocol implementation
Name: gnutls
# The libraries are LGPLv2.1+, utilities are GPLv3+
License: GPLv3+ and LGPLv2+
BuildRequires: p11-kit-devel >= 0.21.3, gettext-devel
BuildRequires: readline-devel, libtasn1-devel >= 4.3
%if %{with certificate_compression}
BuildRequires: zlib-devel, brotli-devel, libzstd-devel
%endif
%if %{with bootstrap}
BuildRequires: automake, autoconf, gperf, libtool, texinfo
%endif
BuildRequires: nettle-devel >= 3.5.1
%if %{with tpm12}
BuildRequires: trousers-devel >= 0.3.11.2
%endif
%if %{with tpm2}
BuildRequires: tpm2-tss-devel >= 3.0.3
%endif
BuildRequires: libidn2-devel
BuildRequires: libunistring-devel
BuildRequires: net-tools, datefudge, softhsm, gcc, gcc-c++
BuildRequires: gnupg2
BuildRequires: git-core

# for a sanity check on cert loading
BuildRequires: p11-kit-trust, ca-certificates
Requires: crypto-policies
Requires: p11-kit-trust
Requires: libtasn1 >= 4.3
Requires: nettle >= 3.4.1
%if %{with tpm12}
Recommends: trousers >= 0.3.11.2
%endif

%if %{with dane}
BuildRequires: unbound-devel unbound-libs
%endif
%if %{with guile}
BuildRequires: guile30-devel
%endif
BuildRequires: make gtk-doc

%if %{with_mingw}
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-libtasn1 >= 4.3
BuildRequires:  mingw32-readline
BuildRequires:  mingw32-zlib
BuildRequires:  mingw32-p11-kit >= 0.23.1
BuildRequires:  mingw32-nettle >= 3.6
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-libtasn1 >= 4.3
BuildRequires:  mingw64-readline
BuildRequires:  mingw64-zlib
BuildRequires:  mingw64-p11-kit >= 0.23.1
BuildRequires:  mingw64-nettle >= 3.6
%endif

URL: http://www.gnutls.org/
%define short_version %(echo %{version} | grep -m1 -o "[0-9]*\.[0-9]*" | head -1)
Source0: https://www.gnupg.org/ftp/gcrypt/gnutls/v%{short_version}/%{name}-%{version}.tar.xz
Source1: https://www.gnupg.org/ftp/gcrypt/gnutls/v%{short_version}/%{name}-%{version}.tar.xz.sig
Source2: gnutls-release-keyring.gpg

# Wildcard bundling exception https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib) = 20130424

%package c++
Summary: The C++ interface to GnuTLS
Requires: %{name}%{?_isa} = %{version}-%{release}

%package devel
Summary: Development files for the %{name} package
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-c++%{?_isa} = %{version}-%{release}
%if %{with dane}
Requires: %{name}-dane%{?_isa} = %{version}-%{release}
%endif
Requires: pkgconfig

%package utils
License: GPLv3+
Summary: Command line tools for TLS protocol
Requires: %{name}%{?_isa} = %{version}-%{release}
%if %{with dane}
Requires: %{name}-dane%{?_isa} = %{version}-%{release}
%endif

%if %{with dane}
%package dane
Summary: A DANE protocol implementation for GnuTLS
Requires: %{name}%{?_isa} = %{version}-%{release}
%endif

%if %{with guile}
%package guile30
Summary: Guile bindings for the GNUTLS library
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: guile30
%endif

%description
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS 
protocols and technologies around them. It provides a simple C language 
application programming interface (API) to access the secure communications 
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and 
other required structures. 

%description c++
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS 
protocols and technologies around them. It provides a simple C language 
application programming interface (API) to access the secure communications 
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and 
other required structures. 

%description devel
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS 
protocols and technologies around them. It provides a simple C language 
application programming interface (API) to access the secure communications 
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and 
other required structures. 
This package contains files needed for developing applications with
the GnuTLS library.

%description utils
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS 
protocols and technologies around them. It provides a simple C language 
application programming interface (API) to access the secure communications 
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and 
other required structures. 
This package contains command line TLS client and server and certificate
manipulation tools.

%if %{with dane}
%description dane
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS 
protocols and technologies around them. It provides a simple C language 
application programming interface (API) to access the secure communications 
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and 
other required structures. 
This package contains library that implements the DANE protocol for verifying
TLS certificates through DNSSEC.
%endif

%if %{with guile}
%description guile30
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS 
protocols and technologies around them. It provides a simple C language 
application programming interface (API) to access the secure communications 
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and 
other required structures. 
This package contains Guile bindings for the library.
%endif

%if %{with_mingw}
%package -n mingw32-%{name}
Summary:        MinGW GnuTLS TLS/SSL encryption library
Requires:       pkgconfig
Requires:       mingw32-libtasn1 >= 4.3
BuildArch:      noarch

%description -n mingw32-gnutls
GnuTLS TLS/SSL encryption library.  This library is cross-compiled
for MinGW.

%package -n mingw64-%{name}
Summary:        MinGW GnuTLS TLS/SSL encryption library
Requires:       pkgconfig
Requires:       mingw64-libtasn1 >= 4.3
BuildArch:      noarch

%description -n mingw64-gnutls
GnuTLS TLS/SSL encryption library.  This library is cross-compiled
for MinGW.

%{?mingw_debug_package}
%endif

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'

%autosetup -p1 -S git

%build
%define _lto_cflags %{nil}

%if %{with bootstrap}
autoreconf -fi
%endif

sed -i -e 's|sys_lib_dlsearch_path_spec="/lib /usr/lib|sys_lib_dlsearch_path_spec="/lib /usr/lib %{_libdir}|g' configure
rm -f lib/minitasn1/*.c lib/minitasn1/*.h

echo "SYSTEM=NORMAL" >> tests/system.prio

CCASFLAGS="$CCASFLAGS -Wa,--generate-missing-build-notes=yes"
export CCASFLAGS

%if %{with guile}
# These should be checked by m4/guile.m4 instead of configure.ac
# taking into account of _guile_suffix
guile_snarf=%{_bindir}/guile-snarf3.0
export guile_snarf
GUILD=%{_bindir}/guild3.0
export GUILD
%endif

%if %{with fips}
eval $(sed -n 's/^\(\(NAME\|VERSION_ID\)=.*\)/OS_\1/p' /etc/os-release)
export FIPS_MODULE_NAME="$OS_NAME ${OS_VERSION_ID%%.*} %name"
%endif

mkdir native_build
pushd native_build
%global _configure ../configure
%configure \
%if %{with fips}
           --enable-fips140-mode \
           --with-fips140-module-name="$FIPS_MODULE_NAME" \
           --with-fips140-module-version=%{version}-%{srpmhash} \
%endif
%if %{with gost}
    	   --enable-gost \
%else
	   --disable-gost \
%endif
	   --enable-sha1-support \
           --disable-static \
           --disable-openssl-compatibility \
           --disable-non-suiteb-curves \
           --with-system-priority-file=%{_sysconfdir}/crypto-policies/back-ends/gnutls.config \
           --with-default-trust-store-pkcs11="pkcs11:" \
%if %{with tpm12}
           --with-trousers-lib=%{_libdir}/libtspi.so.1 \
%else
           --without-tpm \
%endif
%if %{with tpm2}
           --with-tpm2 \
%else
           --without-tpm2 \
%endif
           --enable-ktls \
           --htmldir=%{_docdir}/manual \
%if %{with guile}
           --enable-guile \
           --with-guile-extension-dir=%{_libdir}/guile/3.0 \
%else
           --disable-guile \
%endif
%if %{with dane}
           --with-unbound-root-key-file=/var/lib/unbound/root.key \
           --enable-libdane \
%else
           --disable-libdane \
%endif
%if %{with certificate_compression}
	   --with-zlib --with-brotli --with-zstd \
%else
	   --without-zlib --without-brotli --without-zstd \
%endif
           --disable-rpath \
           --with-default-priority-string="@SYSTEM"

%make_build
popd

%if %{with_mingw}
# MinGW does not support CCASFLAGS
export CCASFLAGS=""
%mingw_configure \
    --enable-sha1-support \
    --disable-static \
    --disable-openssl-compatibility \
    --disable-non-suiteb-curves \
    --disable-guile \
    --disable-libdane \
    --disable-rpath \
    --disable-nls \
    --disable-cxx \
    --enable-local-libopts \
    --enable-shared \
    --without-tpm \
    --with-included-unistring \
    --disable-doc \
    --with-default-priority-string="@SYSTEM"
%mingw_make %{?_smp_mflags}
%endif

%install
%make_install -C native_build
pushd native_build
make -C doc install-html DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/guile/3.0/guile-gnutls*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/guile/3.0/guile-gnutls*.la
%if %{without dane}
rm -f $RPM_BUILD_ROOT%{_libdir}/pkgconfig/gnutls-dane.pc
%endif

%if %{with fips}
# doing it twice should be a no-op the second time,
# and this way we avoid redefining it and missing a future change
%{__spec_install_post}
./lib/fipshmac "$RPM_BUILD_ROOT%{_libdir}/libgnutls.so.30" > $RPM_BUILD_ROOT%{_libdir}/.gnutls.hmac
sed -i "s^$RPM_BUILD_ROOT/usr^^" $RPM_BUILD_ROOT%{_libdir}/.gnutls.hmac
%endif

%if %{with fips}
%define __spec_install_post \
	%{?__debug_package:%{__debug_install_post}} \
	%{__arch_install_post} \
	%{__os_install_post} \
%{nil}
%endif

%find_lang gnutls
popd

%if %{with_mingw}
%mingw_make_install

# Remove .la files
rm -f $RPM_BUILD_ROOT%{mingw32_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{mingw64_libdir}/*.la

# The .def files aren't interesting for other binaries
rm -f $RPM_BUILD_ROOT%{mingw32_bindir}/*.def
rm -f $RPM_BUILD_ROOT%{mingw64_bindir}/*.def

# Remove info and man pages which duplicate stuff in Fedora already.
rm -rf $RPM_BUILD_ROOT%{mingw32_infodir}
rm -rf $RPM_BUILD_ROOT%{mingw32_mandir}
rm -rf $RPM_BUILD_ROOT%{mingw32_docdir}/gnutls

rm -rf $RPM_BUILD_ROOT%{mingw64_infodir}
rm -rf $RPM_BUILD_ROOT%{mingw64_mandir}
rm -rf $RPM_BUILD_ROOT%{mingw64_docdir}/gnutls

# Remove test libraries
rm -f $RPM_BUILD_ROOT%{mingw32_libdir}/crypt32.dll*
rm -f $RPM_BUILD_ROOT%{mingw32_libdir}/ncrypt.dll*
rm -f $RPM_BUILD_ROOT%{mingw64_libdir}/crypt32.dll*
rm -f $RPM_BUILD_ROOT%{mingw64_libdir}/ncrypt.dll*

%mingw_debug_install_post
%endif

%check
%if %{with tests}
pushd native_build
make check %{?_smp_mflags} GNUTLS_SYSTEM_PRIORITY_FILE=/dev/null
popd
%endif

%files -f native_build/gnutls.lang
%{_libdir}/libgnutls.so.30*
%if %{with fips}
%{_libdir}/.gnutls.hmac
%endif
%doc README.md AUTHORS NEWS THANKS
%license LICENSE doc/COPYING doc/COPYING.LESSER

%files c++
%{_libdir}/libgnutlsxx.so.*

%files devel
%{_includedir}/*
%{_libdir}/libgnutls*.so

%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*
%{_infodir}/gnutls*
%{_infodir}/pkcs11-vision*
%{_docdir}/manual/*

%files utils
%{_bindir}/certtool
%if %{with tpm12}
%{_bindir}/tpmtool
%endif
%{_bindir}/ocsptool
%{_bindir}/psktool
%{_bindir}/p11tool
%{_bindir}/srptool
%if %{with dane}
%{_bindir}/danetool
%endif
%{_bindir}/gnutls*
%{_mandir}/man1/*
%doc doc/certtool.cfg

%if %{with dane}
%files dane
%{_libdir}/libgnutls-dane.so.*
%endif

%if %{with guile}
%files guile30
%{_libdir}/guile/3.0/guile-gnutls*.so*
%{_libdir}/guile/3.0/site-ccache/gnutls.go
%{_libdir}/guile/3.0/site-ccache/gnutls/extra.go
%{_datadir}/guile/site/3.0/gnutls.scm
%{_datadir}/guile/site/3.0/gnutls/extra.scm
%endif

%if %{with_mingw}
%files -n mingw32-%{name}
%license LICENSE doc/COPYING doc/COPYING.LESSER
%{mingw32_bindir}/certtool.exe
%{mingw32_bindir}/gnutls-cli-debug.exe
%{mingw32_bindir}/gnutls-cli.exe
%{mingw32_bindir}/gnutls-serv.exe
%{mingw32_bindir}/libgnutls-30.dll
%{mingw32_bindir}/ocsptool.exe
%{mingw32_bindir}/p11tool.exe
%{mingw32_bindir}/psktool.exe
%{mingw32_bindir}/srptool.exe
%{mingw32_libdir}/libgnutls.dll.a
%{mingw32_libdir}/libgnutls-30.def
%{mingw32_libdir}/pkgconfig/gnutls.pc
%{mingw32_includedir}/gnutls/

%files -n mingw64-%{name}
%license LICENSE doc/COPYING doc/COPYING.LESSER
%{mingw64_bindir}/certtool.exe
%{mingw64_bindir}/gnutls-cli-debug.exe
%{mingw64_bindir}/gnutls-cli.exe
%{mingw64_bindir}/gnutls-serv.exe
%{mingw64_bindir}/libgnutls-30.dll
%{mingw64_bindir}/ocsptool.exe
%{mingw64_bindir}/p11tool.exe
%{mingw64_bindir}/psktool.exe
%{mingw64_bindir}/srptool.exe
%{mingw64_libdir}/libgnutls.dll.a
%{mingw64_libdir}/libgnutls-30.def
%{mingw64_libdir}/pkgconfig/gnutls.pc
%{mingw64_includedir}/gnutls/
%endif

%changelog
* Fri Nov 04 2022 Zoltan Fridrich <zfridric@redhat.com> 3.7.8-3
- Cross-compiled mingw sub-RPMs should be 'noarch'

* Wed Oct 19 2022 Zoltan Fridrich <zfridric@redhat.com> 3.7.8-2
- Add mingw package

* Tue Oct 18 2022 Zoltan Fridrich <zfridric@redhat.com> 3.7.8-1
- [packit] 3.7.8 upstream release

* Fri Jul 29 2022 Zoltan Fridrich <zfridric@redhat.com> 3.7.7-1
- [packit] 3.7.7 upstream release

* Wed Jun 22 2022 Daiki Ueno <dueno@redhat.com> 3.7.6-3
- rebuild with nettle 3.8 for fipshmac

* Tue Jun 14 2022 Daiki Ueno <dueno@redhat.com> 3.7.6-2
- Fix %%autorelease usage

* Fri May 27 2022 Zoltan Fridrich <zfridric@redhat.com> 3.7.6-1
- [packit] 3.7.6 upstream release

* Tue May 17 2022 Zoltan Fridrich <zfridric@redhat.com> 3.7.5-1
- [packit] 3.7.5 upstream release

* Tue Apr 26 2022 Zoltan Fridrich <zfridric@redhat.com> 3.7.4-2
- Add dist tag to release

* Mon Apr 25 2022 Zoltan Fridrich <zfridric@redhat.com> 3.7.4-1
- [packit] 3.7.4 upstream release

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 18 2022 Daiki Ueno <dueno@redhat.com> - 3.7.3-1
- Update to upstream 3.7.3 release
- Remove dependency on autogen
- Add build-time conditionals for TPM 1.2 and GOST cryptography

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May 29 2021 Daiki Ueno <dueno@redhat.com> - 3.7.2-1
- Update to upstream 3.7.2 release

* Sun Mar 28 2021 Daiki Ueno <dueno@redhat.com> - 3.7.1-3
- Remove %%defattr invocations which are no longer necessary
- libpkcs11mock1.* is not installed anymore
- hobble-gnutls: Remove SRP removal
- Use correct source URL
- Switch to using %%gpgverify macro

* Tue Mar 16 2021 Daiki Ueno <dueno@redhat.com> - 3.7.1-2
- Restore fipscheck dependency

* Sat Mar 13 2021 Daiki Ueno <dueno@redhat.com> - 3.7.1-1
- Update to upstream 3.7.1 release
- Remove fipscheck dependency, as it is now calculated with an
  internal tool

* Fri Mar  5 2021 Daiki Ueno <dueno@redhat.com> - 3.7.0-4
- Tolerate duplicate certs in the chain also with PKCS #11 trust store

* Tue Mar  2 2021 Daiki Ueno <dueno@redhat.com> - 3.7.0-3
- Reduce BRs for non-bootstrapping build

* Wed Feb 10 2021 Daiki Ueno <dueno@redhat.com> - 3.7.0-2
- Tolerate duplicate certs in the chain

* Mon Feb  8 2021 Daiki Ueno <dueno@redhat.com> - 3.7.0-1
- Update to upstream 3.7.0 release
- Temporarily disable LTO

* Tue Jan 26 2021 Daiki Ueno <dueno@redhat.com> - 3.6.15-4
- Fix broken tests on rawhide (#1908110)
- Add BuildRequires: make (by Tom Stellard)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Sep 28 2020 Jeff Law <law@redhat.com> - 3.6.15-2
- Re-enable LTO now that upstream GCC bugs have been fixed

* Fri Sep  4 2020 Daiki Ueno <dueno@redhat.com> - 3.6.15-1
- Update to upstream 3.6.15 release

* Mon Aug 17 2020 Jeff Law <law@redhat.com> - 3.6.14-7
- Disable LTO on ppc64le

* Tue Aug  4 2020 Daiki Ueno <dueno@redhat.com> - 3.6.14-6
- Fix underlinking of libpthread

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.14-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 02 2020 Anderson Sasaki <ansasaki@redhat.com> - 3.6.14-3
- Rebuild with autogen built with guile-2.2 (#1852706)

* Tue Jun 09 2020 Anderson Sasaki <ansasaki@redhat.com> - 3.6.14-2
- Fix memory leak when serializing iovec_t (#1845083)
- Fix automatic libraries sonames detection (#1845806)

* Thu Jun  4 2020 Daiki Ueno <dueno@redhat.com> - 3.6.14-1
- Update to upstream 3.6.14 release

* Sun May 31 2020 Daiki Ueno <dueno@redhat.com> - 3.6.13-6
- Update gnutls-3.6.13-superseding-chain.patch

* Sun May 31 2020 Daiki Ueno <dueno@redhat.com> - 3.6.13-5
- Fix cert chain validation behavior if the last cert has expired (#1842178)

* Mon May 25 2020 Anderson Sasaki <ansasaki@redhat.com> - 3.6.13-4
- Add option to gnutls-cli to wait for resumption under TLS 1.3

* Tue May 19 2020 Anderson Sasaki <ansasaki@redhat.com> - 3.6.13-3
- Disable RSA blinding during FIPS self-tests

* Thu May 14 2020 Anderson Sasaki <ansasaki@redhat.com> - 3.6.13-2
- Bump linked libraries soname to fix FIPS selftests (#1835265)

* Tue Mar 31 2020 Daiki Ueno <dueno@redhat.com> - 3.6.13-1
- Update to upstream 3.6.13 release

* Thu Mar 26 2020 Anderson Sasaki <ansasaki@redhat.com> - 3.6.12-2
- Fix FIPS POST (#1813384)
- Fix gnutls-serv --echo to not exit when a message is received (#1816583)

* Sun Feb 02 2020 Nikos Mavrogiannopoulos <n.mavrogiannopoulos@gmail.com> - 3.6.12-1
- Update to upstream 3.6.12 release

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 02 2019 Nikos Mavrogiannopoulos <nmav@gnutls.org> - 3.6.11-1
- Update to upstream 3.6.11 release

* Sun Sep 29 2019 Nikos Mavrogiannopoulos <nmav@gnutls.org> - 3.6.10-1
- Update to upstream 3.6.10 release

* Fri Jul 26 2019 Nikos Mavrogiannopoulos <nmav@gnutls.org> - 3.6.9-1
- Update to upstream 3.6.9 release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 15 2019 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.6.8-2
- Rebuilt with guile-2.2

* Tue May 28 2019 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.6.8-1
- Update to upstream 3.6.8 release

* Wed Mar 27 2019 Anderson Toshiyuki Sasaki <ansasaki@redhat.com> - 3.6.7-1
- Update to upstream 3.6.7 release
- Fixed CVE-2019-3836 (#1693214)
- Fixed CVE-2019-3829 (#1693210)

* Fri Feb  1 2019 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.6.6-1
- Update to upstream 3.6.6 release

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 11 2019 Anderson Toshiyuki Sasaki <ansasaki@redhat.com> - 3.6.5-2
- Added explicit Requires for nettle >= 3.4.1

* Tue Dec 11 2018 Anderson Toshiyuki Sasaki <ansasaki@redhat.com> - 3.6.5-1
- Update to upstream 3.6.5 release

* Mon Oct 29 2018 James Antill <james.antill@redhat.com> - 3.6.4-5
- Remove ldconfig scriptlet, now done via. transfiletrigger in glibc.

* Wed Oct 17 2018 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.6.4-4
- Fix issue with rehandshake affecting glib-networking (#1634736)

* Tue Oct 16 2018 Tomáš Mráz <tmraz@redhat.com> - 3.6.4-3
- Add missing annobin notes for assembler sources

* Tue Oct 09 2018 Petr Menšík <pemensik@redhat.com> - 3.6.4-2
- Rebuilt for unbound 1.8

* Tue Sep 25 2018 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.6.4-1
- Updated to upstream 3.6.4 release
- Added support for the latest version of the TLS1.3 protocol
- Enabled SHA1 support as SHA1 deprecation is handled via the
  fedora crypto policies.

* Thu Aug 16 2018 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.6.3-4
- Fixed gnutls-cli input reading
- Ensure that we do not cause issues with version rollback detection
  and TLS1.3.

* Tue Aug 07 2018 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.6.3-3
- Fixed ECDSA public key import (#1612803)

* Thu Jul 26 2018 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.6.3-2
- Backported regression fixes from 3.6.2

* Mon Jul 16 2018 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.6.3-1
- Update to upstream 3.6.3 release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 13 2018 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.6.2-4
- Enable FIPS140-2 mode in Fedora

* Wed Jun 06 2018 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.6.2-3
- Update to upstream 3.6.2 release

* Fri May 25 2018 David Abdurachmanov <david.abdurachmanov@gmail.com> - 3.6.2-2
- Add missing BuildRequires: gnupg2 for gpgv2 in %%prep

* Fri Feb 16 2018 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.6.2-1
- Update to upstream 3.6.2 release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb  2 2018 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.6.1-4
- Rebuilt to address incompatibility with new nettle

* Thu Nov 30 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.6.1-3
- Corrected regression from 3.6.1-2 which prevented the loading of
  arbitrary p11-kit modules (#1507402)

* Mon Nov  6 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.6.1-2
- Prevent the loading of all PKCS#11 modules on certificate verification
  but only restrict to p11-kit trust module (#1507402)

* Sat Oct 21 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.6.1-1
- Update to upstream 3.6.1 release

* Mon Aug 21 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.6.0-1
- Update to upstream 3.6.0 release

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 04 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.5.14-1
- Update to upstream 3.5.14 release

* Wed Jun 07 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.5.13-1
- Update to upstream 3.5.13 release

* Thu May 11 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.5.12-2
- Fix issue with p11-kit-trust arch dependency

* Thu May 11 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.5.12-1
- Update to upstream 3.5.12 release

* Fri Apr 07 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.5.11-1
- Update to upstream 3.5.11 release

* Mon Mar 06 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.5.10-1
- Update to upstream 3.5.10 release

* Wed Feb 15 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.5.9-2
- Work around missing pkg-config file (#1422256)

* Tue Feb 14 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.5.9-1
- Update to upstream 3.5.9 release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Feb  4 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.5.8-2
- Added patch fix initialization issue in gnutls_pkcs11_obj_list_import_url4

* Mon Jan  9 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.5.8-1
- New upstream release

* Tue Dec 13 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.5.7-3
- Fix PKCS#8 file loading (#1404084)

* Thu Dec  8 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.5.7-1
- New upstream release

* Fri Nov  4 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.5.6-1
- New upstream release

* Tue Oct 11 2016 walters@redhat.com - 3.5.5-2
- Apply patch to fix compatibility with ostree (#1383708)

* Mon Oct 10 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.5.5-1
- New upstream release

* Thu Sep  8 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.5.4-1
- New upstream release

* Mon Aug 29 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.5.3-2
- Work around #1371082 for x86
- Fixed issue with DTLS sliding window implementation (#1370881)

* Tue Aug  9 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.5.3-1
- New upstream release

* Wed Jul  6 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.5.2-1
- New upstream release

* Wed Jun 15 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.5.1-1
- New upstream release

* Tue Jun  7 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.4.13-1
- New upstream release (#1343258)
- Addresses issue with setuid programs introduced in 3.4.12 (#1343342)

* Fri May 20 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.4.12-1
- New upstream release

* Mon Apr 11 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.4.11-1
- New upstream release

* Fri Mar  4 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.4.10-1
- New upstream release (#1314576)

* Wed Feb  3 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.4.9-1
- Fix broken key usage flags introduced in 3.4.8 (#1303355)

* Mon Jan 11 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.4.8-1
- New upstream release (#1297079)

* Mon Nov 23 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.4.7-1
- New upstream release (#1284300)
- Documentation updates (#1282864)
- Adds interface to set unique IDs in certificates (#1281343)
- Allow arbitrary key sizes with ARCFOUR (#1284401)

* Wed Oct 21 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.4.6-1
- New upstream release (#1273672)
- Enhances p11tool to write CKA_ISSUER and CKA_SERIAL_NUMBER (#1272178)

* Tue Oct 20 2015 Adam Williamson <awilliam@redhat.com> - 3.4.5-2
- fix interaction with Chrome 45+ (master secret extension) (#1273102)

* Mon Sep 14 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.4.5-1
- New upstream release (#1252192)
- Eliminates hard limits on CRL parsing of certtool.

* Mon Aug 10 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.4.4-1
- new upstream release
- no longer requires trousers patch
- fixes issue in gnutls_x509_privkey_import (#1250020)

* Mon Jul 13 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.4.3-2
- Don't link against trousers but rather dlopen() it when available.
  That avoids a dependency on openssl by the main library.

* Mon Jul 13 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.4.3-1
- new upstream release

* Thu Jul 02 2015 Adam Jackson <ajax@redhat.com> 3.4.2-3
- Only disable -z now for the guile modules

* Thu Jun 18 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.4.2-2
- rename the symbol version for internal symbols to avoid clashes
  with 3.3.x.

* Wed Jun 17 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.4.2-1
- new upstream release

* Tue May  5 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.4.1-2
- Provide missing GNUTLS_SUPPLEMENTAL_USER_MAPPING_DATA definition

* Mon May  4 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.4.1-1
- new upstream release

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.3.14-2
- Rebuilt for GCC 5 C++11 ABI change

* Mon Mar 30 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.14-1
- new upstream release
- improved BER decoding of PKCS #12 structures (#1131461)

* Fri Mar  6 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.13-3
- Build with hardened flags
- Removed -Wl,--no-add-needed linker flag

* Fri Feb 27 2015 Till Maas <opensource@till.name> - 3.3.13-2
- Do not build with hardened flags

* Thu Feb 26 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.13-1
- new upstream release

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 3.3.12-3
- Make build verbose
- Use %%license

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 3.3.12-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Jan 19 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.12-1
- new upstream release

* Mon Jan  5 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.11-2
- enabled guile bindings (#1177847)

* Thu Dec 11 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.11-1
- new upstream release

* Mon Nov 10 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.10-1
- new upstream release

* Thu Oct 23 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.9-2
- applied fix for issue in get-issuer (#1155901)

* Mon Oct 13 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.9-1
- new upstream release

* Fri Sep 19 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.8-2
- strip rpath from library

* Thu Sep 18 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.8-1
- new upstream release

* Mon Aug 25 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.7-1
- new upstream release

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 23 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.6-1
- new upstream release

* Tue Jul 01 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.5-2
- Added work-around for s390 builds with gcc 4.9 (#1102324)

* Mon Jun 30 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.5-1
- new upstream release

* Tue Jun 17 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.4-3
- explicitly depend on p11-kit-trust

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.4-1
- new upstream release

* Fri May 30 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.3-1
- new upstream release

* Wed May 21 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.2-2
- Require crypto-policies

* Fri May 09 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.2-1
- new upstream release

* Mon May 05 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.1-4
- Replaced /etc/crypto-profiles/apps with /etc/crypto-policies/back-ends.
- Added support for "very weak" profile.

* Mon Apr 28 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.1-2
- gnutls_global_deinit() will not do anything if the previous 
  initialization has failed (#1091053)

* Mon Apr 28 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.1-1
- new upstream release

* Mon Apr 14 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.0-1
- new upstream release

* Tue Apr 08 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.2.13-1
- new upstream release

* Wed Mar 05 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.2.12.1-1
- new upstream release

* Mon Mar 03 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.2.12-1
- new upstream release

* Mon Feb 03 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.2.10-2
- use p11-kit trust store for certificate verification

* Mon Feb 03 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.2.10-1
- new upstream release

* Tue Jan 14 2014 Tomáš Mráz <tmraz@redhat.com> 3.2.8-2
- build the crywrap tool

* Mon Dec 23 2013 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.2.8-1
- new upstream release

* Wed Dec  4 2013 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.2.7-2
- Use the correct root key for unbound /var/lib/unbound/root.key (#1012494)
- Pull asm fixes from upstream (#973210)

* Mon Nov 25 2013 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.2.7-1
- new upstream release
- added dependency to autogen-libopts-devel to use the system's
  libopts library
- added dependency to trousers-devel to enable TPM support

* Mon Nov  4 2013 Tomáš Mráz <tmraz@redhat.com> 3.1.16-1
- new upstream release
- fixes CVE-2013-4466 off-by-one in dane_query_tlsa()

* Fri Oct 25 2013 Tomáš Mráz <tmraz@redhat.com> 3.1.15-1
- new upstream release
- fixes CVE-2013-4466 buffer overflow in handling DANE entries

* Wed Oct 16 2013 Tomáš Mráz <tmraz@redhat.com> 3.1.13-3
- enable ECC NIST Suite B curves

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Tomáš Mráz <tmraz@redhat.com> 3.1.13-1
- new upstream release

* Mon May 13 2013 Tomáš Mráz <tmraz@redhat.com> 3.1.11-1
- new upstream release

* Mon Mar 25 2013 Tomas Mraz <tmraz@redhat.com> 3.1.10-1
- new upstream release
- license of the library is back to LGPLv2.1+

* Fri Mar 15 2013 Tomas Mraz <tmraz@redhat.com> 3.1.9-1
- new upstream release

* Thu Mar  7 2013 Tomas Mraz <tmraz@redhat.com> 3.1.8-3
- drop the temporary old library

* Tue Feb 26 2013 Tomas Mraz <tmraz@redhat.com> 3.1.8-2
- don't send ECC algos as supported (#913797)

* Thu Feb 21 2013 Tomas Mraz <tmraz@redhat.com> 3.1.8-1
- new upstream version

* Wed Feb  6 2013 Tomas Mraz <tmraz@redhat.com> 3.1.7-1
- new upstream version, requires rebuild of dependencies
- this release temporarily includes old compatibility .so

* Tue Feb  5 2013 Tomas Mraz <tmraz@redhat.com> 2.12.22-2
- rebuilt with new libtasn1
- make guile bindings optional - breaks i686 build and there is
  no dependent package

* Tue Jan  8 2013 Tomas Mraz <tmraz@redhat.com> 2.12.22-1
- new upstream version

* Wed Nov 28 2012 Tomas Mraz <tmraz@redhat.com> 2.12.21-2
- use RSA bit sizes supported by libgcrypt in FIPS mode for security
  levels (#879643)

* Fri Nov  9 2012 Tomas Mraz <tmraz@redhat.com> 2.12.21-1
- new upstream version

* Thu Nov  1 2012 Tomas Mraz <tmraz@redhat.com> 2.12.20-4
- negotiate only FIPS approved algorithms in the FIPS mode (#871826)

* Wed Aug  8 2012 Tomas Mraz <tmraz@redhat.com> 2.12.20-3
- fix the gnutls-cli-debug manpage - patch by Peter Schiffer

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 18 2012 Tomas Mraz <tmraz@redhat.com> 2.12.20-1
- new upstream version

* Fri May 18 2012 Tomas Mraz <tmraz@redhat.com> 2.12.19-1
- new upstream version

* Thu Mar 29 2012 Tomas Mraz <tmraz@redhat.com> 2.12.18-1
- new upstream version

* Thu Mar  8 2012 Tomas Mraz <tmraz@redhat.com> 2.12.17-1
- new upstream version
- fix leaks in key generation (#796302)

* Fri Feb 03 2012 Kevin Fenzi <kevin@scrye.com> - 2.12.14-3
- Disable largefile on arm arch. (#787287)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov  8 2011 Tomas Mraz <tmraz@redhat.com> 2.12.14-1
- new upstream version

* Mon Oct 24 2011 Tomas Mraz <tmraz@redhat.com> 2.12.12-1
- new upstream version

* Thu Sep 29 2011 Tomas Mraz <tmraz@redhat.com> 2.12.11-1
- new upstream version

* Fri Aug 26 2011 Tomas Mraz <tmraz@redhat.com> 2.12.9-1
- new upstream version

* Tue Aug 16 2011 Tomas Mraz <tmraz@redhat.com> 2.12.8-1
- new upstream version

* Mon Jul 25 2011 Tomas Mraz <tmraz@redhat.com> 2.12.7-2
- fix problem when using new libgcrypt
- split libgnutlsxx to a subpackage (#455146)
- drop libgnutls-openssl (#460310)

* Tue Jun 21 2011 Tomas Mraz <tmraz@redhat.com> 2.12.7-1
- new upstream version

* Mon May  9 2011 Tomas Mraz <tmraz@redhat.com> 2.12.4-1
- new upstream version

* Tue Apr 26 2011 Tomas Mraz <tmraz@redhat.com> 2.12.3-1
- new upstream version

* Mon Apr 18 2011 Tomas Mraz <tmraz@redhat.com> 2.12.2-1
- new upstream version

* Thu Mar  3 2011 Tomas Mraz <tmraz@redhat.com> 2.10.5-1
- new upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec  8 2010 Tomas Mraz <tmraz@redhat.com> 2.10.4-1
- new upstream version

* Thu Dec  2 2010 Tomas Mraz <tmraz@redhat.com> 2.10.3-2
- fix buffer overflow in gnutls-serv (#659259)

* Fri Nov 19 2010 Tomas Mraz <tmraz@redhat.com> 2.10.3-1
- new upstream version

* Thu Sep 30 2010 Tomas Mraz <tmraz@redhat.com> 2.10.2-1
- new upstream version

* Wed Sep 29 2010 jkeating - 2.10.1-4
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Tomas Mraz <tmraz@redhat.com> 2.10.1-3
- more patching for internal errors regression (#629858)
  patch by Vivek Dasmohapatra

* Tue Sep 21 2010 Tomas Mraz <tmraz@redhat.com> 2.10.1-2
- backported patch from upstream git hopefully fixing internal errors
  (#629858)

* Wed Aug  4 2010 Tomas Mraz <tmraz@redhat.com> 2.10.1-1
- new upstream version

* Wed Jun  2 2010 Tomas Mraz <tmraz@redhat.com> 2.8.6-2
- add support for safe renegotiation CVE-2009-3555 (#533125)

* Wed May 12 2010 Tomas Mraz <tmraz@redhat.com> 2.8.6-1
- upgrade to a new upstream version

* Mon Feb 15 2010 Rex Dieter <rdieter@fedoraproject.org> 2.8.5-4
- FTBFS gnutls-2.8.5-3.fc13: ImplicitDSOLinking (#564624)

* Thu Jan 28 2010 Tomas Mraz <tmraz@redhat.com> 2.8.5-3
- drop superfluous rpath from binaries
- do not call autoreconf during build
- specify the license on utils subpackage

* Mon Jan 18 2010 Tomas Mraz <tmraz@redhat.com> 2.8.5-2
- do not create static libraries (#556052)

* Mon Nov  2 2009 Tomas Mraz <tmraz@redhat.com> 2.8.5-1
- upgrade to a new upstream version

* Wed Sep 23 2009 Tomas Mraz <tmraz@redhat.com> 2.8.4-1
- upgrade to a new upstream version

* Fri Aug 14 2009 Tomas Mraz <tmraz@redhat.com> 2.8.3-1
- upgrade to a new upstream version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Tomas Mraz <tmraz@redhat.com> 2.8.1-1
- upgrade to a new upstream version

* Wed Jun  3 2009 Tomas Mraz <tmraz@redhat.com> 2.8.0-1
- upgrade to a new upstream version

* Mon May  4 2009 Tomas Mraz <tmraz@redhat.com> 2.6.6-1
- upgrade to a new upstream version - security fixes

* Tue Apr 14 2009 Tomas Mraz <tmraz@redhat.com> 2.6.5-1
- upgrade to a new upstream version, minor bugfixes only

* Fri Mar  6 2009 Tomas Mraz <tmraz@redhat.com> 2.6.4-1
- upgrade to a new upstream version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 15 2008 Tomas Mraz <tmraz@redhat.com> 2.6.3-1
- upgrade to a new upstream version

* Thu Dec  4 2008 Tomas Mraz <tmraz@redhat.com> 2.6.2-1
- upgrade to a new upstream version

* Tue Nov 11 2008 Tomas Mraz <tmraz@redhat.com> 2.4.2-3
- fix chain verification issue CVE-2008-4989 (#470079)

* Thu Sep 25 2008 Tomas Mraz <tmraz@redhat.com> 2.4.2-2
- add guile subpackage (#463735)
- force new libtool through autoreconf to drop unnecessary rpaths

* Tue Sep 23 2008 Tomas Mraz <tmraz@redhat.com> 2.4.2-1
- new upstream version

* Tue Jul  1 2008 Tomas Mraz <tmraz@redhat.com> 2.4.1-1
- new upstream version
- correct the license tag
- explicit --with-included-opencdk not needed
- use external lzo library, internal not included anymore

* Tue Jun 24 2008 Tomas Mraz <tmraz@redhat.com> 2.4.0-1
- upgrade to latest upstream

* Tue May 20 2008 Tomas Mraz <tmraz@redhat.com> 2.0.4-3
- fix three security issues in gnutls handshake - GNUTLS-SA-2008-1
  (#447461, #447462, #447463)

* Mon Feb  4 2008 Joe Orton <jorton@redhat.com> 2.0.4-2
- use system libtasn1

* Tue Dec  4 2007 Tomas Mraz <tmraz@redhat.com> 2.0.4-1
- upgrade to latest upstream

* Tue Aug 21 2007 Tomas Mraz <tmraz@redhat.com> 1.6.3-2
- license tag fix

* Wed Jun  6 2007 Tomas Mraz <tmraz@redhat.com> 1.6.3-1
- upgrade to latest upstream (#232445)

* Tue Apr 10 2007 Tomas Mraz <tmraz@redhat.com> 1.4.5-2
- properly require install-info (patch by Ville Skyttä)
- standard buildroot and use dist tag
- add COPYING and README to doc

* Wed Feb  7 2007 Tomas Mraz <tmraz@redhat.com> 1.4.5-1
- new upstream version
- drop libtermcap-devel from buildrequires

* Thu Sep 14 2006 Tomas Mraz <tmraz@redhat.com> 1.4.1-2
- detect forged signatures - CVE-2006-4790 (#206411), patch
  from upstream

* Tue Jul 18 2006 Tomas Mraz <tmraz@redhat.com> - 1.4.1-1
- upgrade to new upstream version, only minor changes

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.4.0-1.1
- rebuild

* Wed Jun 14 2006 Tomas Mraz <tmraz@redhat.com> - 1.4.0-1
- upgrade to new upstream version (#192070), rebuild
  of dependent packages required

* Tue May 16 2006 Tomas Mraz <tmraz@redhat.com> - 1.2.10-2
- added missing buildrequires

* Mon Feb 13 2006 Tomas Mraz <tmraz@redhat.com> - 1.2.10-1
- updated to new version (fixes CVE-2006-0645)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2.9-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.9-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan  3 2006 Jesse Keating <jkeating@redhat.com> 1.2.9-3
- rebuilt

* Fri Dec  9 2005 Tomas Mraz <tmraz@redhat.com> 1.2.9-2
- replaced *-config scripts with calls to pkg-config to
  solve multilib conflicts

* Wed Nov 23 2005 Tomas Mraz <tmraz@redhat.com> 1.2.9-1
- upgrade to newest upstream
- removed .la files (#172635)

* Sun Aug  7 2005 Tomas Mraz <tmraz@redhat.com> 1.2.6-1
- upgrade to newest upstream (rebuild of dependencies necessary)

* Mon Jul  4 2005 Tomas Mraz <tmraz@redhat.com> 1.0.25-2
- split the command line tools to utils subpackage

* Sat Apr 30 2005 Tomas Mraz <tmraz@redhat.com> 1.0.25-1
- new upstream version fixes potential DOS attack

* Sat Apr 23 2005 Tomas Mraz <tmraz@redhat.com> 1.0.24-2
- readd the version script dropped by upstream

* Fri Apr 22 2005 Tomas Mraz <tmraz@redhat.com> 1.0.24-1
- update to the latest upstream version on the 1.0 branch

* Wed Mar  2 2005 Warren Togami <wtogami@redhat.com> 1.0.20-6
- gcc4 rebuild

* Tue Jan  4 2005 Ivana Varekova <varekova@redhat.com> 1.0.20-5
- add gnutls Requires zlib-devel (#144069)

* Mon Nov 08 2004 Colin Walters <walters@redhat.com> 1.0.20-4
- Make gnutls-devel Require libgcrypt-devel

* Tue Sep 21 2004 Jeff Johnson <jbj@redhat.com> 1.0.20-3
- rebuild with release++, otherwise unchanged.

* Tue Sep  7 2004 Jeff Johnson <jbj@redhat.com> 1.0.20-2
- patent tainted SRP code removed.

* Sun Sep  5 2004 Jeff Johnson <jbj@redhat.com> 1.0.20-1
- update to 1.0.20.
- add --with-included-opencdk --with-included-libtasn1
- add --with-included-libcfg --with-included-lzo
- add --disable-srp-authentication.
- do "make check" after build.

* Fri Mar 21 2003 Jeff Johnson <jbj@redhat.com> 0.9.2-1
- upgrade to 0.9.2

* Tue Jun 25 2002 Jeff Johnson <jbj@redhat.com> 0.4.4-1
- update to 0.4.4.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sat May 25 2002 Jeff Johnson <jbj@redhat.com> 0.4.3-1
- update to 0.4.3.

* Tue May 21 2002 Jeff Johnson <jbj@redhat.com> 0.4.2-1
- update to 0.4.2.
- change license to LGPL.
- include splint annotations patch.

* Tue Apr  2 2002 Nalin Dahyabhai <nalin@redhat.com> 0.4.0-1
- update to 0.4.0

* Thu Jan 17 2002 Nalin Dahyabhai <nalin@redhat.com> 0.3.2-1
- update to 0.3.2

* Thu Jan 10 2002 Nalin Dahyabhai <nalin@redhat.com> 0.3.0-1
- add a URL

* Thu Dec 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- initial package

