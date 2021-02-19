# This spec file is based on other spec files, ebuilds, PKGBUILDs available from
#  [1] https://repos.fedorapeople.org/repos/spot/chromium/
#  [2] https://copr.fedoraproject.org/coprs/churchyard/chromium-russianfedora-tested/
#  [3] https://www.archlinux.org/packages/extra/x86_64/chromium/
#  [4] https://src.fedoraproject.org/rpms/chromium/
#  [5] https://gitweb.gentoo.org/repo/gentoo.git/tree/www-client/chromium/

# Get the version number of latest stable version
# $ curl -s 'https://omahaproxy.appspot.com/all?os=linux&channel=stable' | sed 1d | cut -d , -f 3

# Require harfbuzz >= 2.4.0 for hb_subset_input_set_retain_gids
%if 0%{?fedora} >= 31
%bcond_without system_harfbuzz
%else
%bcond_with system_harfbuzz
%endif

# Require libxml2 > 2.9.4 for XML_PARSE_NOXXE
%bcond_without system_libxml2

# Python 2 libraries
%if 0%{?fedora} < 32
%bcond_without system_beautifulsoup4
%bcond_without system_html5lib
%bcond_without system_ply
%else
%bcond_with system_beautifulsoup4
%bcond_with system_html5lib
%bcond_with system_ply
%endif

# Requires re2 2016.07.21 for re2::LazyRE2
%bcond_with system_re2

# Allow testing whether icu can be unbundled
%bcond_with system_libicu

# Allow testing whether libvpx can be unbundled
%bcond_with system_libvpx

# Allow building with symbols to ease debugging
# Enabled by default because Fedora Copr has enough memory
%bcond_without symbol

# Allow compiling with clang
# Disabled by default becaue gcc is the system compiler
%bcond_with clang

# Allow using compilation flags set by Fedora RPM macros
# Disabled by default because it causes out-of-memory error on Fedora Copr
%bcond_with fedora_compilation_flags

Name:       chromium
Version:    88.0.4324.182
Release:    100%{?dist}
Summary:    A WebKit (Blink) powered web browser

License:    BSD and LGPLv2+ and ASL 2.0 and IJG and MIT and GPLv2+ and ISC and OpenSSL and (MPLv1.1 or GPLv2 or LGPLv2)
URL:        https://www.chromium.org/Home

# Unfortunately, Fedora Copr forbids uploading sources with patent-encumbered
# ffmpeg code even if they are never compiled and linked to target binraies,
# so we must repackage upstream tarballs to satisfy this requirement. However,
# we cannot simply delete all code of ffmpeg because this will disable support
# for some commonly-used free codecs such as Ogg Theora. Instead, helper
# scripts included in official Fedora packages are copied, modified, and used
# to automate the repackaging work.
#
# If you don't use Fedora services, you can uncomment the following line and
# use the upstream source tarball instead of the repackaged one.
# Source0:    https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz
#
# The repackaged source tarball used here is produced by:
# ./chromium-latest.py --stable --ffmpegclean --ffmpegarm --deleteunrar
Source0:    chromium-%{version}-clean.tar.xz
Source1:    chromium-latest.py
Source2:    chromium-ffmpeg-clean.sh
Source3:    chromium-ffmpeg-free-sources.py

# The following two source files are copied and modified from
# https://repos.fedorapeople.org/repos/spot/chromium/
Source10:   chromium-browser.sh
Source11:   chromium-browser.desktop

# The following two source files are copied verbatim from
# https://src.fedoraproject.org/cgit/rpms/chromium.git/tree/
Source12:   chromium-browser.xml

# Stub unrar wrapper
# https://bugs.chromium.org/p/chromium/issues/detail?id=884521
Patch0:     chromium-stub-unrar-wrapper.patch

# Workaround certificate transparency error
# https://bugs.chromium.org/p/chromium/issues/detail?id=992287
Patch1:     chromium-certificate-transparency-google.patch

# Don't require static libstdc++
Patch2:     chromium-gn-no-static-libstdc++.patch

# Don't use unversioned python commands. This patch is based on
# https://src.fedoraproject.org/rpms/chromium/c/7048e95ab61cd143
# https://src.fedoraproject.org/rpms/chromium/c/cb0be2c990fc724e
Patch20:    chromium-python2.patch

# Pull patches from Fedora
# https://src.fedoraproject.org/rpms/chromium/c/9071ee2d2f996b84
Patch30:    chromium-webrtc-cstring.patch

# Pull patches from stha09
# https://github.com/stha09/chromium-patches/commit/23bfdb7b34fb19bf
# https://github.com/stha09/chromium-patches/commit/3495379e353f96ef
Patch40:    chromium-openscreen-stdint.patch
Patch41:    chromium-ui-memory-vector.patch

# Pull upstream patches
Patch50:    chromium-quiche-gcc9.patch
Patch51:    chromium-gcc10-r831923.patch
Patch52:    chromium-gcc10-r838269.patch

# I don't have time to test whether it work on other architectures
ExclusiveArch: x86_64

# Basic tools and libraries
%if %{with clang}
BuildRequires: clang
%else
BuildRequires: gcc, gcc-c++
%endif
BuildRequires: ninja-build, nodejs, java-headless, bison, gperf, hwdata
BuildRequires: libgcc(x86-32), glibc(x86-32), libatomic
BuildRequires: libcap-devel, cups-devel, alsa-lib-devel, expat-devel
%if 0%{?fedora} >= 30
BuildRequires: minizip-compat-devel
%else
BuildRequires: minizip-devel
%endif
BuildRequires: mesa-libGL-devel, mesa-libEGL-devel, mesa-libgbm-devel
BuildRequires: pkgconfig(gtk+-2.0), pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(libffi), pkgconfig(nss), pkgconfig(libexif)
BuildRequires: pkgconfig(xtst), pkgconfig(xscrnsaver)
BuildRequires: pkgconfig(dbus-1), pkgconfig(libudev)
BuildRequires: pkgconfig(libva), pkgconfig(gnome-keyring-1)
BuildRequires: python2-setuptools
# remove_bundled_libraries.py --do-remove
BuildRequires: python2-rpm-macros
%if %{with system_beautifulsoup4}
BuildRequires: python2-beautifulsoup4
%endif
%if %{with system_html5lib}
BuildRequires: python2-html5lib
%endif
BuildRequires: python2-markupsafe
%if %{with system_ply}
BuildRequires: python2-ply
%endif
BuildRequires: python2-six
# replace_gn_files.py --system-libraries
BuildRequires: flac-devel
BuildRequires: freetype-devel
%if %{with system_harfbuzz}
BuildRequires: harfbuzz-devel
%endif
%if %{with system_libicu}
BuildRequires: libicu-devel
%endif
BuildRequires: libdrm-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libpng-devel
# Chromium requires libvpx 1.5.0 and some non-default options
%if %{with system_libvpx}
BuildRequires: libvpx-devel
%endif
BuildRequires: libwebp-devel
%if %{with system_libxml2}
BuildRequires: pkgconfig(libxml-2.0)
%endif
BuildRequires: pkgconfig(libxslt)
BuildRequires: opus-devel
BuildRequires: re2-devel
BuildRequires: snappy-devel
BuildRequires: zlib-devel
# *_use_*
BuildRequires: pciutils-devel
BuildRequires: speech-dispatcher-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: pkgconfig(libpipewire-0.2)
# install desktop files
BuildRequires: desktop-file-utils
# install AppData files
BuildRequires: libappstream-glib
Requires(post):   desktop-file-utils
Requires(postun): desktop-file-utils
Requires:         hicolor-icon-theme

