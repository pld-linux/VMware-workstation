#
# TODO:
#	- Standarize init script
#	- What about internal libs?
#	- What about config?
#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	smp		# without SMP kernel modules
#
%include	/usr/lib/rpm/macros.perl

%define		_ver	4.5.1
%define		_build	7568
%define		_rel	0.3
%define		_urel	56

Summary:	VMware Workstation
Summary(pl):	VMware Workstation - wirtualna platforma dla stacji roboczej
Name:		VMware-workstation
Version:	%{_ver}.%{_build}
Release:	%{_rel}
License:	custom, non-distributable
Group:		Applications/Emulators
Source0:	http://download3.vmware.com/software/wkst/%{name}-%{_ver}-%{_build}.tar.gz
NoSource:	0
Source1:	http://knihovny.cvut.cz/ftp/pub/vmware/vmware-any-any-update%{_urel}.tar.gz
# Source1-md5:	bde9dbcfbaaaefe3afb5223eaf911e1d
Source2:	%{name}.init
Source3:	%{name}-vmnet.conf
Patch0:		%{name}-Makefile.patch
URL:		http://www.vmware.com/
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.118
BuildRequires:	%{kgcc_package}
Requires:	kernel(vmmon) = %{version}-%{_rel}
%{?with_dist_kernel:BuildRequires:	kernel-headers}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
VMware Workstation Virtual Platform is a thin software layer that
allows multiple guest operating systems to run concurrently on a
single standard PC, without repartitioning or rebooting, and
without significant loss of performance.

%description -l pl
VMware Workstation Virtual Platform to cienka warstwa oprogramowania
pozwalaj�ca na jednoczesne dzia�anie wielu go�cinnych system�w
operacyjnych na jednym zwyk�ym PC, bez repartycjonowania ani
rebootowania, bez znacznej utraty wydajno�ci.

%package debug
Summary:	TODO
Summary(pl):	TODO
Group:		Application/Emulators
Requires:	%{name} = %{version}-%{release}

%description debug
TODO.

%description debug -l pl
TODO.

%package help
Summary:	VMware Workstation help files
Summary(pl):	Pliki pomocy dla VMware Workstation
Group:		Application/Emulators
Requires:	%{name} = %{version}-%{release}
Requires:	mozilla

%description help
VMware Workstation help files.

%description help -l pl
Pliki pomocy dla VMware Workstation.

%package networking
Summary:	TODO
Summary(pl):	TODO
Group:		Application/Emulators
Requires:	%{name} = %{version}-%{release}
Requires:	kernel(vmnet) = %{version}-%{_rel}

%description networking
TODO.

%description networking -l pl
TODO.

%package samba
Summary:	TODO
Summary(pl):	TODO
Group:		Application/Emulators
Requires:	%{name} = %{version}-%{release}

%description samba
TODO.

%description samba -l pl
TODO.

%package -n kernel-misc-vmmon
Summary:	Kernel module for VMware Workstation
Summary(pl):	Modu� j�dra dla VMware Workstation
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Provides:	kernel(vmmon) = %{version}-%{_rel}
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:%requires_releq_kernel_up}

%description -n kernel-misc-vmmon
Kernel modules for VMware Workstation - vmmon.

%description -n kernel-misc-vmmon -l pl
Modu�y j�dra dla VMware Workstation - vmmon.

%package -n kernel-misc-vmnet
Summary:	Kernel module for VMware Workstation
Summary(pl):	Modu� j�dra dla VMware Workstation
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Provides:	kernel(vmnet) = %{version}-%{_rel}
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:%requires_releq_kernel_up}

%description -n kernel-misc-vmnet
Kernel modules for VMware Workstation - vmnet.

%description -n kernel-misc-vmnet -l pl
Modu�y j�dra dla VMware Workstation - vmnet.

%package -n kernel-smp-misc-vmmon
Summary:	SMP kernel module for VMware Workstation
Summary(pl):	Modu� j�dra SMP dla VMware Workstation
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Provides:	kernel(vmmon) = %{version}-%{_rel}
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:%requires_releq_kernel_smp}

