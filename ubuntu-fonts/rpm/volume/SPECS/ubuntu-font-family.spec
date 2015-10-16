Name:           ubuntu-font-family
Version:        0.83
Release:        0
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
* Fri 16 16 Oct 2015 14:35:49 +0500 Podkorytov Pave <podkorytov_pm> - 0.83
- Bump version

* Tue Nov 13 2012 Damian Ivanov <damianatorrpm@gmail.com> - 0.2.6-4
- Rewrite spec file
