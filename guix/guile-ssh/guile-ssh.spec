Name:           guile-ssh
Version:        0.13.1
Release:        1%{?dist}
Summary:        A library that provides access to the SSH protocol for GNU Guile

License:        GPLv3+
URL:            https://github.com/artyom-poptsov/guile-ssh
Source0:        https://github.com/artyom-poptsov/guile-ssh/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/2.2
%global guile_ccache_dir %{_libdir}/guile/2.2/site-ccache

BuildRequires:  gcc
BuildRequires:  autoconf, automake, libtool, texinfo
BuildRequires:  pkgconfig(guile-2.2), pkgconfig(libssh)
Requires:       guile22
Requires(post): info
Requires(preun): info

%description
Guile-SSH is a library that provides access to the SSH protocol for programs
written in GNU Guile interpreter. It is built upon the libssh library.


%prep
%autosetup -p1
%if 0%{?fedora} >= 33
# This test fails with the crypto policy of Fedora 33.
# https://github.com/artyom-poptsov/guile-ssh/issues/26
sed -i '/^	sssh-ssshd\.scm \\$/d' tests/Makefile.am
%endif


%build
autoreconf -fiv
%configure \
    --disable-rpath \
    --disable-static \
    GUILE=%{_bindir}/guile2.2 \
    GUILD=%{_bindir}/guild2.2
%make_build \
    GUILE_SNARF=%{_bindir}/guile-snarf2.2


%check
%{__make} %{?_smp_mflags} check


%install
%make_install
rm %{buildroot}%{_libdir}/libguile-ssh.la


%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi


%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_bindir}/sssh.scm
%{_bindir}/ssshd.scm
%{_libdir}/libguile-ssh.so*
%dir %{guile_source_dir}/ssh
%dir %{guile_ccache_dir}/ssh
%{guile_source_dir}/ssh/*.scm
%{guile_ccache_dir}/ssh/*.go
%dir %{guile_source_dir}/ssh/dist
%dir %{guile_ccache_dir}/ssh/dist
%{guile_source_dir}/ssh/dist/*.scm
%{guile_ccache_dir}/ssh/dist/*.go
%{_datadir}/%{name}
%{_infodir}/%{name}.info.gz
%exclude %{_infodir}/dir


%changelog
* Sun Nov  1 2020 Ting-Wei Lan <lantw44@gmail.com> - 0.13.1-1
- Update to 0.13.1

* Sun Apr 26 2020 Ting-Wei Lan <lantw44@gmail.com> - 0.12.0-1
- Update to 0.12.0

* Fri Sep 20 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.11.3-6
- Fix build with libssh 0.8

* Tue Sep 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.11.3-5
- Fix get-key-type test on libssh 0.9

* Fri May 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.11.3-4
- Switch to Guile 2.2

* Wed May 01 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.11.3-3
- Rebuilt for Fedora 30 and 31

* Tue Oct 23 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.11.3-2
- Add GCC to BuildRequires for Fedora 29 and later
- Disable tests broken on libssh 0.8

* Sat Jul 07 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.11.3-1
- Update to 0.11.3

* Mon Dec 11 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.11.2-3
- Use autosetup and make_build macros
- Rename the source tarball

* Mon Oct 16 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.11.2-2
- Rebuilt for Fedora 27 and 28

* Mon Jul 03 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.11.2-1
- Update to 0.11.2

* Sun May 28 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.11.1-2
- Disable session.scm test for libssh 0.7.5

* Thu May 25 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.11.1-1
- Update to 0.11.1
- Add a check section to run tests

* Wed Mar 08 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.10.2-2
- Rebuilt for Fedora 26 and 27

* Sat Dec 31 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.10.2-1
- Initial packaging
