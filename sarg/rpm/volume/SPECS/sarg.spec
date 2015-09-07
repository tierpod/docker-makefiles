# $Id$
# Authority: dag
# Upstream: Pedro L. Orso <orso$onda,com,br>
# Upstream: <orso$yahoogroups,com>
# Tag: rft

Summary: Squid usage report generator per user/ip/name
Name: sarg
Version: 2.3.10
Release: 2%{?dist}
License: GPL
Group: Applications/Internet
URL: http://sarg.sourceforge.net/sarg.php

Source: http://downloads.sourceforge.net/project/sarg/sarg/sarg-%{version}/sarg-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gcc
BuildRequires: gd-devel >= 1.8
BuildRequires: openldap-devel
BuildRequires: perl
Requires: bash
Requires: gd >= 1.8
Requires: squid
Obsoletes: sqmgrlog

%description
Squid Analysis Report Generator is a tool that allows you to view "where"
your users are going to on the Internet. Sarg generate reports in html
showing users, IP addresses, bytes, sites and times.

%prep
%setup

%{__chmod} u+wx sarg-php/locale/

# Update default config
%{__perl} -pi.orig -e '
        s|^#(access_log) (.+)$|#$1 $2\n$1 %{_localstatedir}/log/squid/access.log.0|;
        s|^#(output_dir) (.+)$|#$1 $2\n$1 %{_localstatedir}/www/html/sarg|;
        s|^#(show_successful_message) (.+)$|#$1 $2\n$1 no|;
        s|^#(mail_utility) (.+)$|#$1 $2\n$1 mail|;
        s|^#(external_css_file) (.+)$|#$1 $2\n$1 /sarg/sarg.css|;
		s|^#(graph_font) (.+)$|#$1 $2\n$1 %{_sysconfdir}/sarg/fonts/DejaVuSans.ttf|;
		s|^#(font_size) (.+)$|#$1 $2\n$1 12px|;
		s|^#(header_font_size) (.+)$|#$1 $2\n$1 12px|;
		s|^#(title_font_size) (.+)$|#$1 $2\n$1 14px|;
    ' sarg.conf

# Add nginx config
%{__cat} <<'EOF' >sarg-nginx.conf
server {
	listen *:443;
	server_name	localhost;

	access_log /var/log/nginx/sarg-ssl-access.log main;

	ssl on;
	ssl_certificate ssl/localhost.crt;
	ssl_certificate_key ssl/localhost.key;

	ssl_protocols SSLv3 TLSv1;
	ssl_ciphers ALL:!ADH:!EXPORT56:RC4:RSA:+HIGH:+MEDIUM:+LOW:+SSLv2:+EXP;
	ssl_prefer_server_ciphers on;

	ssl_session_timeout 5m;

	location /sarg {
		autoindex on;
		root /var/www/html;
		auth_basic "Restricted";
		auth_basic_user_file auth/htpasswd;
	}
}
EOF

# Add cron.d
%{__cat} <<'EOF' >sarg-cron
SHELL=/bin/sh
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root
59 23 * * * root squid-maintenance.sh
EOF

# Add squid-maintenance.sh
%{__cat} <<'EOF' >squid-maintenance.sh
#!/bin/sh -e

PATH=/sbin:/bin:/usr/sbin:/usr/bin

logger -t $0 'Start squid maintenance'

logger -t $0 'Rotate squid logs'
squid -k rotate

sleep 5

logger -t $0 'Generate sarg reports'
sarg -l /var/logs/squid/access.log.0

logger -t $0 'End squid maintenance'
EOF

%build
%configure \
    --bindir="%{_bindir}" \
    --sysconfdir="%{_sysconfdir}/sarg" \
    --mandir="%{_mandir}/man1" \
    --disable-rpath \
    --disable-sargphp \
    --enable-extraprotection \
    --enable-imagedir="%{_sysconfdir}/sarg/images"
%{__make} %{?_smp_mflags} CFLAGS="%{optflags}"

