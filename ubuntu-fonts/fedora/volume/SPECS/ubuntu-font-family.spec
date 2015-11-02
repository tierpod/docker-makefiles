Name:           ubuntu-font-family
Version:        0.83
Release:        1
Summary:        Ubuntu fonts by Dalton Maag
Group:          System/GUI/Other
# -- https://launchpad.net/ubuntu-font-licence
License:        Ubuntu Font License 1.0
URL:            http://launchpad.net/ubuntu-font-family
Source0:		http://font.ubuntu.com/download/%{name}-%{version}.zip
BuildArch:      noarch


%description
Beautiful, clear, libre and open font family under development by Dalton Maag
specially for Ubuntu between 2010–2011 (and beyond via community expansion).
The Ubuntu Font Family will include Regular, Bold, Light and Medium weights,
with italics. There will be a Monospaced member of the family for terminal
applications, as well as a Condensed version for space-critical applications.
A total of 13 variants!


%prep
%setup -q
# -- "Laugh it up Miller" - fix typo
mv LICENCE.txt LICENSE.txt
# fix https://bugs.launchpad.net/ubuntu-font-family/+bug/744812 issue:
# wrong font rendering for qt applications
rm Ubuntu-M.ttf Ubuntu-MI.ttf

%build


%install
for font in `ls | grep ttf`; do
    %{__install} -D -m 0644 $font %{buildroot}%{_datadir}/fonts/%{name}/$font
done

%post
if [ -x /usr/bin/fc-cache ]; then
    /usr/bin/fc-cache /usr/share/fonts/dejavu || :
fi


%postun
if [ $1 -eq 0 -a -x /usr/bin/fc-cache ] ; then
    /usr/bin/fc-cache /usr/share/fonts/dejavu || :
fi

%files
%defattr(-,root,root,-)
%doc copyright.txt FONTLOG.txt LICENSE.txt LICENCE-FAQ.txt
%doc TRADEMARKS.txt CONTRIBUTING.txt
%{_datadir}/fonts/%{name}


%changelog
* Fri Oct 24 2015 Podkorytov Pavel <pod.pavel@gmail.com> - 0.83-1
- Remove Ubuntu-M (Medium), fix for bold qt fonts.

* Fri Oct 16 2015 Podkorytov Pavel <pod.pavel@gmail.com> - 0.83-0
- Bump version

* Tue Nov 13 2012 Damian Ivanov <damianatorrpm@gmail.com> - 0.2.6-4
- Rewrite spec file
