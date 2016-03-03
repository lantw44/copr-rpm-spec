%global pkg with-editor
%global pkgname With-Editor

Name:           emacs-%{pkg}
Version:        2.5.0
Release:        1%{?dist}
Summary:        Use the Emacsclient as the editor of child processes

Group:          Applications/Editors
License:        GPLv3+
URL:            http://magit.vc
Source0:        https://github.com/magit/with-editor/archive/v%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  emacs, emacs-dash, texinfo
Requires:       emacs(bin) >= %{_emacs_version}
Requires:       emacs-dash

%description
%{pkgname} is an add-on package for GNU Emacs. It makes it easy to use the
Emacsclient as the editor of child processes, making sure they know how to
call home.


%prep
%setup -q -n with-editor-%{version}


%build
touch dir
make MAKEINFO='makeinfo --no-split' EFLAGS='-L %{_emacs_sitelispdir}/dash' all


%install
mkdir -p %{buildroot}%{_emacs_sitelispdir}
install -m 755 -d %{buildroot}%{_emacs_sitelispdir}/with-editor
install -m 644 with-editor.el \
    %{buildroot}%{_emacs_sitelispdir}/with-editor/
%{_emacs_bytecompile} %{buildroot}%{_emacs_sitelispdir}/with-editor/with-editor*.el
mkdir -p %{buildroot}%{_infodir}
gzip -9 < with-editor.info > %{buildroot}%{_infodir}/with-editor.info.gz


%post
/sbin/install-info %{_infodir}/with-editor.info.gz %{_infodir}/dir || :


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/with-editor.info.gz %{_infodir}/dir || :
fi


%files
%doc README.md
%dir %{_emacs_sitelispdir}/with-editor
%{_emacs_sitelispdir}/with-editor/with-editor.el
%{_emacs_sitelispdir}/with-editor/with-editor.elc
%{_infodir}/with-editor.info.gz



%changelog
* Fri Mar 04 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.5.0-1
- Initial packaging
