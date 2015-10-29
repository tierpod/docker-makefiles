%define contentdir /var/www

Summary:	Squid proxy log analyzer and report generator
Name:		squidanalyzer
Version:	6.3
Release:	1
License:	GPLv3
Group:		Monitoring
URL:		http://%{name}.darold.net/
#Source:		https://github.com/darold/%{name}/archive/v%{version}.tar.gz
Source:		http://prdownloads.sourceforge.net/squid-report/%{name}-%{version}-%{release}.tar.gz
BuildRequires:	perl
BuildArch:	noarch

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: perl-ExtUtils-MakeMaker, perl-ExtUtils-Install, perl-ExtUtils-Manifest, perl-ExtUtils-ParseXS, perl-Time-HiRes
BuildRequires: gdbm-devel, libdb-devel, perl-devel, systemtap-sdt-devel

%description
Squid proxy native log analyzer and reports generator with full
statistics about times, hits, bytes, users, networks, top URLs and
top domains. Statistic reports are oriented toward user and
bandwidth control; this is not a pure cache statistics generator.

SquidAnalyzer uses flat files to store data and doesn't need any SQL,
SQL Lite or Berkeley databases.

This log analyzer is incremental and should be run in a daily cron,
or more often with heavy proxy usage.

%prep

%setup -q -n %{name}-%{version}-%{release}

# Add cron config
%{__cat} <<EOF > %{name}-cron
SHELL=/bin/sh
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root
59 23 * * * root squid-maintenance.sh
EOF

# Add nginx config
%{__cat} <<EOF >%{name}-nginx.conf
server {
	listen *:443;
	server_name	localhost;

	access_log /var/log/nginx/squidanalyzer-ssl-access.log main;

	ssl on;
	ssl_certificate ssl/localhost.crt;
	ssl_certificate_key ssl/localhost.key;

	ssl_protocols SSLv3 TLSv1;
	ssl_ciphers ALL:!ADH:!EXPORT56:RC4:RSA:+HIGH:+MEDIUM:+LOW:+SSLv2:+EXP;
	ssl_prefer_server_ciphers on;

	ssl_session_timeout 5m;

	location /squidanalyzer {
		autoindex on;
		root /var/www/html;
		auth_basic "Restricted";
		auth_basic_user_file auth/htpasswd;
	}
}
EOF

# Add squid-maintenance.sh
%{__cat} <<'EOF' >squid-maintenance.sh
#!/bin/sh -e

PATH=/sbin:/bin:/usr/sbin:/usr/bin

logger -t $0 'Start squid maintenance'

logger -t $0 'Rotate squid logs'
squid -k rotate

sleep 5

logger -t $0 'Generate squidanalyzer reports'
squid-analyzer --no-year-stat --no-week-stat --preserve 2 -j 2

logger -t $0 'End squid maintenance'
EOF

%build
perl Makefile.PL DESTDIR=%{buildroot} LOGFILE=%{_logdir}/squid/access.log BINDIR=%{_bindir} HTMLDIR=%{contentdir}/html/%{name} BASEURL=/%{name} MANDIR=%{_mandir}/man3 QUIET=yes

make

%install
%{__rm} -rf %{buildroot}

%{__mkdir} -p %{buildroot}%{_sysconfdir}/cron.d/
%{__make} DESTDIR=%{buildroot} install
%{__install} etc/* %{buildroot}%{_sysconfdir}/%{name}/
%{__install} -Dp -m0755 %{name}-cron %{buildroot}%{_sysconfdir}/cron.d/%{name}
%{__install} -Dp -m0644 %{name}-nginx.conf %{buildroot}%{_sysconfdir}/nginx/conf.d/%{name}.conf
%{__install} -Dp -m0755 squid-maintenance.sh %{buildroot}%{_bindir}/squid-maintenance.sh

%files
%defattr(-,root,root)
%doc README ChangeLog
%{_mandir}/man3/*
%{perl_vendorlib}/SquidAnalyzer.pm
%attr(0755,root,root) %{_bindir}/squid-analyzer
%attr(0755,root,root) %{_bindir}/squid-maintenance.sh
%attr(0755,root,root) %{_libdir}/perl5/perllocal.pod
%attr(0755,root,root) %{_libdir}/perl5/vendor_perl/auto/SquidAnalyzer/.packlist
%attr(0755,root,root) %dir %{_sysconfdir}/%{name}
%attr(0664,root,root) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/%{name}/excluded
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/%{name}/included
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/%{name}/network-aliases
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/%{name}/user-aliases
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/cron.d/%{name}
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/nginx/conf.d/%{name}.conf
%attr(0755,root,root) %dir %{_sysconfdir}/%{name}/lang
%{_sysconfdir}/%{name}/lang/*
%attr(0755,root,root) %dir %{contentdir}/html/%{name}
%{contentdir}/html/%{name}/flotr2.js
%{contentdir}/html/%{name}/sorttable.js
%{contentdir}/html/%{name}/%{name}.css
%attr(0755,root,root) %dir %{contentdir}/html/%{name}/images
%{contentdir}/html/%{name}/images/*.png

%clean
rm -rf %{buildroot}

