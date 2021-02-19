Name:           guile-avahi
Version:        0.4
Release:        1%{?dist}
Summary:        Avahi bindings for GNU Guile

License:        LGPLv3+
URL:            https://www.nongnu.org/guile-avahi
Source0:        https://download.savannah.nongnu.org/releases/%{name}/%{name}-%{version}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/2.2
%global guile_ccache_dir %{_libdir}/guile/2.2/site-ccache

BuildRequires:  gcc
BuildRequires:  autoconf, automake, libtool, texinfo, gettext-devel
BuildRequires:  pkgconfig(guile-2.2), pkgconfig(avahi-client), gmp-devel
Requires:       guile22
Requires(post): info
Requires(preun): info

%description
Guile-Avahi is a set of Avahi bindings for GNU Guile. It allows programmers to
use functionalities of the Avahi client library from Guile Scheme programs.


%prep
%autosetup -p1


%build
# Regenerate configure to allow using Guile < 3.
autoreconf -fiv
%configure \
    --disable-rpath \
    --disable-static \
    --with-guilemoduledir=%{guile_source_dir} \
    guile_snarf=%{_bindir}/guile-snarf2.2
%make_build


%check
%{__make} %{?_smp_mflags} check


%install
%make_install
rm %{buildroot}%{_libdir}/libguile-avahi-v-0.la


%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi


%files
%license COPYING COPYING.LESSER
%doc AUTHORS ChangeLog NEWS README THANKS
%{_libdir}/libguile-avahi-v-0.so*
%{guile_source_dir}/avahi.scm
%dir %{guile_source_dir}/avahi
%{guile_source_dir}/avahi/client.scm
%dir %{guile_source_dir}/avahi/client
%{guile_source_dir}/avahi/client/lookup.scm
%{guile_source_dir}/avahi/client/publish.scm
%{_infodir}/%{name}.info.gz
%exclude %{_infodir}/dir


%changelog
* Mon Feb 15 2021 Ting-Wei Lan <lantw44@gmail.com> - 0.4-1
- Initial packaging
