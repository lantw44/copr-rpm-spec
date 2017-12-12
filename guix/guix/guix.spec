# Bootstrap binaries provided by guix don't have build IDs
%global _missing_build_ids_terminate_build 0

Name:           guix
Version:        0.14.0
Release:        5%{?dist}
Summary:        A purely functional package manager for the GNU system

License:        GPLv3+
URL:            https://www.gnu.org/software/guix
Source0:        https://alpha.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
Source1:        https://alpha.gnu.org/gnu/guix/bootstrap/aarch64-linux/20170217/guile-2.0.14.tar.xz#/aarch64-linux-20170217-guile-2.0.14.tar.xz
Source2:        https://alpha.gnu.org/gnu/guix/bootstrap/armhf-linux/20150101/guile-2.0.11.tar.xz#/armhf-linux-20150101-guile-2.0.11.tar.xz
Source3:        https://alpha.gnu.org/gnu/guix/bootstrap/i686-linux/20131110/guile-2.0.9.tar.xz#/i686-linux-20131110-guile-2.0.9.tar.xz
Source4:        https://alpha.gnu.org/gnu/guix/bootstrap/mips64el-linux/20131110/guile-2.0.9.tar.xz#/mips64el-linux-20131110-guile-2.0.9.tar.xz
Source5:        https://alpha.gnu.org/gnu/guix/bootstrap/x86_64-linux/20131110/guile-2.0.9.tar.xz#/x86_64-linux-20131110-guile-2.0.9.tar.xz
Patch0:         guix-fix-cond-expand-for-guile-2.0.patch

%global guix_user         guixbuild
%global guix_group        guixbuild
%global completionsdir    %(pkg-config --variable=completionsdir bash-completion)
%global guile_source_dir  %{_datadir}/guile/site/2.0
%global guile_ccache_dir  %{_libdir}/guile/2.0/site-ccache
%global guix_profile_root %{_localstatedir}/guix/profiles/per-user/root/guix-profile

BuildRequires:  pkgconfig(guile-2.0)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  zlib-devel, bzip2-devel, libgcrypt-devel
BuildRequires:  gettext, help2man, graphviz
BuildRequires:  bash-completion
BuildRequires:  guile-git, guile-json, guile-ssh, gnutls-guile
BuildRequires:  systemd

%{?systemd_requires}

Requires:       guile-git, gzip, bzip2, xz
Requires:       %{_bindir}/dot
Requires:       %{_libdir}/libgcrypt.so
Requires(post): /usr/sbin/useradd
Requires(post): /usr/sbin/usermod
Requires(post): /usr/sbin/groupadd
Requires(post): /usr/sbin/groupmod
Requires(post): /usr/bin/gpasswd
Requires(post): info
Requires(preun): info

Recommends:     guile-json, guile-ssh, gnutls-guile
Suggests:       emacs-guix

%description
GNU Guix is a purely functional package manager for the GNU system. In addition
to standard package management features, Guix supports transactional upgrades
and roll-backs, unprivileged package management, per-user profiles, and garbage
collection. It provides Guile Scheme APIs, including high-level embedded
domain-specific languages (EDSLs), to describe how packages are to be built and
composed.


