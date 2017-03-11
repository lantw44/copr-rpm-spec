Name:           guile-ssh
Version:        0.10.2
Release:        2%{?dist}
Summary:        A library that provides access to the SSH protocol for GNU Guile

License:        GPLv3+
URL:            https://github.com/artyom-poptsov/guile-ssh
Source0:        https://github.com/artyom-poptsov/guile-ssh/archive/v%{version}.tar.gz

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
%dir %{_libdir}/guile/2.0/site-ccache/ssh
%{_libdir}/guile/2.0/site-ccache/ssh/*.go
%dir %{_libdir}/guile/2.0/site-ccache/ssh/dist
%{_libdir}/guile/2.0/site-ccache/ssh/dist/*.go
%{_libdir}/libguile-ssh.so*
%{_datadir}/%{name}
%dir %{_datadir}/guile/site/2.0/ssh
%{_datadir}/guile/site/2.0/ssh/*.scm
%dir %{_datadir}/guile/site/2.0/ssh/dist
%{_datadir}/guile/site/2.0/ssh/dist/*.scm
%{_infodir}/%{name}.info.gz
%exclude %{_infodir}/dir


%changelog
* Wed Mar 08 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.10.2-2
- Rebuilt for Fedora 26 and 27

* Sat Dec 31 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.10.2-1
- Initial packaging
