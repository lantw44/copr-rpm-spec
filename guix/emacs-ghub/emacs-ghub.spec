%global pkg ghub
%global pkgname Ghub
%global commit 11c07daf7abcaf2d4cc2a5f007772506202c6d1f
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           emacs-%{pkg}
Version:        1.3.1
Release:        0.1.20180312git%{shortcommit}%{?dist}
Summary:        Minuscule GitHub client library for Emacs

License:        GPLv3+
URL:            https://magit.vc
Source0:        https://github.com/magit/ghub/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildArch:      noarch
BuildRequires:  emacs, texinfo
Requires:       emacs(bin) >= %{_emacs_version}
Recommends:     git

%description
%{pkgname} is an add-on package for GNU Emacs. It provides basic support for
using the Github REST (v3) and GraphQL (v4) APIs from Emacs packages.


%prep
%autosetup -n ghub-%{commit} -p1


%build
%make_build


%install
mkdir -p %{buildroot}%{_emacs_sitelispdir} %{buildroot}%{_emacs_sitestartdir}
install -m 755 -d %{buildroot}%{_emacs_sitelispdir}/ghub
install -m 644 ghub.el ghub.elc %{buildroot}%{_emacs_sitelispdir}/ghub/
install -m 644 ghub-autoloads.el %{buildroot}%{_emacs_sitestartdir}/ghub.el
mkdir -p %{buildroot}%{_infodir}
gzip -9 < ghub.info > %{buildroot}%{_infodir}/ghub.info.gz


%post
/sbin/install-info %{_infodir}/ghub.info.gz %{_infodir}/dir || :


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/ghub.info.gz %{_infodir}/dir || :
fi


%files
%doc README.md ghub.org
%dir %{_emacs_sitelispdir}/ghub
%{_emacs_sitelispdir}/ghub/ghub.el
%{_emacs_sitelispdir}/ghub/ghub.elc
%{_emacs_sitestartdir}/ghub.el
%{_infodir}/ghub.info.gz



%changelog
* Tue Mar 13 2018 Ting-Wei Lan <lantw44@gmail.com> - 1.3.1-0.1.20180312git11c07da
- Initial packaging
