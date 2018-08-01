%global cross_arch      arm
%global cross_triplet   arm-linux-gnueabi
%global cross_sysroot   %{_prefix}/%{cross_triplet}/sys-root

%if 0%{?_unique_build_ids}
%global _find_debuginfo_opts --build-id-seed "%{name}-%{version}-%{release}"
%endif

%if 0%{?fedora} >= 28
%global enable_obsolete_rpc  0
%global enable_obsolete_nsl  0
%else
%global enable_obsolete_rpc  1
%global enable_obsolete_nsl  1
%endif

%if 0%{?bootstrap:1}
%global headers_only    1
%global pkg_suffix      -headers
%global debug_package   %{nil}
%else
%global headers_only    0
%global pkg_suffix      %{nil}
%endif

%if %{cross_arch} == "arm"
  %global arm_type      %(echo %{cross_triplet} | sed 's/.*-\\([a-z]*\\)$/\\1/')
  %if %{arm_type} == "gnueabi"
    %global loader_suffix     %{nil}
    %global loader_version    3
    %global gnu_hdr_suffix    -soft
    %global lib_dir_name      lib
  %else
    %if %{arm_type} == "gnueabihf"
      %global loader_suffix   -armhf
      %global loader_version  3
      %global gnu_hdr_suffix  -hard
      %global lib_dir_name    lib
    %else
      %{error:Unsupported ARM processor type}
    %endif
  %endif
%else
  %if %{cross_arch} == "arm64"
    %global loader_suffix     -aarch64
    %global loader_version    1
    %global gnu_hdr_suffix    -lp64
    %global lib_dir_name      lib64
  %else
    %global loader_suffix     %{nil}
    %global loader_version    0
    %global gnu_hdr_suffix    %{nil}
    %global lib_dir_name      lib
  %endif
%endif

Name:       %{cross_triplet}-glibc%{pkg_suffix}
Version:    2.28
Release:    1%{?dist}
Summary:    The GNU C Library (%{cross_triplet})

License:    LGPLv2+ and LGPLv2+ with exceptions and GPLv2+
URL:        https://www.gnu.org/software/libc
Source0:    https://ftp.gnu.org/gnu/glibc/glibc-%{version}.tar.xz

BuildRequires: bison
BuildRequires: %{cross_triplet}-filesystem
BuildRequires: %{cross_triplet}-gcc-stage1
BuildRequires: %{cross_triplet}-kernel-headers
Requires:   %{cross_triplet}-filesystem
Requires:   %{cross_triplet}-kernel-headers
Provides:   %{cross_triplet}-glibc-stage1

%if !%{headers_only}
BuildRequires: %{cross_triplet}-gcc-stage2, perl
%endif

%global __provides_exclude_from ^%{cross_sysroot}
%global __requires_exclude_from ^%{cross_sysroot}

%description


%prep
%autosetup -p1 -n glibc-%{version}


%build
mkdir -p %{_builddir}/glibc-build
cd %{_builddir}/glibc-build
export BUILD_CC=%{_bindir}/gcc
export CC=%{_bindir}/%{cross_triplet}-gcc
export CXX=%{_bindir}/%{cross_triplet}-g++
export AR=%{_bindir}/%{cross_triplet}-ar
export RANLIB=%{_bindir}/%{cross_triplet}-ranlib
%global _configure ../glibc-%{version}/configure
%global _hardening_ldflags \\\
    %(echo "%{_hardening_ldflags}" | sed -e 's/-specs=[^ ]*//g')
%global __global_ldflags \\\
    %(echo "%{__global_ldflags}" | \\\
        sed -e 's/-specs=[^ ]*//g' -e 's/-Wl,-z,defs *//g')
%global optflags \\\
    %(echo "%{optflags}" | \\\
        sed -e 's/-m[^ ]*//g' -e 's/-specs=[^ ]*//g' -e 's/-Werror=[^ ]*//g' \\\
            -e 's/-Wp,[^ ]*//g' -e 's/-fasynchronous-unwind-tables *//g' \\\
            -e 's/-fstack-clash-protection *//g' -e 's/-fcf-protection *//g')
# Use /usr directly because it is the path in cross_sysroot
%configure \
    --libdir=/usr/%{lib_dir_name} \
    --host=%{cross_triplet} \
    --build=%{_target_platform} \
    --enable-kernel=2.6.32 \
    --enable-shared \
    --enable-add-ons \
    --enable-multi-arch \
%if %{enable_obsolete_rpc}
    --enable-obsolete-rpc \
%endif
%if %{enable_obsolete_nsl}
    --enable-obsolete-nsl \