%prep
%autosetup -p1
echo '3939909f24dcb955621aa7f81ecde6844bea8a083969c2d275c55699af123ebe  %{SOURCE1}' | sha256sum -c
echo 'e551d05d4d385d6706ab8d574856a087758294dc90ab4c06e70a157a685e23d6  %{SOURCE2}' | sha256sum -c
echo 'b757cd46bf13ecac83fb8e955fb50096ac2d17bb610ca8eb816f29302a00a846  %{SOURCE3}' | sha256sum -c
echo '994680f0001346864aa2c2cc5110f380ee7518dcd701c614291682b8e948f73b  %{SOURCE4}' | sha256sum -c
echo '037b103522a2d0d7d69c7ffd8de683dfe5bb4b59c1fafd70b4ffd397fd2f57f0  %{SOURCE5}' | sha256sum -c
cp %{SOURCE1} gnu/packages/bootstrap/aarch64-linux/guile-2.0.14.tar.xz
cp %{SOURCE2} gnu/packages/bootstrap/armhf-linux/guile-2.0.11.tar.xz
cp %{SOURCE3} gnu/packages/bootstrap/i686-linux/guile-2.0.9.tar.xz
cp %{SOURCE4} gnu/packages/bootstrap/mips64el-linux/guile-2.0.9.tar.xz
cp %{SOURCE5} gnu/packages/bootstrap/x86_64-linux/guile-2.0.9.tar.xz


%build
%configure --disable-rpath --with-bash-completion-dir=%{completionsdir} \
    GUILE=%{_bindir}/guile GUILD=%{_bindir}/guild
%make_build


%check
# user namespace may be unsupported
if ! unshare -Ur true; then
    sed -i 's|tests/syscalls.scm||' Makefile
    sed -i 's|tests/containers.scm||' Makefile
    sed -i 's|tests/guix-environment-container.sh||' Makefile
fi
# don't run tests as root
if [ "$(id -u)" = "0" ]; then
    if [ "%{_topdir}" = "/builddir/build" ]; then
        chown -R nobody:nobody %{_topdir}
        setfacl -m u:nobody:x /builddir
    fi
    runuser nobody -s /bin/sh -c "%{__make} %{?_smp_mflags} check" && exit 0
else
    %{__make} %{?_smp_mflags} check && exit 0
fi


%install
%make_install systemdservicedir=%{_unitdir}
# rename systemd service files provided by upstream
mv %{buildroot}%{_unitdir}/guix-daemon{,-latest}.service
mv %{buildroot}%{_unitdir}/guix-publish{,-latest}.service
# generate default systemd service files from upstream ones
sed -e 's|^ExecStart=%{guix_profile_root}/bin|ExecStart=%{_bindir}|' \
    -e 's|^Description=\(.*\)|Description=\1 (default)|' \
    -e '/^Environment=/d' %{buildroot}%{_unitdir}/guix-daemon-latest.service \
    > %{buildroot}%{_unitdir}/guix-daemon.service
sed -e 's|^ExecStart=%{guix_profile_root}/bin|ExecStart=%{_bindir}|' \
    -e 's|^Description=\(.*\)|Description=\1 (default)|' \
    -e '/^Environment=/d' %{buildroot}%{_unitdir}/guix-publish-latest.service \
    > %{buildroot}%{_unitdir}/guix-publish.service
# generated files must be different from upstream ones
! cmp %{buildroot}%{_unitdir}/guix-daemon{,-latest}.service
! cmp %{buildroot}%{_unitdir}/guix-publish{,-latest}.service
# edit the description of upstream systemd service files
sed -i 's|^Description=\(.*\)|Description=\1 (upstream)|' \
    %{buildroot}%{_unitdir}/guix-daemon-latest.service \
    %{buildroot}%{_unitdir}/guix-publish-latest.service
# drop useless upstart service files
rm %{buildroot}%{_libdir}/upstart/system/guix-daemon.conf
rm %{buildroot}%{_libdir}/upstart/system/guix-publish.conf
rmdir %{buildroot}%{_libdir}/upstart/system
rmdir %{buildroot}%{_libdir}/upstart
# own the configuration directory
mkdir -p %{buildroot}%{_sysconfdir}/guix
%find_lang guix
%find_lang guix-packages


