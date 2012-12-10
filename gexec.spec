%define name	gexec	
%define	version 0.3.6
%define release	%mkrel 11
%define lib_name_orig lib%{name}
%define lib_major 0
%define lib_name        %mklibname %{name} %{lib_major}
%define devel_name	%mklibname -d -s %{name}

Summary:	Scalable cluster remote execution 
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Networking/Remote access
URL:		http://www.cs.berkeley.edu/~bnc/gexec/
Source:		%{name}-%{version}.tar.bz2
Source1:	gexecd
Source2:	gexec.README
Source3:	gexec
Patch0:		gexec-Makefile.in.patch
#Patch0:		
Requires:	authd >= 0.2, xinetd, tftp
Provides:	%{name}-%{version} = %{version}-%{release}
Buildrequires:	libe-devel >= 0.2.1, %{mklibname authd}-devel >= 0.2
BuildRequires:	openssl-devel
#libganglia-monitor1-devel >= 2.4
BuildRoot:	%{_tmppath}/%{name}-%{version}
Prefix:		%{_prefix}

%package	-n %{devel_name}
Summary:        Gexec scalable cluster remote execution devel package
Provides:       %{name}-devel-%{version} = %{version}-%{release}
Group:          Development/Other
Obsoletes:	%{mklibname gexec 0 -d}

%description
GEXEC is a scalable cluster remote execution system which provides 
fast, RSA authenticated remote execution of parallel and distributed 
jobs. It provides transparent forwarding of stdin, stdout, stderr, and 
signals to and from remote processes, provides local environment 
propagation, and is designed to be robust and to scale to systems over 
1000 nodes.

%description -n %{devel_name}
gexec devel package.

%prep
rm -rf ${buildroot}
%setup -q
%patch0 -p0 -b .patch

%build
%configure --prefix=%{buildroot}/usr
#		--enable-ganglia 

make

%install
rm -Rf %{buildroot}
myname=`id -un`
mygroup=`id -gn`
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}/etc/xinetd.d
mkdir -p %{buildroot}/%{_defaultdocdir}/%{name}
%makeinstall INSTALL_USER=$myname INSTALL_GROUP=$mygroup
mv %{buildroot}/%{_bindir}/gexec %{buildroot}/%{_bindir}/gexec_wrap
install -m 644 %{SOURCE1} %{buildroot}/etc/xinetd.d/gexecd
install -m 644 %{SOURCE2} %{buildroot}/%{_defaultdocdir}/%{name}/README
install -m 755 %{SOURCE3} %{buildroot}/%{_bindir}

%clean
rm -fr %{buildroot}

%post
CHECK_PORT=`grep -w 2875 /etc/services`
if [ -z "$CHECK_PORT" ]; then
cat >> /etc/services << EOF
# Port needed by gexecd"
gexec	2875/tcp       # Caltech gexec
EOF
fi 

if [ -f /var/run/xinetd.pid ]; then
	echo "Restarting xinetd service"
	service xinetd restart	
fi

%postun
if [ -f /var/run/xinetd.pid ]; then
	echo "Restarting xinetd service"
	service xinetd restart	
fi

%files
%defattr(-,root,root) 
%doc INSTALL ChangeLog AUTHORS README
%config(noreplace) %{_sysconfdir}/xinetd.d/gexecd
%{_bindir}/gexec
%{_bindir}/gexec_wrap
%{_sbindir}/gexecd

%files -n %{devel_name}
%defattr(-,root,root)
%doc INSTALL AUTHORS ChangeLog README
%{_includedir}/gexec_lib.h
%{_libdir}/libgexec.a

# %config(noreplace) /etc/X11/wmsession.d/*



%changelog
* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.3.6-11mdv2011.0
+ Revision: 610845
- rebuild

* Fri Apr 23 2010 Funda Wang <fwang@mandriva.org> 0.3.6-10mdv2010.1
+ Revision: 538076
- rebuild

* Wed Apr 21 2010 Funda Wang <fwang@mandriva.org> 0.3.6-9mdv2010.1
+ Revision: 537374
- rebuild

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 0.3.6-8mdv2010.0
+ Revision: 437672
- rebuild

