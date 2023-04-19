# Bootstrap binaries provided by guix don't have build IDs.
%global _missing_build_ids_terminate_build 0

%global selinuxtype   targeted
%global selinuxmodule guix-daemon

Name:           guix
Version:        1.4.0
Release:        3%{?dist}
Summary:        A purely functional package manager for the GNU system

License:        GPLv3+
URL:            https://guix.gnu.org
Source0:        https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz

# Fix tests/guix-home.sh when Guix is not installed.
Patch0:         guix-1.4.0-tests-guix-home.patch

%global guix_user         guixbuild
%global guix_group        guixbuild
%global guile_source_dir  %{_datadir}/guile/site/3.0
%global guile_ccache_dir  %{_libdir}/guile/3.0/site-ccache
%global guix_profile_root %{_localstatedir}/guix/profiles/per-user/root/current-guix

%global bash_completion_dir %(pkg-config --variable=completionsdir bash-completion)
%global fish_completion_dir %(pkg-config --variable=completionsdir fish)

%if "%{?fish_completion_dir}" == ""
%global fish_completion_dir %{_datadir}/fish/vendor_completions.d
%endif

BuildRequires:  gcc-c++
BuildRequires:  autoconf, automake, gettext-devel, po4a, help2man, texinfo
BuildRequires:  bzip2-devel, libgcrypt-devel, pkgconfig(sqlite3)
BuildRequires:  gettext, graphviz
BuildRequires:  bash-completion, fish
BuildRequires:  selinux-policy, systemd

BuildRequires:  glibc-langpack-en
BuildRequires:  pkgconfig(guile-3.0) >= 3.0.3
BuildRequires:  guile-gcrypt >= 0.1.0
BuildRequires:  guile30-gnutls
BuildRequires:  guile-sqlite3 >= 0.1.0
BuildRequires:  guile-zlib >= 0.1.0
BuildRequires:  guile-lzlib
BuildRequires:  guile-avahi
BuildRequires:  guile-git >= 0.5.0
BuildRequires:  guile-json >= 4.3.0
BuildRequires:  guile-ssh >= 0.13.0
BuildRequires:  guile-zstd
BuildRequires:  guile-semver
BuildRequires:  guile-lib
BuildRequires:  guile-lzma
BuildRequires:  disarchive

Requires:       guile30 >= 3.0.3
Requires:       guile-gcrypt >= 0.1.0
Requires:       guile30-gnutls
Requires:       guile-sqlite3 >= 0.1.0
Requires:       guile-zlib >= 0.1.0
Requires:       guile-lzlib
Requires:       guile-avahi
Requires:       guile-git >= 0.5.0
Requires:       guile-json >= 4.3.0
Requires:       guile-lzma
Requires:       disarchive

Requires:       gzip, bzip2, xz
Requires:       selinux-policy
Requires:       %{_bindir}/dot
Requires:       %{_libdir}/libgcrypt.so
Requires(post): /usr/sbin/useradd
Requires(post): /usr/sbin/usermod
Requires(post): /usr/sbin/groupadd
Requires(post): /usr/sbin/groupmod
Requires(post): /usr/bin/gpasswd
Requires(post): libselinux-utils, policycoreutils
Requires(post): info
Requires(preun): info

%{?systemd_requires}

Recommends:     guile-ssh >= 0.13.0
Recommends:     guile-zstd
Recommends:     guile-semver
Recommends:     guile-lib
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


%build
# Rename test-tmp to t to save the length of the path.
%configure \
    --disable-rpath \
    --with-bash-completion-dir=%{bash_completion_dir} \
    --with-fish-completion-dir=%{fish_completion_dir} \
    --with-selinux-policy-dir=%{_datadir}/selinux/packages \
    ac_cv_guix_test_root="$(pwd)/t"
# The progress bar of Guile compilation does not work with -O option.
%global _make_output_sync %{nil}
%make_build


%check
if [ "$(curl http://fedoraproject.org/static/hotspot.txt)" != OK ]; then
    echo 'Guix tests require Internet access to work.'
    echo 'Expect failure if the build process has no access to Internet.'