Obsoletes:     chromedriver <= %{version}-%{release}
Obsoletes:     chromium-common <= %{version}-%{release}
Obsoletes:     chromium-headless <= %{version}-%{release}
Obsoletes:     chromium-libs <= %{version}-%{release}
Obsoletes:     chromium-libs-media <= %{version}-%{release}
Provides:      chromedriver = %{version}-%{release}
Provides:      chromium-common = %{version}-%{release}
Provides:      chromium-headless = %{version}-%{release}
Provides:      chromium-libs = %{version}-%{release}
Provides:      chromium-libs-media = %{version}-%{release}

Provides:      chromedriver-stable = %{version}-%{release}
Conflicts:     chromedriver-testing
Conflicts:     chromedriver-unstable

%global chromiumdir %{_libdir}/chromium-browser
%global __provides_exclude_from ^%{chromiumdir}/.*$

%if !%{with symbol}
%global debug_package %{nil}
%endif

%description


%prep
%autosetup -p1

# Don't use unversioned python commands in shebangs. This command is based on
# https://src.fedoraproject.org/rpms/chromium/c/cdad6219176a7615
find -type f -exec \
    sed -i '1s:^#!/usr/bin/\(python\|env python\)$:#!%{__python2}:' '{}' '+'

./build/linux/unbundle/remove_bundled_libraries.py --do-remove \
    base/third_party/cityhash \
    base/third_party/double_conversion \
    base/third_party/dynamic_annotations \
    base/third_party/icu \
    base/third_party/libevent \
    base/third_party/nspr \
    base/third_party/superfasthash \
    base/third_party/symbolize \
    base/third_party/valgrind \
    base/third_party/xdg_mime \
    base/third_party/xdg_user_dirs \
    buildtools/third_party/libc++ \
    buildtools/third_party/libc++abi \
    chrome/third_party/mozilla_security_manager \
    courgette/third_party \
    native_client/src/third_party/dlmalloc \
    native_client/src/third_party/valgrind \
    net/third_party/mozilla_security_manager \
    net/third_party/nss \
    net/third_party/quic \
    net/third_party/uri_template \
    third_party/abseil-cpp \
    third_party/adobe \
    third_party/angle \
    third_party/angle/src/common/third_party/base \
    third_party/angle/src/common/third_party/smhasher \
    third_party/angle/src/common/third_party/xxhash \
    third_party/angle/src/third_party/compiler \
    third_party/angle/src/third_party/libXNVCtrl \
    third_party/angle/src/third_party/trace_event \
    third_party/angle/src/third_party/volk \
    third_party/angle/third_party/glslang \
    third_party/angle/third_party/spirv-headers \
    third_party/angle/third_party/spirv-tools \
    third_party/angle/third_party/vulkan-headers \
    third_party/angle/third_party/vulkan-loader \
    third_party/angle/third_party/vulkan-tools \
    third_party/angle/third_party/vulkan-validation-layers \
    third_party/apple_apsl \
    third_party/axe-core \
    third_party/boringssl \
    third_party/boringssl/src/third_party/fiat \
    third_party/blink \
    third_party/breakpad \
    third_party/breakpad/breakpad/src/third_party/curl \
    third_party/brotli \
    third_party/catapult \
    third_party/catapult/common/py_vulcanize/third_party/rcssmin \
    third_party/catapult/common/py_vulcanize/third_party/rjsmin \
%if !%{with system_beautifulsoup4}
    third_party/catapult/third_party/beautifulsoup4 \
%endif
%if !%{with system_html5lib}
    third_party/catapult/third_party/html5lib-python \
%endif
    third_party/catapult/third_party/polymer \
    third_party/catapult/tracing/third_party/d3 \
    third_party/catapult/tracing/third_party/gl-matrix \
    third_party/catapult/tracing/third_party/jpeg-js \
    third_party/catapult/tracing/third_party/jszip \
    third_party/catapult/tracing/third_party/mannwhitneyu \
    third_party/catapult/tracing/third_party/oboe \
    third_party/catapult/tracing/third_party/pako \
    third_party/ced \
    third_party/cld_3 \
    third_party/closure_compiler \
    third_party/crashpad \
    third_party/crashpad/crashpad/third_party/lss \
    third_party/crashpad/crashpad/third_party/zlib \
    third_party/crc32c \
    third_party/cros_system_api \
    third_party/dav1d \
    third_party/dawn \
    third_party/dawn/third_party/khronos \
    third_party/depot_tools \
    third_party/devscripts \
    third_party/devtools-frontend \
    third_party/devtools-frontend/src/front_end/third_party/acorn \
    third_party/devtools-frontend/src/front_end/third_party/axe-core \
    third_party/devtools-frontend/src/front_end/third_party/chromium \
    third_party/devtools-frontend/src/front_end/third_party/codemirror \
    third_party/devtools-frontend/src/front_end/third_party/fabricjs \
    third_party/devtools-frontend/src/front_end/third_party/i18n \
    third_party/devtools-frontend/src/front_end/third_party/intl-messageformat \
    third_party/devtools-frontend/src/front_end/third_party/lighthouse \
    third_party/devtools-frontend/src/front_end/third_party/lit-html \
    third_party/devtools-frontend/src/front_end/third_party/lodash-isequal \
    third_party/devtools-frontend/src/front_end/third_party/marked \
    third_party/devtools-frontend/src/front_end/third_party/puppeteer \
    third_party/devtools-frontend/src/front_end/third_party/wasmparser \
    third_party/devtools-frontend/src/third_party \
    third_party/dom_distiller_js \
    third_party/emoji-segmenter \
    third_party/ffmpeg \
    third_party/flatbuffers \
    third_party/freetype \
    third_party/fusejs \
    third_party/libgifcodec \
    third_party/glslang \
    third_party/google_input_tools \
    third_party/google_input_tools/third_party/closure_library \
    third_party/google_input_tools/third_party/closure_library/third_party/closure \
    third_party/googletest \
%if !%{with system_harfbuzz}
    third_party/harfbuzz-ng \
%endif
    third_party/harfbuzz-ng/utils \
    third_party/hunspell \
    third_party/iccjpeg \
%if !%{with system_libicu}
    third_party/icu \
%endif
    third_party/inspector_protocol \
    third_party/jinja2 \
    third_party/jsoncpp \
    third_party/jstemplate \
    third_party/khronos \
    third_party/leveldatabase \
    third_party/libaddressinput \
    third_party/libaom \
    third_party/libaom/source/libaom/third_party/vector \
    third_party/libaom/source/libaom/third_party/x86inc \
    third_party/libavif \
    third_party/libjingle \
    third_party/libphonenumber \
    third_party/libsecret \
    third_party/libsrtp \
    third_party/libsync \
    third_party/libudev \
%if !%{with system_libvpx}
    third_party/libvpx \
    third_party/libvpx/source/libvpx/third_party/x86inc \
%endif
    third_party/libwebm \
    third_party/libx11 \
    third_party/libxcb-keysyms \
%if %{with system_libxml2}
    third_party/libxml/chromium \
%else
    third_party/libxml \