* Thu Aug 28 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.6-7mdv2009.0
+ Revision: 276767
- obsolete old devel package

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 0.3.6-6mdv2009.0
+ Revision: 245946
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 0.3.6-4mdv2008.1
+ Revision: 170860
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

* Sun Feb 17 2008 Michael Scherer <misc@mandriva.org> 0.3.6-3mdv2008.1
+ Revision: 169881
- rebuild to clean youri output

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 22 2007 Nicolas Vigier <nvigier@mandriva.com> 0.3.6-2mdv2008.0
+ Revision: 92241
- add buildrequires on openssl-devel
- rebuild for new libopenssl
 - fix docdir
 - fix provides
 - fix develname
 - fix buildrequires

  + Thierry Vignaud <tv@mandriva.org>
    - kill packaged tag

  + Antoine Ginies <aginies@mandriva.com>
    - use %%mkrel macro


* Thu Nov 17 2005 Antoine Ginies <aginies@n3.mandriva.com> 0.3.6-1mdk
- 0.3.6 release
- few fix in spec file

* Tue Mar 22 2005 Antoine Ginies <aginies@n1.mandrakesoft.com> 0.3.5-8mdk
- rebuild

* Wed Apr 21 2004 Erwan Velu <erwan@mandrakesoft.com> 0.3.5-7mdk
- Rebuild against authd (RSA fixes)

* Wed Apr 21 2004 Erwan Velu <erwan@mandrakesoft.com> 0.3.5-6mdk
- Rebuild against latest libe, authd

* Thu Apr 08 2004 Erwan Velu <erwan@mandrakesoft.com> 0.3.5-5mdk
- Enabling gexec wrapper with cluster.sh
- using grep -w instead of grep for gexec in /etc/services

* Fri Jan 30 2004 Antoine Ginies <aginies@bi.mandrakesoft.com> 0.3.5-4mdk
- rebuild cooker

* Fri Jan 03 2003 Antoine Ginies <aginies@mandrakesoft.com> 0.3.5-3mdk
- rebuild for new glibc

* Fri Jan 03 2003 Antoine Ginies <aginies@mandrakesoft.com> 0.3.5-2mdk
- rebuild fo new glibc

* Wed Nov 06 2002 Clic-dev <clic-dev-public@mandrakesoft.com> 0.3.5-1mdk
- release 0.3.5

* Tue Aug 06 2002 Antoine Ginies <aginies@mandrakesoft.com> 0.3.4-8mdk
- build with gcc 3.2

* Thu Jul 11 2002 Antoine Ginies <aginies@mandrakesoft.com> 0.3.4-7mdk
- Build on 8.2 with 2.96

* Fri Jul 05 2002 Antoine Ginies <aginies@mandrakesoft.com> 0.3.4-6mdk
- fix too many argument error

* Fri Jul 05 2002 Antoine Ginies <aginies@mandrakesoft.com> 0.3.4-5mdk
- fix xinetd restart service

* Tue Jun 25 2002 Antoine Ginies <aginies@mandrakesoft.com> 0.3.4-4mdk
- fix %%post tag

* Thu Jun 20 2002 Antoine Ginies <aginies@mandrakesoft.com> 0.3.4-3mdk
- fix %%postun and add require tftp

* Fri May 17 2002 Antoine Ginies <aginies@mandrakesoft.com> 0.3.4-2mdk
- build gcc 3.1

* Tue May 07 2002 Antoine Ginies <aginies@mandrakesoft.com> 0.3.4-1mdk
- new release

* Thu Apr 25 2002 Antoine Ginies <aginies@mandrakesoft.com> 0.3.3-5mdk
- provide Ganglia support

* Wed Apr 24 2002 Antoine Ginies <aginies@mandrakesoft.com> 0.3.3-4mdk
- new release

* Mon Apr 15 2002 Antoine Ginies <aginies@mandrakesoft.com> 0.3.0-3mdk
- first release for Mandrakesoft