%endif
    --enable-stack-protector=strong \
    --enable-tunables \
    --disable-profile \
    --disable-werror \
    --with-headers=%{cross_sysroot}/usr/include \
    --with-tls \
    --with-__thread \
    --without-cvs \
    --without-gd \
%if %{headers_only}
    libc_cv_forced_unwind=yes \
    libc_cv_c_cleanup=yes \
%endif

%if %{headers_only}
%make_build csu/subdir_lib
%else
%make_build
%endif


%install
cd %{_builddir}/glibc-build
%if %{headers_only}
%{__make} install-headers install_root=%{buildroot}%{cross_sysroot} \
    install-bootstrap-headers=yes
touch %{buildroot}%{cross_sysroot}/usr/include/gnu/stubs.h
mkdir -p %{buildroot}%{cross_sysroot}/usr/%{lib_dir_name}
cp csu/crt1.o csu/crti.o csu/crtn.o \
    %{buildroot}%{cross_sysroot}/usr/%{lib_dir_name}
%{cross_triplet}-gcc -nostdlib -nostartfiles -shared -x c /dev/null \
    -o %{buildroot}%{cross_sysroot}/usr/%{lib_dir_name}/libc.so
%else
%{__make} install install_root=%{buildroot}%{cross_sysroot}
rm -rf %{buildroot}%{cross_sysroot}/usr/share/man
rm -rf %{buildroot}%{cross_sysroot}/usr/share/info
rm -rf %{buildroot}%{cross_sysroot}/usr/share/locale
%endif

# Don't any static archive - based on Fedora Project cross-gcc.spec
%global __ar_no_strip $RPM_BUILD_DIR/glibc-%{version}/ar-no-strip
cat > %{__ar_no_strip} << EOF
#!/bin/sh
f=\$2
case \$(basename \$f) in
    *.a)
        ;;
    *)
        %{__strip} \$@
        ;;
esac
EOF
chmod +x %{__ar_no_strip}
%undefine __strip
%global __strip %{__ar_no_strip}