%endif
    third_party/libXNVCtrl \
    third_party/libyuv \
    third_party/lottie \
    third_party/lss \
    third_party/lzma_sdk \
    third_party/mako \
    third_party/mesa \
    third_party/metrics_proto \
    third_party/modp_b64 \
    third_party/nasm \
    third_party/nearby \
    third_party/node \
    third_party/node/node_modules/polymer-bundler/lib/third_party/UglifyJS2 \
    third_party/one_euro_filter \
    third_party/openh264 \
    third_party/opencv \
    third_party/openscreen \
    third_party/openscreen/src/third_party/mozilla \
    third_party/openscreen/src/third_party/tinycbor/src/src \
    third_party/ots \
    third_party/pdfium \
    third_party/pdfium/third_party/agg23 \
    third_party/pdfium/third_party/base \
    third_party/pdfium/third_party/bigint \
    third_party/pdfium/third_party/freetype \
    third_party/pdfium/third_party/lcms \
    third_party/pdfium/third_party/libopenjpeg20 \
    third_party/pdfium/third_party/libpng16 \
    third_party/pdfium/third_party/libtiff \
    third_party/pdfium/third_party/skia_shared \
    third_party/perfetto \
    third_party/pffft \
%if !%{with system_ply}
    third_party/ply \
%endif
    third_party/polymer \
    third_party/private-join-and-compute \
    third_party/private_membership \
    third_party/protobuf \
    third_party/protobuf/third_party/six \
    third_party/pyjson5 \
    third_party/qcms \
%if !%{with system_re2}
    third_party/re2 \
%endif
    third_party/rnnoise \
    third_party/s2cellid \
    third_party/schema_org \
    third_party/securemessage \
    third_party/shaka-player \
    third_party/shell-encryption \
    third_party/simplejson \
    third_party/skia \
    third_party/skia/include/third_party/skcms \
    third_party/skia/include/third_party/vulkan \
    third_party/skia/third_party/skcms \
    third_party/skia/third_party/vulkan \
    third_party/smhasher \
    third_party/speech-dispatcher \
    third_party/spirv-cross/spirv-cross \
    third_party/spirv-headers \
    third_party/SPIRV-Tools \
    third_party/sqlite \
    third_party/swiftshader \
    third_party/swiftshader/third_party/astc-encoder \
    third_party/swiftshader/third_party/llvm-10.0 \
    third_party/swiftshader/third_party/llvm-subzero \
    third_party/swiftshader/third_party/marl \
    third_party/swiftshader/third_party/subzero \
    third_party/swiftshader/third_party/SPIRV-Headers/include/spirv/unified1 \
    third_party/tcmalloc \
    third_party/tint \
    third_party/ukey2 \
    third_party/unrar \
    third_party/usb_ids \
    third_party/usrsctp \
    third_party/vulkan \
    third_party/wayland \
    third_party/web-animations-js \
    third_party/webdriver \
    third_party/webrtc \
    third_party/webrtc/common_audio/third_party/ooura \
    third_party/webrtc/common_audio/third_party/spl_sqrt_floor \
    third_party/webrtc/modules/third_party/fft \
    third_party/webrtc/modules/third_party/g711 \
    third_party/webrtc/modules/third_party/g722 \
    third_party/webrtc/rtc_base/third_party/base64 \
    third_party/webrtc/rtc_base/third_party/sigslot \
    third_party/widevine \
    third_party/woff2 \
    third_party/wuffs \
    third_party/x11proto \
    third_party/xcbproto \
    third_party/zxcvbn-cpp \
    third_party/xdg-utils \
    third_party/zlib/google \
    tools/grit/third_party/six \
    tools/gn/src/base/third_party/icu \
    url/third_party/mozilla \
    v8/src/third_party/siphash \
    v8/src/third_party/valgrind \
    v8/src/third_party/utf8-decoder \
    v8/third_party/inspector_protocol \
    v8/third_party/v8

./build/linux/unbundle/replace_gn_files.py --system-libraries \
    flac \
    freetype \
    fontconfig \
%if %{with system_harfbuzz}
    harfbuzz-ng \
%endif
%if %{with system_libicu}
    icu \
%endif
    libdrm \
    libjpeg \
    libpng \
%if %{with system_libvpx}
    libvpx \
%endif
    libwebp \
%if %{with system_libxml2}
    libxml \
%endif
    libxslt \
    opus \
%if %{with system_re2}
    re2 \
%endif
    snappy \
    zlib

sed -i 's|//third_party/usb_ids|/usr/share/hwdata|g' \
    services/device/public/cpp/usb/BUILD.gn

rmdir third_party/markupsafe
ln -s %{python2_sitearch}/markupsafe third_party/markupsafe

%if %{with system_ply}
rmdir third_party/ply
ln -s %{python2_sitelib}/ply third_party/ply
%endif

mkdir -p third_party/node/linux/node-linux-x64/bin
ln -s %{_bindir}/node third_party/node/linux/node-linux-x64/bin/node


%build
export AR=ar NM=nm
export PNACLPYTHON=%{__python2}

# Fedora 25 doesn't have __global_cxxflags
%if %{with fedora_compilation_flags}
export CFLAGS="$(echo '%{__global_cflags}' | sed 's/-fexceptions//')"
export CXXFLAGS="$(echo '%{?__global_cxxflags}%{!?__global_cxxflags:%{__global_cflags}}' | sed 's/-fexceptions//')"
export LDFLAGS='%{__global_ldflags}'
%endif

%if %{with clang}
export CC=clang CXX=clang++
%else
export CC=gcc CXX=g++
%endif

gn_args=(
    is_debug=false
    is_component_build=false
    use_gold=false
    use_sysroot=false
    use_custom_libcxx=false
    use_aura=true
    use_cups=true
    use_glib=true
    use_gio=true
    use_gtk=true
    use_gnome_keyring=true
    use_kerberos=true
    use_libpci=true
    use_ozone=true
    use_pulseaudio=true
    use_system_freetype=true
%if %{with system_harfbuzz}
    use_system_harfbuzz=true
%endif
    use_system_libdrm=true
    use_system_minigbm=true
    use_xkbcommon=true
    ozone_auto_platforms=false
    ozone_platform_headless=true
    ozone_platform_wayland=true
    ozone_platform_x11=true
    rtc_use_pipewire=true
    rtc_link_pipewire=true
    enable_hangout_services_extension=false
    enable_nacl=false
    fatal_linker_warnings=false
    treat_warnings_as_errors=false
    fieldtrial_testing_like_official_build=true
    'system_libdir="%{_lib}"'
    'custom_toolchain="//build/toolchain/linux/unbundle:default"'
    'host_toolchain="//build/toolchain/linux/unbundle:default"'
    'google_api_key="AIzaSyCcK3laItm4Ik9bm6IeGFC6tVgy4eut0_o"'
    'google_default_client_id="82546407293.apps.googleusercontent.com"'
    'google_default_client_secret="GuvPB069ONrHxN7Y_y0txLKn"'
)

gn_args+=(
%if %{with clang}
    'clang_base_path="/usr"'
%endif
)

gn_args+=(
%if %{with clang}
    is_clang=true
    clang_use_chrome_plugins=false
%else
    is_clang=false
%endif
)

gn_args+=(
%if %{with symbol}
    symbol_level=1
%else
    symbol_level=0
%endif
)

./tools/gn/bootstrap/bootstrap.py --gn-gen-args "${gn_args[*]}"
./out/Release/gn gen out/Release \
    --script-executable=/usr/bin/python2 --args="${gn_args[*]}"

