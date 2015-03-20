Name:       yafu
Version:    1.34
Release:    2%{?dist}
Summary:    Automated integer factorization

Group:      Applications/Engineering
License:    Public Domain
URL:        https://sourceforge.net/projects/yafu
Source0:    https://downloads.sourceforge.net/project/yafu/%{version}/%{name}-%{version}-src.zip

BuildRequires: msieve, gmp-ecm-devel

%description
YAFU (with assistance from other free software) uses the most powerful modern
algorithms (and implementations of them) to factor input integers in a
completely automated way. The automation within YAFU is state-of-the-art,
combining factorization algorithms in an intelligent and adaptive methodology
that minimizes the time to find the factors of arbitrary input integers.
Most algorithm implementations are multi-threaded, allowing YAFU to fully
utilize multi- or many-core processors (including SNFS, GNFS, SIQS, and ECM).


%prep
%setup -qn %{name}-%{version}.3


%build
sed -i 's|-lmsieve|-lmsieve -lz|' Makefile

%ifarch x86_64
make %{?_smp_mflags} x86_64 NFS=1 USE_SSE41=1
%else
false
%endif


%install
mkdir -p %{buildroot}%{_bindir}
install -m 755 yafu %{buildroot}%{_bindir}


%files
%{_bindir}/yafu
%doc CHANGES docfile.txt README yafu.ini



%changelog
* Fri Mar 20 2015 Ting-Wei Lan <lantw44@gmail.com> - 1.34-2
- Rebuilt for Fedora 22 and 23
- Use HTTPS to download the source

* Thu Dec 25 2014 Ting-Wei Lan <lantw44@gmail.com> - 1.34-1
- Initial packaging
