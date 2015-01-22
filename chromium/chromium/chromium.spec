# This spec file is based on other spec files and PKGBUILDs available from
#  [1] https://repos.fedorapeople.org/repos/spot/chromium/
#  [2] https://copr.fedoraproject.org/coprs/churchyard/chromium-russianfedora-tested/
#  [3] https://www.archlinux.org/packages/extra/x86_64/chromium/

# Get the version number of latest stable version
# $ curl -s 'http://omahaproxy.appspot.com/all?os=linux&channel=stable' | sed 1d | cut -d , -f 3

Name:       chromium
Version:    40.0.2214.91
Release:    1%{?dist}
Summary:    An open-source project that aims to build a safer, faster, and more stable browser

Group:      Applications/Internet
License:    BSD and LGPLv2+
URL:        http://www.chromium.org
Source0:    http://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz

# The following two source files are copied and modified from
# https://repos.fedorapeople.org/repos/spot/chromium/
Source1:    chromium-browser.sh
Source2:    chromium-browser.desktop

# I don't have time to test whether it work on other architectures
ExclusiveArch: x86_64

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
BuildRequires: libicu-devel
BuildRequires: jsoncpp-devel
BuildRequires: libevent-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libpng-devel
# libvpx 1.3.0 is still too old to build chromium
# BuildRequires: libvpx-devel
BuildRequires: libwebp-devel
BuildRequires: openssl-devel
BuildRequires: opus-devel
BuildRequires: snappy-devel
BuildRequires: speex-devel
BuildRequires: zlib-devel
# linux_link_*
BuildRequires: brlapi-devel
BuildRequires: gpsd-devel
BuildRequires: pciutils-devel
BuildRequires: speech-dispatcher-devel
BuildRequires: pulseaudio-libs-devel
# install desktop files
BuildRequires: desktop-file-utils
Requires:   desktop-file-utils
Requires:   hicolor-icon-theme


%description


%prep
%setup -q


%build
./build/linux/unbundle/replace_gyp_files.py \
    -Duse_system_expat=1 \
    -Duse_system_flac=1 \
    -Duse_system_harfbuzz=1 \
    -Duse_system_icu=1 \
    -Duse_system_jsoncpp=1 \
    -Duse_system_libevent=1 \
    -Duse_system_libjpeg=1 \
    -Duse_system_libpng=1 \
    -Duse_system_libvpx=0 \
    -Duse_system_libwebp=1 \
    -Duse_system_opus=1 \
    -Duse_system_snappy=1 \
    -Duse_system_speex=1 \
    -Duse_system_zlib=1

GYP_GENERATORS=ninja ./build/gyp_chromium --depth=. \
    -Duse_system_expat=1 \
    -Duse_system_flac=1 \
    -Duse_system_harfbuzz=1 \
    -Duse_system_icu=1 \
    -Duse_system_jsoncpp=1 \
    -Duse_system_libevent=1 \
    -Duse_system_libjpeg=1 \
    -Duse_system_libpng=1 \
    -Duse_system_libvpx=0 \
    -Duse_system_libwebp=1 \
    -Duse_system_opus=1 \
    -Duse_system_snappy=1 \
    -Duse_system_speex=1 \
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
    -Dicu_use_data_file_flag=0 \
    -Dlibspeechd_h_prefix=speech-dispatcher/ \
    -Dclang=0 \
    -Dwerror= \
    -Ddisable_fatal_linker_warnings=1 \
    -Dgoogle_api_key=AIzaSyCcK3laItm4Ik9bm6IeGFC6tVgy4eut0_o \
    -Dgoogle_default_client_id=82546407293.apps.googleusercontent.com \
    -Dgoogle_default_client_secret=GuvPB069ONrHxN7Y_y0txLKn \

./build/download_nacl_toolchains.py --packages \
    nacl_x86_glibc,nacl_x86_newlib,pnacl_newlib,pnacl_translator

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
install -m 755 out/Release/libffmpegsumo.so %{buildroot}%{chromiumdir}/
install -m 755 out/Release/libpdf.so %{buildroot}%{chromiumdir}/
install -m 755 out/Release/nacl_helper %{buildroot}%{chromiumdir}/
install -m 755 out/Release/nacl_helper_bootstrap %{buildroot}%{chromiumdir}/
install -m 644 out/Release/nacl_irt_x86_64.nexe %{buildroot}%{chromiumdir}/
install -m 644 out/Release/*.pak %{buildroot}%{chromiumdir}/
install -m 644 out/Release/locales/*.pak %{buildroot}%{chromiumdir}/locales/
for i in 22 24 32 48 64 128 256; do
    if [ ${i} = 32 ]; then ext=xpm; else ext=png; fi
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
    install -m 644 chrome/app/theme/chromium/product_logo_$i.${ext} \
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
%{chromiumdir}/chromium-browser
%{chromiumdir}/chrome-sandbox
%{chromiumdir}/chromedriver
%{chromiumdir}/libffmpegsumo.so
%{chromiumdir}/libpdf.so
%{chromiumdir}/nacl_helper
%{chromiumdir}/nacl_helper_bootstrap
%{chromiumdir}/nacl_irt_x86_64.nexe
%{chromiumdir}/*.pak
%{chromiumdir}/locales/*.pak
%doc LICENSE AUTHORS



%changelog
* Thu Jan 22 2015 - Ting-Wei Lan <lantw44@gmail.com> - 40.0.2214.91-1
- Update to 40.0.2214.91

* Wed Jan 14 2015 - Ting-Wei Lan <lantw44@gmail.com> - 39.0.2171.99-1
- Update to 39.0.2171.99

* Sat Jan 03 2015 - Ting-Wei Lan <lantw44@gmail.com> - 39.0.2171.95-2
- Make sure that GNOME shell obtains correct application name from the
  chromium-browser.desktop file.

* Fri Jan 02 2015 - Ting-Wei Lan <lantw44@gmail.com> - 39.0.2171.95-1
- Initial packaging
