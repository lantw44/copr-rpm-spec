%global glib2_version 2.61.2
%global gtk3_version 3.24.0
%global webkit2gtk3_version 2.27.3

Name: epiphany
Epoch: 1
Version: 3.38.1
Release: 1%{?dist}.1
Summary: Web browser for GNOME (Copr: lantw44/epiphany-reduce-tab-width)

License: GPLv3+ and CC-BY-SA
URL: https://wiki.gnome.org/Apps/Web
Source0: https://download.gnome.org/sources/epiphany/3.36/%{name}-%{version}.tar.xz

# Fedora bookmarks
Patch0: epiphany-default-bookmarks.patch
# Allow removing it in GNOME Software
Patch1: epiphany-dont-make-compulsory.patch

# Reduce the minimum tab width
Patch2: epiphany-3.34-reduce-tab-width.patch

BuildRequires: desktop-file-utils
BuildRequires: gcc
BuildRequires: gettext-devel
BuildRequires: iso-codes-devel
BuildRequires: itstool
BuildRequires: libappstream-glib-devel
BuildRequires: meson
BuildRequires: pkgconfig(cairo)
BuildRequires: pkgconfig(evince-document-3.0)
BuildRequires: pkgconfig(gcr-3)
BuildRequires: pkgconfig(gdk-3.0) >= %{gtk3_version}
BuildRequires: pkgconfig(gdk-pixbuf-2.0)
BuildRequires: pkgconfig(gio-unix-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(gnome-desktop-3.0) >= %{glib2_version}
BuildRequires: pkgconfig(gtk+-3.0) >= %{gtk3_version}
BuildRequires: pkgconfig(gtk+-unix-print-3.0) >= %{gtk3_version}
BuildRequires: pkgconfig(hogweed)
BuildRequires: pkgconfig(icu-uc)
BuildRequires: pkgconfig(json-glib-1.0)
BuildRequires: pkgconfig(libdazzle-1.0)
BuildRequires: pkgconfig(libhandy-1)
BuildRequires: pkgconfig(libnotify)
BuildRequires: pkgconfig(libportal)
BuildRequires: pkgconfig(libsecret-1)
BuildRequires: pkgconfig(libsoup-2.4)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(libxslt)
BuildRequires: pkgconfig(nettle)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(webkit2gtk-4.0) >= %{webkit2gtk3_version}
BuildRequires: pkgconfig(webkit2gtk-web-extension-4.0) >= %{webkit2gtk3_version}

Requires: gsettings-desktop-schemas
Requires: gtk3%{?_isa} >= %{gtk3_version}
Requires: iso-codes
Requires: webkit2gtk3%{?_isa} >= %{webkit2gtk3_version}

Provides: bundled(gvdb)
Provides: bundled(highlightjs)
Provides: bundled(pdfjs)
Provides: bundled(readabilityjs)

%description
Copr: lantw44/epiphany-reduce-tab-width
Note: This is a modified package. Install it if you want to reduce the tab width
of the GNOME web browser.

Epiphany is the web browser for the GNOME desktop. Its goal is to be
simple and easy to use. Epiphany ties together many GNOME components
in order to let you focus on the Web content, instead of the browser
application.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
%find_lang %{name} --with-gnome

%check
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop

%files -f %{name}.lang
%license COPYING
%doc NEWS README.md
%{_bindir}/epiphany
%{_datadir}/applications/org.gnome.Epiphany.desktop
%{_datadir}/dbus-1/services/org.gnome.Epiphany.SearchProvider.service
%{_datadir}/epiphany
%{_datadir}/icons/hicolor/*/apps/org.gnome.Epiphany*
%{_datadir}/glib-2.0/schemas/org.gnome.epiphany.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.Epiphany.enums.xml
%{_datadir}/metainfo/org.gnome.Epiphany.appdata.xml
%dir %{_datadir}/gnome-shell/
%dir %{_datadir}/gnome-shell/search-providers/
%{_datadir}/gnome-shell/search-providers/org.gnome.Epiphany.SearchProvider.ini
%{_libdir}/epiphany/
%{_libexecdir}/epiphany/
%{_libexecdir}/epiphany-search-provider
%{_mandir}/man*/*

%changelog
* Fri Oct  9 2020 Kalev Lember <klember@redhat.com> - 1:3.38.1-1
- Update to 3.38.1

* Sat Sep 12 2020 Kalev Lember <klember@redhat.com> - 1:3.38.0-1
- Update to 3.38.0

* Fri Sep 04 2020 Kalev Lember <klember@redhat.com> - 1:3.37.92-1
- Update to 3.37.92

* Fri Aug 21 2020 Kalev Lember <klember@redhat.com> - 1:3.37.91-1
- Update to 3.37.91

* Mon Aug 17 2020 Kalev Lember <klember@redhat.com> - 1:3.37.90-1
- Update to 3.37.90

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.37.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 29 2020 Kalev Lember <klember@redhat.com> - 1:3.37.2-1
- Update to 3.37.2

* Mon May 04 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 1:3.37.1-3
- Rebuild for nettle soname bump

* Thu Apr 30 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 1:3.37.1-2
- Don't obsolete the old -runtime subpackage, this belongs to fedora-obsolete-packages
- Add Provides for bundled libraries

* Thu Apr 30 2020 Kalev Lember <klember@redhat.com> - 1:3.37.1-1
- Update to 3.37.1

* Mon Apr 27 2020 Adam Williamson <awilliam@redhat.com> - 1:3.36.1-2
- Obsolete the old -runtime subpackage

* Fri Mar 27 2020 Kalev Lember <klember@redhat.com> - 1:3.36.1-1
- Update to 3.36.1

* Thu Mar 26 2020 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.36.0-2
- Remove epiphany-runtime subpackage again, rhbz#1781359

* Sun Mar 08 2020 Kalev Lember <klember@redhat.com> - 1:3.36.0-1
- Update to 3.36.0

* Mon Mar 02 2020 Kalev Lember <klember@redhat.com> - 1:3.35.92-1
- Update to 3.35.92

* Mon Feb 17 2020 Kalev Lember <klember@redhat.com> - 1:3.35.91-1
- Update to 3.35.91

* Sun Feb 02 2020 Kalev Lember <klember@redhat.com> - 1:3.35.90-1
- Update to 3.35.90

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.35.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 07 2020 Kalev Lember <klember@redhat.com> - 1:3.35.3-1
- Update to 3.35.3

* Tue Dec 10 2019 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.35.2-3
- Restore epiphany-runtime subpackage, it's still needed by fedora-developer-portal

* Mon Dec 09 2019 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.35.2-2
- Remove epiphany-runtime subpackage, rhbz#1781359

* Mon Dec 02 2019 Kalev Lember <klember@redhat.com> - 1:3.35.2-1
- Update to 3.35.2

* Wed Nov 27 2019 Kalev Lember <klember@redhat.com> - 1:3.34.2-1
- Update to 3.34.2

* Mon Oct 07 2019 Kalev Lember <klember@redhat.com> - 1:3.34.1-1
- Update to 3.34.1

* Sat Sep 07 2019 Kalev Lember <klember@redhat.com> - 1:3.34.0-1
- Update to 3.34.0

* Tue Sep 03 2019 Kalev Lember <klember@redhat.com> - 1:3.33.92-1
- Update to 3.33.92

* Tue Aug 20 2019 Kalev Lember <klember@redhat.com> - 1:3.33.91-1
- Update to 3.33.91

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.33.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 15 2019 Kalev Lember <klember@redhat.com> - 1:3.33.4-1
- Update to 3.33.4

* Tue Jun 25 2019 Kalev Lember <klember@redhat.com> - 1:3.33.3-1
- Update to 3.33.3

* Fri Jun 07 2019 Kalev Lember <klember@redhat.com> - 1:3.33.2-1
- Update to 3.33.2

* Thu May 23 2019 Kalev Lember <klember@redhat.com> - 1:3.33.1-1
- Update to 3.33.1

* Tue May 07 2019 Kalev Lember <klember@redhat.com> - 1:3.32.2-2
- Bump required webkitgtk version

* Mon May 06 2019 Kalev Lember <klember@redhat.com> - 1:3.32.2-1
- Update to 3.32.2

* Wed Apr 03 2019 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.32.1.2-2
- Own libexecdir/epiphany

* Fri Mar 22 2019 Kalev Lember <klember@redhat.com> - 1:3.32.1.2-1
- Update to 3.32.1.2

* Thu Mar 21 2019 Kalev Lember <klember@redhat.com> - 1:3.32.1.1-1
- Update to 3.32.1.1

* Wed Mar 20 2019 Kalev Lember <klember@redhat.com> - 1:3.32.1-1
- Update to 3.32.1

* Tue Mar 12 2019 Tim Landscheidt <tim@tim-landscheidt.de> - 1:3.32.0-2
- Remove obsolete requirements for %%post/%%postun scriptlets

* Mon Mar 11 2019 Kalev Lember <klember@redhat.com> - 1:3.32.0-1
- Update to 3.32.0

* Mon Mar 04 2019 Kalev Lember <klember@redhat.com> - 1:3.31.92-1
- Update to 3.31.92

* Tue Feb 19 2019 Kalev Lember <klember@redhat.com> - 1:3.31.91-1
- Update to 3.31.91

* Tue Feb 05 2019 Kalev Lember <klember@redhat.com> - 1:3.31.90-1
- Update to 3.31.90

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.31.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Pete Walter <pwalter@fedoraproject.org> - 1:3.31.4-2
- Rebuild for ICU 63

* Tue Jan 08 2019 Kalev Lember <klember@redhat.com> - 1:3.31.4-1
- Update to 3.31.4

* Mon Oct 22 2018 Kalev Lember <klember@redhat.com> - 1:3.30.2-1
- Update to 3.30.2

* Fri Sep 21 2018 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.30.1-1
- Update to 3.30.1

* Fri Sep 07 2018 Kalev Lember <klember@redhat.com> - 1:3.30.0-1
- Update to 3.30.0

* Mon Aug 20 2018 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.29.91-2
- Add patch to allow removing Epiphany with GNOME Software

* Mon Aug 13 2018 Kalev Lember <klember@redhat.com> - 1:3.29.91-1
- Update to 3.29.91

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.28.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 1:3.28.3.1-2
- Rebuild for ICU 62

* Fri Jun 08 2018 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.28.3.1-1
- Update to 3.28.3.1

* Thu Jun 07 2018 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.28.3-1
- Update to 3.28.3

* Tue May 22 2018 Kalev Lember <klember@redhat.com> - 1:3.28.2.1-1
- Update to 3.28.2.1

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 1:3.28.1.1-2
- Rebuild for ICU 61.1

* Thu Apr 19 2018 Kalev Lember <klember@redhat.com> - 1:3.28.1.1-1
- Update to 3.28.1.1

* Tue Apr 10 2018 Kalev Lember <klember@redhat.com> - 1:3.28.1-1
- Update to 3.28.1

* Sun Mar 11 2018 Kalev Lember <klember@redhat.com> - 1:3.28.0.1-1
- Update to 3.28.0.1

* Sun Mar 11 2018 Kalev Lember <klember@redhat.com> - 1:3.28.0-1
- Update to 3.28.0

* Mon Mar 05 2018 Kalev Lember <klember@redhat.com> - 1:3.27.92-1
- Update to 3.27.92

* Fri Feb 16 2018 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.27.90-1
- Upgrade to 3.27.90. Drop obsolete obsoletes.

* Tue Feb 13 2018 Björn Esser <besser82@fedoraproject.org> - 1:3.27.1-5
- Rebuild against newer gnome-desktop3 package

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.27.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 12 2018 Tomas Popela <tpopela@redhat.com> - 1:3.27.1-3
- Adapt to the webkitgtk4 rename

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 1:3.27.1-2
- Rebuild for ICU 60.1

* Thu Nov 02 2017 Kalev Lember <klember@redhat.com> - 1:3.27.1-1
- Update to 3.27.1

* Wed Nov 01 2017 Kalev Lember <klember@redhat.com> - 1:3.26.2-1
- Update to 3.26.2

* Sun Oct 08 2017 Kalev Lember <klember@redhat.com> - 1:3.26.1-1
- Update to 3.26.1

* Sun Sep 10 2017 Kalev Lember <klember@redhat.com> - 1:3.26.0-1
- Update to 3.26.0

* Tue Sep 05 2017 Kalev Lember <klember@redhat.com> - 1:3.25.92-1
- Update to 3.25.92

* Fri Aug 25 2017 Kalev Lember <klember@redhat.com> - 1:3.25.91-1
- Update to 3.25.91

* Tue Aug 15 2017 Kalev Lember <klember@redhat.com> - 1:3.25.90-1
- Update to 3.25.90

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.25.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.25.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.25.4-1
- Update to 3.25.4

* Wed May 24 2017 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.25.2-1
- Update to 3.25.2

* Wed Apr 26 2017 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.25.1-1
- Update to 3.25.1 with Meson build system

* Tue Apr 11 2017 Kalev Lember <klember@redhat.com> - 1:3.24.1-1
- Update to 3.24.1

* Tue Mar 21 2017 Kalev Lember <klember@redhat.com> - 1:3.24.0-1
- Update to 3.24.0

* Thu Mar 16 2017 Kalev Lember <klember@redhat.com> - 1:3.23.93-1
- Update to 3.23.93

* Sat Mar 11 2017 Richard Hughes <rhughes@redhat.com> - 1:3.23.92-1
- Update to 3.23.92

* Tue Feb 28 2017 Richard Hughes <rhughes@redhat.com> - 1:3.23.91.1-1
- Update to 3.23.91.1

* Tue Feb 14 2017 Richard Hughes <rhughes@redhat.com> - 1:3.23.90-1
- Update to 3.23.90

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.23.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 03 2017 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.23.5-1
- Update to 3.23.5

* Tue Jan 17 2017 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.23.4-1
- Update to 3.23.4

* Tue Jan 03 2017 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.23.3-1
- Update to 3.23.3.
- Spec cleanups.

* Thu Dec 29 2016 Kalev Lember <klember@redhat.com> - 1:3.22.4-1
- Update to 3.22.4

* Thu Nov 24 2016 Kalev Lember <klember@redhat.com> - 1:3.22.3-1
- Update to 3.22.3

* Wed Nov 23 2016 Kalev Lember <klember@redhat.com> - 1:3.22.2-1
- Update to 3.22.2

* Wed Oct 12 2016 Kalev Lember <klember@redhat.com> - 1:3.22.1-1
- Update to 3.22.1

* Mon Sep 19 2016 Kalev Lember <klember@redhat.com> - 1:3.22.0-1
- Update to 3.22.0

* Tue Sep 13 2016 Kalev Lember <klember@redhat.com> - 1:3.21.92-1
- Update to 3.21.92

* Thu Aug 18 2016 Kalev Lember <klember@redhat.com> - 1:3.21.90-1
- Update to 3.21.90
- Use make_install macro
- Move desktop file validation to the check section

* Sun Aug 07 2016 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.21.4-2
- Don't install libtool archive

* Sun Jul 17 2016 Kalev Lember <klember@redhat.com> - 1:3.21.4-1
- Update to 3.21.4

* Mon Jun 20 2016 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.21.3-2
- Bump min WebKitGTK+ version

* Mon Jun 20 2016 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.21.3-1
- Update to 3.21.3

* Thu May 12 2016 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.21.1-2
- Improve default bookmarks patch

* Tue May 03 2016 Kalev Lember <klember@redhat.com> - 1:3.21.1-1
- Update to 3.21.1

* Wed Apr 13 2016 Kalev Lember <klember@redhat.com> - 1:3.20.1-1
- Update to 3.20.1

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 1:3.20.0-1
- Update to 3.20.0

* Tue Mar 15 2016 Richard Hughes <rhughes@redhat.com> - 1:3.19.92-1
- Update to 3.19.92

* Tue Mar 01 2016 Richard Hughes <rhughes@redhat.com> - 1:3.19.91-1
- Update to 3.19.91

* Tue Feb 16 2016 Richard Hughes <rhughes@redhat.com> - 1:3.19.90-1
- Update to 3.19.90

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.19.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 10 2015 Kalev Lember <klember@redhat.com> - 1:3.19.1-1
- Update to 3.19.1

* Fri Nov 20 2015 Kalev Lember <klember@redhat.com> - 1:3.18.1-1
- Update to 3.18.1

* Fri Oct 02 2015 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.18.0-4
- Fix the web extension by overlinking instead of disabling RELRO.

* Thu Oct 01 2015 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.18.0-3
- Bump NVR

* Wed Sep 30 2015 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.18.0-2
- Stop using full relro to fix the web extension.

* Tue Sep 22 2015 Kalev Lember <klember@redhat.com> - 1:3.18.0-1
- Update to 3.18.0

* Wed Sep 09 2015 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.17.91-2
- Restore floating bar patch

* Wed Sep 09 2015 Kalev Lember <klember@redhat.com> - 1:3.17.91-1
- Update to 3.17.91
- Drop upstreamed patches
- Set minimum required webkitgtk4 version

* Sun Aug 02 2015 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.17.2-1
- Update to 3.17.2

* Wed Jul 22 2015 David King <amigadave@amigadave.com> - 1:3.17.1-2
- Bump for new gnome-desktop3

* Tue Jun 23 2015 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.17.1-1
- Update to 3.17.1.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.16.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 David King <amigadave@amigadave.com> - 1:3.16.1-3
- Avoid an undefined symbol in the web extension (#1227948)

* Wed May 27 2015 Michael Catanzaro <mcatanzaro@igalia.com> 1:3.16.1-2
- Drop DRI3 patch since Fedora has switched back to DRI2.

* Tue May 12 2015 Kalev Lember <kalevlember@gmail.com> - 1:3.16.1-1
- Update to 3.16.1

* Mon Apr 06 2015 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.16.0-3
- Also drop title box patch, bgo#741808

* Fri Apr 03 2015 Michael Catanzaro <mcatanzaro@igalia.com> - 1:3.16.0-2
- Drop duplicate menu item patch, rbz#1208906
- Drop xft dpi patch, will be fixed in 3.16.1

* Tue Mar 24 2015 Kalev Lember <kalevlember@gmail.com> - 1:3.16.0-1
- Update to 3.16.0

* Wed Mar 18 2015 Michael Catanzaro <mcatanzaro@gnome.org> - 1:3.15.92-1
- Also drop no-longer-applied, upstreamed patches

* Tue Mar 17 2015 Kalev Lember <kalevlember@gmail.com> - 1:3.15.92-1
- Update to 3.15.92
- Use license macro for the COPYING files

* Wed Mar 04 2015 Michael Catanzaro <mcatanzaro@gnome.org> - 1:3.15.90-4
- Rejigger set of patches.

* Fri Feb 27 2015 Michael Catanzaro <mcatanzaro@gnome.org> - 1:3.15.90-3
- Add patch for rbz#1196847

* Thu Feb 26 2015 Michael Catanzaro <mcatanzaro@gnome.org> - 1:3.15.90-2
- Add several patches that haven't made it upstream yet

* Wed Feb 25 2015 Richard Hughes <rhughes@redhat.com> - 1:3.15.90-1
- Update to 3.15.90

* Fri Feb 06 2015 Michael Catanzaro <mcatanzaro@gnome.org> - 1:3.15.1-2
- Fix the search provider, which was crashing on start

* Fri Dec 12 2014 Michael Catanzaro <mcatanzaro@gnome.org> - 1:3.15.1-1
- Update to 3.15.1

* Thu Nov 13 2014 Michael Catanzaro <mcatanzaro@gnome.org> - 1:3.14.2-2
- Add patch to disable DRI3

* Mon Nov 10 2014 Kalev Lember <kalevlember@gmail.com> - 1:3.14.2-1
- Update to 3.14.2

* Tue Oct 14 2014 Kalev Lember <kalevlember@gmail.com> - 1:3.14.1-1
- Update to 3.14.1

* Wed Sep 24 2014 Kalev Lember <kalevlember@gmail.com> - 1:3.14.0-1
- Update to 3.14.0

* Wed Sep 17 2014 Kalev Lember <kalevlember@gmail.com> - 1:3.13.91-1
- Update to 3.13.91

* Fri Aug 29 2014 Michael Catanzaro <mcatanzaro@gnome.org> - 1:3.13.90-1
- Update to 3.13.90

* Sun Aug 24 2014 Michael Catanzaro <mcatanzaro@gnome.org> - 1:3.12.1-7.20140822gitb0af36e
- Restore desktop-file-utils requirements for update-desktop-database scriplets

* Sat Aug 23 2014 Kalev Lember <kalevlember@gmail.com> - 1:3.12.1-6.20140822gitb0af36e
- Add epoch to -runtime subpackage requires

* Sat Aug 23 2014 Michael Catanzaro <mcatanzaro@gnome.org> - 1:3.12.1-5.20140822gitb0af36e
- Spec file fixes pointed of by Kalev:
 - Restore calls to update-desktop-database "cleaned up" in the last build
 - Tighten -runtime subpackage requirement
 - Move runtime dependencies to -runtime subpackage
 - Call glib-compile-schemas in -runtime subpackage's scriptlets

* Fri Aug 22 2014 Michael Catanzaro <mcatanzaro@gnome.org> - 1:3.12.1-4.20140822gitb0af36e
- Update to git snapshot
- Fix license to GPLv2+ and CC-BY-SA, was GPLv2+ and GFDL prior to 3.10
- Switch to webkitgtk4
- Add epiphany-fix-adblock.patch
- Drop non-applied epiphany-homepage.patch, homepages were removed long ago
- Do not attempt (and fail!) to customize the user agent, this is undesired
- Spec file cleanups

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 15 2014 Kalev Lember <kalevlember@gmail.com> - 1:3.12.1-1
- Update to 3.12.1

* Wed May 07 2014 Kalev Lember <kalevlember@gmail.com> - 1:3.12.0-3
- Drop gnome-icon-theme dependency

* Wed May 07 2014 Kalev Lember <kalevlember@gmail.com> - 1:3.12.0-2
- Backport a fix for a crash with some password forms

* Tue Mar 25 2014 Richard Hughes <rhughes@redhat.com> - 1:3.12.0-1
- Update to 3.12.0

* Thu Mar 20 2014 Matthias Clasen <mclasen@redhat.cpm> - 1:3.11.92-2
- Make the default bookmarks patch more robust; no need
  to crash just because fedora-bookmarks is not installed

* Tue Mar 18 2014 Richard Hughes <rhughes@redhat.com> - 1:3.11.92-1
- Update to 3.11.92

* Tue Mar 04 2014 Richard Hughes <rhughes@redhat.com> - 1:3.11.91-1
- Update to 3.11.91

* Wed Feb 19 2014 Richard Hughes <rhughes@redhat.com> - 1:3.11.90-1
- Update to 3.11.90

* Wed Feb 19 2014 Richard Hughes <rhughes@redhat.com> - 1:3.11.4-2
- Rebuilt for gnome-desktop soname bump

* Fri Feb 07 2014 Kalev Lember <kalevlember@gmail.com> - 1:3.11.4-1
- Update to 3.11.4

* Mon Feb 03 2014 Richard Hughes <rhughes@redhat.com> - 1:3.11.3-2
- Split out a -runtime subpackage to avoid making the gnome-software application
  depend on the epiphany application.

* Tue Jan 14 2014 Richard Hughes <rhughes@redhat.com> - 1:3.11.3-1
- Update to 3.11.3

* Wed Jan 08 2014 Richard Hughes <rhughes@redhat.com> - 1:3.11.2-1
- Update to 3.11.2

* Tue Nov 19 2013 Richard Hughes <rhughes@redhat.com> - 1:3.11.1-1
- Update to 3.11.1

* Mon Nov 18 2013 Richard Hughes <rhughes@redhat.com> - 1:3.10.2-1
- Update to 3.10.2

* Mon Oct 28 2013 Richard Hughes <rhughes@redhat.com> - 1:3.10.1-1
- Update to 3.10.1

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.10.0-1
- Update to 3.10.0

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.9.90-1
- Update to 3.9.90
- Install the appdata and gnome-shell search provider

* Thu Aug 15 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.9.3-1
- Update to 3.9.3

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 31 2013 Debarshi Ray <rishi@fedoraproject.org> - 1:3.9.2-1
- Update to 3.9.2

* Wed Apr 17 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.8.1-1
- Update to 3.8.1

* Wed Mar 27 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.8.0-2
- Rebuilt for libwebkit2gtk soname bump

* Tue Mar 26 2013 Richard Hughes <rhughes@redhat.com> - 1:3.8.0-1
- Update to 3.8.0

* Wed Mar 20 2013 Richard Hughes <rhughes@redhat.com> - 1:3.7.92-1
- Update to 3.7.92

* Mon Mar 11 2013 Debarshi Ray <rishi@fedoraproject.org> - 1:3.7.91-1
- Replace the BuildRequires on libgnome-keyring-devel with libsecret-devel.

* Fri Mar  8 2013 Matthias Clasen <mclasen@redhat.com> - 1:3.7.91-1
- Update to 3.7.91

* Fri Feb 22 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.7.90-2
- Get rid of MOZ_OPT_FLAGS handling

* Fri Feb 22 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.7.90-1
- Update to 3.7.90
- Remove and obsolete the -devel subpackage

* Wed Feb 20 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.7.5-2
- Rebuilt for libgnome-desktop soname bump

* Thu Feb 07 2013 Richard Hughes <rhughes@redhat.com> - 1:3.7.5-1
- Update to 3.7.5

* Wed Feb 06 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.7.3-2
- Rebuilt for libgcr soname bump

* Fri Dec 21 2012 Kalev Lember <kalevlember@gmail.com> - 1:3.7.3-1
- Update to 3.7.3

* Fri Nov 09 2012 Kalev Lember <kalevlember@gmail.com> - 1:3.7.1-1
- Update to 3.7.1
- Adjust for the extension support removal
- Obsolete epiphany-extensions: the most popular extensions will get moved
  into Epiphany proper
- Clean up unneeded BRs and -devel package requires

* Wed Oct 17 2012 Kalev Lember <kalevlember@gmail.com> - 1:3.6.1-2
- Remove last traces of gconf

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 1:3.6.1-1
- Update to 3.6.1

* Thu Oct  4 2012 Matthias Clasen <mclasen@redhat.com> - 1:3.6.0-2
- Update to 3.6.0

* Wed Sep 05 2012 Kalev Lember <kalevlember@gmail.com> - 1:3.5.91.1-1
- Update to 3.5.91.1

* Tue Aug 28 2012 Richard Hughes <hughsient@gmail.com> - 1:3.5.90-1
- Update to 3.5.90

* Tue Aug 07 2012 Richard Hughes <hughsient@gmail.com> - 1:3.5.5-1
- Update to 3.5.5

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Kalev Lember <kalevlember@gmail.com> - 1:3.5.4-1
- Update to 3.5.4

* Tue Jun 26 2012 Richard Hughes <hughsient@gmail.com> - 1:3.5.3-1
- Update to 3.5.3

* Sun May 06 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.1-1
- Update to 3.5.1

* Wed Apr 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1:3.4.1-2
- Add dependency on gnome-icon-theme-symbolic as there's hardcoded references to icons there

* Thu Apr 19 2012 Kalev Lember <kalevlember@gmail.com> - 1:3.4.1-1
- Update to 3.4.1
- Silence the rpm scriptlet output

* Fri Mar 30 2012 Debarshi Ray <rishi@fedoraproject.org> - 1:3.4.0.1-2
- Update %%{major_version}.
- Resolves #808401

* Tue Mar 27 2012 Matthias Clasen <mclasen@redhat.com> - 1:3.4.0.1-1
- Update to 3.4.0.1

* Tue Mar 27 2012 Richard Hughes <hughsient@gmail.com> - 1:3.4.0-1
- Update to 3.4.0

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.92-1
- Update to 3.3.92

* Fri Mar  9 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.91-1
- Update to 3.3.91

* Sun Feb 26 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.90-1
- Update to 3.3.90

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.5-1
- Update to 3.3.5

* Thu Jan 19 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.4.1-1
- Update to 3.3.4.1

* Wed Jan 18 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.4-1
- Update to 3.3.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.3-1
- Update to 3.3.3
- Drop homepage patch; the setting no longer exists

* Wed Nov 30 2011 Bastien Nocera <bnocera@redhat.com> 3.3.2-2
- Remove obsolete BRs, there's no Python support anymore

* Thu Nov 24 2011 Tomas Bzatek <tbzatek@redhat.com> - 1:3.3.2-1
- Update to 3.3.2

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.1-2
- Rebuilt for glibc bug#747377

* Wed Oct 19 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.2.1-1
- Update to 3.2.1

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 1:3.2.0-1
- Update to 3.2.0

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 1:3.1.92-1
- Update to 3.1.92

* Wed Sep  7 2011 Matthias Clasen <mclasen@redhat.com> 3.1.91.1-1
- Update to 3.1.91.1

* Wed Sep 07 2011 Kalev Lember <kalevlember@gmail.com> 3.1.91-1
- Update to 3.1.91

* Wed Aug 31 2011 Kalev Lember <kalevlember@gmail.com> 3.1.90-1
- Update to 3.1.90

* Thu Aug 18 2011 Matthias Clasen <mclasen@redhat.com> 3.1.5-1
- Update to 3.1.5

* Tue Jul 05 2011 Bastien Nocera <bnocera@redhat.com> 3.1.3-1
- Update to 3.1.3

* Fri Jun 17 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.2-1
- Update to 3.1.2

* Thu May 12 2011 Christopher Aillon <caillon@redhat.com> - 1:3.0.3-1
- Update to 3.0.3

* Sun May  8 2011 Christopher Aillon <caillon@redhat.com> - 1:3.0.2-1
- Update to 3.0.2

* Tue Apr 26 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.0.1-1
- Update to 3.0.1

* Tue Apr  5 2011 Christopher Aillon <caillon@redhat.com> 1:3.0.0-2
- devel package no longer needs gnome-desktop-devel

* Mon Apr  4 2011 Christopher Aillon <caillon@redhat.com> 1:3.0.0-1
- Update to 3.0.0

* Thu Mar 24 2011 Dan Williams <dcbw@redhat.com> 1:2.91.92-2
- Rebuild for NM 0.9

* Tue Mar 22 2011 Matthias Clasen <mclasen@redhat.com> 1:2.91.92-1
- Update to 2.91.92

* Sat Mar 12 2011 Christopher Aillon <caillon@redhat.com> 1:2.91.91.1-1
- Update to 2.91.91.1

* Tue Mar  8 2011 Matthias Clasen <mclasen@redhat.com> 1:2.91.91-1
- Update to 2.91.91

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> 1:2.91.90-1
- Update to 2.91.90

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> 1:2.91.6-4
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.91.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Christopher Aillon <caillon@redhat.com> - 1:2.91.6-2
- Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 1:2.91.6-1
- Update to 2.91.6

* Tue Jan 11 2011 Matthias Clasen <mclasen@redhat.com> - 1:2.91.5-1
- Update to 2.91.5

* Sun Jan  9 2011 Matthias Clasen <mclasen@redhat.com> - 1:2.91.4.1-1
- Update to 2.91.4.1

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 1:2.91.3-1
- Update to 2.91.3

* Thu Nov 11 2010 Matthias Clasen <mclasen@redhat.com> - 1:2.91.2.1-1
- Update to 2.91.2.1
- Remove space-saving hacks

* Thu Sep 23 2010 Matthias Clasen <mclasen@redhat.com> - 1:2.31.5-4
- Rebuild with new webkitgtk3

* Mon Aug 23 2010 Matthias Clasen <mclasen@redhat.com> - 1:2.31.5-3
- Co-own /usr/share/gtk-doc

* Wed Aug 11 2010 Matthias Clasen <mclasen@redhat.com> - 1:2.31.5-2
- Add an epoch to stay ahead of F14

* Wed Jul 14 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.5-1
- Update to 2.31.5

* Mon Jul 12 2010 Colin Walters <walters@verbum.org> - 2.31.3-3
- Rebuild against new gobject-introspection

* Fri Jul  2 2010 Matthias Clasen <mclasen@redhat.com> 2.31.3-2
- Rebuild against new webkitgtk

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> 2.31.3-1
- Update to 2.31.3

* Fri May 28 2010 Matthias Clasen <mclasen@redhat.com> 2.31.2-1
- Update to 2.31.2

* Sun Apr 18 2010 Matthias Clasen <mclasen@redhat.com> 2.30.2-1
- Update to 2.30.2
- Use GConf macros

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> 2.30.0-1
- Update to 2.30.0

* Tue Mar 09 2010 Bastien Nocera <bnocera@redhat.com> 2.29.92-1
- Update to 2.29.92

* Mon Feb 22 2010 Matthias Clasen <mclasen@redhat.com> 2.29.91-1
- Update to 2.29.91

* Wed Feb 10 2010 Bastien Nocera <bnocera@redhat.com> 2.29.90.1-1
- Update to 2.29.90.1

* Tue Jan 26 2010 Matthias Clasen <mclasen@redhat.com> 2.29.6-1
- Update to 2.29.6

* Sun Jan 17 2010 Matthias Clasen <mclasen@redhat.com> 2.29.5-1
- Update to 2.29.5

* Wed Dec 09 2009 Bastien Nocera <bnocera@redhat.com> 2.29.3-2
- Remove gnome-vfs2-devel dependency for the devel package

* Tue Dec 01 2009 Bastien Nocera <bnocera@redhat.com> 2.29.3-1
- Update to 2.29.3

* Wed Sep 23 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Mon Sep 14 2009 Bastien Nocera <bnocera@redhat.com> 2.27.92-2
- Call nspluginwrapper's config tool if available

* Tue Sep  8 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.92-1
- Update to 2.27.92

* Tue Aug 25 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.91-1
- Update to 2.27.91

* Tue Aug 11 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.90-1
- Update to 2.27.90

* Mon Aug 10 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.5-2
- Fix a mnemonic mishap

* Tue Jul 28 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.5-1
- Update to 2.27.5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.4-1
- Update to 2.27.4

* Tue Jun 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.3-1
- Update to 2.27.3

* Mon Jun  1 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.2-1
- Update to 2.27.2
- Build against webkit instead of gecko

* Fri May 22 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.26.1-4
- Include /usr/include/epiphany directory (#473651).

* Mon Apr 27 2009 Christopher Aillon <caillon@redhat.com> - 2.26.1-3
- Rebuild against newer gecko

* Mon Apr 27 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-2
- Don't drop schemas translations from po files

* Mon Apr 13 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-1
- Update to 2.26.1
- See http://download.gnome.org/sources/epiphany/2.26/epiphany-2.26.1.changes

* Thu Mar 19 2009 Jan Horak <jhorak@redhat.com> - 2.26.0-2
- Rebuild against newer gecko
- Fix the missing headers by patch

* Tue Mar 17 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Thu Feb 26 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-3
- Fix the build

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Wed Feb  4 2009 Christopher Aillon <caillon@redhat.com> 2.25.5-1
- Update to 2.25.5

* Wed Jan 14 2009 Matěj Cepl <mcepl@redhat.com> 2.24.2.1-5
- Make epiphany own directories for plugins and extensions
  (#479921).

* Tue Jan 06 2009 Christopher Aillon <caillon@redhat.com> - 2.24.2.1-4
- Rebuild against newer gecko

* Tue Dec 23 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.2.1-3
- Rebuild against newer gecko

* Wed Dec 17 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.2.1-2
- Rebuild against new gnome-desktop

* Fri Dec  5 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.2.1-1
- Update to 2.24.2.1

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.24.1-5
- Rebuild for Python 2.6

* Fri Nov 21 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.1-4
- Tweak description

* Thu Nov 13 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.1-3
- Rebuild against newer gecko

* Thu Nov 13 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.1-2
- Rebuild

* Mon Oct 20 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Thu Oct  9 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0.1-4
- Save some more space

* Thu Sep 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0.1-3
- Save some space

* Tue Sep 23 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0.1-2
- Update to 2.24.0.1

* Tue Sep 23 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Wed Jul 23 2008 Christopher Aillon <caillon@redhat.com> - 2.23.5-2
- Rebuild against newer gecko

* Tue Jul 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.5-1
- Update to 2.23.5

* Thu Jul 17 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.22.2-2
- fix license tag

* Wed May 28 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.2-1
- Update to 2.22.2

* Mon Apr  7 2008 Christopher Aillon <caillon@redhat.com> - 2.22.1.1-1
- Update to 2.22.1.1

* Thu Apr  3 2008 Christopher Aillon <caillon@redhat.com> - 2.22.0-4
- Update the Source URL

* Mon Mar 31 2008 Christopher Aillon <caillon@redhat.com> - 2.22.0-3
- Initialize plugins before we startup XPCOM, thanks to Bastien Nocera

* Tue Mar 18 2008 Christopher Aillon <caillon@redhat.com> - 2.22.0-2
- Update the homepage

* Mon Mar 10 2008 Christopher Aillon <caillon@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Fri Mar  7 2008 Christopher Aillon <caillon@redhat.com> - 2.21.92-3
- Update the xulrunner patch and tweak the useragent

* Tue Feb 26 2008 Christopher Aillon <caillon@redhat.com> - 2.21.92-2
- Stop shipping LowContrastLargePrint icons

* Tue Feb 26 2008 Christopher Aillon <caillon@redhat.com> - 2.21.92-1
- Update to 2.21.92
- Update the xulrunner patch
- BR: avahi-gobject-devel
- Fix the file list

* Wed Feb  6 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.90-2
- Fix some cosmetic packaging issues

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.90-1
- Update to 2.21.90

* Sat Jan 12 2008 Christopher Aillon <caillon@redhat.com> - 2.21.5-0.1.svn7856
- Update to newer svn, and update the xulrunner 1.9 patch

* Wed Jan  2 2008 Christopher Aillon <caillon@redhat.com> - 2.21.5-0.1.svn7844
- Update to svn to build against xulrunner 1.9

* Mon Dec 17 2007 Christopher Aillon <caillon@redhat.com> - 2.21.4-1
- Update to 2.21.4

* Thu Nov 29 2007 Martin Stransky <stransky@redhat.com>
- Polished the wrapper patch

* Tue Nov 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.2-1
- Update to 2.20.2
 
* Tue Nov 27 2007 Christopher Aillon <caillon@redhat.com> - 2.20.1-6
- Rebuild against newer gecko

* Mon Nov 19 2007 Martin Stransky <stransky@redhat.com> - 2.20.1-5
- Updated wrapper patch

* Sat Nov 10 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-4
- Rebuild against newer gecko

* Tue Oct 23 2007  Matthias Clasen <mclasen@redhat.com> - 2.20.1-3
- Rebuild against new dbus-glib

* Tue Oct 16 2007 - Bastien Nocera <bnocera@redhat.com> - 2.20.1-2
- Add patch to allow epiphany to use the plugins wrapped by
  nspluginwrapper (#334751)

* Tue Oct 16 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-1
- Update to 2.20.1

* Mon Oct 15 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-2
- Fix network status monitoring with new NM (#332771)

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Tue Sep  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.91-1
- Update to 2.19.91

* Fri Aug 24 2007 Adam Jackson <ajax@redhat.com> - 2.19.90-2
- Rebuild for build ID

* Mon Aug 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.90-1
- Update to 2.19.90

* Wed Aug  8 2007 Christopher Aillon <caillon@redhat.com> - 2.19.6-3
- Rebuild against newer gecko

* Mon Aug  6 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-2
- Update license field
- Use %%find_lang for help files, too

* Mon Jul 30 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-1
- Update to 2.19.6

* Wed Jul 25 2007 Jesse Keating <jkeating@redhat.com> - 2.19.5-4
- Rebuild for RH #249435

* Mon Jul 23 2007 Matthias Clasen  <mclasen@redhat.com> - 2.19.5-3
- Port to new GTK+ tooltips API

* Fri Jul 20 2007 Kai Engert <kengert@redhat.com> - 2.19.5-2
- Rebuild against newer gecko

* Tue Jul 10 2007 Matthias Clasen <mclasen@redhat.com> 2.19.5-1
- Update to 2.19.5

* Fri May 25 2007 Christopher Aillon <caillon@redhat.com> 2.19.2-2
- Rebuild against newer gecko

* Mon May 21 2007 Matthias Clasen <mclasen@redhat.com> 2.19.2-1
- Update to 2.19.2

* Sun Apr 15 2007 Christopher Aillon <caillon@redhat.com> 2.18.1-2
- Use the system default bookmarks
- Remove no longer needed autotools BRs

* Tue Apr 10 2007 Christopher Aillon <caillon@redhat.com> 2.18.1-1
- Update to 2.18.1

* Fri Mar 23 2007 Christopher Aillon <caillon@redhat.com> 2.18.0-3
- Rebuild against newer gecko

* Fri Mar 16 2007 Bastien Nocera <bnocera@redhat.com> 2.18.0-2
- Have ephy pick up on the 64-bit plugins (#204547)

* Tue Feb 27 2007 Matthias Clasen <mclasen@redhat.com> 2.17.92-1
- Update to 2.17.92

* Tue Feb 13 2007 Matthias Clasen <mclasen@redhat.com> 2.17.91-1
- Update to 2.17.91

* Tue Jan 23 2007 Matthias Clasen <mclasen@redhat.com> 2.17.90-1
- Update to 2.17.90

* Thu Jan 11 2007 Matthias Clasen <mclasen@redhat.com> 2.17.5-1
- Update to 2.17.5

* Thu Dec 21 2006 Christopher Aillon <caillon@redhat.com> 2.17.4-2
- Rebuild against newer gecko

* Tue Dec 19 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.4-1
- Update to 2.17.4

* Thu Dec  7 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.3-3
- Fix Requires in -devel (#218863)

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 2.17.3-2
- rebuild for python 2.5

* Tue Dec  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.3-1
- Update to 2.17.3

* Mon Nov  6 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.2-1
- Update to 2.17.2

* Fri Oct 27 2006 Christopher Aillon <caillon@redhat.com> - 2.16.1-2
- Rebuild against newer gecko

* Sat Oct 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.1-1
- Update to 2.16.1

* Thu Oct 12 2006 Christopher Aillon <caillon@redhat.com> - 2.16.0-4.fc6
- Remove console spew about pango; it's no longer relevant.

* Thu Oct 12 2006 Christopher Aillon <caillon@redhat.com> - 2.16.0-3.fc6
- Update requires to the virtual gecko version instead of a specific app

* Thu Sep 14 2006 Christopher Aillon <caillon@redhat.com> - 2.16.0-2.fc6
- Rebuild

* Sun Sep  3 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-1.fc6
- Update to 2.16.0

* Wed Aug 30 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.92-3.fc6
- Install the fonts and pango schemas  (#204602)

* Tue Aug 29 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.92-2.fc6
- Use Pango by default
- Add a BR for perl-XML-Parser

* Mon Aug 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.92-1.fc6
- Update to 2.15.92

* Sun Aug 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.91-2.fc6
- Rebuild

* Sun Aug 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.91-1.fc6
- Update to 2.15.91

* Tue Aug  8 2006 Jesse Keating <jkeating@redhat.com> - 2.15.4-2
- bump

* Sat Jul 29 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.4-1
- Update to 2.15.4
- Rebuild against firefox-devel

* Tue Jul 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.1-2
- Go back to 2.15.1, since gecko 1.8 is still missing

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.15.2-1.1
- rebuild

* Wed May 17 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.2-1
- Update to 2.15.2

* Wed May 10 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.1-1
- Update to 2.15.1

* Thu May  4 2006 Dan Williams <dcbw@redhat.com> - 2.14.1-3
- Rebuild for a mozilla update

* Mon Apr 10 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.1-2
- Update to 2.14.1

* Sun Mar 12 2006 Ray Strode <rstrode@redhat.com> - 2.14.0-1
- Update to 2.14.0

* Mon Feb 27 2006 Matthias Clasen <mclasen@redhat.com> - 1.9.8-1
- Update to 1.9.8

* Mon Feb 13 2006 Christopher Aillon <caillon@redhat.com> - 1.9.7-1
- Update to 1.9.7

* Mon Feb 13 2006 Jesse Keating <jkeating@redhat.com> - 1.9.6-3.1
- rebump for build order issues during double-long bump

* Sat Feb 11 2006 Matthias Clasen <mclasen@redhat.com> - 1.9.6-3
- turn on zeroconf and NetworkManager support

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.9.6-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sun Feb  5 2006 Matthias Clasen <mclasen@redhat.com> 1.9.6-2
- Update requires

* Tue Jan 31 2006 Matthias Clasen <mclasen@redhat.com> 1.9.6-1
- Update to 1.9.6

* Fri Jan 20 2006 Matthias Clasen <mclasen@redhat.com> 1.9.5.1-1
- Update to 1.9.5.1

* Mon Jan  2 2006 Christopher Aillon <caillon@redhat.com> 1.9.4-1
- Update to 1.9.4

* Thu Dec 15 2005 Matthias Clasen <mclasen@redhat.com> 1.9.3.1-1
- Update to 1.9.3.1

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec  2 2005 Matthias Clasen <mclasen@redhat.com> - 1.9.2-1
- Update to 1.9.2
- Package plugins

* Tue Oct 18 2005 Christopher Aillon <caillon@redhat.com> - 1.8.2-3
- Build on ppc64

* Tue Oct 18 2005 Christopher Aillon <caillon@redhat.com> - 1.8.2-2
- Rebuild

* Thu Oct  6 2005 Christopher Aillon <caillon@redhat.com> - 1.8.2-1
- Update to 1.8.2

* Mon Sep  5 2005 Christopher Aillon <caillon@redhat.com> - 1.8.0-1
- Update to 1.8.0

* Mon Aug 29 2005 Christopher Aillon <caillon@redhat.com> - 1.7.6-1
- Update to 1.7.6

* Tue Aug 23 2005 Christopher Aillon <caillon@redhat.com> - 1.7.5-1
- Update to 1.7.5

* Mon Aug 15 2005 Christopher Aillon <caillon@redhat.com> - 1.7.4-2
- Rebuild

* Tue Aug  9 2005 Christopher Aillon <caillon@redhat.com> - 1.7.4-1
- Update to 1.7.4

* Sat Jul 30 2005 Christopher Aillon <caillon@redhat.com> - 1.7.3-2
- Rebuild against new mozilla

* Tue Jul 26 2005 Christopher Aillon <caillon@redhat.com> - 1.7.3-1
- Update to 1.7.3

* Tue Jul 19 2005 Christopher Aillon <caillon@redhat.com> - 1.7.2-2
- Rebuild against new mozilla

* Mon Jul 11 2005 Christopher Aillon <caillon@redhat.com> - 1.7.2-1
- Update to 1.7.2

* Tue Jul  5 2005 Christopher Aillon <caillon@redhat.com> - 1.7.1-3
- Add the packages needed for building against -devel to its Requires:
- Add builds for ia64 s390(x)

* Thu Jun 16 2005 Christopher Aillon <caillon@redhat.com> - 1.7.1-2
- Specfile cleanup
- Make the devel package depend on the main package

* Fri Jun 10 2005 Christopher Aillon <caillon@redhat.com> - 1.7.1-1
- Update to 1.7.1

* Fri May 13 2005 Christopher Aillon <caillon@redhat.com> - 1.6.3-1
- Update to 1.6.3

* Fri May 13 2005 Christopher Aillon <caillon@redhat.com> - 1.6.1-3
- Depend on mozilla 1.7.8

* Sat Apr 16 2005 Christopher Aillon <caillon@redhat.com> - 1.6.1-2
- Depend on mozilla 1.7.7

* Wed Apr  6 2005 Elliot Lee <sopwith@redhat.com> - 1.6.1-1
- Update to 1.6.1

* Wed Mar  9 2005 Christopher Aillon <caillon@redhat.com> - 1.5.8-3
- Depend on mozilla 1.7.6

* Sat Mar  5 2005 Christopher Aillon <caillon@redhat.com> - 1.5.8-2
- Rebuild

* Thu Mar  3 2005 Marco Pesenti Gritti <mpg@redhat.com> - 1.5.8-1
- Update to 1.5.8

* Mon Feb 28 2005 Matthias Clasen <mclasen@redhat.com> - 1.5.7-1
- Update to 1.5.7

* Wed Feb  9 2005 Matthias Clasen <mclasen@redhat.com> - 1.5.6-1
- Update to 1.5.6

* Wed Feb  2 2005 Matthias Clasen <mclasen@redhat.com> - 1.5.5-1
- Update to 1.5.5

* Mon Dec 20 2004 Marco Pesenti Gritti <mpg@redhat.com> - 1.4.7-2
- Add the manual to the package

* Mon Dec 20 2004 Marco Pesenti Gritti <mpg@redhat.com> - 1.4.7-1
- Update to 1.4.7

* Mon Dec 20 2004 Marco Pesenti Gritti <mpg@redhat.com> - 1.4.6-2
- Depend on mozilla 1.7.5

* Mon Dec 20 2004 Marco Pesenti Gritti <mpg@redhat.com> - 1.4.6-1
- Update to 1.4.6

* Tue Nov  9 2004 Marco Pesenti Gritti <mpg@redhat.com> - 1.4.4-6
- Add docs

* Thu Nov  4 2004 Marco Pesenti Gritti <mpg@redhat.com> - 1.4.4-5
- Update the desktop files database. Fix #135566

* Mon Oct 18 2004 Christopher Aillon <caillon@redhat.com> 1.4.4-4
- Put back ppc

* Tue Oct 12 2004 Marco Pesenti Gritti <mpg@redhat.com> - 1.4.4-3
- Remove generic name patch, epiphany is no more default

* Tue Oct 12 2004 Marco Pesenti Gritti <mpg@redhat.com> - 1.4.4-2
- Disable direct handling of downloads by external applications

* Mon Oct 11 2004 Marco Pesenti Gritti <mpg@redhat.com> - 1.4.4-1
- Add a devel package for extensions development

* Mon Oct 11 2004 Marco Pesenti Gritti <mpg@redhat.com> - 1.4.4-0
- Update to 1.4.4

* Thu Oct 07 2004 Marco Pesenti Gritti <mpg@redhat.com> - 1.4.3-0
- Remove mozilla 1.7.3 compatibility patch
- Do not disable the nautilus view, it has been removed upstream
 
* Sun Sep 26 2004 Christopher Blizzard <blizzard@redhat.com> - 1.4.0-0.3.6
- Don't require a specific mozilla rpm release, only the version

* Fri Sep 24 2004 Christopher Blizzard <blizzard@redhat.com> - 1.4.0-0.3.5
- Change .desktop file name to "Web Browser" instead of "Epiphany..."

* Fri Sep 24 2004 Christopher Blizzard <blizzard@redhat.com> - 1.4.0-0.3.4
- Include epiphany's default .desktop file - don't remove it.

* Fri Sep 24 2004 Christopher Blizzard <blizzard@redhat.com> - 1.4.0-0.3.3
- Make sure to include the epoch for the mozilla version.

* Fri Sep 24 2004 Christopher Blizzard <blizzard@redhat.com> - 1.4.0-0.3.2
- Add patch to get this epiphany building with moz 1.7.3.

* Fri Sep 24 2004 Christopher Blizzard <blizzard@redhat.com> - 1.4.0-0.3.1
- Don't query for the mozilla version, use an explicit version number

* Fri Sep 24 2004 Christopher Blizzard <blizzard@redhat.com> - 1.4.0-0.3.0
- Update to 1.4.0

* Fri Sep 24 2004 Mark McLoughlin <markmc@redhat.com> - 1.3.8-0.3.3
- Remove the bookmarks editor from the menu (bug #132549)

* Wed Sep 22 2004 Christopher Aillon <caillon@redhat.com> 1.3.8-0.3.2
- Rebuilt to pick up new mozilla changes
- Drop ppc from the build since mozilla doesn't build there anymore.

* Fri Sep 03 2004 Christopher Blizzard <blizzard@redhat.com>
- Bump release and rebuild.

* Wed Sep 01 2004 Christopher Blizzard <blizzard@redht.com>
- Update to 1.3.8

* Tue Aug 17 2004 Christopher Blizzard <blizzard@redhat.com>
- Update to 1.3.5.
- Remove epiphany-bin - it's not there anymore.
- Change to .bz2 source tarball.

* Mon Aug 09 2004 Christopher Aillon <caillon@redhat.com>
- Rebuild

* Tue Aug 03 2004 Christopher Blizzard <blizzard@redhat.com>
- Update to 1.2.7
- Disable nautilus view since it's broken

* Wed Jun 23 2004 Christopher Blizzard <blizzard@redhat.com>
- Update to 1.2.6

* Tue Jun 22 2004 Christopher Blizzard <blizzard@redhat.com>
- Update to 1.2.5

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 05 2004 Warren Togami <wtogami@redhat.com> - 1.2.4-1
- update to 1.2.4 stable

* Wed Mar 10 2004 Christopher Blizzard <blizzard@redhat.com> - 1.1.12-0
- Update to 1.1.12
- remove jrb patch for file chooser api changes since it appears
  to have been merged upstream

* Fri Mar  5 2004 Jeremy Katz <katzj@redhat.com> - 1.1.10-2
- rebuild

* Thu Mar  4 2004 Jeremy Katz <katzj@redhat.com> - 1.1.10-1
- 1.1.10
- add patch from jrb for file-chooser api changes

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Feb 22 2004 Jeremy Katz <katzj@redhat.com> 1.1.9-1
- update to 1.1.9
- reenable nautilus view

* Thu Feb 19 2004 Christopher Blizzard <blizzard@redhat.com> 1.0.7-3
- disable the nautilus view.  doesn't seem to work anymore.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 20 2004 Jeremy Katz <katzj@redhat.com> 1.0.7-1
- 1.0.7

* Tue Dec 02 2003 Christopher Blizzard <blizzard@redhat.com> 1.0.4-3
- Add a BuildRequires for nautilus so that the view is built properly.

* Mon Oct 27 2003 Jakub Jelinek <jakub@redhat.com> 1.0.4-2
- link epiphany-bin with -Wl,-rpath,/usr/lib/mozilla-1.4.1,--enable-new-dtags
  to make it prelinkable

* Fri Oct 24 2003 Jeremy Katz <katzj@redhat.com> 1.0.4-1
- 1.0.4

* Fri Oct 24 2003 Christopher Blizzard <blizzard@redhat.com> 1.0.1-3
- Enable the nautilus view

* Fri Oct 10 2003 Christopher Blizzard <blizzard@redhat.com> 1.0.1-2
- Add patch to set the home page to the release notes

* Mon Oct  6 2003 Jeremy Katz <katzj@redhat.com> 1.0.1-1
- 1.0.1

* Fri Sep 26 2003 Chris Blizzard <blizzard@redhat.com> 1.0-2
- Updates for Mozilla 1.4.1

* Tue Sep  9 2003 Jeremy Katz <katzj@redhat.com> 1.0-1
- 1.0

* Wed Sep  3 2003 Jeremy Katz <katzj@redhat.com> 0.9.3-1
- 0.9.3

* Mon Aug 25 2003 Jeremy Katz <katzj@redhat.com> 0.9.2-1
- 0.9.2

* Mon Aug 11 2003 Jeremy Katz <katzj@redhat.com> 0.8.4-1
- 0.8.4

* Sun Aug 10 2003 Jeremy Katz <katzj@redhat.com> 0.8.3-1
- 0.8.3

* Sun Aug  3 2003 Jeremy Katz <katzj@redhat.com> 0.8.2-1
- 0.8.2

* Fri Jul 25 2003 Christopher Blizzard <blizzard@redhat.com> 0.8.0-2
- Add ppc to the list of arches.

* Tue Jul 15 2003 Matt Wilson <msw@redhat.com> 0.8.0-1
- 0.8.0

* Fri Jul 11 2003 Christopher Blizzard <blizzard@redhat.com> 0.7.3-3
- be sure to include the mozilla rpm in the build deps since it's
  queried

* Tue Jul 01 2003 Elliot Lee <sopwith@redhat.com> 0.7.3-2
- Fix mozilla dep for new epoch

* Sun Jun 29 2003 Jeremy Katz <katzj@redhat.com> 0.7.3-1
- 0.7.3

* Sat Jun 28 2003 Jeremy Katz <katzj@redhat.com> 0.7.2-1
- update to 0.7.2

* Sun Jun  8 2003 Jeremy Katz <katzj@redhat.com> 0.7.0-4
- fix crash on startup in egg-menu-merge on x86_64

* Sat Jun  7 2003 Jeremy Katz <katzj@redhat.com> 0.7.0-3
- fix build on x86_64

* Sat Jun  7 2003 Jeremy Katz <katzj@redhat.com> 0.7.0-2
- fix build with gcc 3.3

* Sat Jun  7 2003 Jeremy Katz <katzj@redhat.com> 0.7.0-1
- update to 0.7.0

* Mon Jun  2 2003 Elliot Lee <sopwith@redhat.com> 0.6.1-2
- Rebuild to fix broken mozilla dep, patch for mozilla 1.4

* Mon May 19 2003 Jeremy Katz <katzj@redhat.com> 0.6.1-1
- 0.6.1

* Fri May  9 2003 Jeremy Katz <katzj@redhat.com> 0.6.0-4
- add patch to fix gint/gpointer conversion bugs for 64bit arches

* Fri May  9 2003 Jeremy Katz <katzj@redhat.com> 0.6.0-3
- only build on arches mozilla is built on

* Fri May  9 2003 Jeremy Katz <katzj@redhat.com> 0.6.0-2
- rebuild against new mozilla, make mozilla requires dynamic

* Sun May  4 2003 Jeremy Katz <katzj@redhat.com> 0.6.0-1
- update to 0.6.0
- fix tyop in %%postun

* Wed Apr 16 2003 Bill Nottingham <notting@redhat.com> 0.5.0-3
- make it build with mozilla-1.4 (shouldn't affect moz-1.2/moz-1.3 builds)

* Mon Apr 14 2003 Jeremy Katz <katzj@redhat.com> 0.5.0-2
- add some buildrequires, prereq GConf2
- disable building nautilus view

* Sun Apr 13 2003 Jeremy Katz <katzj@redhat.com> 
- Initial build.


