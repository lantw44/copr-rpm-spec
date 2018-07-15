%global debug_package %{nil}

Name:           guile-json
Version:        1.0.1
Release:        1%{?dist}
Summary:        JSON module for Guile

License:        LGPLv3+
URL:            https://savannah.nongnu.org/projects/guile-json
Source0:        https://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  guile
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
%license COPYING COPYING.LESSER
%doc AUTHORS ChangeLog NEWS README
%{_datadir}/guile/site/json.scm
%{_datadir}/guile/site/json.go
%dir %{_datadir}/guile/site/json
%{_datadir}/guile/site/json/builder.go
%{_datadir}/guile/site/json/builder.scm
%{_datadir}/guile/site/json/parser.go
%{_datadir}/guile/site/json/parser.scm



%changelog
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