# Raise the limit of open files because ld.bfd seems to open more files than
# ld.gold. The default limit of 1024 is known to cause malformed archive error.
ulimit -Sn "$(ulimit -Hn)"

%if 0%{?ninja_build:1}
%{ninja_build} -C out/Release chrome chrome_sandbox chromedriver
%else
ninja -v %{_smp_mflags} -C out/Release chrome chrome_sandbox chromedriver
%endif


%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{chromiumdir}/locales
mkdir -p %{buildroot}%{chromiumdir}/MEIPreload
mkdir -p %{buildroot}%{chromiumdir}/swiftshader
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/gnome-control-center/default-apps
mkdir -p %{buildroot}%{_datadir}/metainfo
sed -e "s|@@CHROMIUMDIR@@|%{chromiumdir}|" -e "s|@@BUILDTARGET@@|`cat /etc/redhat-release`|" \
    %{SOURCE10} > chromium-browser.sh
install -m 755 chromium-browser.sh %{buildroot}%{_bindir}/chromium-browser
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE11}
install -m 644 %{SOURCE12} %{buildroot}%{_datadir}/gnome-control-center/default-apps/
install -m 644 chrome/installer/linux/common/chromium-browser/chromium-browser.appdata.xml \
    %{buildroot}%{_datadir}/metainfo/
appstream-util validate-relax --nonet \
    %{buildroot}%{_datadir}/metainfo/chromium-browser.appdata.xml
sed -e "s|@@MENUNAME@@|Chromium|g" -e "s|@@PACKAGE@@|chromium|g" \
    chrome/app/resources/manpage.1.in > chrome.1
