#
# TODO:
#	- Dependencies
#
# Conditional build:
%bcond_with	internal_libs	# internal libs stuff
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	smp		# without SMP kernel modules
#
%include	/usr/lib/rpm/macros.perl

%define		_ver	4.5.1
%define		_build	7568
%define		_rel	4
%define		_urel	57

Summary:	VMware Workstation
Summary(pl):	VMware Workstation - wirtualna platforma dla stacji roboczej
Name:		VMware-workstation
Version:	%{_ver}.%{_build}
Release:	%{_rel}
License:	custom, non-distributable
Group:		Applications/Emulators
Source0:	http://download3.vmware.com/software/wkst/%{name}-%{_ver}-%{_build}.tar.gz
Source1:	http://knihovny.cvut.cz/ftp/pub/vmware/vmware-any-any-update%{_urel}.tar.gz
# Source1-md5:	a8a159a0c24cf9ead71c44a4f5761950
Source2:	%{name}.init
Source3:	%{name}-vmnet.conf
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-compat.patch
Patch2:		%{name}-run_script.patch
NoSource:	0
URL:		http://www.vmware.com/
BuildRequires:	gcc-c++
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.118
BuildRequires:	%{kgcc_package}
Requires:	kernel(vmmon) = %{version}-%{_rel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build}
%{?with_dist_kernel:BuildRequires:	kernel-doc}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoprovfiles %{_libdir}/vmware/lib/.*\.so.*

%description
VMware Workstation Virtual Platform is a thin software layer that
allows multiple guest operating systems to run concurrently on a
single standard PC, without repartitioning or rebooting, and
without significant loss of performance.

%description -l pl
VMware Workstation Virtual Platform to cienka warstwa oprogramowania
pozwalaj±ca na jednoczesne dzia³anie wielu go¶cinnych systemów
operacyjnych na jednym zwyk³ym PC, bez repartycjonowania ani
rebootowania, bez znacznej utraty wydajno¶ci.

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
Summary(pl):	Modu³ j±dra dla VMware Workstation
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Provides:	kernel(vmmon) = %{version}-%{_rel}
Requires:	dev >= 2.9.0-7
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:%requires_releq_kernel_up}

%description -n kernel-misc-vmmon
Kernel modules for VMware Workstation - vmmon.

%description -n kernel-misc-vmmon -l pl
Modu³y j±dra dla VMware Workstation - vmmon.

%package -n kernel-misc-vmnet
Summary:	Kernel module for VMware Workstation
Summary(pl):	Modu³ j±dra dla VMware Workstation
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Provides:	kernel(vmnet) = %{version}-%{_rel}
Requires:	dev >= 2.9.0-7
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:%requires_releq_kernel_up}

%description -n kernel-misc-vmnet
Kernel modules for VMware Workstation - vmnet.

%description -n kernel-misc-vmnet -l pl
Modu³y j±dra dla VMware Workstation - vmnet.

%package -n kernel-smp-misc-vmmon
Summary:	SMP kernel module for VMware Workstation
Summary(pl):	Modu³ j±dra SMP dla VMware Workstation
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Provides:	kernel(vmmon) = %{version}-%{_rel}
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:%requires_releq_kernel_smp}

%description -n kernel-smp-misc-vmmon
SMP kernel modules fov VMware Workstation - vmmon-smp.

%description -n kernel-smp-misc-vmmon -l pl
Modu³y j±dra SMP dla VMware Workstation - vmmon-smp.

%package -n kernel-smp-misc-vmnet
Summary:	SMP kernel module for VMware Workstation
Summary(pl):	Modu³ j±dra SMP dla VMware Workstation
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Provides:	kernel(vmnet) = %{version}-%{_rel}
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:%requires_releq_kernel_smp}

%description -n kernel-smp-misc-vmnet
SMP kernel module for VMware Workstation - vmnet-smp.

%description -n kernel-smp-misc-vmnet -l pl
Modu³y j±dra SMP dla VMware Workstation -  vmnet-smp.

%prep
%setup -q -n vmware-distrib
%setup -qDT -n vmware-distrib -a1
cd vmware-any-any-update%{_urel}
tar xf vmmon.tar
tar xf vmnet.tar
%patch0 -p0
%patch1 -p0
cd -
%patch2 -p1

%build
cd vmware-any-any-update%{_urel}
for mod in vmmon vmnet ; do
    cd $mod-only
    rm -rf built
    mkdir built
    for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
        if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
	    exit 1
	fi
	install -d include/linux
	%{__make} -C %{_kernelsrcdir} mrproper \
	    SUBDIRS=$PWD O=$PWD \
	    RCS_FIND_IGNORE="-name built"
        ln -sf %{_kernelsrcdir}/config-$cfg .config
        ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
        touch include/includeCheck.h
        %{__make} -C %{_kernelsrcdir} scripts modules \
    	    SUBDIRS=$PWD O=$PWD \
	    VM_KBUILD=26
        mv $mod.ko built/$mod-$cfg.ko
    done
    cd -
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
install vmmon-only/built/vmmon-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/vmmon.ko
install vmnet-only/built/vmnet-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/vmnet.ko
%if %{with smp} && %{with dist_kernel}
install vmmon-only/built/vmmon-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/vmmon.ko
install vmnet-only/built/vmnet-smp.ko \
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

cat > $RPM_BUILD_ROOT%{_sysconfdir}/vmware/locations <<EOF
VM_BINDIR=%{_bindir}
VM_LIBDIR=%{_libdir}/vmware
EOF

%if %{with internal_libs}
cp	bin/vmware $RPM_BUILD_ROOT%{_bindir}/vmware.sh
cp -r	lib/lib  $RPM_BUILD_ROOT%{_libdir}/vmware
%endif

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
%dir %{_sysconfdir}/vmware
%{_sysconfdir}/vmware/locations
%attr(755,root,root) %{_bindir}/vmware
%{?with_internal_libs:%attr(755,root,root) %{_bindir}/vmware.sh}
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
%{?with_internal_libs:%{_libdir}/vmware/lib}
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
/lib/modules/%{_kernel_ver}/misc/vmmon.ko*

%files -n kernel-misc-vmnet
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vmnet.ko*

%if %{with smp} && %{with dist_kernel}
%files	-n kernel-smp-misc-vmmon
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/vmmon.ko*

%files	-n kernel-smp-misc-vmnet
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/vmnet.ko*
%endif
