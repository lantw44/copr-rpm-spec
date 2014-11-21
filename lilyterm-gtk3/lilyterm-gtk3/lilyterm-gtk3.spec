# Review at https://bugzilla.redhat.com/show_bug.cgi?id=496167

%global prerelease

Name:           lilyterm-gtk3
Version:        0.9.9.2
Release:        3%{?prerelease:.%{?prerelease}}%{?dist}
Summary:        Light and easy to use X Terminal Emulator (Copr: lantw44/patches)

Group:          User Interface/X
License:        GPLv3+
URL:            http://lilyterm.luna.com.tw
Source0:        http://lilyterm.luna.com.tw/file/lilyterm-%{version}%{?prerelease:~%{?prerelease}}.tar.gz
Patch0:         lilyterm-gtk3.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk3-devel
BuildRequires:  vte3-devel
BuildRequires:  desktop-file-utils intltool

%description
Copr: lantw44/patches
Note: This is a modified package. Install it if you want to use LilyTerm with
GTK+ 3 and latest VTE.

LilyTerm is a light and easy to use libvte based X Terminal Emulator with a 
lot of features:
 * Supports multiple tabs, reorderable tabs and hides the tab tray when there 
   is only one tab
 * Add, close, swith, move, rename tabs with function keys
 * Disable/Enable function keys for temporary (use <Ctrl><`> by default).
 * Shows the foreground running command on tab and/or window title.
 * Change the font name, size, and window size with right click menu.
 * User custom function keys (need to edit profile).
 * Support for User/System profiles.
 * Supports true transparency if the window manager is composited.
 * Support for transparent background and background saturation.
 * Support for text and background color (need to edit profile).
 * Good support for UTF-8.
 * Decide the text encoding via environment. Using UTF-8 by default.
 * Change the text encoding with right click menu.


%prep
%setup -qn lilyterm-%{version}%{?prerelease:~%{?prerelease}}
%patch0 -p1
rename lilyterm lilyterm-gtk3 data/lilyterm.*

%build
%configure --with-gtk=3.0
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
sed -i -e 's/LilyTerm/LilyTermGtk3/' -e 's/lilyterm/lilyterm-gtk3/' \
  ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop
rm -f ${RPM_BUILD_ROOT}%{_datadir}/applications/lilyterm.desktop
desktop-file-install                                       \
  --delete-original                                        \
  --remove-category=Utility                                \
  --add-category=System                                    \
  --dir=${RPM_BUILD_ROOT}%{_datadir}/applications          \
  ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop
%find_lang %{name}
# we install the docfiles versioned
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/doc/lilyterm/


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.*
%{_mandir}/man*/%{name}.*.*


%changelog
* Mon Mar 03 2014 Ting-Wei Lan <lantw44@gmail.com>
- Use GTK+ 3 version

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.9.2-1
- Update to 0.9.9.2
- Disable parallel make for now as it breaks
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9-0.5.rc8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.9.9-0.4.rc8
- Rebuild for new libpng

* Thu Jun 23 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.9-0.3.rc8
- Completely disable GNOME control-center integration, it won't return (#715952)

* Wed Feb 09 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.9-0.2.rc8
- Temporarily disable GNOME control-center integration for 
  https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 22 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.9-0.1.rc8
- Update to 0.9.9 RC8

* Wed Apr 07 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.8-1
- Update to 0.9.8
- License change from BSD to GPLv3+
- Require control-center-filesystem for gnome-default-applications integration

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 09 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.6-2
- Rebuilt for libvte SONAME bump

* Sat Apr 11 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.6-1
- Update to 0.9.6

* Fri Jul 11 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.5-1
- Update to 0.9.5

* Thu Jul 10 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.4-1
- Update to 0.9.4

* Thu Jun 12 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.3-1
- Update to 0.9.3

* Mon May 12 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.0-1
- Update to 0.9.0

* Mon Apr 21 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.6-1
- Initial Fedora RPM
