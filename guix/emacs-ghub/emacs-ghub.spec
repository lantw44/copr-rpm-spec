%global pkg ghub
%global pkgname Ghub

Name:           emacs-%{pkg}
Version:        3.5.6
Release:        3%{?dist}
Summary:        Minuscule client libraries for the APIs of various Git forges

License:        GPLv3+
URL:            https://magit.vc
Source0:        https://github.com/magit/ghub/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  emacs, make, texinfo, texinfo-tex
BuildRequires:  emacs-treepy
Requires:       emacs(bin) >= %{_emacs_version}
Requires:       emacs-treepy
Recommends:     git

%description
%{pkgname} is an add-on package for GNU Emacs. It provides basic support for
using the APIs of various Git forges from Emacs packages. Originally it only
supported the Github REST API, but now it also supports the Github GraphQL API
as well as the REST APIs of Gitlab, Gitea, Gogs and Bitbucket.


%prep
%autosetup -n ghub-%{version} -p1


%build
%make_build LOAD_PATH='-L . -L %{_emacs_sitelispdir}/treepy'


%install
mkdir -p %{buildroot}%{_emacs_sitelispdir} %{buildroot}%{_emacs_sitestartdir}
install -m 755 -d %{buildroot}%{_emacs_sitelispdir}/ghub
for filename in buck ghub{,-graphql} glab gogs gsexp gtea; do
    for suffix in el elc; do
        install -m 644 "lisp/${filename}.${suffix}" \
            %{buildroot}%{_emacs_sitelispdir}/ghub/
    done
done
install -m 644 lisp/ghub-autoloads.el %{buildroot}%{_emacs_sitelispdir}/ghub/
ln -rs %{buildroot}%{_emacs_sitelispdir}/ghub/ghub-autoloads.el \
    %{buildroot}%{_emacs_sitestartdir}
mkdir -p %{buildroot}%{_infodir}
gzip -9 < docs/ghub.info > %{buildroot}%{_infodir}/ghub.info.gz


%post
/sbin/install-info %{_infodir}/ghub.info.gz %{_infodir}/dir || :


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/ghub.info.gz %{_infodir}/dir || :
fi


%files
%license LICENSE
%doc CHANGELOG README.md
%doc docs/ghub.html docs/ghub.org docs/ghub.pdf
%dir %{_emacs_sitelispdir}/ghub
%{_emacs_sitelispdir}/ghub/buck.el
%{_emacs_sitelispdir}/ghub/buck.elc
%{_emacs_sitelispdir}/ghub/ghub.el
%{_emacs_sitelispdir}/ghub/ghub.elc
%{_emacs_sitelispdir}/ghub/ghub-graphql.el
%{_emacs_sitelispdir}/ghub/ghub-graphql.elc
%{_emacs_sitelispdir}/ghub/glab.el
%{_emacs_sitelispdir}/ghub/glab.elc
%{_emacs_sitelispdir}/ghub/gogs.el
%{_emacs_sitelispdir}/ghub/gogs.elc
%{_emacs_sitelispdir}/ghub/gsexp.el
%{_emacs_sitelispdir}/ghub/gsexp.elc
%{_emacs_sitelispdir}/ghub/gtea.el
%{_emacs_sitelispdir}/ghub/gtea.elc
%{_emacs_sitelispdir}/ghub/ghub-autoloads.el
%{_emacs_sitestartdir}/ghub-autoloads.el
%{_infodir}/ghub.info.gz


%changelog
* Wed Apr 19 2023 Ting-Wei Lan <lantw44@gmail.com> - 3.5.6-3
- Rebuilt for Fedora 38 and 39

* Sat Oct 29 2022 Ting-Wei Lan <lantw44@gmail.com> - 3.5.6-2
- Rebuilt for Fedora 37 and 38

* Thu Apr 28 2022 Ting-Wei Lan <lantw44@gmail.com> - 3.5.6-1
- Update to 3.5.6

* Sat Sep 25 2021 Ting-Wei Lan <lantw44@gmail.com> - 3.5.3-2
- Rebuilt for Fedora 35 and 36

* Mon Jun 14 2021 Ting-Wei Lan <lantw44@gmail.com> - 3.5.3-1
- Update to 3.5.3

* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 3.5.1-2
- Rebuilt for Fedora 34 and 35

* Mon Feb 15 2021 Ting-Wei Lan <lantw44@gmail.com> - 3.5.1-1
- Update to 3.5.1

* Sun Nov  1 2020 Ting-Wei Lan <lantw44@gmail.com> - 3.4.2-1
- Update to 3.4.2

* Sun Apr 26 2020 Ting-Wei Lan <lantw44@gmail.com> - 3.3.0-1
- Update to 3.3.0

* Tue Sep 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 3.2.0-3
- Rebuilt for Fedora 31 and 32

* Wed May 15 2019 Ting-Wei Lan <lantw44@gmail.com> - 3.2.0-2
- Add CHANGELOG to doc
- Update description from upstream README

* Thu May 02 2019 Ting-Wei Lan <lantw44@gmail.com> - 3.2.0-1
- Update to 3.2.0

* Sun Dec 02 2018 Ting-Wei Lan <lantw44@gmail.com> - 3.0.0-1
- Update to 3.0.0

* Tue Oct 23 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.0.1-2
- Rebuilt for Fedora 29 and 30

* Sat Jul 07 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.0.1-1
- Update to 2.0.1
- Fix autoloads by creating a symlink instead of moving the script itself

* Tue Mar 13 2018 Ting-Wei Lan <lantw44@gmail.com> - 1.3.1-0.1.20180312git11c07da
- Initial packaging
