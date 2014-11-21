%global blender_api 2.69
%global blender_fontdir %{_fontbasedir}/blender

# [Fedora] Turn off the brp-python-bytecompile script 
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

%global blenderlib  %{_datadir}/blender/%{blender_api}
%global blenderarch %{_libdir}/blender/%{blender_api}
%global __python %{__python3}
%global pyver %(%{__python} -c "import sys ; print(sys.version[:3])")

%global fontname blender

Name:           blender
Epoch:          1
Version:        %{blender_api}
Release:        5%{?dist}

Summary:        3D modeling, animation, rendering and post-production (Copr: lantw44/patches)

Group:          Applications/Multimedia
License:        GPLv2
URL:            http://www.blender.org

Source0:        http://download.blender.org/source/blender-%{version}.tar.gz
Source1:        blenderplayer.1
Source5:        blender.xml

Source10:       macros.blender

Patch1:         blender-2.68a-syspath.patch
Patch2:         blender-2.68a-droid.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  libtool
BuildRequires:  openssl-devel
BuildRequires:  python3-devel >= 3.3
BuildRequires:  cmake
BuildRequires:  SDL-devel
BuildRequires:  expat-devel
BuildRequires:  pcre-devel
BuildRequires:  libxml2-devel
BuildRequires:  boost-devel
BuildRequires:  jemalloc-devel

# Compression stuff
BuildRequires:  xz-devel
BuildRequires:  zlib-devel

BuildRequires:  libXi-devel
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  libGL-devel
BuildRequires:  libGLU-devel
BuildRequires:  freetype-devel
BuildRequires:  OpenEXR-devel
BuildRequires:  glew-devel
BuildRequires:  freeglut-devel

BuildRequires:  fftw-devel
BuildRequires:  ftgl-devel
BuildRequires:  ode-devel
BuildRequires:  openjpeg-devel
BuildRequires:  qhull-devel

# Picture/Vidoe stuff
BuildRequires:  libjpeg-devel
BuildRequires:  openjpeg-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libogg-devel
BuildRequires:  libtheora-devel
BuildRequires:  libvorbis-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  OpenImageIO-devel
BuildRequires:  OpenColorIO-devel
BuildRequires:  ffmpeg-devel

# Audio stuff
BuildRequires:  libsamplerate-devel
BuildRequires:  libao-devel
BuildRequires:  libsndfile-devel
BuildRequires:  esound-devel
BuildRequires:  freealut-devel
BuildRequires:  jack-audio-connection-kit-devel

BuildRequires:  openCOLLADA-devel >= svn825

BuildRequires:  subversion-devel

BuildRequires:  libspnav-devel

BuildRequires:  fontpackages-devel

Requires(post): desktop-file-utils
Requires(post): shared-mime-info
Requires(postun): desktop-file-utils
Requires(postun): shared-mime-info

Requires:         google-droid-sans-fonts
Requires:         blender-fonts = %{?epoch:%{epoch}:}%{version}-%{release}

Provides:         blender(ABI) = %{blender_api}

%description
Copr: lantw44/patches
Note: This is a modified package. Install it if you want FFmpeg support
in blender. FFmpeg is required to use various common video formats.

Blender is the essential software solution you need for 3D, from modeling,
animation, rendering and post-production to interactive creation and playback.

Professionals and novices can easily and inexpensively publish stand-alone,
secure, multi-platform content to the web, CD-ROMs, and other media.

%package -n blenderplayer
Summary:       Standalone blender player
Group:         Applications/Multimedia

Provides:      blender(ABI) = %{blender_api}

%description -n blenderplayer
Copr: lantw44/patches
Note: This is a modified package. Install it if you want FFmpeg support
in blender. FFmpeg is required to use various common video formats.

This package contains a stand alone release of the blender player.
You will need this package to play games which are based on the
Blender Game Engine.

%package rpm-macros
Summary:       RPM macros to build third-party blender addons packages
Group:         Development/Tools
BuildArch:     noarch

%description rpm-macros
Copr: lantw44/patches
Note: This is a modified package. Install it if you want FFmpeg support
in blender. FFmpeg is required to use various common video formats.

This package provides rpm macros to support the creation of third-party
addon packages to extend blender.

%package -n fonts-blender
Summary:       International blender mono space font
Group:         User Interface/X
License:       ASL 2.0 and GPlv3 and Bitstream Vera and Public Domain
BuildArch:     noarch

Provides:      blender-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:     blender-fonts <= 2.48a-9

%description -n fonts-blender
Copr: lantw44/patches
Note: This is a modified package. Install it if you want FFmpeg support
in blender. FFmpeg is required to use various common video formats.

