Name:           keepassx
Version:        2.0
Release:        1%{?dist}
Summary:        Cross-platform password manager
Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://www.keepassx.org
Source0:        https://www.keepassx.org/releases/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  gcc-c++
BuildRequires:  qt4-devel > 4.1
BuildRequires:  libXtst-devel
BuildRequires:  ImageMagick
BuildRequires:  desktop-file-utils
BuildRequires:  cmake
BuildRequires:  libgcrypt-devel
Requires:       hicolor-icon-theme
Requires:       libgcrypt

%description
KeePassX is an application for people with extremly high demands on secure
personal data management.
KeePassX saves many different information e.g. user names, passwords, urls,
attachemts and comments in one single database. For a better management
user-defined titles and icons can be specified for each single entry.
Furthermore the entries are sorted in groups, which are customizable as well.
The integrated search function allows to search in a single group or the
complete database.
KeePassX offers a little utility for secure password generation. The password
generator is very customizable, fast and easy to use. Especially someone who
generates passwords frequently will appreciate this feature.
The complete database is always encrypted either with AES (alias Rijndael) or
Twofish encryption algorithm using a 256 bit key. Therefore the saved
information can be considered as quite safe. KeePassX uses a database format
that is compatible with KeePass Password Safe for MS Windows.

%prep
#%setup -qn keepassx-2.0-beta2
%setup -q

%build
mkdir build
cd build
cmake .. \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DCMAKE_VERBOSE_MAKEFILE=ON \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DWITH_GUI_TESTS=ON

make %{?_smp_mflags}

%install
cd build
make install DESTDIR=%{buildroot}
       
desktop-file-install \
        --dir %{buildroot}%{_datadir}/applications \
        --delete-original \
        --add-mime-type application/x-keepass \
        %{buildroot}%{_datadir}/applications/%{name}.desktop

# Associate KDB* files
cat > x-keepass.desktop << EOF
[Desktop Entry]
Comment=
Hidden=false
Icon=keepassx
MimeType=application/x-keepass
Patterns=*.kdb;*.KDB;*.kdbx;*.KDBX*;
Type=MimeType
EOF
install -D -m 644 -p x-keepass.desktop \
  %{buildroot}%{_datadir}/mimelnk/application/x-keepass.desktop


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null ||:
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null ||:
update-mime-database %{_datadir}/mime &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc CHANGELOG INSTALL COPYING LICENSE*

%{_bindir}/keepassx
%{_libdir}/keepassx/*.so
%{_datadir}/keepassx
%{_datadir}/applications/*.desktop
%{_datadir}/mimelnk/application/*.desktop
%{_datadir}/mime/packages/keepassx.xml
%{_datadir}/icons/hicolor/*/apps/keepassx.*
%{_datadir}/icons/hicolor/*/mimetypes/application-x-keepassx.*

%changelog
* Fri Dec 18 2015 Pavel Podkorytov <pod.pavel@gmail.com> - 2.0-1
- 2.0 release
- Fixed 'Bogus date' error

* Tue Oct 20 2015 George Sapkin <george.sapkin@gmail.com> - 2.0-1.beta2.1
- 2.0 beta 2

* Fri Oct 10 2014 George Sapkin <george.sapkin@gmail.com> - 2.0-1.20141009.0
- git master 20141009

* Tue Oct 7 2014 George Sapkin <george.sapkin@gmail.com> - 2.0-1.20140929
- git master 20140929

