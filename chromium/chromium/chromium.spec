# This spec file is based on other spec files, ebuilds, PKGBUILDs available from
#  [1] https://repos.fedorapeople.org/repos/spot/chromium/
#  [2] https://copr.fedoraproject.org/coprs/churchyard/chromium-russianfedora-tested/
#  [3] https://www.archlinux.org/packages/extra/x86_64/chromium/
#  [4] https://src.fedoraproject.org/rpms/chromium/
#  [5] https://gitweb.gentoo.org/repo/gentoo.git/tree/www-client/chromium/

# Get the version number of latest stable version
# $ curl -s 'https://omahaproxy.appspot.com/all?os=linux&channel=stable' | sed 1d | cut -d , -f 3

# Require dav1d >= 1.0.0 for Dav1dSettings.n_threads
%if 0%{?fedora} >= 37
%bcond_without system_dav1d
%else
%bcond_with system_dav1d
%endif

# Require freetype >= 2.11.1 for FT_ClipBox
%if 0%{?fedora} >= 36
%bcond_without system_freetype
%else
%bcond_with system_freetype
%endif

# Require harfbuzz >= 4.4.0 for hb-cplusplus.hh
%if 0%{?fedora} >= 37
%bcond_without system_harfbuzz
%else
%bcond_with system_harfbuzz
%endif

# Require libaom >= 3.4.0 for AOM_IMG_FMT_NV12
%if 0%{?fedora} >= 37
%bcond_without system_libaom
%else
%bcond_with system_libaom
%endif

# Require libxml2 > 2.9.4 for XML_PARSE_NOXXE
%bcond_without system_libxml2

# Requires re2 2016.07.21 for re2::LazyRE2
%bcond_without system_re2

# Allow testing whether icu can be unbundled
%bcond_with system_libicu

# Allow testing whether libvpx can be unbundled
%bcond_with system_libvpx

# Allow building with symbols to ease debugging
# Enabled by default because Fedora Copr has enough memory
%bcond_without symbol

# Allow linking with ld.gold
# Enabled by default because it is faster than ld.bfd
# Disabled on Fedora 34 and older because it segfault too frequently
%if 0%{?fedora} >= 35
%bcond_without gold
%else
%bcond_with gold
%endif

# Allow compiling with clang
# Disabled by default becaue gcc is the system compiler
%bcond_with clang

# Allow using compilation flags set by Fedora RPM macros
# Disabled by default because it causes out-of-memory error on Fedora Copr
%bcond_with fedora_compilation_flags

Name:       chromium
Version:    112.0.5615.49
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
%dnl Source0:    https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz
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

# Don't use static libstdc++ or -Werror
Patch1:     chromium-gn-no-static-libstdc++-allow-warnings.patch

# Don't use unversioned python commands. This patch is based on
# https://src.fedoraproject.org/rpms/chromium/c/7048e95ab61cd143
# https://src.fedoraproject.org/rpms/chromium/c/cb0be2c990fc724e
Patch2:     chromium-python3.patch

# Fix missing opus dependency for media/mojo/services/gpu_mojo_media_client.cc
Patch3:     chromium-media-mojo-services-opus.patch

# Fix incomplete type error for v8/src/codegen/tnode.h
Patch4:     chromium-v8-WasmArray-incomplete-type.patch

# Pull upstream patches
Patch10:    chromium-gcc-12-r1111077.patch
Patch11:    chromium-gcc-12-r1113983.patch
Patch12:    chromium-gcc-13-r1126024.patch
Patch13:    chromium-vulkan_memory_allocator-gcc-13.patch
Patch14:    chromium-webrtc-gcc-13.patch