This package contains an international blender mono space font which is
a composition of several mono space fonts to cover several character
sets.

%prep
%setup -q
 
%patch1 -p1 -b .syspath
%patch2 -p1 -b .droid

find -name '.svn' -print | xargs rm -rf

%build
mkdir cmake-make
cd cmake-make
export CFLAGS="$RPM_OPT_FLAGS -fPIC -funsigned-char -fno-strict-aliasing"
export CXXFLAGS="$CFLAGS"
cmake .. -DCMAKE_INSTALL_PREFIX=%{_prefix} \
%ifnarch %{ix86} x86_64
  -DWITH_RAYOPTIMIZATION=OFF \
%endif
 -DCMAKE_SKIP_RPATH=ON \
 -DBUILD_SHARED_LIBS=OFF \
 -DWITH_FFTW3:BOOL=ON \
 -DWITH_JACK:BOOL=ON \
 -DWITH_CODEC_SNDFILE:BOOL=ON \
 -DWITH_IMAGE_OPENJPEG:BOOL=ON \
 -DWITH_OPENCOLLADA:BOOL=ON \
 -DWITH_CYCLES:BOOL=ON \
 -DWITH_FFTW3:BOOL=ON \
 -DWITH_MOD_OCEANSIM:BOOL=ON \
 -DOPENCOLLADA=%{_includedir} \
 -DWITH_PYTHON:BOOL=ON \
 -DPYTHON_VERSION:STRING=%{pyver} \
 -DWITH_PYTHON_INSTALL:BOOL=OFF \
 -DWITH_CODEC_FFMPEG:BOOL=ON \
 -DWITH_GAMEENGINE:BOOL=ON \
 -DWITH_CXX_GUARDEDALLOC:BOOL=OFF \
 -DWITH_BUILTIN_GLEW=OFF \
 -DWITH_INSTALL_PORTABLE=OFF \
 -DWITH_PYTHON_SAFETY=ON \
 -DWITH_PLAYER=ON \
 -DWITH_MEM_JEMALLOC=ON \
 -DBOOST_ROOT=%{_prefix}

make %{?_smp_mflags}

%install
cd cmake-make
make install DESTDIR=${RPM_BUILD_ROOT}
cd ..

#
# Create empty %%{_libdir}/blender/scripts to claim ownership
#

mkdir -p ${RPM_BUILD_ROOT}%{blenderarch}/{scripts,plugins/sequence,plugins/texture}

find release/datafiles/locale -name '.svn' -exec rm -f {} ';'

cp -a release/datafiles/locale ${RPM_BUILD_ROOT}%{_datadir}

