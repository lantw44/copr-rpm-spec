# This spec file is based on:
#  [1] https://github.com/PhantomX/chinforpms/blob/991712ffa984e7fa/lzlib/lzlib.spec

Name:           lzlib
Version:        1.11
Release:        2%{?dist}
Summary:        A compression library for the lzip file format

License:        GPLv2+
URL:            https://www.nongnu.org/lzip/%{name}.html
Source0:        https://download.savannah.gnu.org/releases/lzip/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  gcc


%description
Lzlib is a data compression library providing in-memory LZMA compression
and decompression functions, including integrity checking of the
decompressed data.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1


%build
%configure \
  --disable-static \
  --enable-shared \
  --disable-ldconfig \
  CFLAGS+='%{build_cflags}' \
  LDFLAGS='%{build_ldflags}'
%make_build


%install
%make_install



%files
%license COPYING COPYING.GPL
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/liblz.so.*
%{_infodir}/%{name}.info*
%exclude %{_infodir}/dir

%files devel
%{_includedir}/%{name}.h
%{_libdir}/liblz.so


%changelog
* Wed Sep 18 2019 Ting-Wei Lan <lantw44@gmail.com> - 1.11-2
- Use HTTPS links
- Use CFLAGS+= instead of CFLAGS=
- Use exclude macro to drop info dir file
- Don't use wildcards to specify the name of the library

* Fri May 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.11-1
- Initial spec