# Fix missing includes
Patch20:    chromium-autofill-cstdint.patch
Patch21:    chromium-base-cstdint.patch
Patch22:    chromium-blink-cstdint.patch
Patch23:    chromium-cc-cstdint.patch
Patch24:    chromium-chrome-cstdint.patch
Patch25:    chromium-crash-cstdint.patch
Patch26:    chromium-dawn-cstdint.patch
Patch27:    chromium-device-cstdint.patch
Patch28:    chromium-feature_engagement-cstdint.patch
Patch29:    chromium-gpu-cstdint.patch
Patch30:    chromium-maldoca-cstdint.patch
Patch31:    chromium-net-cstdint.patch
Patch32:    chromium-omnibox-cstdint.patch
Patch33:    chromium-openscreen-cstdint.patch
Patch34:    chromium-password_manager-cstdint.patch
Patch35:    chromium-payments-cstdint.patch
Patch36:    chromium-pdf-cstdint.patch
Patch37:    chromium-pdfium-cstdint.patch
Patch38:    chromium-perfetto-cstdint.patch
Patch39:    chromium-quiche-cstdint.patch
Patch40:    chromium-ruy-string.patch
Patch41:    chromium-s2cellid-cstdint.patch
Patch42:    chromium-swiftshader-cstdint.patch
Patch43:    chromium-tflite-cstdint.patch
Patch44:    chromium-ui-cstdint.patch
Patch45:    chromium-viz-cstdint.patch

# I don't have time to test whether it work on other architectures
ExclusiveArch: x86_64

# Basic tools and libraries
%if %{with clang}
BuildRequires: clang
%else
BuildRequires: gcc, gcc-c++
%endif
BuildRequires: java-headless, nodejs, python2, python3
BuildRequires: bison, git, gperf, hwdata, ninja-build
BuildRequires: libgcc(x86-32), glibc(x86-32), libatomic
BuildRequires: alsa-lib-devel, cups-devel, expat-devel
BuildRequires: libcap-devel, libcurl-devel
%if 0%{?fedora} >= 30
BuildRequires: minizip-compat-devel
%else
BuildRequires: minizip-devel
%endif
BuildRequires: mesa-libGL-devel, mesa-libEGL-devel, mesa-libgbm-devel
BuildRequires: pkgconfig(gtk+-2.0), pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(libffi), pkgconfig(nss), pkgconfig(libexif)
BuildRequires: pkgconfig(xtst), pkgconfig(xscrnsaver), pkgconfig(xshmfence)
BuildRequires: pkgconfig(dbus-1), pkgconfig(libudev)
BuildRequires: pkgconfig(libva), pkgconfig(gnome-keyring-1)
# replace_gn_files.py --system-libraries
BuildRequires: flac-devel
%if %{with system_freetype}
BuildRequires: freetype-devel
%endif
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
%if %{with system_libaom}
BuildRequires: pkgconfig(aom)
%endif
%if %{with system_dav1d}
BuildRequires: pkgconfig(dav1d)
%endif
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
BuildRequires: pulseaudio-libs-devel
BuildRequires: wayland-devel
BuildRequires: pkgconfig(libpipewire-0.3)
BuildRequires: pkgconfig(Qt5Core), pkgconfig(Qt5Widgets)
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

%if !%{with fedora_compilation_flags}
%undefine _auto_set_build_flags
%endif

%description


%prep
%autosetup -p1


# Don't use unversioned python commands in shebangs. This command is based on
# https://src.fedoraproject.org/rpms/chromium/c/cdad6219176a7615
find -type f -exec \
    sed -i '1s:^#!/usr/bin/\(python\|env python\)$:#!%{__python3}:' '{}' '+'

./build/linux/unbundle/remove_bundled_libraries.py --do-remove \
    base/third_party/cityhash \
    base/third_party/double_conversion \
    base/third_party/dynamic_annotations \
    base/third_party/icu \
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
    third_party/angle \
    third_party/angle/src/common/third_party/xxhash \
    third_party/angle/src/third_party/ceval \
    third_party/angle/src/third_party/libXNVCtrl \
    third_party/angle/src/third_party/systeminfo \
    third_party/angle/src/third_party/volk \
    third_party/apple_apsl \
    third_party/axe-core \
    third_party/bidimapper \
    third_party/blink \
    third_party/boringssl \
    third_party/boringssl/src/third_party/fiat \
    third_party/breakpad \
    third_party/breakpad/breakpad/src/third_party/curl \
    third_party/brotli \
    third_party/catapult \
    third_party/catapult/common/py_vulcanize/third_party/rcssmin \
    third_party/catapult/common/py_vulcanize/third_party/rjsmin \
    third_party/catapult/third_party/beautifulsoup4-4.9.3 \
    third_party/catapult/third_party/html5lib-1.1 \
    third_party/catapult/third_party/polymer \
    third_party/catapult/third_party/six \
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
    third_party/content_analysis_sdk \
    third_party/cpuinfo \
    third_party/crashpad \
    third_party/crashpad/crashpad/third_party/lss \
    third_party/crashpad/crashpad/third_party/zlib \
    third_party/crc32c \
    third_party/cros_system_api \
