# This spec file is based on other spec files and PKGBUILDs available from
#  [1] https://repos.fedorapeople.org/repos/spot/chromium/
#  [2] https://copr.fedoraproject.org/coprs/churchyard/chromium-russianfedora-tested/
#  [3] https://www.archlinux.org/packages/extra/x86_64/chromium/

# Get the version number of latest stable version
# $ curl -s 'https://omahaproxy.appspot.com/all?os=linux&channel=stable' | sed 1d | cut -d , -f 3

Name:       chromium
Version:    48.0.2564.116
Release:    1%{?dist}
Summary:    An open-source project that aims to build a safer, faster, and more stable browser

Group:      Applications/Internet
License:    BSD and LGPLv2+
URL:        https://www.chromium.org
Source0:    https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz

# The following two source files are copied and modified from
# https://repos.fedorapeople.org/repos/spot/chromium/
Source1:    chromium-browser.sh
Source2:    chromium-browser.desktop

# Add a patch from Arch Linux
# https://code.google.com/p/chromium/issues/detail?id=480415
# https://projects.archlinux.org/svntogit/packages.git/commit/trunk?h=packages/chromium&id=37c3842
Patch0:     chromium-fix-print-preview-on-en_GB-locale.patch

# Add another patch from Arch Linux to fix icu 56 build issue
# https://projects.archlinux.org/svntogit/packages.git/commit/trunk?h=packages/chromium&id=d820900
Patch1:     chromium-use-non-versioned-icu-namespace.patch

# I don't have time to test whether it work on other architectures
ExclusiveArch: x86_64

# Make sure we don't encounter GCC 5.1 bug
%if 0%{?fedora} >= 22
BuildRequires: gcc >= 5.1.1-2
%endif
# Basic tools and libraries
BuildRequires: ninja-build, bison, gperf
BuildRequires: libgcc(x86-32), glibc(x86-32)
BuildRequires: libcap-devel, cups-devel, minizip-devel, alsa-lib-devel
BuildRequires: pkgconfig(gtk+-2.0), pkgconfig(libexif), pkgconfig(nss)
BuildRequires: pkgconfig(xtst), pkgconfig(xscrnsaver)
BuildRequires: pkgconfig(dbus-1), pkgconfig(libudev)
BuildRequires: pkgconfig(gnome-keyring-1)
# use_system_*
BuildRequires: expat-devel
BuildRequires: flac-devel
BuildRequires: harfbuzz-devel
# Chromium requires icu 55
%if 0%{?fedora} >= 24
BuildRequires: libicu-devel
%endif
BuildRequires: jsoncpp-devel
BuildRequires: libevent-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libpng-devel
# Chromium requires libvpx 1.5.0 and some non-default options
# BuildRequires: libvpx-devel
BuildRequires: libwebp-devel
BuildRequires: pkgconfig(libxslt), pkgconfig(libxml-2.0)
BuildRequires: openssl-devel
BuildRequires: opus-devel
BuildRequires: snappy-devel
BuildRequires: speex-devel
BuildRequires: yasm
BuildRequires: zlib-devel
# linux_link_*
BuildRequires: brlapi-devel
BuildRequires: gpsd-devel
BuildRequires: pciutils-devel
BuildRequires: speech-dispatcher-devel
BuildRequires: pulseaudio-libs-devel
# install desktop files
BuildRequires: desktop-file-utils
Requires(post):   desktop-file-utils
Requires(postun): desktop-file-utils
Requires:         hicolor-icon-theme


%description


%prep
%autosetup -p1
touch chrome/test/data/webui/i18n_process_css_test.html
# https://code.google.com/p/chromium/issues/detail?id=541273
# https://projects.archlinux.org/svntogit/packages.git/commit/trunk?h=packages/chromium&id=37c3842
sed -i "/'target_name': 'libvpx'/s/libvpx/&_new/" build/linux/unbundle/libvpx.gyp

