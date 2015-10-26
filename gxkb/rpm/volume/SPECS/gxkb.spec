Name: gxkb
Version: 0.7.6
Release: 0%{?dist}

Summary: Keyboard indicator and switcher
License: GPLv2
Group: System/X11
Url: http://sourceforge.net/projects/%name/

Source: http://download.sourceforge.net/%name/%name-%version.tar.gz

BuildRequires: gtk2-devel libxklavier-devel libwnck-devel

%description
GXKB shows a flag of current keyboard in a systray area and allows you to
switch to another one. It's written in C and uses the GTK library.

%prep
%setup

%build
%configure
%make_build

%install
%make_install

%files
%{_bindir}/%name
%{_datadir}/applications/%name.desktop
%{_datadir}/%name/
%{_datadir}/pixmaps/%name.xpm
%{_mandir}/man1/%name.1.*
%doc doc/AUTHORS doc/NEWS

%changelog
* Mon Oct 26 2015 Pavel Podkorytov <pod.pavel@gmail.com> 0.7.6-0
- Adopted for Fedora 22

* Wed Sep 09 2015 Yuri N. Sedunov <aris@altlinux.org> 0.7.6-alt1
- 0.7.6

* Tue May 05 2015 Yuri N. Sedunov <aris@altlinux.org> 0.7.5-alt1
- 0.7.5

* Tue May 05 2015 Yuri N. Sedunov <aris@altlinux.org> 0.7.4-alt1
- 0.7.4

* Thu Oct 30 2014 Yuri N. Sedunov <aris@altlinux.org> 0.7.3-alt1
- first build for Sisyphus