%description -n kernel-smp-misc-vmmon
SMP kernel modules fov VMware Workstation - vmmon-smp.

%description -n kernel-smp-misc-vmmon -l pl
Modu�y j�dra SMP dla VMware Workstation - vmmon-smp.

%package -n kernel-smp-misc-vmnet
Summary:	SMP kernel module for VMware Workstation
Summary(pl):	Modu� j�dra SMP dla VMware Workstation
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Provides:	kernel(vmnet) = %{version}-%{_rel}
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:%requires_releq_kernel_smp}

%description -n kernel-smp-misc-vmnet
SMP kernel module for VMware Workstation - vmnet-smp.

%description -n kernel-smp-misc-vmnet -l pl
Modu�y j�dra SMP dla VMware Workstation -  vmnet-smp.

%prep
%setup -q -n vmware-distrib
%setup -qDT -n vmware-distrib -a1
cd vmware-any-any-update%{_urel}
tar xf vmmon.tar
tar xf vmnet.tar
%patch0 -p0

%build
cd vmware-any-any-update%{_urel}
for mod in vmmon vmnet ; do
	for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
		if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
			exit 1
		fi
		cd ${mod}-only
		%{__make} clean
		install -d include/{linux,config}
		%{__make} -C %{_kernelsrcdir} mrproper SUBDIRS=$PWD O=$PWD
		ln -sf %{_kernelsrcdir}/config-$cfg .config
		ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
		touch include/linux/MARKER
		touch includeCheck.h
		%{__make} -C %{_kernelsrcdir} modules \
			%{?with_smp:CPPFLAGS=\"-D__SMP__ SUPPORT_SMP=1\"} \
			SUBDIRS=$PWD O=$PWD \
			VM_KBUILD=26
		mv ${mod}.ko ${mod}-$cfg.ko
		cd -
	done
done
cd -

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT%{_sysconfdir}/vmware \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_libdir}/vmware/bin \
	$RPM_BUILD_ROOT%{_mandir} \
	$RPM_BUILD_ROOT/etc/rc.d/init.d \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc \
	$RPM_BUILD_ROOT/var/run/vmware

cd vmware-any-any-update%{_urel}
install vmmon-only/vmmon-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/vmmon.ko
install vmnet-only/vmnet-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/vmnet.ko
%if %{with smp} && %{with dist_kernel}
install vmmon-only/vmmon-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/vmmon.ko
install vmnet-only/vmnet-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/vmnet.ko
%endif
cd -

install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/vmnet
install %{SOURCE3} $RPM_BUILD_ROOT/etc/vmware/vmnet.conf

