%global pkg graphql
%global pkgname GraphQL

Name:           emacs-%{pkg}
Version:        0.1.1
Release:        2%{?dist}
Summary:        Functions for interacting with GraphQL web services

License:        GPLv3+
URL:            https://github.com/vermiculus/graphql.el
Source0:        https://github.com/vermiculus/graphql.el/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  emacs

Requires:       emacs(bin) >= %{_emacs_version}

%description
%{pkgname} is an add-on package for GNU Emacs. It provides a set of generic
functions for interacting with GraphQL web services.


%prep
%autosetup -n graphql.el-%{version} -p1
rm examples.el


%build


%install
mkdir -p %{buildroot}%{_emacs_sitelispdir}
install -m 755 -d %{buildroot}%{_emacs_sitelispdir}/graphql
install -m 644 *.el %{buildroot}%{_emacs_sitelispdir}/graphql/
%{_emacs_bytecompile} %{buildroot}%{_emacs_sitelispdir}/graphql/*.el


%files
%doc README.md
%dir %{_emacs_sitelispdir}/graphql
%{_emacs_sitelispdir}/graphql/graphql.el
%{_emacs_sitelispdir}/graphql/graphql.elc


%changelog
* Wed May 01 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.1.1-2
- Rebuilt for Fedora 30 and 31

* Sun Dec 02 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.1.1-1
- Initial packaging