%if !%{with system_dav1d}
    third_party/dav1d \
%endif
    third_party/dawn \
    third_party/dawn/third_party/gn/webgpu-cts \
    third_party/dawn/third_party/khronos \
    third_party/depot_tools \
    third_party/devscripts \
    third_party/devtools-frontend \
    third_party/devtools-frontend/src/front_end/third_party/acorn \
    third_party/devtools-frontend/src/front_end/third_party/additional_readme_paths.json \
    third_party/devtools-frontend/src/front_end/third_party/axe-core \
    third_party/devtools-frontend/src/front_end/third_party/chromium \
    third_party/devtools-frontend/src/front_end/third_party/codemirror \
    third_party/devtools-frontend/src/front_end/third_party/diff \
    third_party/devtools-frontend/src/front_end/third_party/i18n \
    third_party/devtools-frontend/src/front_end/third_party/intl-messageformat \
    third_party/devtools-frontend/src/front_end/third_party/lighthouse \
    third_party/devtools-frontend/src/front_end/third_party/lit \
    third_party/devtools-frontend/src/front_end/third_party/lodash-isequal \
    third_party/devtools-frontend/src/front_end/third_party/marked \
    third_party/devtools-frontend/src/front_end/third_party/puppeteer \
    third_party/devtools-frontend/src/front_end/third_party/puppeteer/package/lib/esm/third_party/mitt \
    third_party/devtools-frontend/src/front_end/third_party/vscode.web-custom-data \
    third_party/devtools-frontend/src/front_end/third_party/wasmparser \
    third_party/devtools-frontend/src/test/unittests/front_end/third_party/i18n \
    third_party/devtools-frontend/src/third_party \
    third_party/distributed_point_functions \
    third_party/dom_distiller_js \
    third_party/eigen3 \
    third_party/emoji-segmenter \
    third_party/farmhash \
    third_party/fdlibm \
    third_party/ffmpeg \
    third_party/fft2d \
    third_party/flatbuffers \
    third_party/fp16 \
%if !%{with system_freetype}
    third_party/freetype \
%endif
    third_party/fusejs \
    third_party/fxdiv \
    third_party/gemmlowp \
    third_party/google_input_tools \
    third_party/google_input_tools/third_party/closure_library \
    third_party/google_input_tools/third_party/closure_library/third_party/closure \
    third_party/googletest \
%if !%{with system_harfbuzz}
    third_party/harfbuzz-ng \
%endif
    third_party/highway \
    third_party/hunspell \
    third_party/iccjpeg \
%if !%{with system_libicu}
    third_party/icu \
%endif
    third_party/inspector_protocol \
    third_party/ipcz \
    third_party/jinja2 \
    third_party/jsoncpp \
    third_party/jstemplate \
    third_party/khronos \
    third_party/leveldatabase \
    third_party/libaddressinput \
%if !%{with system_libaom}
    third_party/libaom \
    third_party/libaom/source/libaom/third_party/fastfeat \
    third_party/libaom/source/libaom/third_party/SVT-AV1 \
    third_party/libaom/source/libaom/third_party/vector \
    third_party/libaom/source/libaom/third_party/x86inc \