cp	bin/*-* $RPM_BUILD_ROOT%{_bindir}

cp	lib/bin/vmware $RPM_BUILD_ROOT%{_bindir}

cp -r	lib/bin/vmware-vmx \
	$RPM_BUILD_ROOT%{_libdir}/vmware/bin

cp -r	lib/{bin-debug,config,floppies,help*,isoimages,licenses,messages,smb,xkeymap} \
	$RPM_BUILD_ROOT%{_libdir}/vmware

cp -r	man/* $RPM_BUILD_ROOT%{_mandir}
gunzip	$RPM_BUILD_ROOT%{_mandir}/man?/*.gz

%clean
rm -rf $RPM_BUILD_ROOT

%post networking
/sbin/chkconfig --add vmnet
if [ -r /var/lock/subsys/vmnet ]; then
	/etc/rc.d/init.d/vmnet restart >&2
else
	echo "Run \"/etc/rc.d/init.d/vmnet start\" to start VMware networking service."
fi

%preun networking
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/vmnet ]; then
		/etc/rc.d/init.d/vmnet stop >&2
	fi
	/sbin/chkconfig --del vmnet
fi

%post	-n kernel-misc-vmmon
%depmod %{_kernel_ver}

%postun -n kernel-misc-vmmon
%depmod %{_kernel_ver}

%post	-n kernel-misc-vmnet
%depmod %{_kernel_ver}

%postun -n kernel-misc-vmnet
%depmod %{_kernel_ver}

%post	-n kernel-smp-misc-vmmon
%depmod %{_kernel_ver}

%postun -n kernel-smp-misc-vmmon
%depmod %{_kernel_ver}

%post	-n kernel-smp-misc-vmnet
%depmod %{_kernel_ver}

%postun -n kernel-smp-misc-vmnet
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
%doc doc/* lib/configurator/vmnet-{dhcpd,nat}.conf
%dev (c,10,165) %attr(640,root,root) /dev/vmmon
%dev (c,119,10) %attr(640,root,root) /dev/vmnet0
%dev (c,119,10) %attr(640,root,root) /dev/vmnet1
%dev (c,119,10) %attr(640,root,root) /dev/vmnet2
%dev (c,119,10) %attr(640,root,root) /dev/vmnet3
%dev (c,119,10) %attr(640,root,root) /dev/vmnet4
%dev (c,119,10) %attr(640,root,root) /dev/vmnet5
%dev (c,119,10) %attr(640,root,root) /dev/vmnet6
%dev (c,119,10) %attr(640,root,root) /dev/vmnet7
%dev (c,119,10) %attr(640,root,root) /dev/vmnet8
%dir %{_sysconfdir}/vmware
%attr(755,root,root) %{_bindir}/vmware
%attr(755,root,root) %{_bindir}/vmware-loop
%attr(755,root,root) %{_bindir}/vmware-mount.pl
%attr(755,root,root) %{_bindir}/vmware-wizard
%dir %{_libdir}/vmware
%dir %{_libdir}/vmware/bin
# warning: SUID !!!
%attr(4755,root,root) %{_libdir}/vmware/bin/vmware-vmx
%{_libdir}/vmware/config
%{_libdir}/vmware/floppies
%{_libdir}/vmware/isoimages
%{_libdir}/vmware/licenses
%dir %{_libdir}/vmware/messages
%{_libdir}/vmware/messages/en
%lang(ja) %{_libdir}/vmware/messages/ja
%{_libdir}/vmware/xkeymap
%{_mandir}/man1/*
%attr(1777,root,root) %dir /var/run/vmware

%files debug
%defattr(644,root,root,755)
%dir %{_libdir}/vmware/bin-debug
# warning: SUID !!!
%attr(4755,root,root) %{_libdir}/vmware/bin-debug/vmware-vmx

%files help
%defattr(644,root,root,755)
%{_libdir}/vmware/help*

%files networking
%defattr(644,root,root,755)
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/vmware/vmnet.conf
%attr(754,root,root) /etc/rc.d/init.d/vmnet
%attr(755,root,root) %{_bindir}/vmnet-bridge
%attr(755,root,root) %{_bindir}/vmnet-dhcpd
%attr(755,root,root) %{_bindir}/vmnet-natd
%attr(755,root,root) %{_bindir}/vmnet-netifup
%attr(755,root,root) %{_bindir}/vmnet-sniffer
%attr(755,root,root) %{_bindir}/vmware-ping

%files samba
%defattr(644,root,root,755)
%doc lib/configurator/vmnet-smb.conf
%attr(755,root,root) %{_bindir}/vmware-nmbd
%attr(755,root,root) %{_bindir}/vmware-smbd
%attr(755,root,root) %{_bindir}/vmware-smbpasswd
%attr(755,root,root) %{_bindir}/vmware-smbpasswd.bin
%{_libdir}/vmware/smb

%files -n kernel-misc-vmmon
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vmmon.*

%files -n kernel-misc-vmnet
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vmnet.*

%if %{with smp} && %{with dist_kernel}
%files	-n kernel-smp-misc-vmmon
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/vmmon-smp.*

%files	-n kernel-smp-misc-vmnet
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/vmnet-smp.*
%endif