%post
cat << EOF | ( cd "%{guile_source_dir}/gnu/packages/bootstrap" && sha256sum -c >/dev/null ) || exit 1
e3bf6ffe357eebcc28221ffdbb5b00b4ed1237cb101aba4b1b8119b08c732387  aarch64-linux/bash
444c2af9fefd11d4fc20ee9281fa2c46cbe3cfb3df89cc30bcd50d20cdb6d6c0  aarch64-linux/mkdir
05273f978a072269193e3a09371c23d6d149f6d807f8e413a4f79aa5a1bb6f25  aarch64-linux/tar
48e9baa8a6c2527a5b4ecb8f0ac87767e2b055979256acab2a3dbff4f6171637  aarch64-linux/xz
2ad82bb9ee6e77eaff284222e1d43a2829b5a1e2bcf158b08564a26da48e0045  armhf-linux/bash
a19e386b31ebc8a46b5f934c11bca86e28f8aa997272a5fcd052b52d5019f790  armhf-linux/mkdir
da56be0b332fac3880b151abe60c1eeb2649cd192379b18658b1d872f7aa53e8  armhf-linux/tar
6507d04d55210e3a8cdc2e5758d79a4b0da3cb53bb142f60a78788af7b915ab1  armhf-linux/xz
ed059a9ae964d538605c923c4e73128bd5ca912994709b3fe2d71d061751e8c5  i686-linux/bash
b369264bda7bbb98d1acf0bf53ebc9077e82f48b190f3956fa23cb73d6e99f92  i686-linux/mkdir
9f7e79e52aa369fc9ed69359e503d4f8179117842df8261fc0cae5629cc896cb  i686-linux/tar
d23173dfe66c41e1c8d8eef905d14d1f39aaa52c9d70621f366c275e9139b415  i686-linux/xz
213cfb8794ffdf4a71cb321a89987ee61704edcec5d1203912575f0a626a239c  mips64el-linux/bash
d436070fde044366d72d7e59d8d12b1ba72b32d7b0f13e409b61118bdc8254c8  mips64el-linux/mkdir
d27fcb52f9b4a42fafdae3164fffd200f52e04d142574dcf06212dbf7701cbb8  mips64el-linux/tar
107eac7523b0148d18f461d81bec9d0db6154d6c61e4caf3a4cdb43a9a6afb3c  mips64el-linux/xz
265d2f633a5ab35747fc4836b5e3ca32bf56ad44cc24f3bd358f1ff6cf0779a5  x86_64-linux/bash
50689abdf2d5374e17ea8c51801f04f7590ad604af33a12a940cc11d137a4a2f  x86_64-linux/mkdir
16440b4495a2ff9c6aa50c05a8c9066e1004a5990b75aa891f08cdf8753c8689  x86_64-linux/tar
930ad7e88ca0b2275dc459b24aea912fadd5b7c9e95be06788d4b61efc7ef470  x86_64-linux/xz
EOF
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
if [ "$1" = 1 ]; then
    /usr/sbin/groupadd -r %{guix_group}
    /usr/sbin/useradd -r -M -N -g %{guix_group} -d /var/empty -s /sbin/nologin \
        -c "Guix build user" %{guix_user}
    /usr/bin/gpasswd -a %{guix_user} %{guix_group} >/dev/null
elif [ "$1" -gt 1 ]; then
    /usr/sbin/groupmod -n %{guix_group} guix-builder 2>/dev/null || :
    /usr/sbin/usermod -l %{guix_user} -d /var/empty guix-builder 2>/dev/null || :
fi
%systemd_post guix-daemon.service guix-daemon-latest.service
%systemd_post guix-publish.service guix-publish-latest.service


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi
%systemd_preun guix-daemon.service guix-daemon-latest.service
%systemd_preun guix-publish.service guix-publish-latest.service


%postun
%systemd_postun_with_restart guix-daemon.service guix-daemon-latest.service
%systemd_postun_with_restart guix-publish.service guix-publish-latest.service