%endif
    third_party/libavif \
    third_party/libevent \
    third_party/libgav1 \
    third_party/libjingle \
    third_party/libphonenumber \
    third_party/libsecret \
    third_party/libsrtp \
    third_party/libsync \
    third_party/libudev \
    third_party/liburlpattern \
    third_party/libva_protected_content \
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
    third_party/libyuv \
    third_party/libzip \
    third_party/lottie \
    third_party/lss \
    third_party/lzma_sdk \
    third_party/mako \
    third_party/maldoca \
    third_party/maldoca/src/third_party/tensorflow_protos \
    third_party/maldoca/src/third_party/zlibwrapper \
    third_party/markupsafe \
    third_party/material_color_utilities \
    third_party/mesa \
    third_party/metrics_proto \
    third_party/minigbm \
    third_party/modp_b64 \
    third_party/nasm \
    third_party/nearby \
    third_party/neon_2_sse \
    third_party/node \
    third_party/omnibox_proto \
    third_party/one_euro_filter \
    third_party/openh264 \
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
    third_party/pdfium/third_party/libopenjpeg \
    third_party/pdfium/third_party/libtiff \
    third_party/pdfium/third_party/skia_shared \
    third_party/perfetto \
    third_party/perfetto/protos/third_party/chromium \
    third_party/pffft \
    third_party/ply \
    third_party/polymer \
    third_party/private-join-and-compute \
    third_party/private_membership \
    third_party/protobuf \
    third_party/pthreadpool \
    third_party/pyjson5 \
    third_party/pyyaml \
    third_party/qcms \
%if !%{with system_re2}
    third_party/re2 \
%endif
    third_party/rnnoise \
    third_party/ruy \
    third_party/s2cellid \
    third_party/securemessage \
    third_party/selenium-atoms \
    third_party/shell-encryption \
    third_party/simplejson \
    third_party/six \
    third_party/skia \
    third_party/skia/include/third_party/vulkan \
    third_party/skia/third_party/vulkan \
    third_party/smhasher \
    third_party/speech-dispatcher \
    third_party/sqlite \
    third_party/swiftshader \
    third_party/swiftshader/third_party/astc-encoder \
    third_party/swiftshader/third_party/llvm-10.0 \
    third_party/swiftshader/third_party/llvm-subzero \
    third_party/swiftshader/third_party/marl \
    third_party/swiftshader/third_party/SPIRV-Headers/include/spirv \
    third_party/swiftshader/third_party/SPIRV-Tools \
    third_party/swiftshader/third_party/subzero \
    third_party/tensorflow_models \
    third_party/tensorflow-text \
    third_party/tflite \
    third_party/tflite/src/third_party/eigen3 \
    third_party/tflite/src/third_party/fft2d \
    third_party/ukey2 \
    third_party/unrar \
    third_party/usb_ids \
    third_party/utf \
    third_party/vulkan \
    third_party/wayland \
    third_party/web-animations-js \
    third_party/webdriver \
    third_party/webgpu-cts \
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
    third_party/xnnpack \
    third_party/xdg-utils \
    third_party/zlib/google \
    third_party/zxcvbn-cpp \
    tools/gn/src/base/third_party/icu \
    url/third_party/mozilla \
    v8/src/third_party/siphash \
    v8/src/third_party/utf8-decoder \
    v8/src/third_party/valgrind \
    v8/third_party/glibc \
    v8/third_party/inspector_protocol \
    v8/third_party/v8

./build/linux/unbundle/replace_gn_files.py --system-libraries \
%if %{with system_dav1d}
    dav1d \
%endif
    flac \
    fontconfig \
%if %{with system_freetype}
    freetype \
%endif
%if %{with system_harfbuzz}
    harfbuzz-ng \
%endif
%if %{with system_libicu}
    icu \
%endif
%if %{with system_libaom}
    libaom \
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

mkdir -p third_party/node/linux/node-linux-x64/bin
ln -s %{_bindir}/node third_party/node/linux/node-linux-x64/bin/node

ln -s %{_bindir}/java third_party/jdk/current/bin/java

mkdir -p buildtools/third_party/eu-strip/bin
ln -s %{_bindir}/true buildtools/third_party/eu-strip/bin/eu-strip


