Summary: Pidgin plugin for toolbar shrink
Name: pidgin-toolbar-shrink
Version: 1.1.1
Release: 0%{?dist}
License: GPL
Group: Applications/Internet
URL: https://launchpad.net/pidgin-toolbar-shrink

Source: https://launchpad.net/pidgin-toolbar-shrink/trunk/1.1.1/+download/pidgin-toolbar-shrink-1.1.1.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Requires: pidgin
BuildRequires: gcc
BuildRequires: intltool
BuildRequires: pidgin-devel
BuildRequires: glib2-devel

%define _unpackaged_files_terminate_build 0

%description
Pidgin plugin for toolbar shrink

%prep
%setup


%build
%configure
make %{?_smp_mflags}

%install
%make_install

%clean
#%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc ChangeLog README NEWS AUTHORS COPYING INSTALL VERSION
%{_libdir}/pidgin/toolbar_shrink.so
%{_datadir}/locale/*/LC_MESSAGES/pidgin-toolbar-shrink.mo

%changelog
* Wed Oct 14 2015 +0500 Pavel Podkorytov <pod.pavel@gmail.com> - 1.1.1
- Initial release