%files
%license COPYING COPYING.LIB LICENSES
%doc ChangeLog MAINTAINERS NEWS README
%{cross_sysroot}/usr/include/a.out.h
%{cross_sysroot}/usr/include/aio.h
%{cross_sysroot}/usr/include/aliases.h
%{cross_sysroot}/usr/include/alloca.h
%{cross_sysroot}/usr/include/ar.h
%{cross_sysroot}/usr/include/argp.h
%{cross_sysroot}/usr/include/argz.h
%dir %{cross_sysroot}/usr/include/arpa
%{cross_sysroot}/usr/include/arpa/ftp.h
%{cross_sysroot}/usr/include/arpa/inet.h
%{cross_sysroot}/usr/include/arpa/nameser.h
%{cross_sysroot}/usr/include/arpa/nameser_compat.h
%{cross_sysroot}/usr/include/arpa/telnet.h
%{cross_sysroot}/usr/include/arpa/tftp.h
%{cross_sysroot}/usr/include/assert.h
%{cross_sysroot}/usr/include/bits
%{cross_sysroot}/usr/include/byteswap.h
%{cross_sysroot}/usr/include/complex.h
%{cross_sysroot}/usr/include/cpio.h
%{cross_sysroot}/usr/include/crypt.h
%{cross_sysroot}/usr/include/ctype.h
%{cross_sysroot}/usr/include/dirent.h
%{cross_sysroot}/usr/include/dlfcn.h
%{cross_sysroot}/usr/include/elf.h
%{cross_sysroot}/usr/include/endian.h
%{cross_sysroot}/usr/include/envz.h
%{cross_sysroot}/usr/include/err.h
%{cross_sysroot}/usr/include/errno.h
%{cross_sysroot}/usr/include/error.h
%{cross_sysroot}/usr/include/execinfo.h
%{cross_sysroot}/usr/include/fcntl.h
%{cross_sysroot}/usr/include/features.h
%{cross_sysroot}/usr/include/fenv.h
%{cross_sysroot}/usr/include/fmtmsg.h
%{cross_sysroot}/usr/include/fnmatch.h
%{cross_sysroot}/usr/include/fpu_control.h
%{cross_sysroot}/usr/include/fstab.h
%{cross_sysroot}/usr/include/fts.h
%{cross_sysroot}/usr/include/ftw.h
%{cross_sysroot}/usr/include/gconv.h
%{cross_sysroot}/usr/include/getopt.h
%{cross_sysroot}/usr/include/glob.h
%{cross_sysroot}/usr/include/gnu-versions.h
%dir %{cross_sysroot}/usr/include/gnu
%{cross_sysroot}/usr/include/gnu/lib-names.h
%{cross_sysroot}/usr/include/gnu/libc-version.h
%{cross_sysroot}/usr/include/gnu/stubs.h
%{cross_sysroot}/usr/include/grp.h
%{cross_sysroot}/usr/include/gshadow.h
%{cross_sysroot}/usr/include/iconv.h
%{cross_sysroot}/usr/include/ieee754.h
%{cross_sysroot}/usr/include/ifaddrs.h
%{cross_sysroot}/usr/include/inttypes.h
%{cross_sysroot}/usr/include/langinfo.h
%{cross_sysroot}/usr/include/lastlog.h
%{cross_sysroot}/usr/include/libgen.h
%{cross_sysroot}/usr/include/libintl.h
%{cross_sysroot}/usr/include/limits.h
%{cross_sysroot}/usr/include/link.h
%{cross_sysroot}/usr/include/locale.h
%{cross_sysroot}/usr/include/malloc.h
%{cross_sysroot}/usr/include/math.h
%{cross_sysroot}/usr/include/mcheck.h
%{cross_sysroot}/usr/include/memory.h
%{cross_sysroot}/usr/include/mntent.h
%{cross_sysroot}/usr/include/monetary.h
%{cross_sysroot}/usr/include/mqueue.h
%dir %{cross_sysroot}/usr/include/net
%{cross_sysroot}/usr/include/net/ethernet.h
%{cross_sysroot}/usr/include/net/if.h
%{cross_sysroot}/usr/include/net/if_arp.h
%{cross_sysroot}/usr/include/net/if_packet.h
%{cross_sysroot}/usr/include/net/if_ppp.h
%{cross_sysroot}/usr/include/net/if_shaper.h
%{cross_sysroot}/usr/include/net/if_slip.h
%{cross_sysroot}/usr/include/net/ppp-comp.h
%{cross_sysroot}/usr/include/net/ppp_defs.h
%{cross_sysroot}/usr/include/net/route.h
%dir %{cross_sysroot}/usr/include/netash
%{cross_sysroot}/usr/include/netash/ash.h
%dir %{cross_sysroot}/usr/include/netatalk
%{cross_sysroot}/usr/include/netatalk/at.h
%dir %{cross_sysroot}/usr/include/netax25
%{cross_sysroot}/usr/include/netax25/ax25.h
%{cross_sysroot}/usr/include/netdb.h
%dir %{cross_sysroot}/usr/include/neteconet
%{cross_sysroot}/usr/include/neteconet/ec.h
%dir %{cross_sysroot}/usr/include/netinet
%{cross_sysroot}/usr/include/netinet/ether.h
%{cross_sysroot}/usr/include/netinet/icmp6.h
%{cross_sysroot}/usr/include/netinet/if_ether.h
%{cross_sysroot}/usr/include/netinet/if_fddi.h
%{cross_sysroot}/usr/include/netinet/if_tr.h
%{cross_sysroot}/usr/include/netinet/igmp.h
%{cross_sysroot}/usr/include/netinet/in.h
%{cross_sysroot}/usr/include/netinet/in_systm.h
%{cross_sysroot}/usr/include/netinet/ip.h
%{cross_sysroot}/usr/include/netinet/ip6.h
%{cross_sysroot}/usr/include/netinet/ip_icmp.h
%{cross_sysroot}/usr/include/netinet/tcp.h
%{cross_sysroot}/usr/include/netinet/udp.h
%dir %{cross_sysroot}/usr/include/netipx
%{cross_sysroot}/usr/include/netipx/ipx.h
%dir %{cross_sysroot}/usr/include/netiucv
%{cross_sysroot}/usr/include/netiucv/iucv.h
%dir %{cross_sysroot}/usr/include/netpacket
%{cross_sysroot}/usr/include/netpacket/packet.h
%dir %{cross_sysroot}/usr/include/netrom
%{cross_sysroot}/usr/include/netrom/netrom.h
%dir %{cross_sysroot}/usr/include/netrose
%{cross_sysroot}/usr/include/netrose/rose.h
%dir %{cross_sysroot}/usr/include/nfs
%{cross_sysroot}/usr/include/nfs/nfs.h
%{cross_sysroot}/usr/include/nl_types.h
%{cross_sysroot}/usr/include/nss.h
%{cross_sysroot}/usr/include/obstack.h
%{cross_sysroot}/usr/include/paths.h
%{cross_sysroot}/usr/include/poll.h
%{cross_sysroot}/usr/include/printf.h
%{cross_sysroot}/usr/include/proc_service.h
%dir %{cross_sysroot}/usr/include/protocols
%{cross_sysroot}/usr/include/protocols/routed.h
%{cross_sysroot}/usr/include/protocols/rwhod.h
%{cross_sysroot}/usr/include/protocols/talkd.h
%{cross_sysroot}/usr/include/protocols/timed.h
%{cross_sysroot}/usr/include/pthread.h
%{cross_sysroot}/usr/include/pty.h
%{cross_sysroot}/usr/include/pwd.h
%{cross_sysroot}/usr/include/re_comp.h
%{cross_sysroot}/usr/include/regex.h
%{cross_sysroot}/usr/include/regexp.h
%{cross_sysroot}/usr/include/resolv.h
%dir %{cross_sysroot}/usr/include/rpc
%{cross_sysroot}/usr/include/rpc/netdb.h
%if %{enable_obsolete_rpc}
%{cross_sysroot}/usr/include/rpc/auth_des.h
%{cross_sysroot}/usr/include/rpc/auth.h
%{cross_sysroot}/usr/include/rpc/auth_unix.h
%{cross_sysroot}/usr/include/rpc/clnt.h
%{cross_sysroot}/usr/include/rpc/des_crypt.h
%{cross_sysroot}/usr/include/rpc/key_prot.h
%{cross_sysroot}/usr/include/rpc/pmap_clnt.h
%{cross_sysroot}/usr/include/rpc/pmap_prot.h
%{cross_sysroot}/usr/include/rpc/pmap_rmt.h
%{cross_sysroot}/usr/include/rpc/rpc_des.h
%{cross_sysroot}/usr/include/rpc/rpc.h
%{cross_sysroot}/usr/include/rpc/rpc_msg.h
%{cross_sysroot}/usr/include/rpc/svc_auth.h
%{cross_sysroot}/usr/include/rpc/svc.h
%{cross_sysroot}/usr/include/rpc/types.h
%{cross_sysroot}/usr/include/rpc/xdr.h
%{cross_sysroot}/usr/include/rpcsvc
%endif
%{cross_sysroot}/usr/include/sched.h
%{cross_sysroot}/usr/include/scsi
%{cross_sysroot}/usr/include/search.h
%{cross_sysroot}/usr/include/semaphore.h
%{cross_sysroot}/usr/include/setjmp.h
%{cross_sysroot}/usr/include/sgtty.h
%{cross_sysroot}/usr/include/shadow.h
%{cross_sysroot}/usr/include/signal.h
%{cross_sysroot}/usr/include/spawn.h
%{cross_sysroot}/usr/include/stab.h
%{cross_sysroot}/usr/include/stdc-predef.h
%{cross_sysroot}/usr/include/stdint.h
%{cross_sysroot}/usr/include/stdio.h
%{cross_sysroot}/usr/include/stdio_ext.h
%{cross_sysroot}/usr/include/stdlib.h
%{cross_sysroot}/usr/include/string.h
%{cross_sysroot}/usr/include/strings.h
%{cross_sysroot}/usr/include/stropts.h
%dir %{cross_sysroot}/usr/include/sys
%{cross_sysroot}/usr/include/sys/acct.h
%{cross_sysroot}/usr/include/sys/auxv.h
%{cross_sysroot}/usr/include/sys/bitypes.h
%{cross_sysroot}/usr/include/sys/cdefs.h
%{cross_sysroot}/usr/include/sys/dir.h
%{cross_sysroot}/usr/include/sys/elf.h
%{cross_sysroot}/usr/include/sys/epoll.h
%{cross_sysroot}/usr/include/sys/errno.h
%{cross_sysroot}/usr/include/sys/eventfd.h
%{cross_sysroot}/usr/include/sys/fanotify.h
%{cross_sysroot}/usr/include/sys/fcntl.h
%{cross_sysroot}/usr/include/sys/file.h
%{cross_sysroot}/usr/include/sys/fsuid.h
%{cross_sysroot}/usr/include/sys/gmon.h
%{cross_sysroot}/usr/include/sys/gmon_out.h
%{cross_sysroot}/usr/include/sys/inotify.h
%if %{cross_arch} == "arm"
%{cross_sysroot}/usr/include/sys/io.h
%endif
%{cross_sysroot}/usr/include/sys/ioctl.h
%{cross_sysroot}/usr/include/sys/ipc.h
%{cross_sysroot}/usr/include/sys/kd.h
%{cross_sysroot}/usr/include/sys/klog.h
%{cross_sysroot}/usr/include/sys/mman.h
%{cross_sysroot}/usr/include/sys/mount.h
%{cross_sysroot}/usr/include/sys/msg.h
%{cross_sysroot}/usr/include/sys/mtio.h
%{cross_sysroot}/usr/include/sys/param.h
%{cross_sysroot}/usr/include/sys/pci.h
%{cross_sysroot}/usr/include/sys/personality.h
%{cross_sysroot}/usr/include/sys/poll.h
%{cross_sysroot}/usr/include/sys/prctl.h
%{cross_sysroot}/usr/include/sys/procfs.h
%{cross_sysroot}/usr/include/sys/profil.h
%{cross_sysroot}/usr/include/sys/ptrace.h
%{cross_sysroot}/usr/include/sys/queue.h
%{cross_sysroot}/usr/include/sys/quota.h
%{cross_sysroot}/usr/include/sys/random.h
%{cross_sysroot}/usr/include/sys/raw.h
%{cross_sysroot}/usr/include/sys/reboot.h
%{cross_sysroot}/usr/include/sys/resource.h
%{cross_sysroot}/usr/include/sys/select.h
%{cross_sysroot}/usr/include/sys/sem.h
%{cross_sysroot}/usr/include/sys/sendfile.h
%{cross_sysroot}/usr/include/sys/shm.h
%{cross_sysroot}/usr/include/sys/signal.h
%{cross_sysroot}/usr/include/sys/signalfd.h
%{cross_sysroot}/usr/include/sys/socket.h
%{cross_sysroot}/usr/include/sys/socketvar.h
%{cross_sysroot}/usr/include/sys/soundcard.h
%{cross_sysroot}/usr/include/sys/stat.h
%{cross_sysroot}/usr/include/sys/statfs.h
%{cross_sysroot}/usr/include/sys/statvfs.h
%{cross_sysroot}/usr/include/sys/stropts.h
%{cross_sysroot}/usr/include/sys/swap.h
%{cross_sysroot}/usr/include/sys/syscall.h
%{cross_sysroot}/usr/include/sys/sysctl.h
%{cross_sysroot}/usr/include/sys/sysinfo.h
%{cross_sysroot}/usr/include/sys/syslog.h
%{cross_sysroot}/usr/include/sys/sysmacros.h
%{cross_sysroot}/usr/include/sys/termios.h
%{cross_sysroot}/usr/include/sys/time.h
%{cross_sysroot}/usr/include/sys/timeb.h
%{cross_sysroot}/usr/include/sys/timerfd.h
%{cross_sysroot}/usr/include/sys/times.h
%{cross_sysroot}/usr/include/sys/timex.h
%{cross_sysroot}/usr/include/sys/ttychars.h
%{cross_sysroot}/usr/include/sys/ttydefaults.h
%{cross_sysroot}/usr/include/sys/types.h
%{cross_sysroot}/usr/include/sys/ucontext.h
%{cross_sysroot}/usr/include/sys/uio.h
%{cross_sysroot}/usr/include/sys/un.h
%{cross_sysroot}/usr/include/sys/unistd.h
%{cross_sysroot}/usr/include/sys/user.h
%{cross_sysroot}/usr/include/sys/utsname.h
%{cross_sysroot}/usr/include/sys/vfs.h
%{cross_sysroot}/usr/include/sys/vlimit.h
%{cross_sysroot}/usr/include/sys/vt.h
%{cross_sysroot}/usr/include/sys/vtimes.h
%{cross_sysroot}/usr/include/sys/wait.h
%{cross_sysroot}/usr/include/sys/xattr.h
%{cross_sysroot}/usr/include/syscall.h
%{cross_sysroot}/usr/include/sysexits.h
%{cross_sysroot}/usr/include/syslog.h
%{cross_sysroot}/usr/include/tar.h
%{cross_sysroot}/usr/include/termio.h
%{cross_sysroot}/usr/include/termios.h
%{cross_sysroot}/usr/include/tgmath.h
%{cross_sysroot}/usr/include/thread_db.h
%{cross_sysroot}/usr/include/threads.h
%{cross_sysroot}/usr/include/time.h
%{cross_sysroot}/usr/include/ttyent.h
%{cross_sysroot}/usr/include/uchar.h
%{cross_sysroot}/usr/include/ucontext.h
%{cross_sysroot}/usr/include/ulimit.h
%{cross_sysroot}/usr/include/unistd.h
%{cross_sysroot}/usr/include/utime.h
%{cross_sysroot}/usr/include/utmp.h
%{cross_sysroot}/usr/include/utmpx.h
%{cross_sysroot}/usr/include/values.h
%{cross_sysroot}/usr/include/wait.h
%{cross_sysroot}/usr/include/wchar.h
%{cross_sysroot}/usr/include/wctype.h
%{cross_sysroot}/usr/include/wordexp.h
%{cross_sysroot}/usr/%{lib_dir_name}/crt1.o
%{cross_sysroot}/usr/%{lib_dir_name}/crti.o
%{cross_sysroot}/usr/%{lib_dir_name}/crtn.o
%{cross_sysroot}/usr/%{lib_dir_name}/libc.so
%if !%{headers_only}
%{cross_sysroot}/etc/rpc
%if %{cross_arch} == "arm64"
%{cross_sysroot}/lib/ld-linux%{loader_suffix}.so.%{loader_version}
%else
%{cross_sysroot}/%{lib_dir_name}/ld-linux%{loader_suffix}.so.%{loader_version}
%endif
%{cross_sysroot}/%{lib_dir_name}/ld-%{version}.so
%{cross_sysroot}/%{lib_dir_name}/libBrokenLocale-%{version}.so
%{cross_sysroot}/%{lib_dir_name}/libBrokenLocale.so.1
%{cross_sysroot}/%{lib_dir_name}/libSegFault.so
%{cross_sysroot}/%{lib_dir_name}/libanl-%{version}.so
%{cross_sysroot}/%{lib_dir_name}/libanl.so.1
%{cross_sysroot}/%{lib_dir_name}/libc-%{version}.so
%{cross_sysroot}/%{lib_dir_name}/libc.so.6
%{cross_sysroot}/%{lib_dir_name}/libcrypt-%{version}.so
%{cross_sysroot}/%{lib_dir_name}/libcrypt.so.1
%{cross_sysroot}/%{lib_dir_name}/libdl-%{version}.so
%{cross_sysroot}/%{lib_dir_name}/libdl.so.2
%{cross_sysroot}/%{lib_dir_name}/libm-%{version}.so
%{cross_sysroot}/%{lib_dir_name}/libm.so.6
%{cross_sysroot}/%{lib_dir_name}/libmemusage.so
%{cross_sysroot}/%{lib_dir_name}/libnsl-%{version}.so
%{cross_sysroot}/%{lib_dir_name}/libnsl.so.1
%{cross_sysroot}/%{lib_dir_name}/libnss_compat-%{version}.so
%{cross_sysroot}/%{lib_dir_name}/libnss_compat.so.2
%{cross_sysroot}/%{lib_dir_name}/libnss_db-%{version}.so
%{cross_sysroot}/%{lib_dir_name}/libnss_db.so.2
%{cross_sysroot}/%{lib_dir_name}/libnss_dns-%{version}.so
%{cross_sysroot}/%{lib_dir_name}/libnss_dns.so.2
%{cross_sysroot}/%{lib_dir_name}/libnss_files-%{version}.so
%{cross_sysroot}/%{lib_dir_name}/libnss_files.so.2
%{cross_sysroot}/%{lib_dir_name}/libnss_hesiod-%{version}.so
%{cross_sysroot}/%{lib_dir_name}/libnss_hesiod.so.2
%if %{enable_obsolete_nsl}
%{cross_sysroot}/%{lib_dir_name}/libnss_nis-%{version}.so
%{cross_sysroot}/%{lib_dir_name}/libnss_nis.so.2
%{cross_sysroot}/%{lib_dir_name}/libnss_nisplus-%{version}.so
%{cross_sysroot}/%{lib_dir_name}/libnss_nisplus.so.2
%endif
%{cross_sysroot}/%{lib_dir_name}/libpcprofile.so
%{cross_sysroot}/%{lib_dir_name}/libpthread-%{version}.so
%{cross_sysroot}/%{lib_dir_name}/libpthread.so.0
%{cross_sysroot}/%{lib_dir_name}/libresolv-%{version}.so
%{cross_sysroot}/%{lib_dir_name}/libresolv.so.2
%{cross_sysroot}/%{lib_dir_name}/librt-%{version}.so
%{cross_sysroot}/%{lib_dir_name}/librt.so.1
%{cross_sysroot}/%{lib_dir_name}/libthread_db-1.0.so
%{cross_sysroot}/%{lib_dir_name}/libthread_db.so.1
%{cross_sysroot}/%{lib_dir_name}/libutil-%{version}.so
%{cross_sysroot}/%{lib_dir_name}/libutil.so.1
%{cross_sysroot}/sbin/ldconfig
%{cross_sysroot}/sbin/sln
%{cross_sysroot}/usr/bin/catchsegv
%{cross_sysroot}/usr/bin/gencat
%{cross_sysroot}/usr/bin/getconf
%{cross_sysroot}/usr/bin/getent
%{cross_sysroot}/usr/bin/iconv
%{cross_sysroot}/usr/bin/ldd
%{cross_sysroot}/usr/bin/locale
%{cross_sysroot}/usr/bin/localedef
%{cross_sysroot}/usr/bin/makedb
%{cross_sysroot}/usr/bin/mtrace
%{cross_sysroot}/usr/bin/pcprofiledump
%{cross_sysroot}/usr/bin/pldd
%if %{enable_obsolete_rpc}
%{cross_sysroot}/usr/bin/rpcgen
%endif
%{cross_sysroot}/usr/bin/sotruss
%{cross_sysroot}/usr/bin/sprof
%{cross_sysroot}/usr/bin/tzselect
%{cross_sysroot}/usr/bin/xtrace
%{cross_sysroot}/usr/include/gnu/lib-names%{gnu_hdr_suffix}.h
%{cross_sysroot}/usr/include/gnu/stubs%{gnu_hdr_suffix}.h
%{cross_sysroot}/usr/%{lib_dir_name}/?crt1.o
%{cross_sysroot}/usr/%{lib_dir_name}/audit
%{cross_sysroot}/usr/%{lib_dir_name}/gconv
%{cross_sysroot}/usr/%{lib_dir_name}/libBrokenLocale.a
%{cross_sysroot}/usr/%{lib_dir_name}/libBrokenLocale.so
%{cross_sysroot}/usr/%{lib_dir_name}/libanl.a
%{cross_sysroot}/usr/%{lib_dir_name}/libanl.so
%{cross_sysroot}/usr/%{lib_dir_name}/libc.a
%{cross_sysroot}/usr/%{lib_dir_name}/libc_nonshared.a
%{cross_sysroot}/usr/%{lib_dir_name}/libcrypt.a
%{cross_sysroot}/usr/%{lib_dir_name}/libcrypt.so
%{cross_sysroot}/usr/%{lib_dir_name}/libdl.a
%{cross_sysroot}/usr/%{lib_dir_name}/libdl.so
%{cross_sysroot}/usr/%{lib_dir_name}/libg.a
%{cross_sysroot}/usr/%{lib_dir_name}/libm.a
%{cross_sysroot}/usr/%{lib_dir_name}/libm.so
%{cross_sysroot}/usr/%{lib_dir_name}/libmcheck.a
%if %{enable_obsolete_nsl}
%{cross_sysroot}/usr/%{lib_dir_name}/libnsl.a
%{cross_sysroot}/usr/%{lib_dir_name}/libnsl.so
%endif
%{cross_sysroot}/usr/%{lib_dir_name}/libnss_compat.so
%{cross_sysroot}/usr/%{lib_dir_name}/libnss_db.so
%{cross_sysroot}/usr/%{lib_dir_name}/libnss_dns.so
%{cross_sysroot}/usr/%{lib_dir_name}/libnss_files.so
%{cross_sysroot}/usr/%{lib_dir_name}/libnss_hesiod.so
%if %{enable_obsolete_nsl}
%{cross_sysroot}/usr/%{lib_dir_name}/libnss_nis.so
%{cross_sysroot}/usr/%{lib_dir_name}/libnss_nisplus.so
%endif
%{cross_sysroot}/usr/%{lib_dir_name}/libpthread.a
%{cross_sysroot}/usr/%{lib_dir_name}/libpthread.so
%{cross_sysroot}/usr/%{lib_dir_name}/libresolv.a
%{cross_sysroot}/usr/%{lib_dir_name}/libresolv.so
%if %{enable_obsolete_rpc}
%{cross_sysroot}/usr/%{lib_dir_name}/librpcsvc.a
%endif
%{cross_sysroot}/usr/%{lib_dir_name}/librt.a
%{cross_sysroot}/usr/%{lib_dir_name}/librt.so
%{cross_sysroot}/usr/%{lib_dir_name}/libthread_db.so
%{cross_sysroot}/usr/%{lib_dir_name}/libutil.a
%{cross_sysroot}/usr/%{lib_dir_name}/libutil.so
%dir %{cross_sysroot}/usr/libexec/getconf
%if %{cross_arch} == "arm"
%{cross_sysroot}/usr/libexec/getconf/POSIX_V6_ILP32_OFF32
%{cross_sysroot}/usr/libexec/getconf/POSIX_V6_ILP32_OFFBIG
%{cross_sysroot}/usr/libexec/getconf/POSIX_V7_ILP32_OFF32
%{cross_sysroot}/usr/libexec/getconf/POSIX_V7_ILP32_OFFBIG
%{cross_sysroot}/usr/libexec/getconf/XBS5_ILP32_OFF32
%{cross_sysroot}/usr/libexec/getconf/XBS5_ILP32_OFFBIG
%else
%if %{cross_arch} == "arm64"
%{cross_sysroot}/usr/libexec/getconf/POSIX_V6_LP64_OFF64
%{cross_sysroot}/usr/libexec/getconf/POSIX_V7_LP64_OFF64
%{cross_sysroot}/usr/libexec/getconf/XBS5_LP64_OFF64
%endif
%endif
%{cross_sysroot}/usr/sbin/iconvconfig
%{cross_sysroot}/usr/sbin/nscd
%{cross_sysroot}/usr/sbin/zdump
%{cross_sysroot}/usr/sbin/zic
%dir %{cross_sysroot}/usr/share/i18n
%{cross_sysroot}/usr/share/i18n/charmaps
%{cross_sysroot}/usr/share/i18n/locales
%{cross_sysroot}/var/db/Makefile
%endif


