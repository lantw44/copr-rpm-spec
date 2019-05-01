%global debug_package %{nil}

Name:           guile-json
Version:        1.3.2
Release:        2%{?dist}
Summary:        JSON module for Guile

License:        GPLv3+
URL:            https://savannah.nongnu.org/projects/guile-json
Source0:        https://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.tar.gz

%global guile_source_dir %{_datadir}/guile/site/2.0
%global guile_ccache_dir %{_libdir}/guile/2.0/site-ccache

BuildRequires:  pkgconfig(guile-2.0)
Requires:       guile

%description
guile-json is a JSON module for Guile. It supports parsing and building JSON
documents according to the https://json.org specification. These are the main
features:

- Strictly complies to https://json.org specification.
- Build JSON documents programmatically via macros.
- Unicode support for strings.
- Allows JSON pretty printing.


%prep
%autosetup -p1


%build
%configure
%make_build


%install
%make_install


%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{guile_source_dir}/json.scm
%{guile_ccache_dir}/json.go
%dir %{guile_source_dir}/json
%dir %{guile_ccache_dir}/json
%{guile_source_dir}/json/builder.scm
%{guile_ccache_dir}/json/builder.go
%{guile_source_dir}/json/parser.scm
%{guile_ccache_dir}/json/parser.go



%changelog
* Wed May 01 2019 Ting-Wei Lan <lantw44@gmail.com> - 1.3.2-2
- Rebuilt for Fedora 30 and 31

* Mon Dec 03 2018 Ting-Wei Lan <lantw44@gmail.com> - 1.3.2-1
- Update to 1.3.2

* Tue Oct 23 2018 Ting-Wei Lan <lantw44@gmail.com> - 1.0.1-2
- Rebuilt for Fedora 29 and 30

* Sat Jul 07 2018 Ting-Wei Lan <lantw44@gmail.com> - 1.0.1-1
- Update to 1.0.1

* Mon Dec 11 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.6.0-5
- Use autosetup and make_build macros
- Use HTTPS links in description

* Sun Dec 10 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.6.0-4
- Remove noarch because .go files are not architecture-independent

* Sat Dec 09 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.6.0-3
- Use HTTPS to download the source

* Mon Oct 16 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.6.0-2
- Rebuilt for Fedora 27 and 28

* Wed Mar 08 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.6.0-1
- Update to 0.6.0

* Sat Sep 10 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.5.0-2
- Rebuilt for Fedora 25 and 26

* Fri Apr 01 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.5.0-1
- Update to 0.5.0

* Thu Mar 03 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.4.0-2
- Rebuilt for Fedora 24 and 25

* Sat Nov 21 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.4.0-1
- Initial packaging
