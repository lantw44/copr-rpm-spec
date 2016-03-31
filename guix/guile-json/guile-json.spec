Name:           guile-json
Version:        0.5.0
Release:        1%{?dist}
Summary:        JSON module for Guile

License:        LGPLv3+
URL:            https://savannah.nongnu.org/projects/guile-json
Source0:        http://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  guile
Requires:       guile

%description
guile-json is a JSON module for Guile. It supports parsing and building JSON
documents according to the http://json.org specification. These are the main
features:

- Strictly complies to http://json.org specification.
- Build JSON documents programmatically via macros.
- Unicode support for strings.
- Allows JSON pretty printing.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


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
%{_datadir}/guile/site/json/syntax.go
%{_datadir}/guile/site/json/syntax.scm



%changelog
* Fri Apr 01 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.5.0-1
- Update to 0.5.0

* Thu Mar 03 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.4.0-2
- Rebuilt for Fedora 24 and 25

* Sat Nov 21 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.4.0-1
- Initial packaging
