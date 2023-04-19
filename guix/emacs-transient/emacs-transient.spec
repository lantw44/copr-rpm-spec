%global pkg transient
%global pkgname Transient

Name:           emacs-%{pkg}
Version:        0.3.7
Release:        3%{?dist}
Summary:        Transient commands

License:        GPLv3+
URL:            https://magit.vc
Source0:        https://github.com/magit/transient/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  emacs, make, texinfo, texinfo-tex
Requires:       emacs(bin) >= %{_emacs_version}

%description
%{pkgname} is an add-on package for GNU Emacs. It implements a similar
abstraction involving a prefix command, infix arguments and suffix commands. We
could call this abstraction a “transient command”, but because it always
involves at least two commands (a prefix and a suffix) we prefer to call it
just a “transient”.


%prep
%autosetup -n transient-%{version} -p1


%build
%make_build


%install
mkdir -p %{buildroot}%{_emacs_sitelispdir} %{buildroot}%{_emacs_sitestartdir}
install -m 755 -d %{buildroot}%{_emacs_sitelispdir}/transient
install -m 644 lisp/transient.{el,elc} \
    %{buildroot}%{_emacs_sitelispdir}/transient/
install -m 644 lisp/transient-autoloads.el \
    %{buildroot}%{_emacs_sitelispdir}/transient/
ln -rs %{buildroot}%{_emacs_sitelispdir}/transient/transient-autoloads.el \
    %{buildroot}%{_emacs_sitestartdir}
mkdir -p %{buildroot}%{_infodir}
gzip -9 < docs/transient.info > %{buildroot}%{_infodir}/transient.info.gz


%post
/sbin/install-info %{_infodir}/transient.info.gz %{_infodir}/dir || :


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/transient.info.gz %{_infodir}/dir || :
fi


%files
%license LICENSE
%doc docs/CHANGELOG README.md
%doc docs/transient.html docs/transient.org docs/transient.pdf
%dir %{_emacs_sitelispdir}/transient
%{_emacs_sitelispdir}/transient/transient.el
%{_emacs_sitelispdir}/transient/transient.elc
%{_emacs_sitelispdir}/transient/transient-autoloads.el
%{_emacs_sitestartdir}/transient-autoloads.el
%{_infodir}/transient.info.gz


%changelog
* Wed Apr 19 2023 Ting-Wei Lan <lantw44@gmail.com> - 0.3.7-3
- Rebuilt for Fedora 38 and 39

* Sat Oct 29 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.3.7-2
- Rebuilt for Fedora 37 and 38

* Thu Apr 28 2022 Ting-Wei Lan <lantw44@gmail.com> - 0.3.7-1
- Initial packaging