%install
%{__rm} -rf %{buildroot}
%{__install} -Dp -m0755 sarg %{buildroot}%{_bindir}/sarg
%{__install} -Dp -m0755 squid-maintenance.sh %{buildroot}%{_bindir}/squid-maintenance.sh
%{__install} -Dp -m0644 sarg.conf %{buildroot}%{_sysconfdir}/sarg/sarg.conf
%{__install} -Dp -m0644 exclude_codes %{buildroot}%{_sysconfdir}/sarg/exclude_codes
%{__install} -Dp -m0644 sarg.1 %{buildroot}%{_mandir}/man1/sarg.1

%{__install} -Dp -m0644 sarg-nginx.conf %{buildroot}%{_sysconfdir}/nginx/conf.d/sarg.conf
%{__install} -Dp -m0644 css.tpl %{buildroot}%{_localstatedir}/www/html/sarg/sarg.css
%{__install} -Dp -m0755 sarg-cron %{buildroot}%{_sysconfdir}/cron.d/sarg

%{__cp} -av fonts/ images/ %{buildroot}%{_sysconfdir}/sarg/

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc ChangeLog CONTRIBUTORS COPYING DONATIONS README
%doc %{_mandir}/man1/sarg.1*
%dir %{_sysconfdir}/sarg/
%config %{_sysconfdir}/sarg/exclude_codes
%config(noreplace) %{_sysconfdir}/sarg/sarg.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/sarg.conf
%{_bindir}/sarg
%{_bindir}/squid-maintenance.sh
%{_localstatedir}/www/html/sarg/
%{_sysconfdir}/sarg/fonts/
%{_sysconfdir}/sarg/images/
%{_sysconfdir}/cron.d/sarg

%changelog
* Mon Sep 07 2015 Pavel Podkorytov <pod.pavel@gmail.com> - 2.3.10-3
- Added cron.d script and squid-maintenance.sh scrips
- Moved nginx directory to /var/www/html/sarg (centos 7 default)

* Fri Sep 04 2015 Pavel Podkorytov <pod.pavel@gmail.com> - 2.3.10-2
- Remove unused cron tasks
- Remove sarg-index.html
- Replace sarg-httpd with sarg-nginx config

* Fri May 22 2015 Pavel Podkorytov <pod.pavel@gmail.com> - 2.3.10-1
- Update to version 2.3.10-1
- Remove 'language' directory

* Thu Oct 13 2011 Thiago Coutinho <root@thiagoc.net> - 2.3.1-1
- Updated to version 2.3.1.
- Fixed cron scripts to support RHEL/CentOS 6.

* Tue Jun 22 2010 Christoph Maser <cmaser@gmx.de> - 2.3-2
- Build with ldap support.

* Tue Jun 22 2010 Christoph Maser <cmaser@gmx.de> - 2.3-1
- Updated to version 2.3.

* Thu Jun 19 2008 Dries Verachtert <dries@ulyssis.org> - 2.2.5-1
- Updated to release 2.2.5.

* Sat Aug 25 2007 Dag Wieers <dag@wieers.com> - 2.2.3.1-1
- Updated to release 2.2.3.1.

* Sat Aug 25 2007 Dag Wieers <dag@wieers.com> - 2.2.3-1
- Updated to release 2.2.3.
- Fixed typo in monthly script. (Rabie Van der Merwe)

* Mon May 29 2006 Dag Wieers <dag@wieers.com> - 2.2.1-1
- Updated to release 2.2.1.
- Many changes to reflect release 2.2. (Bernard Lheureux)

* Wed Aug 04 2004 Dag Wieers <dag@wieers.com> - 1.4.1-5
- Fixed ugly bug in weekly and monthly cron entries. (Viktor Zoubkov)

* Wed Jun 30 2004 Dag Wieers <dag@wieers.com> - 1.4.1-4
- Fixed default mail_utility. (John Florian)

* Sat Apr 10 2004 Dag Wieers <dag@wieers.com> - 1.4.1-3
- Fixed problem with inline cron-scripts. (Luigi Iotti)

* Tue Apr 06 2004 Dag Wieers <dag@wieers.com> - 1.4.1-2
- Fixed missing directories in sarg. (William Hooper)

* Wed Mar 17 2004 Dag Wieers <dag@wieers.com> - 1.4.1-1
- Initial package. (using DAR)