fi
# The default path used by mock is /builddir/build/BUILD/guix-<version>, whose
# length is at least 32 bytes. However, the test tests/gexp.scm fails when the
# path is longer than 29 bytes because of the length limit of the shebang line.
# We raise the working directory length limit from 29 to 36 by overriding the
# autoconf cache variable ac_cv_guix_test_root, saving 7 bytes by renaming
# test-tmp to t.
cwd_str="$(pwd)"
cwd_len="${#cwd_str}"
if [ "${cwd_len}" -gt 36 ]; then
    echo "${cwd_str} is too long."
    echo 'The working directory cannot be longer than 36 bytes.'
    exit 1
fi
# Running tests in parallel causes errors:
# In procedure copy-file: Permission denied:
# "/builddir/build/BUILD/guix-1.4.0/gnu/packages/bootstrap/i686-linux/bash"
%{__make} check
# Grant write permission so rpmbuild can clean the build root.
chmod -R u+w "$(pwd)/t"


%install
%make_install systemdservicedir=%{_unitdir}
# Rename systemd service files provided by upstream.
mv %{buildroot}%{_unitdir}/guix-daemon{,-latest}.service
mv %{buildroot}%{_unitdir}/guix-gc{,-latest}.service
mv %{buildroot}%{_unitdir}/guix-publish{,-latest}.service
# Generate default systemd service files from upstream ones.
sed -e 's|^ExecStart=%{guix_profile_root}/bin|ExecStart=%{_bindir}|' \
    -e 's|^Description=\(.*\)|Description=\1 (default)|' \
    -e '/^Environment=/d' %{buildroot}%{_unitdir}/guix-daemon-latest.service \
    > %{buildroot}%{_unitdir}/guix-daemon.service
sed -e 's|^ExecStart=%{guix_profile_root}/bin|ExecStart=%{_bindir}|' \
    -e 's|^Description=\(.*\)|Description=\1 (default)|' \
    -e '/^Environment=/d' %{buildroot}%{_unitdir}/guix-gc-latest.service \
    > %{buildroot}%{_unitdir}/guix-gc.service
sed -e 's|^ExecStart=%{guix_profile_root}/bin|ExecStart=%{_bindir}|' \
    -e 's|^Description=\(.*\)|Description=\1 (default)|' \
    -e '/^Environment=/d' %{buildroot}%{_unitdir}/guix-publish-latest.service \
    > %{buildroot}%{_unitdir}/guix-publish.service
# Generated files must be different from upstream ones.
! cmp %{buildroot}%{_unitdir}/guix-daemon{,-latest}.service
! cmp %{buildroot}%{_unitdir}/guix-gc{,-latest}.service
! cmp %{buildroot}%{_unitdir}/guix-publish{,-latest}.service
# Edit the description of upstream systemd service files.
sed -i 's|^Description=\(.*\)|Description=\1 (upstream)|' \
    %{buildroot}%{_unitdir}/guix-daemon-latest.service \
    %{buildroot}%{_unitdir}/guix-gc-latest.service \
    %{buildroot}%{_unitdir}/guix-publish-latest.service
# Drop useless upstart service files.
rm %{buildroot}%{_libdir}/upstart/system/guix-daemon.conf
rm %{buildroot}%{_libdir}/upstart/system/guix-publish.conf
rmdir %{buildroot}%{_libdir}/upstart/system
rmdir %{buildroot}%{_libdir}/upstart
# Drop useless openrc service files.
rm %{buildroot}%{_sysconfdir}/openrc/guix-daemon
rmdir %{buildroot}%{_sysconfdir}/openrc
# Drop useless sysvinit service files.
rm %{buildroot}%{_sysconfdir}/init.d/guix-daemon
rmdir %{buildroot}%{_sysconfdir}/init.d
# Own the configuration directory.
mkdir -p %{buildroot}%{_sysconfdir}/guix
%find_lang guix
%find_lang guix-packages


%pre
#selinux_relabel_pre -s %{selinuxtype}


%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
if [ "$1" = 1 ]; then
    /usr/sbin/groupadd -r %{guix_group}
    /usr/sbin/useradd -r -M -N -g %{guix_group} -d /var/empty -s /sbin/nologin \
        -c 'Guix build user' %{guix_user}
    /usr/bin/gpasswd -a %{guix_user} %{guix_group} >/dev/null
elif [ "$1" -gt 1 ]; then
    /usr/sbin/groupmod -n %{guix_group} guix-builder 2>/dev/null || :
    /usr/sbin/usermod -l %{guix_user} -d /var/empty guix-builder 2>/dev/null || :
