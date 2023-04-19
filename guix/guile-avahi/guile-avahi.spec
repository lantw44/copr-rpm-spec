Name:           guile-avahi
Version:        0.4.1
Release:        2%{?dist}
Summary:        Avahi bindings for GNU Guile

License:        LGPLv3+
URL:            https://www.nongnu.org/guile-avahi
Source0:        https://download.savannah.nongnu.org/releases/%{name}/%{name}-%{version}.tar.gz

%global guile_source_dir     %{_datadir}/guile/site/3.0
%global guile_ccache_dir     %{_libdir}/guile/3.0/site-ccache
%global guile_extensions_dir %{_libdir}/guile/3.0/extensions

BuildRequires:  gcc
BuildRequires:  autoconf, automake, libtool, texinfo, gettext-devel
BuildRequires:  pkgconfig(guile-3.0), pkgconfig(avahi-client), gmp-devel
Requires:       guile30
Requires(post): info
Requires(preun): info

%description
Guile-Avahi is a set of Avahi bindings for GNU Guile. It allows programmers to
use functionalities of the Avahi client library from Guile Scheme programs.


%prep
%autosetup -p1


%build
%configure \
    --disable-rpath \
    --disable-static \
    --with-guilemoduledir=%{guile_source_dir} \
    guile_snarf=%{_bindir}/guile-snarf3.0
%make_build


%check
%{__make} %{?_smp_mflags} check


%install
%make_install
rm %{buildroot}%{guile_extensions_dir}/guile-avahi-v-0.la


%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi


%files
%license COPYING COPYING.LESSER
%doc AUTHORS ChangeLog NEWS README THANKS
%{guile_source_dir}/avahi.scm
%{guile_ccache_dir}/avahi.go
%dir %{guile_source_dir}/avahi
%dir %{guile_ccache_dir}/avahi
%{guile_source_dir}/avahi/client.scm
%{guile_ccache_dir}/avahi/client.go
%dir %{guile_source_dir}/avahi/client
%dir %{guile_ccache_dir}/avahi/client
%{guile_source_dir}/avahi/client/lookup.scm
%{guile_ccache_dir}/avahi/client/lookup.go
%{guile_source_dir}/avahi/client/publish.scm
%{guile_ccache_dir}/avahi/client/publish.go
%{guile_extensions_dir}/guile-avahi-v-0.so*
%{_infodir}/%{name}.info.gz
%exclude %{_infodir}/dir


%changelog
* Wed Apr 19 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.4.1-2
- Rebuilt for Fedora 38 and 39

* Sun Feb 12 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.4.1-1
- Update to 0.4.1
- Switch to Guile 3.0

* Sat Oct 29 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.4-5
- Rebuilt for Fedora 37 and 38

* Thu Apr 28 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.4-4
- Rebuilt for Fedora 36 and 37

* Sat Sep 25 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.4-3
- Rebuilt for Fedora 35 and 36

* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.4-2
- Rebuilt for Fedora 34 and 35

* Mon Feb 15 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.4-1
- Initial packaging
