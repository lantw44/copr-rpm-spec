%define cross_arch      arm
%define cross_triplet   arm-linux-gnueabi
%define cross_sysroot   %{_prefix}/%{cross_triplet}/sys-root

%if 0%{?bootstrap:1}
%define headers_only    1
%define pkg_suffix      -headers
%else
%define headers_only    0
%define pkg_suffix      %{nil}
%endif

Name:       %{cross_triplet}-glibc%{pkg_suffix}
Version:    2.20
Release:    1%{?dist}
Summary:    The GNU C Library (%{cross_triplet}

Group:      Development/Libraries
License:    LGPLv2+ and LGPLv2+ with exceptions and GPLv2+
URL:        https://www.gnu.org/software/libc
Source0:    https://ftp.gnu.org/gnu/glibc/glibc-%{version}.tar.xz

BuildRequires: %{cross_triplet}-gcc-pass1
BuildRequires: %{cross_triplet}-kernel-headers

%if !%{headers_only}
BuildRequires: %{cross_triplet}-gcc-pass2
Provides:   %{cross_triplet}-glibc-headers = %{version}
Obsoletes:  %{cross_triplet}-glibc-headers <= %{version}
%endif

%description


%prep
%setup -qn glibc-%{version}


%build
mkdir -p %{_builddir}/glibc-build
cd %{_builddir}/glibc-build
BUILD_CC=%{_bindir}/gcc \
CC=%{_bindir}/%{cross_triplet}-gcc \
CXX=%{_bindir}/%{cross_triplet}-g++ \
AR=%{_bindir}/%{cross_triplet}-ar \
RANLIB=%{_bindir}/%{cross_triplet}-ranlib \
../glibc-%{version}/configure \
    --prefix=/usr \
    --host=%{cross_triplet} \
    --build=%{_target_platform} \
    --enable-kernel=2.6.32 \
    --enable-shared \
    --enable-add-ons \
    --enable-obsolete-rpc \
    --disable-profile \
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
make %{?_smp_mflags} csu/subdir_lib
%else
make %{?_smp_mflags}
%endif


%install
cd %{_builddir}/glibc-build
%if %{headers_only}
make install-headers install_root=%{buildroot}%{cross_sysroot} \
    install-bootstrap-headers=yes
touch %{buildroot}%{cross_sysroot}/usr/include/gnu/stubs.h
mkdir -p %{buildroot}%{cross_sysroot}/usr/lib
cp csu/crt1.o csu/crti.o csu/crtn.o %{buildroot}%{cross_sysroot}/usr/lib
%{cross_triplet}-gcc -nostdlib -nostartfiles -shared -x c /dev/null \
    -o %{buildroot}%{cross_sysroot}/usr/lib/libc.so
%else
make install install_root=%{buildroot}%{cross_sysroot}
rm -rf %{buildroot}%{cross_sysroot}/usr/share/man
rm -rf %{buildroot}%{cross_sysroot}/usr/share/info
rm -rf %{buildroot}%{cross_sysroot}/usr/share/locale
%endif

# Don't any static archive - based on Fedora Project cross-gcc.spec
%define __ar_no_strip $RPM_BUILD_DIR/glibc-%{version}/ar-no-strip
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
%define __strip %{__ar_no_strip}


%files
%{cross_sysroot}/usr/include/_G_config.h
%{cross_sysroot}/usr/include/a.out.h
%{cross_sysroot}/usr/include/aio.h
%{cross_sysroot}/usr/include/aliases.h
%{cross_sysroot}/usr/include/alloca.h
%{cross_sysroot}/usr/include/ar.h
%{cross_sysroot}/usr/include/argp.h
%{cross_sysroot}/usr/include/argz.h
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
%{cross_sysroot}/usr/include/libio.h
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
%{cross_sysroot}/usr/include/netash/ash.h
%{cross_sysroot}/usr/include/netatalk/at.h
%{cross_sysroot}/usr/include/netax25/ax25.h
%{cross_sysroot}/usr/include/netdb.h
%{cross_sysroot}/usr/include/neteconet/ec.h
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
%{cross_sysroot}/usr/include/netipx/ipx.h
%{cross_sysroot}/usr/include/netiucv/iucv.h
%{cross_sysroot}/usr/include/netpacket/packet.h
%{cross_sysroot}/usr/include/netrom/netrom.h
%{cross_sysroot}/usr/include/netrose/rose.h
%{cross_sysroot}/usr/include/nfs/nfs.h
%{cross_sysroot}/usr/include/nl_types.h
%{cross_sysroot}/usr/include/nss.h
%{cross_sysroot}/usr/include/obstack.h
%{cross_sysroot}/usr/include/paths.h
%{cross_sysroot}/usr/include/poll.h
%{cross_sysroot}/usr/include/printf.h
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
%{cross_sysroot}/usr/include/rpc
%{cross_sysroot}/usr/include/rpcsvc
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
%{cross_sysroot}/usr/include/sys/io.h
%{cross_sysroot}/usr/include/sys/ioctl.h
%{cross_sysroot}/usr/include/sys/ipc.h
%{cross_sysroot}/usr/include/sys/kd.h
%{cross_sysroot}/usr/include/sys/kdaemon.h
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
%{cross_sysroot}/usr/include/sys/ultrasound.h
%{cross_sysroot}/usr/include/sys/un.h
%{cross_sysroot}/usr/include/sys/unistd.h
%{cross_sysroot}/usr/include/sys/user.h
%{cross_sysroot}/usr/include/sys/ustat.h
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
%{cross_sysroot}/usr/include/time.h
%{cross_sysroot}/usr/include/ttyent.h
%{cross_sysroot}/usr/include/uchar.h
%{cross_sysroot}/usr/include/ucontext.h
%{cross_sysroot}/usr/include/ulimit.h
%{cross_sysroot}/usr/include/unistd.h
%{cross_sysroot}/usr/include/ustat.h
%{cross_sysroot}/usr/include/utime.h
%{cross_sysroot}/usr/include/utmp.h
%{cross_sysroot}/usr/include/utmpx.h
%{cross_sysroot}/usr/include/values.h
%{cross_sysroot}/usr/include/wait.h
%{cross_sysroot}/usr/include/wchar.h
%{cross_sysroot}/usr/include/wctype.h
%{cross_sysroot}/usr/include/wordexp.h
%{cross_sysroot}/usr/include/xlocale.h
%{cross_sysroot}/usr/lib/crt1.o
%{cross_sysroot}/usr/lib/crti.o
%{cross_sysroot}/usr/lib/crtn.o
%{cross_sysroot}/usr/lib/libc.so
%if !%{headers_only}
%{cross_sysroot}/etc/rpc
%{cross_sysroot}/lib/ld-%{version}.so
%{cross_sysroot}/lib/ld-linux.so.3
%{cross_sysroot}/lib/libBrokenLocale-%{version}.so
%{cross_sysroot}/lib/libBrokenLocale.so.1
%{cross_sysroot}/lib/libSegFault.so
%{cross_sysroot}/lib/libanl-%{version}.so
%{cross_sysroot}/lib/libanl.so.1
%{cross_sysroot}/lib/libc-%{version}.so
%{cross_sysroot}/lib/libc.so.6
%{cross_sysroot}/lib/libcidn-%{version}.so
%{cross_sysroot}/lib/libcidn.so.1
%{cross_sysroot}/lib/libcrypt-%{version}.so
%{cross_sysroot}/lib/libcrypt.so.1
%{cross_sysroot}/lib/libdl-%{version}.so
%{cross_sysroot}/lib/libdl.so.2
%{cross_sysroot}/lib/libm-%{version}.so
%{cross_sysroot}/lib/libm.so.6
%{cross_sysroot}/lib/libmemusage.so
%{cross_sysroot}/lib/libnsl-%{version}.so
%{cross_sysroot}/lib/libnsl.so.1
%{cross_sysroot}/lib/libnss_compat-%{version}.so
%{cross_sysroot}/lib/libnss_compat.so.2
%{cross_sysroot}/lib/libnss_db-%{version}.so
%{cross_sysroot}/lib/libnss_db.so.2
%{cross_sysroot}/lib/libnss_dns-%{version}.so
%{cross_sysroot}/lib/libnss_dns.so.2
%{cross_sysroot}/lib/libnss_files-%{version}.so
%{cross_sysroot}/lib/libnss_files.so.2
%{cross_sysroot}/lib/libnss_hesiod-%{version}.so
%{cross_sysroot}/lib/libnss_hesiod.so.2
%{cross_sysroot}/lib/libnss_nis-%{version}.so
%{cross_sysroot}/lib/libnss_nis.so.2
%{cross_sysroot}/lib/libnss_nisplus-%{version}.so
%{cross_sysroot}/lib/libnss_nisplus.so.2
%{cross_sysroot}/lib/libpcprofile.so
%{cross_sysroot}/lib/libpthread-%{version}.so
%{cross_sysroot}/lib/libpthread.so.0
%{cross_sysroot}/lib/libresolv-%{version}.so
%{cross_sysroot}/lib/libresolv.so.2
%{cross_sysroot}/lib/librt-%{version}.so
%{cross_sysroot}/lib/librt.so.1
%{cross_sysroot}/lib/libthread_db-1.0.so
%{cross_sysroot}/lib/libthread_db.so.1
%{cross_sysroot}/lib/libutil-%{version}.so
%{cross_sysroot}/lib/libutil.so.1
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
%{cross_sysroot}/usr/bin/rpcgen
%{cross_sysroot}/usr/bin/sotruss
%{cross_sysroot}/usr/bin/sprof
%{cross_sysroot}/usr/bin/tzselect
%{cross_sysroot}/usr/bin/xtrace
%{cross_sysroot}/usr/include/gnu/stubs-soft.h
%{cross_sysroot}/usr/lib/?crt1.o
%{cross_sysroot}/usr/lib/audit
%{cross_sysroot}/usr/lib/gconv
%{cross_sysroot}/usr/lib/libBrokenLocale.a
%{cross_sysroot}/usr/lib/libBrokenLocale.so
%{cross_sysroot}/usr/lib/libanl.a
%{cross_sysroot}/usr/lib/libanl.so
%{cross_sysroot}/usr/lib/libc.a
%{cross_sysroot}/usr/lib/libc_nonshared.a
%{cross_sysroot}/usr/lib/libcidn.so
%{cross_sysroot}/usr/lib/libcrypt.a
%{cross_sysroot}/usr/lib/libcrypt.so
%{cross_sysroot}/usr/lib/libdl.a
%{cross_sysroot}/usr/lib/libdl.so
%{cross_sysroot}/usr/lib/libg.a
%{cross_sysroot}/usr/lib/libieee.a
%{cross_sysroot}/usr/lib/libm.a
%{cross_sysroot}/usr/lib/libm.so
%{cross_sysroot}/usr/lib/libmcheck.a
%{cross_sysroot}/usr/lib/libnsl.a
%{cross_sysroot}/usr/lib/libnsl.so
%{cross_sysroot}/usr/lib/libnss_compat.so
%{cross_sysroot}/usr/lib/libnss_db.so
%{cross_sysroot}/usr/lib/libnss_dns.so
%{cross_sysroot}/usr/lib/libnss_files.so
%{cross_sysroot}/usr/lib/libnss_hesiod.so
%{cross_sysroot}/usr/lib/libnss_nis.so
%{cross_sysroot}/usr/lib/libnss_nisplus.so
%{cross_sysroot}/usr/lib/libpthread.a
%{cross_sysroot}/usr/lib/libpthread.so
%{cross_sysroot}/usr/lib/libpthread_nonshared.a
%{cross_sysroot}/usr/lib/libresolv.a
%{cross_sysroot}/usr/lib/libresolv.so
%{cross_sysroot}/usr/lib/librpcsvc.a
%{cross_sysroot}/usr/lib/librt.a
%{cross_sysroot}/usr/lib/librt.so
%{cross_sysroot}/usr/lib/libthread_db.so
%{cross_sysroot}/usr/lib/libutil.a
%{cross_sysroot}/usr/lib/libutil.so
%{cross_sysroot}/usr/libexec/getconf/POSIX_V6_ILP32_OFF32
%{cross_sysroot}/usr/libexec/getconf/POSIX_V6_ILP32_OFFBIG
%{cross_sysroot}/usr/libexec/getconf/POSIX_V7_ILP32_OFF32
%{cross_sysroot}/usr/libexec/getconf/POSIX_V7_ILP32_OFFBIG
%{cross_sysroot}/usr/libexec/getconf/XBS5_ILP32_OFF32
%{cross_sysroot}/usr/libexec/getconf/XBS5_ILP32_OFFBIG
%{cross_sysroot}/usr/sbin/iconvconfig
%{cross_sysroot}/usr/sbin/nscd
%{cross_sysroot}/usr/sbin/zdump
%{cross_sysroot}/usr/sbin/zic
%{cross_sysroot}/usr/share/i18n/charmaps
%{cross_sysroot}/usr/share/i18n/locales
%{cross_sysroot}/var/db/Makefile
%endif


%changelog
* Fri Dec 19 2014 Ting-Wei Lan <lantw44@gmail.com> - 2.20-1
- Initial packaging
