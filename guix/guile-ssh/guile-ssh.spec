Name:           guile-ssh
Version:        0.11.1
Release:        1%{?dist}
Summary:        A library that provides access to the SSH protocol for GNU Guile

License:        GPLv3+
URL:            https://github.com/artyom-poptsov/guile-ssh
Source0:        https://github.com/artyom-poptsov/guile-ssh/archive/v%{version}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/2.0
%global guile_ccache_dir %{_libdir}/guile/2.0/site-ccache

BuildRequires:  autoconf, automake, libtool, texinfo
BuildRequires:  pkgconfig(guile-2.0), pkgconfig(libssh)
Requires:       guile
Requires(post): info
Requires(preun): info

%description
Guile-SSH is a library that provides access to the SSH protocol for programs
written in GNU Guile interpreter. It is built upon the libssh library.


%prep
%setup -q


%build
autoreconf -fi
%configure --disable-rpath --disable-static
make %{?_smp_mflags}


%check
# try a few more times before failing
for i in {1..24}; do
    make %{?_smp_mflags} check && exit 0
done
exit 1


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
* Thu May 25 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.11.1-1
- Update to 0.11.1
- Add a check section to run tests

* Wed Mar 08 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.10.2-2
- Rebuilt for Fedora 26 and 27

* Sat Dec 31 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.10.2-1
- Initial packaging