%build
export AR=ar NM=nm PATH="${PATH}:%{_qt5_bindir}"

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
%if 0%{?fedora} >= 38
export CXXFLAGS="$CXXFLAGS -Wno-error=changes-meaning"
%endif
%endif

gn_args=(
    is_debug=false
    is_component_build=false
    dcheck_always_on=false
    dcheck_is_configurable=false
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
    use_qt=true
%if %{with system_freetype}
    use_system_freetype=true
%endif
%if %{with system_harfbuzz}
    use_system_harfbuzz=true
%endif
    use_system_libdrm=true
    use_system_libffi=true
    use_system_minigbm=true
    use_xkbcommon=true
    ozone_auto_platforms=false
    'ozone_platform="x11"'
    ozone_platform_headless=true
    ozone_platform_wayland=true
    ozone_platform_x11=true
    rtc_use_pipewire=true
    rtc_link_pipewire=true
    enable_hangout_services_extension=false
    enable_nacl=false
    fatal_linker_warnings=false
    treat_warnings_as_errors=false
    disable_fieldtrial_testing_config=true
    'system_libdir="%{_lib}"'
    'custom_toolchain="//build/toolchain/linux/unbundle:default"'
    'host_toolchain="//build/toolchain/linux/unbundle:default"'
    'google_api_key="AIzaSyCcK3laItm4Ik9bm6IeGFC6tVgy4eut0_o"'
    'google_default_client_id="82546407293.apps.googleusercontent.com"'
    'google_default_client_secret="GuvPB069ONrHxN7Y_y0txLKn"'
)

