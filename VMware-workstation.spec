#
# TODO:
#	- init script
#	- kernel modules
#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	smp		# without SMP kernel modules
#
%include	/usr/lib/rpm/macros.perl
Summary:	VMware Workstation
Summary(pl):	VMware Workstation - wirtualna platforma dla stacji roboczej
Name:		VMware-workstation
Version:	4.0.5
%define		_build	6030
%define		_rel	0.%{_build}.2
Release:	%{_rel}
License:	custom, non-distributable
Group:		Applications/Emulators
Source0:	http://download3.vmware.com/software/wkst/%{name}-%{version}-%{_build}.tar.gz
NoSource:	0
Source1:	http://knihovny.cvut.cz/ftp/pub/vmware/vmware-any-any-update53.tar.gz
# Source1-md5:	6e7c462f5dcb8881db5ccc709f43f56f
Patch0:		%{name}-Makefile.patch
URL:		http://www.vmware.com/
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.118
BuildRequires:	%{kgcc_package}
Requires:	kernel(vmmon) = %{version}-%{_build}
Requires:	kernel(vmnet) = %{version}-%{_build}
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

%package -n kernel-misc-vmware_workstation
Summary:	Kernel modules for VMware Workstation
Summary(pl):	Modu�y j�dra dla VMware Workstation
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Provides:	kernel(vmmon) = %{version}-%{_build}
Provides:	kernel(vmnet) = %{version}-%{_build}
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:%requires_releq_kernel_up}

%description -n kernel-misc-vmware_workstation
Kernel modules for VMware Workstation: vmmon and vmnet.

%description -n kernel-misc-vmware_workstation -l pl
Modu�y j�dra dla VMware Workstation: vmmon i vmnet.

%package -n kernel-smp-misc-vmware_workstation
Summary:	SMP kernel modules for VMware Workstation
Summary(pl):	Modu�y j�dra SMP dla VMware Workstation
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Provides:	kernel(vmmon) = %{version}-%{_build}
Provides:	kernel(vmnet) = %{version}-%{_build}
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:%requires_releq_kernel_smp}

%description -n kernel-smp-misc-vmware_workstation
SMP kernel modules fov VMware Workstation: vmmon-smp and vmnet-smp.

%description -n kernel-smp-misc-vmware_workstation -l pl
Modu�y j�dra SMP dla VMware Workstation: vmmon-smp i vmnet-smp.

%prep
%setup -q -n vmware-distrib
%setup -qDT -n vmware-distrib -a1
cd vmware-any-any-update53
tar xf vmmon.tar
tar xf vmnet.tar
cd ..
%patch0 -p1

%build
cd vmware-any-any-update53

for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do

    if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
	exit 1
    fi

    cd vmmon-only
    %{__make} clean
    install -d include/{linux,config}
    %{__make} -C %{_kernelsrcdir} mrproper \
        SUBDIRS=$PWD \
	O=$PWD
    ln -sf %{_kernelsrcdir}/config-$cfg .config
    ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
    touch include/linux/MARKER
    touch includeCheck.h
    %{__make} -C %{_kernelsrcdir} modules %{?with_smp:CPPFLAGS=\"-D__SMP__ SUPPORT_SMP=1\"} \
        SUBDIRS=$PWD \
        O=$PWD \
        VM_KBUILD=26
    mv vmmon.ko vmmon-$cfg.ko
    cd ..
    
    cd vmnet-only
    %{__make} clean
    install -d include/{linux,config}
    %{__make} -C %{_kernelsrcdir} mrproper \
        SUBDIRS=$PWD \
	O=$PWD
    ln -sf %{_kernelsrcdir}/config-$cfg .config
    ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
    touch include/linux/MARKER
    touch includeCheck.h
    %{__make} -C %{_kernelsrcdir} modules %{?with_smp:CPPFLAGS=\"-D__SMP__ SUPPORT_SMP=1\"} \
        SUBDIRS=$PWD \
        O=$PWD \
        VM_KBUILD=26
    mv vmnet.ko vmnet-$cfg.ko
    cd ..
done

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{,vmware} \
	$RPM_BUILD_ROOT%{_mandir} \
	$RPM_BUILD_ROOT%{_libdir}/vmware \
	$RPM_BUILD_ROOT%{_datadir}/vmware \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver_str}{,smp}/misc

cd vmware-any-any-update53
install vmmon-only/vmmon-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver_str}/misc/vmmon.ko
install vmnet-only/vmnet-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver_str}/misc/vmnet.ko
%if %{with smp} && %{with dist_kernel}
install vmmon-only/vmmon-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver_str}smp/misc/vmmon.ko
install vmnet-only/vmnet-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver_str}smp/misc/vmnet.ko
%endif
cd ..

cp	bin/* $RPM_BUILD_ROOT%{_bindir}
cp -r	man/* $RPM_BUILD_ROOT%{_mandir}
gunzip	$RPM_BUILD_ROOT%{_mandir}/man?/*.gz

cp -r	lib/{bin*,config*,floppies,isoimages,lib,licenses,messages,smb,xkeymap} \
	$RPM_BUILD_ROOT%{_libdir}/vmware

cat << EOF > $RPM_BUILD_ROOT%{_sysconfdir}/vmware/locations
answer BINDIR %{_bindir}
answer LIBDIR %{_libdir}/vmware
answer MANDIR %{_mandir}
answer INITDIR /tmp
answer INITSCRIPTSDIR /tmp
answer RUN_CONFIGURATOR no
answer EULA_AGREED yes
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-misc-vmware_workstation
%depmod %{_kernel_ver_str}

%postun -n kernel-misc-vmware_workstation
%depmod %{_kernel_ver_str}

%post	-n kernel-smp-misc-vmware_workstation
%depmod %{_kernel_ver_str}

%postun -n kernel-smp-misc-vmware_workstation
%depmod %{_kernel_ver_str}

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/vmnet*
%attr(755,root,root) %{_bindir}/vmware
%attr(755,root,root) %{_bindir}/vmware-loop
%attr(755,root,root) %{_bindir}/vmware-mount.pl
%attr(755,root,root) %{_bindir}/vmware-nmbd
%attr(755,root,root) %{_bindir}/vmware-ping
%attr(755,root,root) %{_bindir}/vmware-smb*
%attr(755,root,root) %{_bindir}/vmware-wizard
%doc doc/*
%{_sysconfdir}/vmware
%dir %{_libdir}/vmware
%dir %{_libdir}/vmware/bin
%attr(755,root,root) %{_libdir}/vmware/bin/vmware
%attr(755,root,root) %{_libdir}/vmware/bin/vmware-mks
# warning: SUID !!!
%attr(4755,root,root) %{_libdir}/vmware/bin/vmware-vmx
#
%{_libdir}/vmware/config
%{_libdir}/vmware/configurator
%{_libdir}/vmware/floppies
%{_libdir}/vmware/isoimages
%{_libdir}/vmware/lib
%{_libdir}/vmware/licenses
%{_libdir}/vmware/smb
%{_libdir}/vmware/xkeymap
%{_mandir}/man1/*

%files -n kernel-misc-vmware_workstation
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver_str}/misc/*

%if %{with smp} && %{with dist_kernel}
%files	-n kernel-smp-misc-vmware_workstation
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver_str}smp/misc/*
%endif