fi
%systemd_post guix-daemon.service guix-daemon-latest.service
%systemd_post guix-gc.service guix-gc-latest.service
%systemd_post guix-publish.service guix-publish-latest.service
#selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxmodule}.cil


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
    #selinux_modules_uninstall -s %{selinuxtype} %{selinuxmodule}
fi
%systemd_preun guix-daemon.service guix-daemon-latest.service
%systemd_preun guix-gc.service guix-gc-latest.service
%systemd_preun guix-publish.service guix-publish-latest.service


%postun
%systemd_postun_with_restart guix-daemon.service guix-daemon-latest.service
%systemd_postun_with_restart guix-gc.service guix-gc-latest.service
%systemd_postun_with_restart guix-publish.service guix-publish-latest.service


%posttrans
#selinux_relabel_post -s %{selinuxtype}


%files -f guix.lang -f guix-packages.lang
%license COPYING
%doc AUTHORS ChangeLog CODE-OF-CONDUCT NEWS README ROADMAP THANKS TODO
%{_bindir}/guix
%{_bindir}/guix-daemon
%dir %{_libexecdir}/guix
%{_libexecdir}/guix/guile
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
%{guile_source_dir}/gnu/ci.scm
%{guile_ccache_dir}/gnu/ci.go
%{guile_source_dir}/gnu/compression.scm
%{guile_ccache_dir}/gnu/compression.go
%{guile_source_dir}/gnu/home.scm
%{guile_ccache_dir}/gnu/home.go
%dir %{guile_source_dir}/gnu/home
%dir %{guile_ccache_dir}/gnu/home
%{guile_source_dir}/gnu/home/services.scm
%{guile_ccache_dir}/gnu/home/services.go
%dir %{guile_source_dir}/gnu/home/services
%dir %{guile_ccache_dir}/gnu/home/services
%{guile_source_dir}/gnu/home/services/*.scm
%{guile_ccache_dir}/gnu/home/services/*.go
%{guile_source_dir}/gnu/image.scm
%{guile_ccache_dir}/gnu/image.go
%{guile_source_dir}/gnu/installer.scm
%dir %{guile_source_dir}/gnu/installer
%{guile_source_dir}/gnu/installer/*.scm
%{guile_source_dir}/gnu/installer/logo.txt
%dir %{guile_source_dir}/gnu/installer/newt
%{guile_source_dir}/gnu/installer/newt/*.scm
%{guile_source_dir}/gnu/machine.scm
%{guile_ccache_dir}/gnu/machine.go
%dir %{guile_source_dir}/gnu/machine
%dir %{guile_ccache_dir}/gnu/machine
%{guile_source_dir}/gnu/machine/digital-ocean.scm
%{guile_ccache_dir}/gnu/machine/digital-ocean.go
%{guile_source_dir}/gnu/machine/ssh.scm
%{guile_ccache_dir}/gnu/machine/ssh.go
%{guile_source_dir}/gnu/packages.scm
%{guile_ccache_dir}/gnu/packages.go
%dir %{guile_source_dir}/gnu/packages
%dir %{guile_ccache_dir}/gnu/packages
%{guile_source_dir}/gnu/packages/*.scm
%{guile_ccache_dir}/gnu/packages/*.go
%{guile_source_dir}/gnu/packages/ld-wrapper.in
%dir %{guile_source_dir}/gnu/packages/aux-files
%dir %{guile_source_dir}/gnu/packages/aux-files/chromium
%{guile_source_dir}/gnu/packages/aux-files/chromium/master-preferences.json
%dir %{guile_source_dir}/gnu/packages/aux-files/emacs
%{guile_source_dir}/gnu/packages/aux-files/emacs/guix-emacs.el
%{guile_source_dir}/gnu/packages/aux-files/guix.vim
%dir %{guile_source_dir}/gnu/packages/aux-files/linux-libre
%{guile_source_dir}/gnu/packages/aux-files/linux-libre/*-arm.conf
%{guile_source_dir}/gnu/packages/aux-files/linux-libre/*-arm64.conf
%{guile_source_dir}/gnu/packages/aux-files/linux-libre/*-i686.conf
%{guile_source_dir}/gnu/packages/aux-files/linux-libre/*-x86_64.conf
%{guile_source_dir}/gnu/packages/aux-files/pack-audit.c
%dir %{guile_source_dir}/gnu/packages/aux-files/python
%{guile_source_dir}/gnu/packages/aux-files/python/sanity-check.py
%{guile_source_dir}/gnu/packages/aux-files/python/sanity-check-next.py
%{guile_source_dir}/gnu/packages/aux-files/python/sitecustomize.py
%dir %{guile_source_dir}/gnu/packages/aux-files/renpy
%{guile_source_dir}/gnu/packages/aux-files/renpy/renpy.in
%{guile_source_dir}/gnu/packages/aux-files/run-in-namespace.c
%dir %{guile_source_dir}/gnu/packages/patches
%{guile_source_dir}/gnu/packages/patches/*.diff
%{guile_source_dir}/gnu/packages/patches/*.patch
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
%{guile_source_dir}/gnu/system/examples/asus-c201.tmpl
%{guile_source_dir}/gnu/system/examples/bare-bones.tmpl
%{guile_source_dir}/gnu/system/examples/bare-hurd.tmpl
%{guile_source_dir}/gnu/system/examples/beaglebone-black.tmpl
%{guile_source_dir}/gnu/system/examples/desktop.tmpl
%{guile_source_dir}/gnu/system/examples/docker-image.tmpl
%{guile_source_dir}/gnu/system/examples/lightweight-desktop.tmpl
%{guile_source_dir}/gnu/system/examples/vm-image.tmpl
%dir %{guile_source_dir}/gnu/system/images
%dir %{guile_ccache_dir}/gnu/system/images
%{guile_source_dir}/gnu/system/images/hurd.scm
%{guile_ccache_dir}/gnu/system/images/hurd.go
%{guile_source_dir}/gnu/system/images/novena.scm
%{guile_ccache_dir}/gnu/system/images/novena.go
%{guile_source_dir}/gnu/system/images/pine64.scm
%{guile_ccache_dir}/gnu/system/images/pine64.go
%{guile_source_dir}/gnu/system/images/pinebook-pro.scm
%{guile_ccache_dir}/gnu/system/images/pinebook-pro.go
%{guile_source_dir}/gnu/system/images/rock64.scm
%{guile_ccache_dir}/gnu/system/images/rock64.go
%{guile_source_dir}/gnu/system/images/wsl2.scm
%{guile_ccache_dir}/gnu/system/images/wsl2.go
%{guile_source_dir}/gnu/tests.scm
%{guile_ccache_dir}/gnu/tests.go
%dir %{guile_source_dir}/gnu/tests
%dir %{guile_ccache_dir}/gnu/tests
%{guile_source_dir}/gnu/tests/*.scm
%{guile_ccache_dir}/gnu/tests/*.go
%dir %{guile_source_dir}/gnu/tests/data
%{guile_source_dir}/gnu/tests/data/jami-dummy-account.dat
%{guile_source_dir}/guix.scm
%{guile_ccache_dir}/guix.go
%dir %{guile_source_dir}/guix
%dir %{guile_ccache_dir}/guix
%{guile_source_dir}/guix/d3.v3.js
%{guile_source_dir}/guix/graph.js
%{guile_source_dir}/guix/*.scm
%{guile_ccache_dir}/guix/*.go
%dir %{guile_source_dir}/guix/build
%dir %{guile_ccache_dir}/guix/build
%{guile_source_dir}/guix/build/*.scm
%{guile_ccache_dir}/guix/build/*.go
%dir %{guile_source_dir}/guix/build/maven
%dir %{guile_ccache_dir}/guix/build/maven
%{guile_source_dir}/guix/build/maven/*.scm
%{guile_ccache_dir}/guix/build/maven/*.go
%dir %{guile_source_dir}/guix/build-system
%dir %{guile_ccache_dir}/guix/build-system
%{guile_source_dir}/guix/build-system/*.scm
%{guile_ccache_dir}/guix/build-system/*.go
%dir %{guile_source_dir}/guix/import
%dir %{guile_ccache_dir}/guix/import
%{guile_source_dir}/guix/import/*.scm
%{guile_ccache_dir}/guix/import/*.go
%dir %{guile_source_dir}/guix/platforms
%dir %{guile_ccache_dir}/guix/platforms
%{guile_source_dir}/guix/platforms/*.scm
%{guile_ccache_dir}/guix/platforms/*.go
%dir %{guile_source_dir}/guix/scripts
%dir %{guile_ccache_dir}/guix/scripts
%{guile_source_dir}/guix/scripts/*.scm
%{guile_ccache_dir}/guix/scripts/*.go
%dir %{guile_source_dir}/guix/scripts/container
%dir %{guile_ccache_dir}/guix/scripts/container
%{guile_source_dir}/guix/scripts/container/*.scm
%{guile_ccache_dir}/guix/scripts/container/*.go
%dir %{guile_source_dir}/guix/scripts/git
%dir %{guile_ccache_dir}/guix/scripts/git
%{guile_source_dir}/guix/scripts/git/*.scm
%{guile_ccache_dir}/guix/scripts/git/*.go
%dir %{guile_source_dir}/guix/scripts/home
%dir %{guile_ccache_dir}/guix/scripts/home
%{guile_source_dir}/guix/scripts/home/*.scm
%{guile_ccache_dir}/guix/scripts/home/*.go
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
%{guile_source_dir}/guix/store/schema.sql
%{guile_source_dir}/guix/store/*.scm
%{guile_ccache_dir}/guix/store/*.go
%dir %{guile_ccache_dir}/guix/tests
%{guile_ccache_dir}/guix/tests/*.go
%dir %{_datadir}/guix
%{_datadir}/guix/berlin.guix.gnu.org.pub
%{_datadir}/guix/bordeaux.guix.gnu.org.pub
%{_datadir}/guix/ci.guix.gnu.org.pub
%{_datadir}/guix/ci.guix.info.pub
%{_datadir}/selinux/packages/%{selinuxmodule}.cil
%{_infodir}/%{name}.info*
%{_infodir}/%{name}.de.info*
%{_infodir}/%{name}.es.info*
%{_infodir}/%{name}.fr.info*
%{_infodir}/%{name}.pt_BR.info*
%{_infodir}/%{name}.ru.info*
%{_infodir}/%{name}.zh_CN.info*
%{_infodir}/%{name}-cookbook.info*
%{_infodir}/%{name}-cookbook.de.info*
%{_infodir}/%{name}-cookbook.fr.info*
%{_infodir}/%{name}-cookbook.ko.info*
%{_infodir}/%{name}-cookbook.sk.info*
%dir %{_infodir}/images
%{_infodir}/images/bootstrap-graph.png.gz
%{_infodir}/images/bootstrap-packages.png.gz
%{_infodir}/images/coreutils-bag-graph.png.gz
%{_infodir}/images/coreutils-graph.png.gz
%{_infodir}/images/coreutils-size-map.png.gz
%{_infodir}/images/gcc-core-mesboot0-graph.png.gz
%{_infodir}/images/installer-network.png.gz
%{_infodir}/images/installer-partitions.png.gz
%{_infodir}/images/installer-resume.png.gz
%{_infodir}/images/service-graph.png.gz
%{_infodir}/images/shepherd-graph.png.gz
%exclude %{_infodir}/dir
%{_mandir}/man1/guix-archive.1*
%{_mandir}/man1/guix-build.1*
%{_mandir}/man1/guix-challenge.1*
%{_mandir}/man1/guix-container.1*
%{_mandir}/man1/guix-copy.1*
%{_mandir}/man1/guix-daemon.1*
%{_mandir}/man1/guix-deploy.1*
%{_mandir}/man1/guix-describe.1*
%{_mandir}/man1/guix-download.1*
%{_mandir}/man1/guix-edit.1*
%{_mandir}/man1/guix-environment.1*
%{_mandir}/man1/guix-gc.1*
%{_mandir}/man1/guix-git.1*
%{_mandir}/man1/guix-graph.1*
%{_mandir}/man1/guix-hash.1*
%{_mandir}/man1/guix-home.1*
%{_mandir}/man1/guix-import.1*
%{_mandir}/man1/guix-lint.1*
%{_mandir}/man1/guix-offload.1*
%{_mandir}/man1/guix-pack.1*
%{_mandir}/man1/guix-package.1*
%{_mandir}/man1/guix-processes.1*
%{_mandir}/man1/guix-publish.1*
%{_mandir}/man1/guix-pull.1*
%{_mandir}/man1/guix-refresh.1*
%{_mandir}/man1/guix-repl.1*
%{_mandir}/man1/guix-shell.1*
%{_mandir}/man1/guix-size.1*
%{_mandir}/man1/guix-style.1*
%{_mandir}/man1/guix-system.1*
%{_mandir}/man1/guix-time-machine.1*
%{_mandir}/man1/guix-weather.1*
%{_mandir}/man1/guix.1*
%{bash_completion_dir}/guix
%{bash_completion_dir}/guix-daemon
%{fish_completion_dir}/guix.fish
%{_datadir}/zsh/site-functions/_guix
%dir %{_sysconfdir}/guix
%{_unitdir}/gnu-store.mount
%{_unitdir}/guix-daemon.service
%{_unitdir}/guix-daemon-latest.service
%{_unitdir}/guix-gc.service
%{_unitdir}/guix-gc-latest.service
%{_unitdir}/guix-publish.service
%{_unitdir}/guix-publish-latest.service



%changelog
* Wed Apr 19 2023 Ting-Wei Lan <lantw44@gmail.com> - 1.4.0-3
- Rebuilt for Fedora 38 and 39

* Tue Feb 28 2023 Ting-Wei Lan <lantw44@gmail.com> - 1.4.0-2
- Switch to the standalone GnuTLS Guile bindings

* Sun Feb 12 2023 Ting-Wei Lan <lantw44@gmail.com> - 1.4.0-1
- Update to 1.4.0
- Switch to Guile 3.0 because Guile 2.2 is no longer supported

* Thu Nov 03 2022 Ting-Wei Lan <lantw44@gmail.com> - 1.3.0-4
- Drop unused code from the check stage
- Grant write permission to fix the rmbuild stage on Fedora 37 and later

* Thu Apr 28 2022 Ting-Wei Lan <lantw44@gmail.com> - 1.3.0-3
- Rebuilt for Fedora 36 and 37

* Sat Sep 25 2021 Ting-Wei Lan <lantw44@gmail.com> - 1.3.0-2
- Rebuilt for Fedora 35 and 36

* Mon Jun 14 2021 Ting-Wei Lan <lantw44@gmail.com> - 1.3.0-1
- Update to 1.3.0

* Sat Mar 13 2021 Ting-Wei Lan <lantw44@gmail.com> - 1.2.0-2
- Rebuilt for Fedora 34 and 35

* Wed Feb 17 2021 Ting-Wei Lan <lantw44@gmail.com> - 1.2.0-1
- Update to 1.2.0

* Sun Nov  1 2020 Ting-Wei Lan <lantw44@gmail.com> - 1.1.0-2
- Rebuilt for Fedora 33 and 34
- Update project website URL

* Sun Apr 26 2020 Ting-Wei Lan <lantw44@gmail.com> - 1.1.0-1
- Update to 1.1.0

* Wed Sep 18 2019 Ting-Wei Lan <lantw44@gmail.com> - 1.0.2-0.1.20190917git0ed97e6
- Update to a git snapshot from master branch to fix tests
- Move guile-json from Recommends to Requires because emacs-guix needs it

* Tue Sep 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 1.0.1-2
- Use gnutls-guile on Fedora 31 and later

* Fri May 24 2019 Ting-Wei Lan <lantw44@gmail.com> - 1.0.1-1
- Update to 1.0.1

* Fri May 17 2019 Ting-Wei Lan <lantw44@gmail.com> - 1.0.0-1
- Update to 1.0.0
- Switch to Guile 2.2 because Guile 2.0 is no longer supported

* Wed May 01 2019 Ting-Wei Lan <lantw44@gmail.com> - 0.16.0-3
- Rebuilt for Fedora 30 and 31

* Sat Dec 22 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.16.0-2
- Fix ExecStart paths in systemd service files

* Sun Dec 16 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.16.0-1
- Update to 0.16.0

* Tue Oct 23 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.15.0-2
- Add GCC to BuildRequires for Fedora 29 and later

* Sun Jul 15 2018 Ting-Wei Lan <lantw44@gmail.com> - 0.15.0-1
- Update to 0.15.0
- Skip all tests because of the number of test failure
- Skip SELinux module installation because it is not complete

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
