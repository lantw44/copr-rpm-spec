%global pkg edit-indirect
%global pkgname edit-indirect

Name:           emacs-%{pkg}
Version:        0.1.5
Release:        1%{?dist}
Summary:        Edit regions in separate buffers

License:        BSD
URL:            https://github.com/Fanael/edit-indirect
Source0:        https://github.com/Fanael/edit-indirect/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  emacs

Requires:       emacs(bin) >= %{_emacs_version}

%description
%{pkgname} is an add-on package for GNU Emacs. It allows editing regions in
%separate buffers.


%prep
%autosetup -n edit-indirect-%{version} -p1


%build


%install
mkdir -p %{buildroot}%{_emacs_sitelispdir}
install -m 755 -d %{buildroot}%{_emacs_sitelispdir}/edit-indirect
install -m 644 *.el %{buildroot}%{_emacs_sitelispdir}/edit-indirect/
%{_emacs_bytecompile} %{buildroot}%{_emacs_sitelispdir}/edit-indirect/*.el


%files
%dir %{_emacs_sitelispdir}/edit-indirect
%{_emacs_sitelispdir}/edit-indirect/edit-indirect.el
%{_emacs_sitelispdir}/edit-indirect/edit-indirect.elc


%changelog
* Thu May 16 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.1.5-1
- Initial packaging
