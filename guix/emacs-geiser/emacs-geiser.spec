%global pkg geiser
%global pkgname Geiser

Name:       emacs-%{pkg} 
Version:    0.7
Release:    1%{?dist}
Summary:    Geiser is an Emacs environment to hack and have fun in Scheme.

License:    BSD
URL:        http://nongnu.org/geiser
Source0:    http://download.sv.gnu.org/releases/geiser/%{version}/%{pkg}-%{version}.tar.gz

BuildArch:  noarch
BuildRequires: emacs
Requires:   guile >= 2.0.9
Requires(post):  /sbin/install-info
Requires(preun): /sbin/install-info

%description
%{pkgname} is an add-on package for GNU Emacs. It is a collection of Emacs
major and minor modes that conspire with one or more Scheme interpreters to
keep the Lisp Machine Spirit alive. 

%package el
Summary:    Source for Geiser
Requires:   %{name} = %{version}-%{release}
BuildArch:  noarch

%description el
Source package for %{pkgname}.


%prep
%setup -q -n %{pkg}-%{version}


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%post
/sbin/install-info %{_infodir}/geiser.info.gz %{_infodir}/dir || :


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/geiser.info.gz %{_infodir}/dir || :
fi



%files
%doc AUTHORS ChangeLog COPYING NEWS README THANKS
%{_bindir}/geiser-racket
%{_infodir}/geiser.info.gz
%{_datadir}/geiser/chicken/geiser/emacs.scm
%{_datadir}/geiser/guile/geiser/xref.scm
%{_datadir}/geiser/guile/geiser/utils.scm
%{_datadir}/geiser/guile/geiser/modules.scm
%{_datadir}/geiser/guile/geiser/evaluation.scm
%{_datadir}/geiser/guile/geiser/emacs.scm
%{_datadir}/geiser/guile/geiser/doc.scm
%{_datadir}/geiser/guile/geiser/completion.scm
%{_datadir}/geiser/racket/geiser/utils.rkt
%{_datadir}/geiser/racket/geiser/user.rkt
%{_datadir}/geiser/racket/geiser/startup.rkt
%{_datadir}/geiser/racket/geiser/server.rkt
%{_datadir}/geiser/racket/geiser/modules.rkt
%{_datadir}/geiser/racket/geiser/main.rkt
%{_datadir}/geiser/racket/geiser/locations.rkt
%{_datadir}/geiser/racket/geiser/images.rkt
%{_datadir}/geiser/racket/geiser/eval.rkt
%{_datadir}/geiser/racket/geiser/enter.rkt
%{_datadir}/geiser/racket/geiser/completions.rkt
%{_datadir}/geiser/racket/geiser/autodoc.rkt
%{_emacs_sitelispdir}/geiser.elc
%{_emacs_sitelispdir}/geiser-*.elc
%exclude %{_infodir}/dir


%files el
%{_emacs_sitelispdir}/geiser.el
%{_emacs_sitelispdir}/geiser-*.el



%changelog
* Fri Mar 20 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.7-1
- Rebuilt for Fedora 22 and 23
- Update to 0.7

* Sat Nov 22 2014 Ting-Wei Lan <lantw44@gmail.com> - 0.6-1
- Initial packaging