install -m 644 chrome.1 %{buildroot}%{_mandir}/man1/chromium-browser.1
install -m 755 out/Release/chrome %{buildroot}%{chromiumdir}/chromium-browser
install -m 4755 out/Release/chrome_sandbox %{buildroot}%{chromiumdir}/chrome-sandbox
install -m 755 out/Release/chromedriver %{buildroot}%{chromiumdir}/
%if !%{with system_libicu}
install -m 644 out/Release/icudtl.dat %{buildroot}%{chromiumdir}/
%endif
install -m 644 out/Release/v8_context_snapshot.bin %{buildroot}%{chromiumdir}/
install -m 644 out/Release/vk_swiftshader_icd.json %{buildroot}%{chromiumdir}/
install -m 755 out/Release/*.so %{buildroot}%{chromiumdir}/
install -m 644 out/Release/*.pak %{buildroot}%{chromiumdir}/
install -m 644 out/Release/locales/*.pak %{buildroot}%{chromiumdir}/locales/
install -m 644 out/Release/MEIPreload/* %{buildroot}%{chromiumdir}/MEIPreload/
install -m 755 out/Release/swiftshader/*.so %{buildroot}%{chromiumdir}/swiftshader/
for i in 16 32; do
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
    install -m 644 chrome/app/theme/default_100_percent/chromium/product_logo_$i.png \
        %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/chromium-browser.png
done
for i in 24 32 48 64 128 256; do
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
%license LICENSE
%doc AUTHORS README.md
%{_bindir}/chromium-browser
%{_datadir}/applications/chromium-browser.desktop
%{_datadir}/gnome-control-center/default-apps/chromium-browser.xml
%{_datadir}/icons/hicolor/16x16/apps/chromium-browser.png
%{_datadir}/icons/hicolor/24x24/apps/chromium-browser.png
%{_datadir}/icons/hicolor/32x32/apps/chromium-browser.png
%{_datadir}/icons/hicolor/32x32/apps/chromium-browser.xpm
%{_datadir}/icons/hicolor/48x48/apps/chromium-browser.png
%{_datadir}/icons/hicolor/64x64/apps/chromium-browser.png
%{_datadir}/icons/hicolor/128x128/apps/chromium-browser.png
%{_datadir}/icons/hicolor/256x256/apps/chromium-browser.png
%{_datadir}/metainfo/chromium-browser.appdata.xml
%{_mandir}/man1/chromium-browser.1.gz
%dir %{chromiumdir}
%{chromiumdir}/chromium-browser
%{chromiumdir}/chrome-sandbox
%{chromiumdir}/chromedriver
%if !%{with system_libicu}
%{chromiumdir}/icudtl.dat
%endif
%{chromiumdir}/libEGL.so
%{chromiumdir}/libGLESv2.so
%{chromiumdir}/libVkICD_mock_icd.so
%{chromiumdir}/libvk_swiftshader.so
%{chromiumdir}/libvulkan.so
%{chromiumdir}/v8_context_snapshot.bin
%{chromiumdir}/vk_swiftshader_icd.json
%{chromiumdir}/*.pak
%dir %{chromiumdir}/locales
%{chromiumdir}/locales/*.pak
%dir %{chromiumdir}/MEIPreload
%{chromiumdir}/MEIPreload/manifest.json
%{chromiumdir}/MEIPreload/preloaded_data.pb
%dir %{chromiumdir}/swiftshader
%{chromiumdir}/swiftshader/libEGL.so
%{chromiumdir}/swiftshader/libGLESv2.so



%changelog
* Thu Feb 18 2021 - Ting-Wei Lan <lantw44@gmail.com> - 88.0.4324.182-100
- Update to 88.0.4324.182

* Sat Feb  6 2021 - Ting-Wei Lan <lantw44@gmail.com> - 88.0.4324.150-100
- Update to 88.0.4324.150

* Thu Feb  4 2021 - Ting-Wei Lan <lantw44@gmail.com> - 88.0.4324.146-100
- Update to 88.0.4324.146

* Tue Feb  2 2021 - Ting-Wei Lan <lantw44@gmail.com> - 88.0.4324.96-100
- Update to 88.0.4324.96

* Sun Jan 10 2021 - Ting-Wei Lan <lantw44@gmail.com> - 87.0.4280.141-100
- Update to 87.0.4280.141

* Fri Dec 04 2020 - Ting-Wei Lan <lantw44@gmail.com> - 87.0.4280.88-100
- Update to 87.0.4280.88

* Sat Nov 21 2020 - Ting-Wei Lan <lantw44@gmail.com> - 87.0.4280.66-101
- Explicity enable ozone platforms for headess, X11, Wayland

* Fri Nov 20 2020 - Ting-Wei Lan <lantw44@gmail.com> - 87.0.4280.66-100
- Update to 87.0.4280.66

* Thu Nov 12 2020 - Ting-Wei Lan <lantw44@gmail.com> - 86.0.4240.198-100
- Update to 86.0.4240.198

* Tue Nov 10 2020 - Ting-Wei Lan <lantw44@gmail.com> - 86.0.4240.193-100
- Update to 86.0.4240.193

* Tue Nov  3 2020 - Ting-Wei Lan <lantw44@gmail.com> - 86.0.4240.183-100
- Update to 86.0.4240.183

* Wed Oct 21 2020 - Ting-Wei Lan <lantw44@gmail.com> - 86.0.4240.111-100
- Update to 86.0.4240.111

* Sun Oct 18 2020 - Ting-Wei Lan <lantw44@gmail.com> - 86.0.4240.75-102
- Disable gold because it segfault on Fedora 33 and later

* Sat Oct 17 2020 - Ting-Wei Lan <lantw44@gmail.com> - 86.0.4240.75-101
- Fix build issues for GCC 9

* Thu Oct 15 2020 - Ting-Wei Lan <lantw44@gmail.com> - 86.0.4240.75-100
- Update to 86.0.4240.75

* Tue Sep 22 2020 - Ting-Wei Lan <lantw44@gmail.com> - 85.0.4183.121-100
- Update to 85.0.4183.121

* Fri Sep 11 2020 - Ting-Wei Lan <lantw44@gmail.com> - 85.0.4183.102-100
- Update to 85.0.4183.102

* Fri Aug 28 2020 - Ting-Wei Lan <lantw44@gmail.com> - 85.0.4183.83-100
- Update to 85.0.4183.83

* Thu Aug 20 2020 - Ting-Wei Lan <lantw44@gmail.com> - 84.0.4147.135-100
- Update to 84.0.4147.135

* Tue Aug 11 2020 - Ting-Wei Lan <lantw44@gmail.com> - 84.0.4147.125-100
- Update to 84.0.4147.125

* Tue Jul 28 2020 - Ting-Wei Lan <lantw44@gmail.com> - 84.0.4147.105-100
- Update to 84.0.4147.105

* Sun Jul 26 2020 - Ting-Wei Lan <lantw44@gmail.com> - 84.0.4147.89-101
- Fix build issues for GCC 9

* Sun Jul 26 2020 - Ting-Wei Lan <lantw44@gmail.com> - 84.0.4147.89-100
- Update to 84.0.4147.89

* Tue Jun 23 2020 - Ting-Wei Lan <lantw44@gmail.com> - 83.0.4103.116-100
- Update to 83.0.4103.116

* Tue Jun 16 2020 - Ting-Wei Lan <lantw44@gmail.com> - 83.0.4103.106-100
- Update to 83.0.4103.106

* Thu Jun 04 2020 - Ting-Wei Lan <lantw44@gmail.com> - 83.0.4103.97-100
- Update to 83.0.4103.97

* Fri May 22 2020 - Ting-Wei Lan <lantw44@gmail.com> - 83.0.4103.61-100
- Update to 83.0.4103.61

* Wed May 06 2020 - Ting-Wei Lan <lantw44@gmail.com> - 81.0.4044.138-100
- Update to 81.0.4044.138

* Tue Apr 28 2020 - Ting-Wei Lan <lantw44@gmail.com> - 81.0.4044.129-100
- Update to 81.0.4044.129

* Fri Apr 24 2020 - Ting-Wei Lan <lantw44@gmail.com> - 81.0.4044.122-100
- Update to 81.0.4044.122

* Sun Apr 19 2020 - Ting-Wei Lan <lantw44@gmail.com> - 81.0.4044.113-100
- Update to 81.0.4044.113

* Sun Apr 12 2020 - Ting-Wei Lan <lantw44@gmail.com> - 81.0.4044.92-102
- Fix BuildRequires for Fedora 33

* Sat Apr 11 2020 - Ting-Wei Lan <lantw44@gmail.com> - 81.0.4044.92-101
- Fix build issues for GCC 10

* Sat Apr 11 2020 - Ting-Wei Lan <lantw44@gmail.com> - 81.0.4044.92-100
- Update to 81.0.4044.92
- Disable NaCl because of build failures and being deprecated for a long time
- Building without Internet access becomes possible because we no longer have to
  download NaCl toolchains in prep stage

* Sat Apr 04 2020 - Ting-Wei Lan <lantw44@gmail.com> - 80.0.3987.163-100
- Update to 80.0.3987.163

* Thu Apr 02 2020 - Ting-Wei Lan <lantw44@gmail.com> - 80.0.3987.162-100
- Update to 80.0.3987.162

* Wed Mar 18 2020 - Ting-Wei Lan <lantw44@gmail.com> - 80.0.3987.149-100
- Update to 80.0.3987.149

* Wed Mar 04 2020 - Ting-Wei Lan <lantw44@gmail.com> - 80.0.3987.132-100
- Update to 80.0.3987.132

* Tue Feb 25 2020 - Ting-Wei Lan <lantw44@gmail.com> - 80.0.3987.122-100
- Update to 80.0.3987.122

* Wed Feb 19 2020 - Ting-Wei Lan <lantw44@gmail.com> - 80.0.3987.116-100
- Update to 80.0.3987.116

* Sat Feb 15 2020 - Ting-Wei Lan <lantw44@gmail.com> - 80.0.3987.106-100
- Update to 80.0.3987.106

* Sun Feb 09 2020 - Ting-Wei Lan <lantw44@gmail.com> - 80.0.3987.87-100
- Update to 80.0.3987.87

* Sat Jan 18 2020 - Ting-Wei Lan <lantw44@gmail.com> - 79.0.3945.130-100
- Update to 79.0.3945.130

* Wed Jan 08 2020 - Ting-Wei Lan <lantw44@gmail.com> - 79.0.3945.117-100
- Update to 79.0.3945.117

* Wed Dec 18 2019 - Ting-Wei Lan <lantw44@gmail.com> - 79.0.3945.88-100
- Update to 79.0.3945.88

* Sun Dec 15 2019 - Ting-Wei Lan <lantw44@gmail.com> - 79.0.3945.79-101
- Remove -fpermissive from CXXFLAGS
- Bundle beautifulsoup4, html5lib, ply on Fedora 32 and later because these
  Python 2 libraries have been removed

* Wed Dec 11 2019 - Ting-Wei Lan <lantw44@gmail.com> - 79.0.3945.79-100
- Update to 79.0.3945.79
- Disable jumbo build because upstream no longer supports it
- Remove GCC 8 undefined reference workaround because Fedora 29 is EOL
- Replace the sed command used to disable static libstdc++ with a patch file
  because the command can create Python syntax error

* Wed Nov 20 2019 - Ting-Wei Lan <lantw44@gmail.com> - 78.0.3904.108-100
- Update to 78.0.3904.108

* Thu Nov 07 2019 - Ting-Wei Lan <lantw44@gmail.com> - 78.0.3904.97-100
- Update to 78.0.3904.97

* Fri Nov 01 2019 - Ting-Wei Lan <lantw44@gmail.com> - 78.0.3904.87-100
- Update to 78.0.3904.87

* Wed Oct 23 2019 - Ting-Wei Lan <lantw44@gmail.com> - 78.0.3904.70-100
- Update to 78.0.3904.70
- Bring -fpermissive back to CXXFLAGS again

* Fri Oct 11 2019 - Ting-Wei Lan <lantw44@gmail.com> - 77.0.3865.120-100
- Update to 77.0.3865.120

* Thu Sep 19 2019 - Ting-Wei Lan <lantw44@gmail.com> - 77.0.3865.90-100
- Update to 77.0.3865.90

* Mon Sep 16 2019 - Ting-Wei Lan <lantw44@gmail.com> - 77.0.3865.75-102
- Merge changes from the official Fedora package

* Thu Sep 12 2019 - Ting-Wei Lan <lantw44@gmail.com> - 77.0.3865.75-101
- Patch pulse_stubs for Fedora 31 and later
- Fix harfbuzz linking issue on Fedora 31 and later

* Wed Sep 11 2019 - Ting-Wei Lan <lantw44@gmail.com> - 77.0.3865.75-100
- Update to 77.0.3865.75
- Fix python package names for Fedora 31

* Tue Aug 27 2019 - Ting-Wei Lan <lantw44@gmail.com> - 76.0.3809.132-100
- Update to 76.0.3809.132

* Sat Aug 10 2019 - Ting-Wei Lan <lantw44@gmail.com> - 76.0.3809.100-100
- Update to 76.0.3809.100

* Fri Aug 09 2019 - Ting-Wei Lan <lantw44@gmail.com> - 76.0.3809.87-101
- Workaround certificate transparency error for popular sites such as
  Google, Facebook, Yahoo

* Wed Jul 31 2019 - Ting-Wei Lan <lantw44@gmail.com> - 76.0.3809.87-100
- Update to 76.0.3809.87

* Tue Jul 16 2019 - Ting-Wei Lan <lantw44@gmail.com> - 75.0.3770.142-100
- Update to 75.0.3770.142

* Tue Jun 25 2019 - Ting-Wei Lan <lantw44@gmail.com> - 75.0.3770.100-101
- Make unrar wrapper a stub instead of patching safe browsing code

* Wed Jun 19 2019 - Ting-Wei Lan <lantw44@gmail.com> - 75.0.3770.100-100
- Update to 75.0.3770.100

* Fri Jun 14 2019 - Ting-Wei Lan <lantw44@gmail.com> - 75.0.3770.90-100
- Update to 75.0.3770.90

* Sat Jun 08 2019 - Ting-Wei Lan <lantw44@gmail.com> - 75.0.3770.80-102
- Workaround GCC 8 undefined reference error with -fno-ipa-cp-clone

* Sat Jun 08 2019 - Ting-Wei Lan <lantw44@gmail.com> - 75.0.3770.80-101
- Fix crash on Fedora 30

* Fri Jun 07 2019 - Ting-Wei Lan <lantw44@gmail.com> - 75.0.3770.80-100
- Update to 75.0.3770.80

* Wed May 22 2019 - Ting-Wei Lan <lantw44@gmail.com> - 74.0.3729.169-100
- Update to 74.0.3729.169

* Wed May 15 2019 - Ting-Wei Lan <lantw44@gmail.com> - 74.0.3729.157-100
- Update to 74.0.3729.157

* Wed May 01 2019 - Ting-Wei Lan <lantw44@gmail.com> - 74.0.3729.131-100
- Update to 74.0.3729.131

* Thu Apr 25 2019 - Ting-Wei Lan <lantw44@gmail.com> - 74.0.3729.108-100
- Update to 74.0.3729.108

* Sat Apr 06 2019 - Ting-Wei Lan <lantw44@gmail.com> - 73.0.3683.103-100
- Update to 73.0.3683.103

* Sat Mar 23 2019 - Ting-Wei Lan <lantw44@gmail.com> - 73.0.3683.86-101
- Enable jumbo build
- Install MEIPreload
- Use upstream AppStream data file and move to metainfo

* Thu Mar 21 2019 - Ting-Wei Lan <lantw44@gmail.com> - 73.0.3683.86-100
- Update to 73.0.3683.86

* Wed Mar 13 2019 - Ting-Wei Lan <lantw44@gmail.com> - 73.0.3683.75-100
- Update to 73.0.3683.75

* Sat Mar 02 2019 - Ting-Wei Lan <lantw44@gmail.com> - 72.0.3626.121-100
- Update to 72.0.3626.121

* Fri Feb 22 2019 - Ting-Wei Lan <lantw44@gmail.com> - 72.0.3626.119-100
- Update to 72.0.3626.119

* Thu Feb 14 2019 - Ting-Wei Lan <lantw44@gmail.com> - 72.0.3626.109-100
- Update to 72.0.3626.109

* Fri Feb 08 2019 - Ting-Wei Lan <lantw44@gmail.com> - 72.0.3626.96-100
- Update to 72.0.3626.96

* Sat Feb 02 2019 - Ting-Wei Lan <lantw44@gmail.com> - 72.0.3626.81-100
- Update to 72.0.3626.81
- Remove -fno-delete-null-pointer-checks because it causes nullptr checks in
  constexpr to fail to compile.

* Thu Dec 13 2018 - Ting-Wei Lan <lantw44@gmail.com> - 71.0.3578.98-100
- Update to 71.0.3578.98

* Mon Dec 10 2018 - Ting-Wei Lan <lantw44@gmail.com> - 71.0.3578.80-100
- Update to 71.0.3578.80
- Bundle re2 because the one included in Fedora is too old

* Tue Nov 20 2018 - Ting-Wei Lan <lantw44@gmail.com> - 70.0.3538.110-100
- Update to 70.0.3538.110

* Wed Nov 14 2018 - Ting-Wei Lan <lantw44@gmail.com> - 70.0.3538.102-100
- Update to 70.0.3538.102

* Thu Oct 25 2018 - Ting-Wei Lan <lantw44@gmail.com> - 70.0.3538.77-100
- Update to 70.0.3538.77

* Wed Oct 17 2018 - Ting-Wei Lan <lantw44@gmail.com> - 70.0.3538.67-100
- Update to 70.0.3538.67
- Add -fpermissive to CXXFLAGS again

* Tue Sep 18 2018 - Ting-Wei Lan <lantw44@gmail.com> - 69.0.3497.100-100
- Update to 69.0.3497.100

* Fri Sep 14 2018 - Ting-Wei Lan <lantw44@gmail.com> - 69.0.3497.92-101
- Remove -fpermissive from CXXFLAGS

* Wed Sep 12 2018 - Ting-Wei Lan <lantw44@gmail.com> - 69.0.3497.92-100
- Update to 69.0.3497.92
- Remove workaround for debugedit on Fedora 26 and older

* Tue Sep 11 2018 - Ting-Wei Lan <lantw44@gmail.com> - 69.0.3497.81-102
- Remove conditions for unsupported Fedora releases
- Use minizip-compat on Fedora 30 and later

* Sun Sep 09 2018 - Ting-Wei Lan <lantw44@gmail.com> - 69.0.3497.81-101
- Don't use unversioned python commands on Fedora 29 and later

* Wed Sep 05 2018 - Ting-Wei Lan <lantw44@gmail.com> - 69.0.3497.81-100
- Update to 69.0.3497.81

* Thu Aug 09 2018 - Ting-Wei Lan <lantw44@gmail.com> - 68.0.3440.106-100
- Update to 68.0.3440.106

* Wed Aug 01 2018 - Ting-Wei Lan <lantw44@gmail.com> - 68.0.3440.84-100
- Update to 68.0.3440.84

* Thu Jul 26 2018 - Ting-Wei Lan <lantw44@gmail.com> - 68.0.3440.75-100
- Update to 68.0.3440.75

* Tue Jun 26 2018 - Ting-Wei Lan <lantw44@gmail.com> - 67.0.3396.99-100
- Update to 67.0.3396.99

* Wed Jun 13 2018 - Ting-Wei Lan <lantw44@gmail.com> - 67.0.3396.87-100
- Update to 67.0.3396.87

* Thu Jun 07 2018 - Ting-Wei Lan <lantw44@gmail.com> - 67.0.3396.79-100
- Update to 67.0.3396.79

* Fri Jun 01 2018 - Ting-Wei Lan <lantw44@gmail.com> - 67.0.3396.62-100
- Update to 67.0.3396.62

* Wed May 16 2018 - Ting-Wei Lan <lantw44@gmail.com> - 66.0.3359.181-100
- Update to 66.0.3359.181

* Fri May 11 2018 - Ting-Wei Lan <lantw44@gmail.com> - 66.0.3359.170-100
- Update to 66.0.3359.170

* Fri Apr 27 2018 - Ting-Wei Lan <lantw44@gmail.com> - 66.0.3359.139-100
- Update to 66.0.3359.139

* Thu Apr 26 2018 - Ting-Wei Lan <lantw44@gmail.com> - 66.0.3359.117-103
- Add harfbuzz back to the list of replace_gn_files

* Mon Apr 23 2018 - Ting-Wei Lan <lantw44@gmail.com> - 66.0.3359.117-102
- Fix crash by replacing snapshot_blob.bin with v8_context_snapshot.bin

* Sat Apr 21 2018 - Ting-Wei Lan <lantw44@gmail.com> - 66.0.3359.117-101
- Import patches from upstream to fix build on Fedora 26
- Import patches from Fedora to fix build on Fedora 28

* Wed Apr 18 2018 - Ting-Wei Lan <lantw44@gmail.com> - 66.0.3359.117-100
- Update to 66.0.3359.117
- Workaround empty third_party/blink/tools/blinkpy/common directory
- Disable debuginfo package when debug symbols are disabled
- Remove duplicate items in files section
- Remove unrar sources

* Wed Mar 21 2018 - Ting-Wei Lan <lantw44@gmail.com> - 65.0.3325.181-100
- Update to 65.0.3325.181

* Wed Mar 14 2018 - Ting-Wei Lan <lantw44@gmail.com> - 65.0.3325.162-100
- Update to 65.0.3325.162

* Sun Mar 11 2018 - Ting-Wei Lan <lantw44@gmail.com> - 65.0.3325.146-101
- Import patches from upstream to fix build on Fedora 26

* Thu Mar 08 2018 - Ting-Wei Lan <lantw44@gmail.com> - 65.0.3325.146-100
- Update to 65.0.3325.146
- Temporarily add -fpermissive to CXXFLAGS

* Mon Feb 26 2018 - Ting-Wei Lan <lantw44@gmail.com> - 64.0.3282.186-100
- Update to 64.0.3282.186

* Wed Feb 14 2018 - Ting-Wei Lan <lantw44@gmail.com> - 64.0.3282.167-100
- Update to 64.0.3282.167

* Sat Feb 03 2018 - Ting-Wei Lan <lantw44@gmail.com> - 64.0.3282.140-100
- Update to 64.0.3282.140

* Mon Jan 29 2018 - Ting-Wei Lan <lantw44@gmail.com> - 64.0.3282.119-101
- Workaround debugedit failure caused by double slashes on Fedora 26 and older

* Thu Jan 25 2018 - Ting-Wei Lan <lantw44@gmail.com> - 64.0.3282.119-100
- Update to 64.0.3282.119

* Fri Jan 05 2018 - Ting-Wei Lan <lantw44@gmail.com> - 63.0.3239.132-100
- Update to 63.0.3239.132

* Mon Dec 18 2017 - Ting-Wei Lan <lantw44@gmail.com> - 63.0.3239.108-100
- Update to 63.0.3239.108
- Bundle harfbuzz on Fedora 27 and older
- Temporarily remove harfbuzz from the list of replace_gn_files

* Wed Nov 15 2017 - Ting-Wei Lan <lantw44@gmail.com> - 62.0.3202.94-100
- Update to 62.0.3202.94

* Tue Nov 07 2017 - Ting-Wei Lan <lantw44@gmail.com> - 62.0.3202.89-100
- Update to 62.0.3202.89

* Sat Oct 28 2017 - Ting-Wei Lan <lantw44@gmail.com> - 62.0.3202.75-101
- Merge changes from the official Fedora package
- Remove group tag because it is deprecated in Fedora
- Unbundle freetype

* Fri Oct 27 2017 - Ting-Wei Lan <lantw44@gmail.com> - 62.0.3202.75-100
- Update to 62.0.3202.75
- Replace 'if 0' with single bcond_with because they are unlikely to change
- Add more comments to bcond_* to explain the meaning of default values

* Wed Oct 18 2017 - Ting-Wei Lan <lantw44@gmail.com> - 62.0.3202.62-100
- Update to 62.0.3202.62
- Unbundle libxml2 on Fedora 27 and later
- Use environment variables to pass compiler flags

* Fri Sep 22 2017 - Ting-Wei Lan <lantw44@gmail.com> - 61.0.3163.100-100
- Update to 61.0.3163.100

* Fri Sep 15 2017 - Ting-Wei Lan <lantw44@gmail.com> - 61.0.3163.91-100
- Update to 61.0.3163.91

* Mon Sep 11 2017 - Ting-Wei Lan <lantw44@gmail.com> - 61.0.3163.79-102
- Fix GLIBC 2.26 build issue on Fedora 27 and later
- Add mesa development packages to BuildRequires for Fedora 27 and later

* Mon Sep 11 2017 - Ting-Wei Lan <lantw44@gmail.com> - 61.0.3163.79-101
- Reduce symbol_level to 1 to fix find-debuginfo.sh on Fedora 26

* Thu Sep 07 2017 - Ting-Wei Lan <lantw44@gmail.com> - 61.0.3163.79-100
- Update to 61.0.3163.79

* Fri Aug 25 2017 - Ting-Wei Lan <lantw44@gmail.com> - 60.0.3112.113-100
- Update to 60.0.3112.113

* Tue Aug 15 2017 - Ting-Wei Lan <lantw44@gmail.com> - 60.0.3112.101-100
- Update to 60.0.3112.101

* Thu Aug 03 2017 - Ting-Wei Lan <lantw44@gmail.com> - 60.0.3112.90-100
- Update to 60.0.3112.90

* Wed Jul 26 2017 - Ting-Wei Lan <lantw44@gmail.com> - 60.0.3112.78-100
- Update to 60.0.3112.78
- Unbundle opus

* Mon Jul 03 2017 - Ting-Wei Lan <lantw44@gmail.com> - 59.0.3071.115-101
- Filter provides in chromiumdir

* Tue Jun 27 2017 - Ting-Wei Lan <lantw44@gmail.com> - 59.0.3071.115-100
- Update to 59.0.3071.115
- Workaround missing third_party/freetype/src directory

* Wed Jun 21 2017 - Ting-Wei Lan <lantw44@gmail.com> - 59.0.3071.109-100
- Update to 59.0.3071.109

* Fri Jun 16 2017 - Ting-Wei Lan <lantw44@gmail.com> - 59.0.3071.104-100
- Update to 59.0.3071.104

* Wed Jun 07 2017 - Ting-Wei Lan <lantw44@gmail.com> - 59.0.3071.86-100
- Update to 59.0.3071.86
- Use xz -9 to compress the repackaged source tarball
- Bundle libxml2 because it depends on an unreleased version
- Bundle harfbuzz on Fedora 25 and older
- Unbundle libdrm

* Wed May 10 2017 - Ting-Wei Lan <lantw44@gmail.com> - 58.0.3029.110-100
- Update to 58.0.3029.110

* Wed May 03 2017 - Ting-Wei Lan <lantw44@gmail.com> - 58.0.3029.96-100
- Update to 58.0.3029.96

* Thu Apr 20 2017 - Ting-Wei Lan <lantw44@gmail.com> - 58.0.3029.81-100
- Update to 58.0.3029.81
- Bundle libvpx because it needs symbols from unreleased version
- Replace all HTTP links in comments with HTTPS links
- Group patch files by using 2-digit numbers

* Thu Mar 30 2017 - Ting-Wei Lan <lantw44@gmail.com> - 57.0.2987.133-100
- Update to 57.0.2987.133

* Fri Mar 17 2017 - Ting-Wei Lan <lantw44@gmail.com> - 57.0.2987.110-100
- Update to 57.0.2987.110

* Sun Mar 12 2017 - Ting-Wei Lan <lantw44@gmail.com> - 57.0.2987.98-101
- Fix GCC 7 build issue on Fedora 26 and later
- Bundle python2-jinja2 on Fedora 26 and later

* Sat Mar 11 2017 - Ting-Wei Lan <lantw44@gmail.com> - 57.0.2987.98-100
- Update to 57.0.2987.98

* Sun Feb 05 2017 - Ting-Wei Lan <lantw44@gmail.com> - 56.0.2924.87-100
- Update to 56.0.2924.87

* Fri Jan 27 2017 - Ting-Wei Lan <lantw44@gmail.com> - 56.0.2924.76-100
- Update to 56.0.2924.76
- Update repackaging scripts
- Avoid build error when symbol condition is enabled (#304121)

* Tue Dec 13 2016 - Ting-Wei Lan <lantw44@gmail.com> - 55.0.2883.87-100
- Update to 55.0.2883.87

* Tue Dec 06 2016 - Ting-Wei Lan <lantw44@gmail.com> - 55.0.2883.75-100
- Update to 55.0.2883.75
- Re-add the option used to unbundle icu
- Raise release number to 100 to avoid being replaced by official packages

* Fri Nov 11 2016 - Ting-Wei Lan <lantw44@gmail.com> - 54.0.2840.100-1
- Update to 54.0.2840.100

* Thu Nov 03 2016 - Ting-Wei Lan <lantw44@gmail.com> - 54.0.2840.90-1
- Update to 54.0.2840.90

* Fri Oct 21 2016 - Ting-Wei Lan <lantw44@gmail.com> - 54.0.2840.71-1
- Update to 54.0.2840.71

* Thu Oct 20 2016 - Ting-Wei Lan <lantw44@gmail.com> - 54.0.2840.59-1
- Update to 54.0.2840.59
- Use ninja_build macro if available
- Fix GCC 6 crashes caused by problems in build flags
- Disable the clang build, but BuildRequires is still kept to support nacl
- Move all downloading and patching tasks to prep section
- Switch to GN build system because GYP is no longer supported
- Bundle icu because replace_gn_files.py doesn't support unbundling it
- Bundle libevent because there seems to be a known problem
- Unbundle python2-jinja2, python2-markupsafe, python2-ply by using symlinks
- Unbundle python-beautifulsoup4, python-html5lib in catapult

* Fri Sep 30 2016 - Ting-Wei Lan <lantw44@gmail.com> - 53.0.2785.143-1
- Update to 53.0.2785.143

* Thu Sep 15 2016 - Ting-Wei Lan <lantw44@gmail.com> - 53.0.2785.116-1
- Update to 53.0.2785.116

* Wed Sep 14 2016 - Ting-Wei Lan <lantw44@gmail.com> - 53.0.2785.113-1
- Update to 53.0.2785.113

* Thu Sep 08 2016 - Ting-Wei Lan <lantw44@gmail.com> - 53.0.2785.101-1
- Update to 53.0.2785.101

* Thu Sep 08 2016 - Ting-Wei Lan <lantw44@gmail.com> - 53.0.2785.92-2
- Use _smp_mflags to set the number of parallel jobs
- Import gnome-control-center a default-apps file and an AppData file from
  the official Fedora package

* Sat Sep 03 2016 - Ting-Wei Lan <lantw44@gmail.com> - 53.0.2785.92-1
- Update to 53.0.2785.92

* Fri Sep 02 2016 - Ting-Wei Lan <lantw44@gmail.com> - 53.0.2785.89-1
- Update to 53.0.2785.89

* Sat Aug 13 2016 - Ting-Wei Lan <lantw44@gmail.com> - 52.0.2743.116-2
- Repackage upstream sources to delete patent-encumbered ffmpeg sources
- Allow replacing official packages with this package

* Wed Aug 10 2016 - Ting-Wei Lan <lantw44@gmail.com> - 52.0.2743.116-1
- Update to 52.0.2743.116

* Fri Jul 22 2016 - Ting-Wei Lan <lantw44@gmail.com> - 52.0.2743.82-2
- Fix build issue for cups 2.2

* Thu Jul 21 2016 - Ting-Wei Lan <lantw44@gmail.com> - 52.0.2743.82-1
- Update to 52.0.2743.82

* Fri Jun 24 2016 - Ting-Wei Lan <lantw44@gmail.com> - 51.0.2704.106-1
- Update to 51.0.2704.106

* Fri Jun 17 2016 - Ting-Wei Lan <lantw44@gmail.com> - 51.0.2704.103-1
- Update to 51.0.2704.103

* Tue Jun 07 2016 - Ting-Wei Lan <lantw44@gmail.com> - 51.0.2704.84-1
- Update to 51.0.2704.84

* Thu Jun 02 2016 - Ting-Wei Lan <lantw44@gmail.com> - 51.0.2704.79-1
- Update to 51.0.2704.79

* Thu May 26 2016 - Ting-Wei Lan <lantw44@gmail.com> - 51.0.2704.63-1
- Update to 51.0.2704.63

* Thu May 12 2016 - Ting-Wei Lan <lantw44@gmail.com> - 50.0.2661.102-1
- Update to 50.0.2661.102

* Fri Apr 29 2016 - Ting-Wei Lan <lantw44@gmail.com> - 50.0.2661.94-1
- Update to 50.0.2661.94

* Thu Apr 21 2016 - Ting-Wei Lan <lantw44@gmail.com> - 50.0.2661.86-1
- Update to 50.0.2661.86

* Thu Apr 14 2016 - Ting-Wei Lan <lantw44@gmail.com> - 50.0.2661.75-1
- Update to 50.0.2661.75
- Use bcond_with and bcond_without macros
- Install png-format logos for size 16 and 32
- Unbundle libvpx on Fedora 24 or later
- Temporarily disable the use of system icu because it needs a private header

* Sat Apr 09 2016 - Ting-Wei Lan <lantw44@gmail.com> - 49.0.2623.112-1
- Update to 49.0.2623.112

* Tue Mar 29 2016 - Ting-Wei Lan <lantw44@gmail.com> - 49.0.2623.110-1
- Update to 49.0.2623.110

* Fri Mar 25 2016 - Ting-Wei Lan <lantw44@gmail.com> - 49.0.2623.108-1
- Update to 49.0.2623.108

* Wed Mar 09 2016 - Ting-Wei Lan <lantw44@gmail.com> - 49.0.2623.87-1
- Update to 49.0.2623.87

* Tue Mar 08 2016 - Ting-Wei Lan <lantw44@gmail.com> - 49.0.2623.75-2
- Workaround GCC 6 crashes by compiling with clang on Fedora 24 or later

* Thu Mar 03 2016 - Ting-Wei Lan <lantw44@gmail.com> - 49.0.2623.75-1
- Update to 49.0.2623.75

* Thu Mar 03 2016 - Ting-Wei Lan <lantw44@gmail.com> - 48.0.2564.116-2
- Fix GCC 6 build issue on Fedora 24 and later

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
