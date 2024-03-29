%define beanstalkd_user      beanstalkd
%define beanstalkd_group     %{beanstalkd_user}
%define beanstalkd_home      %{_localstatedir}/lib/beanstalkd
%define beanstalkd_logdir    %{_localstatedir}/log/beanstalkd

Name:           beanstalkd
Version:        1.12
Release:        0%{?dist}
Summary:        A simple, fast workqueue service

Group:          System Environment/Daemons
License:        GPLv3+
URL:            http://xph.us/software/%{name}/
Source0:        http://xph.us/dist/%{name}/rel/%{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(pre):      %{_sbindir}/useradd
Requires(post):     /sbin/chkconfig
Requires(preun):    /sbin/chkconfig, /sbin/service
Requires(postun):   /sbin/service


%description
Beanstalk is a simple, fast workqueue service. Its interface is generic, but
was originally designed for reducing the latency of page views in high-volume
web applications by running time-consuming tasks asynchronously.


%prep
%setup -q
if [ ! -e configure ]; then
  sh buildconf.sh
fi

%build
%configure --disable-rpath --docdir=%{_defaultdocdir}/%{name}-%{version}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%{__install} -p -D -m 0644 doc/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
%{__install} -p -D -m 0755 scripts/%{name}.init %{buildroot}%{_initrddir}/%{name}
%{__install} -p -D -m 0644 scripts/%{name}.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{name}


%clean
rm -rf $RPM_BUILD_ROOT

%pre
%{_sbindir}/useradd -c "beanstalkd user" -s /bin/false -r -m -d %{beanstalkd_home} %{beanstalkd_user} 2>/dev/null || :

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc %{_defaultdocdir}/%{name}-%{version}/protocol.txt
%doc README COPYING doc/protocol.txt
%{_initrddir}/%{name}
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}


%changelog
* Thu Oct 1 2009 Keith Rarick <kr@xph.us> - 1.4-0
- Convert this file to an autoconf template
- Tweak the summary and description

* Sun Jan 4 2009 Ask Bjørn Hansen <ask@develooper.com> - 1.2-0
- 1.2-tobe
- Use man page and .init/sysconfig scripts from .tar.gz

* Sat Nov 22 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.1-1
- initial spec creation
