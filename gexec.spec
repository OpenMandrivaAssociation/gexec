%define name	gexec	
%define	version 0.3.6
%define release	%mkrel 3
%define lib_name_orig lib%{name}
%define lib_major 0
%define lib_name        %mklibname %{name} %{lib_major}
%define devel_name	%mklibname -d -s %{name}

Summary:	Gexec is a scalable cluster remote execution 
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