%files -f guix.lang -f guix-packages.lang
%license COPYING
%doc AUTHORS ChangeLog CODE-OF-CONDUCT NEWS README ROADMAP THANKS TODO
%{_bindir}/guix
%{_bindir}/guix-daemon
%{_sbindir}/guix-register
%{_libexecdir}/guix/download
%{_libexecdir}/guix/list-runtime-roots
%{_libexecdir}/guix/offload
%{_libexecdir}/guix/substitute
%{_libexecdir}/guix-authenticate
%{guile_source_dir}/gnu.scm
%{guile_ccache_dir}/gnu.go
%dir %{guile_source_dir}/gnu
%dir %{guile_ccache_dir}/gnu
%{guile_source_dir}/gnu/artwork.scm
%{guile_ccache_dir}/gnu/artwork.go
%dir %{guile_source_dir}/gnu/build
%dir %{guile_ccache_dir}/gnu/build
%{guile_source_dir}/gnu/bootloader.scm
%{guile_ccache_dir}/gnu/bootloader.go
%dir %{guile_source_dir}/gnu/bootloader
%dir %{guile_ccache_dir}/gnu/bootloader
%{guile_source_dir}/gnu/bootloader/*.scm
%{guile_ccache_dir}/gnu/bootloader/*.go
%{guile_source_dir}/gnu/build/*.scm
%{guile_ccache_dir}/gnu/build/*.go
%{guile_source_dir}/gnu/packages.scm
%{guile_ccache_dir}/gnu/packages.go
%dir %{guile_source_dir}/gnu/packages
%dir %{guile_ccache_dir}/gnu/packages
%{guile_source_dir}/gnu/packages/*.scm
%{guile_ccache_dir}/gnu/packages/*.go
%{guile_source_dir}/gnu/packages/ld-wrapper.in
%dir %{guile_source_dir}/gnu/packages/aux-files
%dir %{guile_source_dir}/gnu/packages/aux-files/emacs
%{guile_source_dir}/gnu/packages/aux-files/emacs/guix-emacs.el
%dir %{guile_source_dir}/gnu/packages/aux-files/linux-libre
%{guile_source_dir}/gnu/packages/aux-files/linux-libre/*-arm.conf
%{guile_source_dir}/gnu/packages/aux-files/linux-libre/*-i686.conf
%{guile_source_dir}/gnu/packages/aux-files/linux-libre/*-x86_64.conf
%dir %{guile_source_dir}/gnu/packages/patches
%{guile_source_dir}/gnu/packages/patches/*.patch
%dir %{guile_source_dir}/gnu/packages/bootstrap
%dir %{guile_source_dir}/gnu/packages/bootstrap/aarch64-linux
%{guile_source_dir}/gnu/packages/bootstrap/aarch64-linux/tar
%{guile_source_dir}/gnu/packages/bootstrap/aarch64-linux/xz
%{guile_source_dir}/gnu/packages/bootstrap/aarch64-linux/mkdir
%{guile_source_dir}/gnu/packages/bootstrap/aarch64-linux/bash
%{guile_source_dir}/gnu/packages/bootstrap/aarch64-linux/guile-2.0.14.tar.xz
%dir %{guile_source_dir}/gnu/packages/bootstrap/armhf-linux
%{guile_source_dir}/gnu/packages/bootstrap/armhf-linux/tar
%{guile_source_dir}/gnu/packages/bootstrap/armhf-linux/xz
%{guile_source_dir}/gnu/packages/bootstrap/armhf-linux/mkdir
%{guile_source_dir}/gnu/packages/bootstrap/armhf-linux/bash
%{guile_source_dir}/gnu/packages/bootstrap/armhf-linux/guile-2.0.11.tar.xz
%dir %{guile_source_dir}/gnu/packages/bootstrap/mips64el-linux
%{guile_source_dir}/gnu/packages/bootstrap/mips64el-linux/tar
%{guile_source_dir}/gnu/packages/bootstrap/mips64el-linux/xz
%{guile_source_dir}/gnu/packages/bootstrap/mips64el-linux/mkdir
%{guile_source_dir}/gnu/packages/bootstrap/mips64el-linux/bash
%{guile_source_dir}/gnu/packages/bootstrap/mips64el-linux/guile-2.0.9.tar.xz
%dir %{guile_source_dir}/gnu/packages/bootstrap/i686-linux
%{guile_source_dir}/gnu/packages/bootstrap/i686-linux/tar
%{guile_source_dir}/gnu/packages/bootstrap/i686-linux/xz
%{guile_source_dir}/gnu/packages/bootstrap/i686-linux/mkdir
%{guile_source_dir}/gnu/packages/bootstrap/i686-linux/bash
%{guile_source_dir}/gnu/packages/bootstrap/i686-linux/guile-2.0.9.tar.xz
%dir %{guile_source_dir}/gnu/packages/bootstrap/x86_64-linux
%{guile_source_dir}/gnu/packages/bootstrap/x86_64-linux/tar
%{guile_source_dir}/gnu/packages/bootstrap/x86_64-linux/xz
%{guile_source_dir}/gnu/packages/bootstrap/x86_64-linux/mkdir
%{guile_source_dir}/gnu/packages/bootstrap/x86_64-linux/bash
%{guile_source_dir}/gnu/packages/bootstrap/x86_64-linux/guile-2.0.9.tar.xz
%{guile_source_dir}/gnu/services.scm
%{guile_ccache_dir}/gnu/services.go
%dir %{guile_source_dir}/gnu/services
%dir %{guile_ccache_dir}/gnu/services
%{guile_source_dir}/gnu/services/*.scm
%{guile_ccache_dir}/gnu/services/*.go
%{guile_source_dir}/gnu/system.scm
%{guile_ccache_dir}/gnu/system.go
%dir %{guile_source_dir}/gnu/system
%dir %{guile_ccache_dir}/gnu/system
%{guile_source_dir}/gnu/system/*.scm
%{guile_ccache_dir}/gnu/system/*.go
%dir %{guile_source_dir}/gnu/system/examples
%{guile_source_dir}/gnu/system/examples/bare-bones.tmpl
%{guile_source_dir}/gnu/system/examples/desktop.tmpl
%{guile_source_dir}/gnu/system/examples/lightweight-desktop.tmpl
%{guile_source_dir}/gnu/system/examples/vm-image.tmpl
%{guile_source_dir}/gnu/tests.scm
%{guile_ccache_dir}/gnu/tests.go
%dir %{guile_source_dir}/gnu/tests
%dir %{guile_ccache_dir}/gnu/tests
%{guile_source_dir}/gnu/tests/*.scm
%{guile_ccache_dir}/gnu/tests/*.go
%{guile_source_dir}/guix.scm
%{guile_ccache_dir}/guix.go
%dir %{guile_source_dir}/guix
%dir %{guile_ccache_dir}/guix
%{guile_source_dir}/guix/*.scm
%{guile_ccache_dir}/guix/*.go
%dir %{guile_source_dir}/guix/build
%dir %{guile_ccache_dir}/guix/build
%{guile_source_dir}/guix/build/*.scm
%{guile_ccache_dir}/guix/build/*.go
%dir %{guile_source_dir}/guix/build-system
%dir %{guile_ccache_dir}/guix/build-system
%{guile_source_dir}/guix/build-system/*.scm
%{guile_ccache_dir}/guix/build-system/*.go
%dir %{guile_source_dir}/guix/import
%dir %{guile_ccache_dir}/guix/import
%{guile_source_dir}/guix/import/*.scm
%{guile_ccache_dir}/guix/import/*.go
%dir %{guile_source_dir}/guix/scripts
%dir %{guile_ccache_dir}/guix/scripts
%{guile_source_dir}/guix/scripts/*.scm
%{guile_ccache_dir}/guix/scripts/*.go
%dir %{guile_source_dir}/guix/scripts/container
%dir %{guile_ccache_dir}/guix/scripts/container
%{guile_source_dir}/guix/scripts/container/*.scm
%{guile_ccache_dir}/guix/scripts/container/*.go
%dir %{guile_source_dir}/guix/scripts/import
%dir %{guile_ccache_dir}/guix/scripts/import
%{guile_source_dir}/guix/scripts/import/*.scm
%{guile_ccache_dir}/guix/scripts/import/*.go
%dir %{guile_source_dir}/guix/scripts/system
%dir %{guile_ccache_dir}/guix/scripts/system
%{guile_source_dir}/guix/scripts/system/*.scm
%{guile_ccache_dir}/guix/scripts/system/*.go
%dir %{guile_source_dir}/guix/store
%dir %{guile_ccache_dir}/guix/store
%{guile_source_dir}/guix/store/ssh.scm
%{guile_ccache_dir}/guix/store/ssh.go
%dir %{guile_ccache_dir}/guix/tests
%{guile_ccache_dir}/guix/tests/*.go
%dir %{_datadir}/guix
%{_datadir}/guix/berlin.guixsd.org.pub
%{_datadir}/guix/hydra.gnu.org.pub
%{_infodir}/%{name}.info*
%dir %{_infodir}/images
%{_infodir}/images/bootstrap-graph.png.gz
%{_infodir}/images/bootstrap-packages.png.gz
%{_infodir}/images/coreutils-bag-graph.png.gz
%{_infodir}/images/coreutils-graph.png.gz
%{_infodir}/images/coreutils-size-map.png.gz
%{_infodir}/images/service-graph.png.gz
%{_infodir}/images/shepherd-graph.png.gz
%exclude %{_infodir}/dir
%{_mandir}/man1/guix-archive.1*
%{_mandir}/man1/guix-build.1*
%{_mandir}/man1/guix-challenge.1*
%{_mandir}/man1/guix-daemon.1*
%{_mandir}/man1/guix-download.1*
%{_mandir}/man1/guix-edit.1*
%{_mandir}/man1/guix-environment.1*
%{_mandir}/man1/guix-gc.1*
%{_mandir}/man1/guix-hash.1*
%{_mandir}/man1/guix-import.1*
%{_mandir}/man1/guix-lint.1*
%{_mandir}/man1/guix-package.1*
%{_mandir}/man1/guix-publish.1*
%{_mandir}/man1/guix-pull.1*
%{_mandir}/man1/guix-refresh.1*
%{_mandir}/man1/guix-size.1*
%{_mandir}/man1/guix-system.1*
%{_mandir}/man1/guix.1*
%{completionsdir}/guix
%{_datadir}/zsh/site-functions/_guix
%dir %{_sysconfdir}/guix
%{_unitdir}/guix-daemon.service
%{_unitdir}/guix-daemon-latest.service
%{_unitdir}/guix-publish.service
%{_unitdir}/guix-publish-latest.service



%changelog
* Tue Dec 12 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.14.0-5
- Use make_install macro

* Tue Dec 12 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.14.0-4
- Fix TLS crash with upstream commit 7f04197

* Sun Dec 10 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.14.0-3
- Workaround TLS crash by reverting upstream commit 866f37f

* Sun Dec 10 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.14.0-2
- Move guile-git to Requires because it is not optional
- Do not show OK messages when validating bootstrap binraies

* Sat Dec 09 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.14.0-1
- Update to 0.14.0
- Avoid running tests as root
- Use /var/empty as the home directory because it is what the manual uses
- Validate bootstrap binraies during installation

* Mon Oct 16 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.13.0-2
- Rebuilt for Fedora 27 and 28

* Sat May 27 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.13.0-1
- Update to 0.13.0
- Use HTTPS to download the source
- Use systemd_requires macro
- Allow building without access to internet
- Move provides and obsoletes of old emacs sub-packages to emacs-guix
- Remove emacs interface because it has been moved to a separate package
- Rename systemd service files provided by upstream because they include
  references to the guix profile of root user
- Generate default systemd service files from upstream ones to minimize the
  difference between them

* Sun Mar 12 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.12.0-3
- Workaround missing build-id error for Fedora 27

* Wed Mar 08 2017 Ting-Wei Lan <lantw44@gmail.com> - 0.12.0-2
- Rebuilt for Fedora 26 and 27

* Sat Dec 31 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.12.0-1
- Update to 0.12.0

* Fri Nov 04 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.11.0-3
- Use autosetup macro
- Fix build failure on Guile 2.0.13

* Sat Sep 10 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.11.0-2
- Rebuilt for Fedora 25 and 26

* Thu Aug 04 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.11.0-1
- Update to 0.11.0

* Fri Apr 01 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.10.0-1
- Update to 0.10.0
- Add help2man to BuildRequires
- Add dot to both BuildRequires and Requires

* Thu Mar 03 2016 Ting-Wei Lan <lantw44@gmail.com> - 0.9.0-3
- Rebuilt for Fedora 24 and 25

* Tue Nov 24 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.9.0-2
- Own /usr/share/info/images because no other packages use it
- Use _libdir macro instead of hard-coding /usr/lib64

* Sun Nov 22 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.9.0-1
- Update to 0.9.0
- Don't clutter the system site-lisp directory
- The build user of guix-daemon should be a system account

* Sat Oct 10 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.8.3-2
- Remove group tag, which is not required
- Use pkgconfig in BuildRequires
- Use info instead of /sbin/install-info in Requires
- Handle systemd service files
- Don't hard-code .gz when listing man pages
- Merge emacs sub-packages back into the main package

* Thu Jul 23 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.8.3-1
- Update to 0.8.3
- Remove checks that depend on missing remote resources
- Remove checks that are not allowed to run in mock
- Remove the systemd service file written by me. Upstream already provides a
  better systemd service file.
- Rename guix-builder group to guixbuild, which is the default of guix-daemon
  and upstream systemd service file.

* Thu May 21 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.8.2-3
- We no longer have to create /gnu/store and /var/log/guix manually. Guix can
  create and set correct permissions for these directories.

* Sun May 17 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.8.2-2
- Use license marco to install the license file

* Fri May 15 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.8.2-1
- Update to 0.8.2
- Add a check section to run the test

* Wed Apr 15 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.8.1-3
- Use /usr/sbin/useradd and /usr/sbin/groupadd instead of /sbin/useradd and
  /sbin/groupadd to make this package work with DNF

* Fri Mar 20 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.8.1-2
- Rebuilt for Fedora 22 and 23
- Add epoch to guile dependency to prevent it from using compat-guile18

* Fri Jan 30 2015 Ting-Wei Lan <lantw44@gmail.com> - 0.8.1-1
- Update to 0.8.1

* Sat Nov 22 2014 Ting-Wei Lan <lantw44@gmail.com> - 0.8-2
- Do not create /var/guix, which prevents guix-daemon from populating /var/guix
  and /gnu/store on the first start.

* Wed Nov 19 2014 Ting-Wei Lan <lantw44@gmail.com> - 0.8-1
- Update to 0.8

* Tue Jul 29 2014 Ting-Wei Lan <lantw44@gmail.com> - 0.7-1
- Update to 0.7

* Fri Apr 18 2014 Ting-Wei Lan <lantw44@gmail.com> - 0.6-2
- Add a systemd service file

* Thu Apr 10 2014 Ting-Wei Lan <lantw44@gmail.com> - 0.6-1
- Update to 0.6

* Tue Dec 17 2013 Ting-Wei Lan <lantw44@gmail.com> - 0.5-1
- Update to 0.5

* Mon Sep 30 2013 Ting-Wei Lan <lantw44@gmail.com> - 0.4-4
- Initial packaging