%build
./build/linux/unbundle/replace_gyp_files.py \
    -Duse_system_expat=1 \
    -Duse_system_flac=1 \
    -Duse_system_harfbuzz=1 \
%if 0%{?fedora} >= 24
    -Duse_system_icu=1 \
%else
    -Duse_system_icu=0 \
%endif
    -Duse_system_jsoncpp=1 \
    -Duse_system_libevent=1 \
    -Duse_system_libjpeg=1 \
    -Duse_system_libpng=1 \
    -Duse_system_libvpx=0 \
    -Duse_system_libwebp=1 \
    -Duse_system_libxml=1 \
    -Duse_system_opus=1 \
    -Duse_system_snappy=1 \
    -Duse_system_speex=1 \
    -Duse_system_yasm=1 \
    -Duse_system_zlib=1

%if 0%{?fedora} >= 24
find third_party/icu -type f '!' -regex '.*\.\(gyp\|gypi\|isolate\)' -delete
%endif

GYP_GENERATORS=ninja ./build/gyp_chromium --depth=. \
    -Duse_system_expat=1 \
    -Duse_system_flac=1 \
    -Duse_system_harfbuzz=1 \
%if 0%{?fedora} >= 24
    -Duse_system_icu=1 \
%else
    -Duse_system_icu=0 \
%endif
    -Duse_system_jsoncpp=1 \
    -Duse_system_libevent=1 \
    -Duse_system_libjpeg=1 \
    -Duse_system_libpng=1 \
    -Duse_system_libvpx=0 \
    -Duse_system_libwebp=1 \
    -Duse_system_libxml=1 \
    -Duse_system_opus=1 \
    -Duse_system_snappy=1 \
    -Duse_system_speex=1 \
    -Duse_system_yasm=1 \
    -Duse_system_zlib=1 \
    -Duse_gconf=0 \
    -Dlinux_use_bundled_gold=0 \
    -Dlinux_use_bundled_binutils=0 \
    -Dlinux_link_gsettings=1 \
    -Dlinux_link_kerberos=1 \
    -Dlinux_link_libbrlapi=1 \
    -Dlinux_link_libgps=1 \
    -Dlinux_link_libpci=1 \
    -Dlinux_link_libspeechd=1 \
    -Dlinux_link_pulseaudio=1 \
%if 0%{?fedora} >= 24
    -Dicu_use_data_file_flag=0 \
%else
    -Dicu_use_data_file_flag=1 \
%endif
    -Dlibspeechd_h_prefix=speech-dispatcher/ \
    -Dclang=0 \
    -Dwerror= \
    -Ddisable_fatal_linker_warnings=1 \
    -Denable_hotwording=0 \
    -Dlogging_like_official_build=1 \
    -Dtracing_like_official_build=1 \
    -Dfieldtrial_testing_like_official_build=1 \
    -Dgoogle_api_key=AIzaSyCcK3laItm4Ik9bm6IeGFC6tVgy4eut0_o \
    -Dgoogle_default_client_id=82546407293.apps.googleusercontent.com \
    -Dgoogle_default_client_secret=GuvPB069ONrHxN7Y_y0txLKn \

./build/download_nacl_toolchains.py --packages \
    nacl_x86_glibc,nacl_x86_newlib,pnacl_newlib,pnacl_translator sync --extract

ninja-build -C out/Release chrome chrome_sandbox chromedriver


%install
%define chromiumdir %{_libdir}/chromium-browser
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{chromiumdir}/locales
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_datadir}/applications
sed -e "s|@@CHROMIUMDIR@@|%{chromiumdir}|" -e "s|@@BUILDTARGET@@|`cat /etc/redhat-release`|" \
    %{SOURCE1} > chromium-browser.sh