%changelog
* Tue Aug 14 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.28-1
- Update to 2.28
- Disable -Werror for aarch64

* Mon Apr 30 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.27-2
- Disable obsolete Sun RPC and libnsl on Fedora 28 and later

* Mon Feb 26 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.27-1
- Update to 2.27
- Remove -fcf-protection from compiler flags because it needs -m options
- Remove -specs from _hardening_ldflags because it is now used directly
- Remove group tag because it is deprecated in Fedora

* Sun Jan 28 2018 Ting-Wei Lan <lantw44@gmail.com> - 2.26-6
- Remove the unsupported -fstack-clash-protection compiler flag
- Remove the -Wl,-z,defs linker flag to avoid linking failure
- Fix build failure with GNU Binutils 2.30

* Mon Dec 11 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.26-5
- Use configure and make_build macros
- Replace define with global

* Thu Dec 07 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.26-4
- Fix build ID conflict for Fedora 27 and later

* Mon Oct 16 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.26-3
- Rebuilt for Fedora 27 and 28

* Tue Aug 15 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.26-2
- Disable debuginfo package for bootstrap build to fix failure on Fedora 27

* Thu Aug 03 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.26-1
- Update to 2.26

* Mon Jul 03 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.25-3
- Fix build failure with GNU Binutils 2.29