cp -R -a -p release/scripts/* ${RPM_BUILD_ROOT}%{blenderlib}/scripts

find ${RPM_BUILD_ROOT}%{blenderlib}/scripts -type f -exec sed -i -e 's/\r$//g' {} \;

# Install hicolor icons.
for i in 16x16 22x22 32x32 48x48 256x256 ; do
  mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/${i}/apps
  install -pm 0644 release/freedesktop/icons/${i}/apps/%{name}.png \
    ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/${i}/apps/%{name}.png
done

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/scalable/apps
install -pm 0644 release/freedesktop/icons/scalable/apps/%{name}.svg \
    ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

install -p -D -m 644 %{SOURCE5} ${RPM_BUILD_ROOT}%{_datadir}/mime/packages/blender.xml

desktop-file-validate ${RPM_BUILD_ROOT}%{_datadir}/applications/blender.desktop

# Plugins are not support now
rm -rf ${RPM_BUILD_ROOT}%{blenderarch}/plugins/*

#
# man page
#

mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man1
install -p -D -m 644 doc/manpage/blender.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/
install -p -D -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_mandir}/man1/

rm -rf ${RPM_BUILD_ROOT}%{_bindir}/blender-thumbnailer.py

rm -rf ${RPM_BUILD_ROOT}%{_docdir}/blender/*

rm -rf ${RPM_BUILD_ROOT}/%{blenderlib}/datafiles/locale/*
cp -a release/datafiles/locale/languages ${RPM_BUILD_ROOT}/%{blenderlib}/datafiles/locale/

rm -rf ${RPM_BUILD_ROOT}/%{blenderlib}/datafiles/fonts

#
# rpm macros
#

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/rpm

sed -e 's/@VERSION@/%{blender_api}/g' %{SOURCE10} \
     >${RPM_BUILD_ROOT}%{_sysconfdir}/rpm/macros.blender

rm ${RPM_BUILD_ROOT}/%{_datadir}/locale/languages

mkdir -p ${RPM_BUILD_ROOT}/%{blender_fontdir}/
cp -p release/datafiles/fonts/*.ttf.gz \
    ${RPM_BUILD_ROOT}%{blender_fontdir}/

%find_lang %{name}

%post
%{_bindir}/update-mime-database %{_datadir}/mime &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi 
%{_bindir}/update-desktop-database %{_datadir}/applications || :

%postun
%{_bindir}/update-mime-database %{_datadir}/mime &> /dev/null || :
%{_bindir}/update-desktop-database %{_datadir}/applications
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi || :

%files -f blender.lang
%defattr(-,root,root,-)
%{_bindir}/blender
%{_datadir}/applications/blender.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_libdir}/blender/
%{_datadir}/blender/
%{_datadir}/mime/packages/blender.xml
%{_mandir}/man1/blender.*
%doc COPYING doc/license/*-license.txt 

%files -n blenderplayer
%defattr(-,root,root,-)
%{_bindir}/blenderplayer
%{_mandir}/man1/blenderplayer.*
%doc COPYING doc/license/*-license.txt

%files rpm-macros
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.blender

%files -n fonts-blender
%defattr(-,root,root,-)
%{blender_fontdir}/
%doc release/datafiles/LICENSE-bmonofont-i18n.ttf.txt

%changelog
* Sun Feb  2 2014 Ting-Wei Lan <lantw44@gmail.com> - 1:2.69-5
- Enable FFmpeg codec.

* Tue Dec 31 2013 François Cami <fcami@fedoraproject.org> - 1:2.69-5
- Enable parallel building.

* Tue Dec 31 2013 François Cami <fcami@fedoraproject.org> - 1:2.69-4
- Add Ocean Simulation (#1047589).
- Fix mixed use of tabs and spaces in blender.spec (rpmlint).

* Wed Nov 27 2013 Rex Dieter <rdieter@fedoraproject.org> - 1:2.69-3
- rebuild (openexr)

* Mon Nov 18 2013 Dave Airlie <airlied@redhat.com> - 1:2.69-2
- rebuilt for GLEW 1.10

* Thu Oct 31 2013 Jochen Schmitt <Jochen herr-schmitt de> - 1:2.69-1
- New upsream release

* Mon Sep  9 2013 François Cami <fcami@fedoraproject.org> - 1:2.68a-6
- Rebuild.

* Wed Sep  4 2013 Jochen Schmitt <Jochen herr-schmitt de> - 1:2.68a-5
- Include derived DoridSans font for CJK support (#867205)

* Sun Sep  1 2013 Jochen Schmitt <Jochen herr-schmitt de> - 1:2.68a-4
- Aboid twice occurance of locale files
- Fix typo in DroideSans font name

* Wed Aug 28 2013 François Cami <fcami@fedoraproject.org> - 1:2.68a-3
- Enable jemalloc and OpenColorIO. (#1002197)
- Re-enable localization (#867285)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.68a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Jochen Schmitt <Jochen herr-schmitt de> - 1:2.68a-1
- New minor upstream bugfix release

* Mon Jul 29 2013 Petr Machata <pmachata@redhat.com> - 1:2.68-4
- Rebuild for boost 1.54.0

* Tue Jul 23 2013 Jochen Schmitt <Jochen herr-schmitt de> - 1:2.68-3
- Rebuilt again

* Mon Jul 22 2013 Richard Shaw <hobbes1069@gmail.com> - 1:2.68-2
- Rebuild for updated OpenImageIO.

* Fri Jul 19 2013 Jochen Schmitt <Jochen herr-schmitt de> - 1:2.68-1
- New upstream release

* Sun Jul  7 2013 Jochen Schmitt <Jochen herr-schmitt de> - 1:2.67b-3
- Suppress output of update-mime-database (#541041)

* Fri Jun  7 2013 Jochen Schmitt <Jochen herr-schmitt de> - 1:2.67b-1
- Minor upstream bugfix update

* Mon Jun  3 2013 Jochen Schmitt <Jochen herr-schmitt de> - 1:2.67a-3
- Fix crash in blender/makerna/intern/rna_access.c (ä969043)

* Sun May 26 2013 Dan Horák <dan[at]danny.cz> - 1:2.67a-2
- fix build on non-x86 arches

* Fri May 24 2013 Jochen Schmitt <Jochen herr-schmitt de> - 1:2.67a-1
- New minor upstream release

* Fri May 17 2013 Jochen Schmitt <Jochen herr-schmitt de> - 1:2.67-2
- Fix dependency issues with fonts subpackage
- Make fonts subpackage noarch

* Wed May  8 2013 Jochen Schmitt <Jochen herr-schmitt de> - 1:2.67-1
- New upstream release
- Add subpackage for international mono space font

* Sun Mar 10 2013 Rex Dieter <rdieter@fedoraproject.org> - 1:2.66a-2
- rebuild (OpenEXR)

* Wed Mar  6 2013 Jochen Schmitt <Jochen herr-schmitt de> - 1:2.66a-1
- New upstream release

* Sat Feb 23 2013 Jochen Schmitt <Jochen herr-schmitt de> - 1:2.66-2
- Fix wrong font name for international feature (#867205)

* Thu Feb 21 2013 Jochen Schmitt <Jochen herr-schmitt de> - 1:2.66-1
- New upstream release
- Remove unnecessaries patches
- Add Patch to remove '//' in includes

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1:2.65a-5
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1:2.65a-4
- Rebuild for Boost-1.53.0

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1:2.65a-3
- rebuild due to "jpeg8-ABI" feature drop

* Tue Jan 15 2013 Richard Shaw <hobbes1069@gmail.com> - 1:2.65a-2
- Rebuild for updated OpenImageIO library.

* Thu Dec 20 2012 Jochen Schmitt <Jochen herr-schmitt de> - 1:2.65a-1
- New upstream release

* Sat Dec 15 2012 Jochen Schmitt <JOchen herr-schmitt de> - 1:2.65-4
- Fix SEGFAULT in blf_lang.c (#887413)

* Fri Dec 14 2012 Jochen Schmitt <Jochen herr-schmitt de> - 1:2.65-3
- Remove Req. to the DejaVu Sans font

* Thu Dec 13 2012 Adam Jackson <ajax@redhat.com> - 1:2.65-2
- Rebuild for glew 1.9.0

* Tue Dec 11 2012 Jochen Schmitt <Jochen herr schmitt de> - 1:2.65-1
- New upstream release

* Mon Oct 29 2012 Dan Horák <dan[at]danny.cz> - 1:2.64a-3
- fix build on big endian arches

* Thu Oct 18 2012 Jochen Schmitt <Jochen herr-schmitt de> - 1:2.64a-2
- Loading droid-sans font from /usr/share/fonts (#867205)

* Tue Oct  9 2012 Jochen Schmitt <Jochen herr-schmitt de> - 1:2.64a-1
- New minor upstream update release

* Fri Oct  5 2012 Dan Horák <dan[at]danny.cz> - 1:2.64-2
- fix build on non-x86 64-bit arches

* Wed Oct  3 2012 Jochen Schmitt <Jochen herr-schmitt de> - 1:2.64-1
- New upstream release

* Fri Sep  7 2012 Jochen Schmitt <JOchen herr-schmitt de> - 1:2.63a-10
- Add forgotten O_EXCL to CVE-patch

* Thu Sep  6 2012 Jochen Schmitt <JOchen herr-schmitt de> - 1:2.63a-8
- Porting blender-2.49b-cve.patch (#855092, CVE-2008-1103)

* Fri Aug 10 2012 Richard Shaw <hobbes1069@gmail.com> - 1:2.63a-7
- Rebuild for libboost 1.50.

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 1:2.63a-6
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Wed Aug 01 2012 Adam Jackson <ajax@redhat.com> - 1:2.63a-5
- -Rebuild for new glew

* Sun Jul 29 2012 Jochen Schmitt <Jochen herr-schmitt de> - 1:2.63a-4
- Rebult to fix broken dependencies

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.63a-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Richard Shaw <hobbes1069@gmail.com> 1:2.63a-2
- Bump revision to be >= f17 for AutoQA.

* Fri May 11 2012 Jochen Schmitt <Jochen herr-schmitt de> 1:2.63a-1
- New upstream release

* Fri Apr 27 2012 Jochen Schmitt <JOchen herr-schmitt de> 1:2.63-1
- New upstream release

* Wed Apr 25 2012 Jochen Schmitt <Jochen herr-schmitt de> 1:2.62-6
- Fix crash in libspnav (#814665)

* Tue Apr 24 2012 Jochen Schmitt <Jochen herr-schmitt de> 1:2.62-5
- Add cycles support (#812354)

* Fri Apr 13 2012 Jochen Schmitt <Jochen herr-schmitt de> 1:2.62-4
- Add BR to libspnav-devel

* Sun Mar 18 2012 Jochen Schmitt <Jochen herr-schmitt de> 1:2.62-3
- Rebuild for new OpenImageIO release

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1:2.62-2
- Rebuilt for c++ ABI breakage

* Thu Feb 16 2012 Jochen Schmitt <Jochen herr-schmitt de> 1:2.62-1
- New upstream release

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> 1:2.61-6
- Rebuild against PCRE 8.30

* Thu Feb 09 2012 Rex Dieter <rdieter@fedoraproject.org> 1:2.61-5
- rebuild (openjpeg)

* Thu Feb  9 2012 Jochen Schmitt <Jochen herr-schmitt de> 1:2.61-4
- Remove unnecessary gcc-4.5 patch

* Wed Feb  8 2012 Jochen Schmitt <Jochen herr-schmitt de> 1:2.61-3
- Fix gcc-4.7 related issue

* Thu Jan  5 2012 Jochen Schmitt <JOchen herr-schmitt de> 1:2.61-2
- Fix typo in syspth patch (#771814)

* Wed Dec 14 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.61-1
- New upstream release
- Add OpenImageIO-devel as a BR
- Package cleanup

* Wed Nov 23 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.60a-8
- Set BuildArch to noarch for blender-rpm-macros

* Wed Nov 23 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.60a-7
- Remove %%blender_requires and %%blenderplayer_requires entirely

* Wed Nov 23 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.60a-6
- Futher rework on macros.blender
- Add explicit BR to boost-devel

* Mon Nov 21 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.60a-4
- Fix error in macros.blender, add %%blendert_addons

* Mon Nov  7 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.60a-3
- Rebuilt for new openCOLLADA release

* Tue Nov  1 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.60a-2
- Rebuilt for new openCOLLADA release

* Wed Oct 26 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.60a-1
- New upstream release

* Wed Oct 19 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.60-1
- New upstream release

* Sun Aug 14 2011 Jochen Schmitt <JOchen herr-schmitt de> 1:2.59-1
- New upstream release

* Thu Aug 11 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.58a-6
- Fix issues with blneder_requires macro

* Tue Aug  9 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.58a-5
- Suppres python byte compiling
- Add additional codecs

* Sun Aug  7 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.58a-4
- Add man page for blenderplayer
- Add support for openCOLLADA
- Remove debugging statement from syspath patch

* Mon Aug  1 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.58a-3
- Cleanup

* Mon Aug  1 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.58a-2
- Remove scons configuration file

* Sun Jul 10 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.58a-1
- New upstream release with minor bug fixes

* Thu Jun 30 2011 Jochen Schmitt <Jochen herr schmitt.de>  1:2.58-4
- Rework on cmake build

* Mon Jun 27 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.58-3
- Migrating to the cmake build system

* Mon Jun 27 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.58-2
- New upstream release

* Mon Jun 20 2011 ajax@redhat.com - 1:2.57b-5
- Rebuild for new glew soname

* Tue May 17 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.57b-4
- Add virtual provides for blenderplayer(ABI)

* Tue May 17 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.57b-3
- Add virtual provides for blender ABI

* Tue May 17 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.57b-2
- Definition of blender_api macro

* Fri Apr 29 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.57b-1
- New minor upstream update

* Wed Apr 27 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.57-3
- Add patch to solve CVE-2009-3850 (#5333395)

* Sat Apr 16 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.57-2
- Add plugin directory
- Add locale

* Thu Apr 14 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.57-1
- First non-beta release of the 2.5 series (taken from svn)

* Wed Apr 13 2011 Jochen Schmitt <Jochen herr-schmitt de> 1:2.56-12.svn36007%{?dist}
- Increase Epoch
- Add rpm-macros subpackage
- Exclude currently unsed directories (plugin support)

* Sun Apr 10 2011 Jochen Schmitt <Jochen herr-schmitt de> 2.56-11.svn36007%{?dist}
- Add accidently removed files

* Thu Apr  7 2011 Jochen Schmitt <Jochen herr-schmitt de> 2.56-10.svn36007%{?dist}
- Change compiler flags to fixed UI issue (#671284)
- Exclude plugin directory (not supported in current release)

* Wed Apr  6 2011 Jochen Schmitt <Jochen herr-schmitt de> 2.56-9.svn36007%{?dist}
- New upstream release
- Missing UI issue fixed (#671284)

* Wed Mar 23 2011 Jochen Schmitt <Jochen herr-schmitt de> 2.56-8.svn35722%{?dist}
- Update to snapshot svn35722

* Tue Feb 08 2011 Paulo Roma <roma@lcg.ufrj.br> - 2.56-7
- Rebuilt without linking to libgettextlib (bugzilla #650471).
- Applied gcc46 patch

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.56-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Jochen Schmitt <Jochen herr-schmitt de> 2.56-5
- Remove ref to #extern/glew/include from all scons files

* Wed Jan 19 2011 Jochen Schmitt <Jochen herr-schmitt de> 2.56-4
- Readd blenderplayer subpackage

* Wed Jan 19 2011 Jochen Schmitt <Jochen herr-schmitt de> 2.56-3
- Fix RPM_OPT_FLAGS honour issue

* Wed Jan 19 2011 Dan Horák <dan[at]danny.cz> 2.56-2
- use SSE optimization only on x86 platforms

* Wed Jan 12 2011 Rex Dieter <rdieter@fedoraproject.org> 2.49b-11
- rebuild (openjpeg)

* Tue Jul 27 2010 David Malcolm <dmalcolm@redhat.com> 2.49b-10
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jun 21 2010 Nicolas Chauvet <kwizart@gmail.com> 2.49b-9
- Rebuild for gettext

* Wed May 26 2010 Jochen Schmitt <Jochen herr-schmitt de> 2.49b-8
- Add large file support for 32-bit plattforms (#585668)

* Thu Apr  8 2010 Jochen Schmitt <s4504kr@omega> 2.49b-7
- Remove unused BR fontpackages-devel

* Sun Mar 28 2010 Jochen Schmitt <s4504kr@omega> 2.49b-6
- Try to fix copy of userid into files.owner (#572186)

* Wed Jan 13 2010 Jochen Schmitt <Jochen herr-schmitt de> 2.49b-5
- Add forgotten patch

* Wed Jan 13 2010 Jochen Schmitt <Jochen herr-schmitt de> 2.49b-4
- Fix O_CREAT issue on existing quit.blend file (#553959)
- Move quit.blend to ~/.blender

* Mon Nov 23 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.49b-3
- Remove symlink to DejaVu font from package

* Thu Nov 12 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.49b-2
- Rebuild

* Mon Sep  7 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.49b-1
- New upstream release (#520780)

* Tue Aug 11 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.49a-6
- Build again new freealut relase (openalut-soft)

* Mon Aug  3 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.49a-5
- Revoke using of system FTGL library

* Mon Aug  3 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.49a-4
- Rebuild for python-2.6.2

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.49a-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul  6 2009 kwizart < kwizart at gmail.com > 2.49a-2
- Fix perm on blend2renderinfo.py - raised by #506957

* Fri Jun 19 2009 kwizart < kwizart at gmail.com > 2.49a-1
- Update to 2.49a

* Fri Jun 19 2009 kwizart < kwizart at gmail.com > 2.49-6
- Update blender-wrapper script.
- Repackage the sources archive.
- Remove deprecated import/export-3ds-0.7.py
- Pick desktop and icons from tarball and use hicolor icons.
- Hack config.py to add system libqhull along with gettexlib.

* Fri Jun 12 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.49-5
- Fix Type
- Change symlink to %%{_fontbasedir}/Dejavu/...

* Wed Jun  3 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.49-4
- Rework on the blender wrapper script

* Tue Jun  2 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.49-3
- Try to build agains more system libraries as possible

* Mon Jun  1 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.49-1
- New upstream release

* Wed May 13 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-22
- Copy bpydata/config/* into ~/.blender/.../bpydata/config in blender-wrapper script

* Mon Apr 20 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-21
- Chamge BR mesa-libGL* into libGL* 

* Mon Apr 20 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-20
- Remove x264 from source tar ball
- Some cosmetic changes

* Wed Apr  1 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-19
- Change nonfree to freeworld

* Tue Mar 31 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-18
- Fix typo

* Tue Mar 31 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-17
- Create drop-in for non-free blender release

* Wed Mar 11 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-16
- Put blenderplayer into a separate subpackage (#489685) 

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.48a-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-14
- Fix broken wrapper script

* Wed Jan 21 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-13
- Do some fixes on blender-wrapeer

* Sun Jan 18 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-12
- Change Req. for font package because fonts naming was changed (#480444)

* Thu Jan 15 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-11
- Rebuild for new openssl package

* Sun Jan 11 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-10
- Create symlink to DajaVu-Sans

* Tue Jan  6 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-9
- Create fonts sub-package (#477370)

* Sat Dec 27 2008 Lubomir Rintel <lkundrak@v3.sk> 2.48a-7
- Fix optflags use, this time for real

* Sat Dec 27 2008 Lubomir Rintel <lkundrak@v3.sk> 2.48a-6
- Use proper compiler flags (see #199418)
- Minor grammar & language fixes and tidy-ups

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 2.48a-5
- Rebuild for Python 2.6

* Mon Nov  3 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-4
- Fix security issue (#469655, CVE-2008-4863)
[5~
* Sun Oct 26 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-3
- Create %%{_libdir}/blender/scripts/ to claim ownership

* Sun Oct 26 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-1
- New upstream release

* Wed Oct 15 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.48-1
- New upstream release
- Build agains system glew library (#466755)

* Tue Oct  7 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.47-5
- Reorganisation directory structure to fix sysinfo.py issue

* Tue Oct  7 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.47-4
- Avoid duplicate python script (#465810)

* Sun Sep  7 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.47-3
- Fix prerelease SPEC file

* Thu Aug 14 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.47-1
- New upstream release

* Tue Aug 12 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.47-0.2
- New upstream release (blender-2.47rc)

* Mon May 19 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.46-1
- New upstream release

* Wed May  7 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.46-0.3.1
- Some fixes for CVE-2008-1003

* Tue May  6 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.46-0.3
- Release Canditate for 2.46

* Sun Apr 27 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.45-13
- More generic patch for scons issue

* Thu Apr 24 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.45-12
- Fix odd scons compatibility issue

* Thu Apr 24 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.45-11
- Fix CVS-2008-1102 (#443937)

* Wed Mar 12 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.45-10
- Clarification of restrictions caused by legal issues

* Tue Mar  4 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.45-9
- Apply yafray patch only on 64-bit systems

* Thu Feb 28 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.45-8
- Fix yafray load bug (#451571)

* Sun Feb 10 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.45-7
- Rebuild for gcc-4.3

* Sat Jan 26 2008 Alex Lancaster <alexlan[AT]fedoraproject org> 2.45-6
- Rebuild for new gettext

* Thu Jan 17 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.45-5
- Fix gcc-4.3 related issues

* Tue Oct 16 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.45-4
- Rebuild again for OpenEXR

* Sun Oct 14 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.45-3
- Rebuild

* Sun Sep 23 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.45-2
- Change method how to determinate python version

* Thu Sep 20 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.45-1
- New upstream release

* Thu Aug  9 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.44-8
- Fix koji-python issue

* Wed Aug  8 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.44-6
- Changing license tag
- Add python as an BR

* Mon May 21 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.44-4
- Use of $$RPM_OPT_FLAGS to compile blender

* Sun May 20 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.44-2
- Increase release number

* Tue May 15 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.44-1
- New upstream release

* Wed May  9 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-24
- Remove ffmpeg lib during a legal issue (#239476)

* Tue May  8 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-23
- Exclude ppc64 arch

* Mon May  7 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-21
- Fix security issue (#239338)

* Sun Apr 22 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-20
- Romove package from the x86_64 arch (#237423)

* Mon Jan  8 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-18
- Rebult

* Thu Dec 14 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-17
- Replace x86-patch with one from the blender project

* Thu Dec 14 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-16
- Rebuild

* Tue Dec 12 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-12
- Fix typo

* Tue Dec 12 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-11
- Try x64-patch for complle with python-2.5

* Tue Dec 12 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-10
- Exclude x86_64 arch (#219329)

* Mon Dec 11 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-9
- New build to solve broken deps

* Wed Nov 29 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-6
- Rebuild to solve broken deps

* Tue Oct 31 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-5
- Rebuilt to fix broken deps

* Mon Oct 16 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-4
- /usr/lib/blender should own by the package

* Wed Oct 11 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-3
- Correct invalid locale paths (#210209)

* Wed Sep 13 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-2
- Update to new upstream release

* Tue Sep 12 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42-10
- Rebuild to solve broken deps

* Sun Sep  3 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42-9
- Rebuild for FC-6

* Thu Aug 10 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42-7
- Remove %%ghost for pyo files for fullfilling new packaging guidelines

* Thu Aug 10 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42-6
- Rebuilt to solve broken deps

* Wed Jul 26 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42-5
- Fix symlink in blender-wrapper to locale

* Thu Jul 20 2006 Jochen Schmitt <jochen herr-schmitt de> 2.42-4
- Fix UI Problem (#199418)

* Mon Jul 17 2006 Jochen Schmitt <jochen herr-schmitt de> 2.42-3
- Fix some BR stuff.

* Sun Jul 16 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42-1
- New upstream release.

* Sun Feb 19 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.41-3
- Rebuild for FC-5.

* Mon Feb  6 2006 Jochen Schmitt <Jochen herr-schmitt.de> 2.41-2
- Add freealut as dependancy.

* Sun Jan 30 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.41-1
- Update to new upstream release.

* Wed Jan 18 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.40-2
- New upstream release.
- adapting to mudular X.
- add libtiff-devel as BuildRequires.

* Mon Jun 6 2005 Toshio Kuratomi <toshio-tiki-lounge.com> 2.37-3
- Bump release for development.

* Sun Jun 5 2005 Toshio Kuratomi <toshio-tiki-lounge.com> 2.37-2
- Patch to fix compilation errors on x86_64.

* Sun Jun 5 2005 Toshio Kuratomi <toshio-tiki-lounge.com> 2.37-1
- Update to 2.37.
- Drop gcc4 patch.

* Mon May 16 2005 Toshio Kuratomi <toshio-tiki-lounge.com> 2.36-3
- Bump and rebuild now that scons is available on all platforms.

* Sat May 14 2005 Toshio Kuratomi <toshio-tiki-lounge.com> 2.36-2
- Fix a gcc4 error.

* Fri May 13 2005 Toshio Kuratomi <toshio-tiki-lounge.com> 2.36-1
- Update to 2.36.
- Rebuild with new gcc4.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Mon Nov 15 2004 Phillip Compton <pcompton[AT]proteinmedia.com> 2.35-1
- 2.35.

* Thu Nov 11 2004 Phillip Compton <pcompton[AT]proteinmedia.com> 2.34-0.fdr.3
- Mime-type corrections for FC3.
- Dropped redundent BR XFree86-devel.

* Thu Aug 05 2004 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.34-0.fdr.2
- blender.applications file.
- blender.xml file.
- post/postun update-mime-database.

* Thu Aug 05 2004 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.34-0.fdr.1
- Updated to 2.34.

* Thu Aug 05 2004 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.33-0.fdr.2.a
- Include 3ds import/export scripts.
- Added mime info.
- Added mime icon (from yattacier theme).

* Wed Aug 04 2004 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.33-0.fdr.1.a
- 2.33a.
- Now building with scons.

* Tue Feb 10 2004 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.32-0.fdr.2
- Now including scripts.

* Thu Feb 05 2004 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.32-0.fdr.1
- Updated to 2.32.

* Sun Jan 11 2004 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.31-0.fdr.3.a
- --enable-openal.
- --disable-rpath.
- remove --enable-international.
- modify .desktop to execute with -w.

* Thu Dec 04 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.31-0.fdr.2.a
- Updated to 2.31a.

* Sun Nov 30 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.31-0.fdr.1
- Updated to 2.31.
- enable-international.

* Tue Nov 18 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.30-0.fdr.1
- Updated to 2.30.

* Fri Oct 10 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.28-0.fdr.5.c
- Updated to 2.28c.

* Tue Oct 07 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.28-0.fdr.4.a
- Removed BuildReq smpeg-devel

* Mon Sep 15 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.28-0.fdr.3.a
- Moved 'a' out of version according to naming guidelines.

* Fri Sep 12 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.28a-0.fdr.2
- changed file permission on tarball.
- dropped redundant messages about aclocal, etc.
- configure --disable-shared.
- automake --foreign.
- added doc/python-dev-guide.txt doc/GPL-license.txt doc/bf-members.txt to %%doc.

* Wed Sep 10 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.28a-0.fdr.1
- Updated to 2.28a.

* Wed Aug 13 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.28-0.fdr.2
- New Icon.

* Thu Jul 24 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.28-0.fdr.1
- Updated to 2.28.
- BuildReq libvorbis-devel.
- BuildReq smpeg-devel.
- BuildReq esound-devel.
- BuildReq libogg-devel.
- BuildReq vorbis-tools.
- BuildReq openal-devel
- BuildReq libtool

* Mon May 26 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.27-0.fdr.2
- Removed post/postun ldconfig.
- Added autoconf workaround.

* Mon May 19 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.27-0.fdr.1
- Updated to 2.27.
- Removed devel package.

* Wed Apr 09 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.26-0.fdr.9
- Corrected devel Group.

* Tue Apr 01 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.26-0.fdr.8
- Added desktop-file-utils to BuildRequires.
- Changed category to X-Fedora-Extra.

* Mon Mar 31 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.26-0.fdr.7
- Added Missing BuildRequires.

* Sun Mar 30 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.26-0.fdr.6
- Cleaned up BuildRequires.
- Added Epoch:0.

* Sat Mar 22 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 2.26-0.fdr.5
- Spec file cleanup.

* Sat Mar 08 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 2.26-1.fdr.4
- Spec file cleanup.

* Wed Feb 26 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 2.26-1.fedora.3
- Spec file cleanup.

* Thu Feb 20 2003 Warren Togami
- Add BuildRequires python-devel

* Wed Feb 19 2003 Phillip Compton
- Initial RPM release.