install -m 755 chromium-browser.sh %{buildroot}%{_bindir}/chromium-browser
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE2}
install -m 644 out/Release/chrome.1 %{buildroot}%{_mandir}/man1/chromium-browser.1
install -m 755 out/Release/chrome %{buildroot}%{chromiumdir}/chromium-browser
install -m 4755 out/Release/chrome_sandbox %{buildroot}%{chromiumdir}/chrome-sandbox
install -m 755 out/Release/chromedriver %{buildroot}%{chromiumdir}/
%if 0%{?fedora} < 24
install -m 644 out/Release/icudtl.dat %{buildroot}%{chromiumdir}/
%endif
install -m 755 out/Release/nacl_helper %{buildroot}%{chromiumdir}/
install -m 755 out/Release/nacl_helper_bootstrap %{buildroot}%{chromiumdir}/
install -m 644 out/Release/nacl_irt_x86_64.nexe %{buildroot}%{chromiumdir}/
install -m 644 out/Release/natives_blob.bin %{buildroot}%{chromiumdir}/
install -m 644 out/Release/snapshot_blob.bin %{buildroot}%{chromiumdir}/
install -m 644 out/Release/*.pak %{buildroot}%{chromiumdir}/
install -m 644 out/Release/locales/*.pak %{buildroot}%{chromiumdir}/locales/
for i in 22 24 32 48 64 128 256; do
    if [ ${i} = 32 ]; then ext=xpm; else ext=png; fi
    if [ ${i} = 32 ]; then dir=linux/; else dir=; fi
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
    install -m 644 chrome/app/theme/chromium/${dir}product_logo_$i.${ext} \
        %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/chromium-browser.${ext}
done


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%{_bindir}/chromium-browser
%{_datadir}/applications/chromium-browser.desktop
%{_datadir}/icons/hicolor/22x22/apps/chromium-browser.png
%{_datadir}/icons/hicolor/24x24/apps/chromium-browser.png
%{_datadir}/icons/hicolor/32x32/apps/chromium-browser.xpm
%{_datadir}/icons/hicolor/48x48/apps/chromium-browser.png
%{_datadir}/icons/hicolor/64x64/apps/chromium-browser.png
%{_datadir}/icons/hicolor/128x128/apps/chromium-browser.png
%{_datadir}/icons/hicolor/256x256/apps/chromium-browser.png
%{_mandir}/man1/chromium-browser.1.gz
%dir %{chromiumdir}
%{chromiumdir}/chromium-browser
%{chromiumdir}/chrome-sandbox
%{chromiumdir}/chromedriver
%if 0%{?fedora} < 24
%{chromiumdir}/icudtl.dat
%endif
%{chromiumdir}/nacl_helper
%{chromiumdir}/nacl_helper_bootstrap
%{chromiumdir}/nacl_irt_x86_64.nexe
%{chromiumdir}/natives_blob.bin
%{chromiumdir}/snapshot_blob.bin
%{chromiumdir}/*.pak
%dir %{chromiumdir}/locales
%{chromiumdir}/locales/*.pak
%license LICENSE
%doc AUTHORS



%changelog
* Fri Feb 19 2016 - Ting-Wei Lan <lantw44@gmail.com> - 48.0.2564.116-1
- Update to 48.0.2564.116

* Wed Feb 10 2016 - Ting-Wei Lan <lantw44@gmail.com> - 48.0.2564.109-1
- Update to 48.0.2564.109

* Fri Feb 05 2016 - Ting-Wei Lan <lantw44@gmail.com> - 48.0.2564.103-1
- Update to 48.0.2564.103

* Thu Jan 28 2016 - Ting-Wei Lan <lantw44@gmail.com> - 48.0.2564.97-1
- Update to 48.0.2564.97

* Sat Jan 23 2016 - Ting-Wei Lan <lantw44@gmail.com> - 48.0.2564.82-2
- Fix build issue for icu 56
- Use autosetup macro

* Thu Jan 21 2016 - Ting-Wei Lan <lantw44@gmail.com> - 48.0.2564.82-1
- Update to 48.0.2564.82

* Thu Jan 14 2016 - Ting-Wei Lan <lantw44@gmail.com> - 47.0.2526.111-1
- Update to 47.0.2526.111

* Wed Dec 16 2015 - Ting-Wei Lan <lantw44@gmail.com> - 47.0.2526.106-1
- Update to 47.0.2526.106

* Wed Dec 09 2015 - Ting-Wei Lan <lantw44@gmail.com> - 47.0.2526.80-1
- Update to 47.0.2526.80

* Wed Dec 02 2015 - Ting-Wei Lan <lantw44@gmail.com> - 47.0.2526.73-2
- Apply patch that fixes print preview with the en_GB locale

* Wed Dec 02 2015 - Ting-Wei Lan <lantw44@gmail.com> - 47.0.2526.73-1
- Update to 47.0.2526.73

* Fri Nov 13 2015 - Ting-Wei Lan <lantw44@gmail.com> - 46.0.2490.86-2
- Use system icu on Fedora 24 or later

* Wed Nov 11 2015 - Ting-Wei Lan <lantw44@gmail.com> - 46.0.2490.86-1
- Update to 46.0.2490.86

* Fri Oct 23 2015 - Ting-Wei Lan <lantw44@gmail.com> - 46.0.2490.80-1
- Update to 46.0.2490.80

* Wed Oct 14 2015 - Ting-Wei Lan <lantw44@gmail.com> - 46.0.2490.71-1
- Update to 46.0.2490.71
- Make desktop-file-utils dependency more correct
- Own directories that are only used by this package

* Fri Sep 25 2015 - Ting-Wei Lan <lantw44@gmail.com> - 45.0.2454.101-1
- Update to 45.0.2454.101

* Tue Sep 22 2015 - Ting-Wei Lan <lantw44@gmail.com> - 45.0.2454.99-1
- Update to 45.0.2454.99

* Wed Sep 16 2015 - Ting-Wei Lan <lantw44@gmail.com> - 45.0.2454.93-1
- Update to 45.0.2454.93

* Wed Sep 02 2015 - Ting-Wei Lan <lantw44@gmail.com> - 45.0.2454.85-1
- Update to 45.0.2454.85
- Temporarily disable the use of system libvpx because it needs libvpx 1.4.0

* Sun Aug 23 2015 - Ting-Wei Lan <lantw44@gmail.com> - 44.0.2403.157-2
- Fix GLIBC 2.22 build issue on Fedora 23 and later

* Fri Aug 21 2015 - Ting-Wei Lan <lantw44@gmail.com> - 44.0.2403.157-1
- Update to 44.0.2403.157

* Wed Aug 12 2015 - Ting-Wei Lan <lantw44@gmail.com> - 44.0.2403.155-1
- Update to 44.0.2403.155

* Wed Aug 05 2015 - Ting-Wei Lan <lantw44@gmail.com> - 44.0.2403.130-1
- Update to 44.0.2403.130

* Thu Jul 30 2015 - Ting-Wei Lan <lantw44@gmail.com> - 44.0.2403.125-1
- Update to 44.0.2403.125

* Sat Jul 25 2015 - Ting-Wei Lan <lantw44@gmail.com> - 44.0.2403.107-1
- Update to 44.0.2403.107

* Thu Jul 23 2015 - Ting-Wei Lan <lantw44@gmail.com> - 44.0.2403.89-1
- Update to 44.0.2403.89
- Temporarily disable the use of system icu because it needs icu 55

* Wed Jul 15 2015 - Ting-Wei Lan <lantw44@gmail.com> - 43.0.2357.134-1
- Update to 43.0.2357.134

* Wed Jul 08 2015 - Ting-Wei Lan <lantw44@gmail.com> - 43.0.2357.132-1
- Update to 43.0.2357.132

* Wed Jun 24 2015 - Ting-Wei Lan <lantw44@gmail.com> - 43.0.2357.130-2
- Remove workaround for GCC 5.1
- Disable 'Ok Google' hotwording feature

* Tue Jun 23 2015 - Ting-Wei Lan <lantw44@gmail.com> - 43.0.2357.130-1
- Update to 43.0.2357.130

* Fri Jun 12 2015 - Ting-Wei Lan <lantw44@gmail.com> - 43.0.2357.125-1
- Update to 43.0.2357.125

* Wed Jun 10 2015 - Ting-Wei Lan <lantw44@gmail.com> - 43.0.2357.124-1
- Update to 43.0.2357.124

* Tue May 26 2015 - Ting-Wei Lan <lantw44@gmail.com> - 43.0.2357.81-2
- Revert the clang build because it causes C++11 ABI problems on Fedora 23
- Workaround GCC 5.1 issues by using C++03 mode to compile problematic files
- Workaround GCC 5.1 issues by replacing wrong signed integer usage

* Tue May 26 2015 - Ting-Wei Lan <lantw44@gmail.com> - 43.0.2357.81-1
- Update to 43.0.2357.81

* Tue May 26 2015 - Ting-Wei Lan <lantw44@gmail.com> - 43.0.2357.65-2
- Workaround GCC 5.1 issues by compiling with clang on Fedora 22 or later
- Unbundle libvpx on Fedora 23 or later

* Wed May 20 2015 - Ting-Wei Lan <lantw44@gmail.com> - 43.0.2357.65-1
- Update to 43.0.2357.65

* Sun May 17 2015 - Ting-Wei Lan <lantw44@gmail.com> - 42.0.2311.135-2
- Use license marco to install the license file

* Wed Apr 29 2015 - Ting-Wei Lan <lantw44@gmail.com> - 42.0.2311.135-1
- Update to 42.0.2311.135

* Thu Apr 02 2015 - Ting-Wei Lan <lantw44@gmail.com> - 42.0.2311.90-1
- Update to 42.0.2311.90

* Thu Apr 02 2015 - Ting-Wei Lan <lantw44@gmail.com> - 41.0.2272.118-1
- Update to 41.0.2272.118

* Fri Mar 20 2015 - Ting-Wei Lan <lantw44@gmail.com> - 41.0.2272.101-1
- Update to 41.0.2272.101

* Wed Mar 11 2015 - Ting-Wei Lan <lantw44@gmail.com> - 41.0.2272.89-1
- Update to 41.0.2272.89

* Wed Mar 04 2015 - Ting-Wei Lan <lantw44@gmail.com> - 41.0.2272.76-1
- Update to 41.0.2272.76

* Sat Feb 21 2015 - Ting-Wei Lan <lantw44@gmail.com> - 40.0.2214.115-1
- Update to 40.0.2214.115

* Fri Feb 06 2015 - Ting-Wei Lan <lantw44@gmail.com> - 40.0.2214.111-1
- Update to 40.0.2214.111

* Thu Feb 05 2015 - Ting-Wei Lan <lantw44@gmail.com> - 40.0.2214.95-1
- Update to 40.0.2214.95

* Fri Jan 30 2015 - Ting-Wei Lan <lantw44@gmail.com> - 40.0.2214.94-1
- Update to 40.0.2214.94

* Tue Jan 27 2015 - Ting-Wei Lan <lantw44@gmail.com> - 40.0.2214.93-1
- Update to 40.0.2214.93

* Thu Jan 22 2015 - Ting-Wei Lan <lantw44@gmail.com> - 40.0.2214.91-1
- Update to 40.0.2214.91

* Wed Jan 14 2015 - Ting-Wei Lan <lantw44@gmail.com> - 39.0.2171.99-1
- Update to 39.0.2171.99

* Sat Jan 03 2015 - Ting-Wei Lan <lantw44@gmail.com> - 39.0.2171.95-2
- Make sure that GNOME shell obtains correct application name from the
  chromium-browser.desktop file.

* Fri Jan 02 2015 - Ting-Wei Lan <lantw44@gmail.com> - 39.0.2171.95-1
- Initial packaging