gn_args+=(
%if %{with gold}
    use_gold=true
%else
    use_gold=false
%endif
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
    --script-executable=/usr/bin/python3 --args="${gn_args[*]}"

# Raise the limit of open files because ld.bfd seems to open more files than
# ld.gold. The default limit of 1024 is known to cause malformed archive error.
ulimit -Sn "$(ulimit -Hn)"

%if 0%{?ninja_build:1}
%{ninja_build} -C out/Release chrome chrome_sandbox chromedriver
%else
ninja -v %{_smp_mflags} -C out/Release chrome chrome_sandbox chromedriver
%endif

mv out/Release/chromedriver{.unstripped,}


%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{chromiumdir}/locales
mkdir -p %{buildroot}%{chromiumdir}/MEIPreload
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
install -m 755 out/Release/chrome_crashpad_handler %{buildroot}%{chromiumdir}/
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
%{chromiumdir}/chrome_crashpad_handler
%{chromiumdir}/chromedriver
%if !%{with system_libicu}
%{chromiumdir}/icudtl.dat
%endif
%{chromiumdir}/libEGL.so
%{chromiumdir}/libGLESv2.so
%{chromiumdir}/libqt5_shim.so
%{chromiumdir}/libVkICD_mock_icd.so
%{chromiumdir}/libVkLayer_khronos_validation.so
%{chromiumdir}/libvk_swiftshader.so
%{chromiumdir}/v8_context_snapshot.bin
%{chromiumdir}/vk_swiftshader_icd.json
%{chromiumdir}/*.pak
%dir %{chromiumdir}/locales
%{chromiumdir}/locales/*.pak
%dir %{chromiumdir}/MEIPreload
%{chromiumdir}/MEIPreload/manifest.json
%{chromiumdir}/MEIPreload/preloaded_data.pb


%changelog
* Sat Apr 08 2023 - Ting-Wei Lan <lantw44@gmail.com> - 112.0.5615.49-100
- Update to 112.0.5615.49

* Fri Mar 31 2023 - Ting-Wei Lan <lantw44@gmail.com> - 111.0.5563.146-100
- Update to 111.0.5563.146

* Thu Mar 23 2023 - Ting-Wei Lan <lantw44@gmail.com> - 111.0.5563.110-100
- Update to 111.0.5563.110

* Wed Mar 15 2023 - Ting-Wei Lan <lantw44@gmail.com> - 111.0.5563.64-100
- Update to 111.0.5563.64
- Fix build issues for GCC 13

* Sat Feb 25 2023 - Ting-Wei Lan <lantw44@gmail.com> - 110.0.5481.177-100
- Update to 110.0.5481.177

* Fri Feb 17 2023 - Ting-Wei Lan <lantw44@gmail.com> - 110.0.5481.100-100
- Update to 110.0.5481.100

* Tue Feb 14 2023 - Ting-Wei Lan <lantw44@gmail.com> - 110.0.5481.77-100
- Update to 110.0.5481.77

* Sun Jan 29 2023 - Ting-Wei Lan <lantw44@gmail.com> - 109.0.5414.119-100
- Update to 109.0.5414.119

* Sat Jan 14 2023 - Ting-Wei Lan <lantw44@gmail.com> - 109.0.5414.74-100
- Update to 109.0.5414.74

* Sat Dec 17 2022 - Ting-Wei Lan <lantw44@gmail.com> - 108.0.5359.124-100
- Update to 108.0.5359.124

* Mon Dec 12 2022 - Ting-Wei Lan <lantw44@gmail.com> - 108.0.5359.98-100
- Update to 108.0.5359.98

* Mon Dec 05 2022 - Ting-Wei Lan <lantw44@gmail.com> - 108.0.5359.94-100
- Update to 108.0.5359.94

* Sat Nov 26 2022 - Ting-Wei Lan <lantw44@gmail.com> - 107.0.5304.121-100
- Update to 107.0.5304.121

* Thu Nov 10 2022 - Ting-Wei Lan <lantw44@gmail.com> - 107.0.5304.110-100
- Update to 107.0.5304.110

* Thu Nov 03 2022 - Ting-Wei Lan <lantw44@gmail.com> - 107.0.5304.87-100
- Update to 107.0.5304.87
- Unbundle dav1d and libaom on Fedora 37 and later
- Enable Qt backend

* Wed Oct 12 2022 - Ting-Wei Lan <lantw44@gmail.com> - 106.0.5249.119-100
- Update to 106.0.5249.119

* Wed Oct 05 2022 - Ting-Wei Lan <lantw44@gmail.com> - 106.0.5249.91-100
- Update to 106.0.5249.91

* Thu Sep 15 2022 - Ting-Wei Lan <lantw44@gmail.com> - 105.0.5195.125-100
- Update to 105.0.5195.125

* Sat Sep 03 2022 - Ting-Wei Lan <lantw44@gmail.com> - 105.0.5195.102-100
- Update to 105.0.5195.102

* Fri Sep 02 2022 - Ting-Wei Lan <lantw44@gmail.com> - 105.0.5195.52-100
- Update to 105.0.5195.52

* Thu Aug 18 2022 - Ting-Wei Lan <lantw44@gmail.com> - 104.0.5112.101-100
- Update to 104.0.5112.101

* Thu Aug 04 2022 - Ting-Wei Lan <lantw44@gmail.com> - 104.0.5112.79-100
- Update to 104.0.5112.79

* Thu Jul 21 2022 - Ting-Wei Lan <lantw44@gmail.com> - 103.0.5060.134-100
- Update to 103.0.5060.134

* Mon Jul 11 2022 - Ting-Wei Lan <lantw44@gmail.com> - 103.0.5060.114-100
- Update to 103.0.5060.114

* Mon Jun 27 2022 - Ting-Wei Lan <lantw44@gmail.com> - 103.0.5060.53-100
- Update to 103.0.5060.53

* Sat Jun 11 2022 - Ting-Wei Lan <lantw44@gmail.com> - 102.0.5005.115-100
- Update to 102.0.5005.115

* Sun May 29 2022 - Ting-Wei Lan <lantw44@gmail.com> - 102.0.5005.61-100
- Update to 102.0.5005.61

* Thu May 12 2022 - Ting-Wei Lan <lantw44@gmail.com> - 101.0.4951.64-100
- Update to 101.0.4951.64

* Sat May 07 2022 - Ting-Wei Lan <lantw44@gmail.com> - 101.0.4951.54-100
- Update to 101.0.4951.54

* Sat Apr 30 2022 - Ting-Wei Lan <lantw44@gmail.com> - 101.0.4951.41-100
- Update to 101.0.4951.41

* Sat Apr 16 2022 - Ting-Wei Lan <lantw44@gmail.com> - 100.0.4896.127-100
- Update to 100.0.4896.127

* Sun Apr 10 2022 - Ting-Wei Lan <lantw44@gmail.com> - 100.0.4896.75-100
- Update to 100.0.4896.75

* Sun Apr 10 2022 - Ting-Wei Lan <lantw44@gmail.com> - 100.0.4896.60-100
- Update to 100.0.4896.60

* Thu Mar 31 2022 - Ting-Wei Lan <lantw44@gmail.com> - 99.0.4844.84-100
- Update to 99.0.4844.84

* Mon Mar 21 2022 - Ting-Wei Lan <lantw44@gmail.com> - 99.0.4844.82-100
- Update to 99.0.4844.82

* Wed Mar 16 2022 - Ting-Wei Lan <lantw44@gmail.com> - 99.0.4844.74-100
- Update to 99.0.4844.74

* Sat Mar 12 2022 - Ting-Wei Lan <lantw44@gmail.com> - 99.0.4844.51-101
- Fix build issues for GCC 12
- Unbundle FreeType on Fedora 36 and later
- Disable automatic set_build_flags by default because it can introduce
  incompatible compiler flags into the build

* Tue Mar 08 2022 - Ting-Wei Lan <lantw44@gmail.com> - 99.0.4844.51-100
- Update to 99.0.4844.51

* Sat Feb 19 2022 - Ting-Wei Lan <lantw44@gmail.com> - 98.0.4758.102-100
- Update to 98.0.4758.102

* Fri Feb 11 2022 - Ting-Wei Lan <lantw44@gmail.com> - 98.0.4758.80-100
- Update to 98.0.4758.80

* Mon Jan 24 2022 - Ting-Wei Lan <lantw44@gmail.com> - 97.0.4692.99-100
- Update to 97.0.4692.99

* Thu Jan 13 2022 - Ting-Wei Lan <lantw44@gmail.com> - 97.0.4692.71-100
- Update to 97.0.4692.71

* Thu Dec 16 2021 - Ting-Wei Lan <lantw44@gmail.com> - 96.0.4664.110-100
- Update to 96.0.4664.110

* Sun Dec 12 2021 - Ting-Wei Lan <lantw44@gmail.com> - 96.0.4664.93-101
- Drop certificate transparency patch because the error can no longer be
  reproduced on current Fedora releases

* Fri Dec 10 2021 - Ting-Wei Lan <lantw44@gmail.com> - 96.0.4664.93-100
- Update to 96.0.4664.93

* Wed Nov 17 2021 - Ting-Wei Lan <lantw44@gmail.com> - 96.0.4664.45-100
- Update to 96.0.4664.45
- Enable gold on Fedora 35 and later because it doesn't crash there

* Fri Oct 29 2021 - Ting-Wei Lan <lantw44@gmail.com> - 95.0.4638.69-100
- Update to 95.0.4638.69

* Sun Oct 24 2021 - Ting-Wei Lan <lantw44@gmail.com> - 95.0.4638.54-101
- Fix build issues for HarfBuzz 3.0

* Sat Oct 23 2021 - Ting-Wei Lan <lantw44@gmail.com> - 95.0.4638.54-100
- Update to 95.0.4638.54
- Set the default ozone platform to X11 because it cannot automatically choose
  the appropriate platform at runtime

* Fri Oct 08 2021 - Ting-Wei Lan <lantw44@gmail.com> - 94.0.4606.81-100
- Update to 94.0.4606.81

* Fri Oct 01 2021 - Ting-Wei Lan <lantw44@gmail.com> - 94.0.4606.71-100
- Update to 94.0.4606.71

* Sat Sep 25 2021 - Ting-Wei Lan <lantw44@gmail.com> - 94.0.4606.61-100
- Update to 94.0.4606.61

* Fri Sep 24 2021 - Ting-Wei Lan <lantw44@gmail.com> - 94.0.4606.54-101
- Use dnl macro to avoid the rpmbuild warning
- Fix Python 3.10 and GLIBC 2.34 build issues for Fedora 35
- Bundle freetype because it needs features from an unreleased version
- Unbundle re2

* Thu Sep 23 2021 - Ting-Wei Lan <lantw44@gmail.com> - 94.0.4606.54-100
- Update to 94.0.4606.54
- Explicitly disable DCHECK because it is now enabled by default
- Bundle harfbuzz on Fedora 35 and older because it needs harfbuzz 3.0.0

* Tue Sep 14 2021 - Ting-Wei Lan <lantw44@gmail.com> - 93.0.4577.82-100
- Update to 93.0.4577.82

* Fri Sep 03 2021 - Ting-Wei Lan <lantw44@gmail.com> - 93.0.4577.63-100
- Update to 93.0.4577.63
- Fix text rendering on Fedora 34

* Tue Aug 17 2021 - Ting-Wei Lan <lantw44@gmail.com> - 92.0.4515.159-100
- Update to 92.0.4515.159

* Tue Aug 03 2021 - Ting-Wei Lan <lantw44@gmail.com> - 92.0.4515.131-100
- Update to 92.0.4515.131

* Sun Jul 25 2021 - Ting-Wei Lan <lantw44@gmail.com> - 92.0.4515.107-100
- Update to 92.0.4515.107
- Switch to Python 3
- Remove unbundling options for Python dependencies because porting these mostly
  broken options to Python 3 is unlikely to be useful

* Sat Jul 17 2021 - Ting-Wei Lan <lantw44@gmail.com> - 91.0.4472.164-100
- Update to 91.0.4472.164

* Fri Jun 18 2021 - Ting-Wei Lan <lantw44@gmail.com> - 91.0.4472.114-100
- Update to 91.0.4472.114

* Tue Jun 15 2021 - Ting-Wei Lan <lantw44@gmail.com> - 91.0.4472.106-100
- Update to 91.0.4472.106

* Thu Jun 10 2021 - Ting-Wei Lan <lantw44@gmail.com> - 91.0.4472.101-100
- Update to 91.0.4472.101

* Mon May 31 2021 - Ting-Wei Lan <lantw44@gmail.com> - 91.0.4472.77-100
- Update to 91.0.4472.77

* Tue May 11 2021 - Ting-Wei Lan <lantw44@gmail.com> - 90.0.4430.212-100
- Update to 90.0.4430.212

* Tue Apr 27 2021 - Ting-Wei Lan <lantw44@gmail.com> - 90.0.4430.93-100
- Update to 90.0.4430.93

* Thu Apr 22 2021 - Ting-Wei Lan <lantw44@gmail.com> - 90.0.4430.85-100
- Update to 90.0.4430.85

* Sat Apr 17 2021 - Ting-Wei Lan <lantw44@gmail.com> - 90.0.4430.72-100
- Update to 90.0.4430.72

* Wed Apr 14 2021 - Ting-Wei Lan <lantw44@gmail.com> - 89.0.4389.128-100
- Update to 89.0.4389.128

* Sat Apr 10 2021 - Ting-Wei Lan <lantw44@gmail.com> - 89.0.4389.114-101
- Drop dependency on python2-six to fix Fedora 34 build
- Pull upstream patches for libva to fix Fedora 34 build

* Wed Mar 31 2021 - Ting-Wei Lan <lantw44@gmail.com> - 89.0.4389.114-100
- Update to 89.0.4389.114

* Sat Mar 13 2021 - Ting-Wei Lan <lantw44@gmail.com> - 89.0.4389.90-100
- Update to 89.0.4389.90
- Bundle markupsafe on Fedora 34 and later due to Python 2 library removal

* Wed Mar 10 2021 - Ting-Wei Lan <lantw44@gmail.com> - 89.0.4389.82-100
- Update to 89.0.4389.82

* Tue Mar 09 2021 - Ting-Wei Lan <lantw44@gmail.com> - 89.0.4389.72-100
- Update to 89.0.4389.72
- Switch to PipeWire 0.3

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
