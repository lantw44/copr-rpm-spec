Name:           guile-ssh
Version:        0.17.0
Release:        1%{?dist}
Summary:        A library that provides access to the SSH protocol for GNU Guile

License:        GPLv3+
URL:            https://memory-heap.org/~avp/projects/guile-ssh
Source0:        https://github.com/artyom-poptsov/guile-ssh/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

Patch0:         guile-ssh-0.17.0-bool.patch
Patch1:         guile-ssh-0.17.0-dsa-1.patch
Patch2:         guile-ssh-0.17.0-dsa-2.patch
Patch3:         guile-ssh-0.17.0-dsa-3.patch
Patch4:         guile-ssh-0.17.0-dsa-4.patch

%global guile_source_dir %{_datadir}/guile/site/3.0
%global guile_ccache_dir %{_libdir}/guile/3.0/site-ccache

BuildRequires:  gcc
BuildRequires:  autoconf, automake, libtool, texinfo
BuildRequires:  pkgconfig(guile-3.0), pkgconfig(libssh)
Requires:       guile30
Requires(post): info
Requires(preun): info

%description
Guile-SSH is a library that provides access to the SSH protocol for programs
written in GNU Guile interpreter. It is built upon the libssh library.


%prep
%autosetup -p1


%build
autoreconf -fiv
%configure \
    --disable-rpath \
    --disable-static \
    guile_snarf=%{_bindir}/guile-snarf3.0
%make_build


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
* Sat Nov 02 2024 Ting-Wei Lan <lantw44@gmail.com> - 0.17.0-1
- Update to 0.17.0

* Wed Apr 19 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.16.3-1
- Update to 0.16.3

* Sun Feb 12 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.16.2-1
- Update to 0.16.2
- Switch to Guile 3.0

* Sat Oct 29 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.16.0-1
- Update to 0.16.0

* Thu Apr 28 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.15.1-1
- Update to 0.15.1

* Sat Sep 25 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.13.1-4
- Rebuilt for Fedora 35 and 36

* Mon Jun 14 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.13.1-3
- Fix sssh-ssshd.scm on Fedora 33 and later

* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.13.1-2
- Rebuilt for Fedora 34 and 35

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