* Mon Jul 03 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.25-2
- Filter provides and requires in cross_sysroot

* Tue Mar 07 2017 Ting-Wei Lan <lantw44@gmail.com> - 2.25-1
- Update to 2.25
- Enable stack protector
- Enable tunables feature

* Sat Sep 10 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.24-2
- Rebuilt for Fedora 25 and 26
- Add perl to BuildRequires because it is required to build mtrace

* Tue Aug 16 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.24-1
- Update to 2.24

* Sun May 08 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.23-3
- Fix GCC 6 build issue

* Thu Mar 03 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.23-2
- Rebuilt for Fedora 24 and 25

* Tue Mar 01 2016 Ting-Wei Lan <lantw44@gmail.com> - 2.23-1
- Update to 2.23

* Mon Dec 28 2015 Ting-Wei Lan <lantw44@gmail.com> - 2.22-5
- Sync configure options with Fedora
- Support arm-linux-gnueabihf and aarch64-linux-gnu

* Sat Dec 05 2015 Ting-Wei Lan <lantw44@gmail.com> - 2.22-4
- Fix the build with dnf on Fedora 24

* Tue Nov 24 2015 Ting-Wei Lan <lantw44@gmail.com> - 2.22-3
- Own the i18n and the getconf directory
- Require the filesystem sub-package

* Sun Nov 22 2015 Ting-Wei Lan <lantw44@gmail.com> - 2.22-2
- Install license files and documentation

* Wed Aug 12 2015 Ting-Wei Lan <lantw44@gmail.com> - 2.22-1
- Update to 2.22

* Tue Jul 28 2015 Ting-Wei Lan <lantw44@gmail.com> - 2.21-3
- Rebuilt for Fedora 23 and 24

* Fri Mar 20 2015 Ting-Wei Lan <lantw44@gmail.com> - 2.21-2
- Rebuilt for Fedora 22 and 23

* Sun Mar 15 2015 Ting-Wei Lan <lantw44@gmail.com> - 2.21-1
- Update to 2.21

* Sun Dec 21 2014 Ting-Wei Lan <lantw44@gmail.com> - 2.20-2
- Pull in %{cross_arch}-kernel-headers

* Fri Dec 19 2014 Ting-Wei Lan <lantw44@gmail.com> - 2.20-1
- Initial packaging
