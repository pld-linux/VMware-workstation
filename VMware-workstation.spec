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
pozwalaj帷a na jednoczesne dzia豉nie wielu go軼innych system闚
operacyjnych na jednym zwyk造m PC, bez repartycjonowania ani
rebootowania, bez znacznej utraty wydajno軼i.

%package -n kernel-misc-vmware_workstation
Summary:	Kernel modules for VMware Workstation
Summary(pl):	Modu造 j康ra dla VMware Workstation
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Provides:	kernel(vmmon) = %{version}-%{_build}
Provides:	kernel(vmnet) = %{version}-%{_build}
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:%requires_releq_kernel_up}

%description -n kernel-misc-vmware_workstation
Kernel modules for VMware Workstation: vmmon and vmnet.

%description -n kernel-misc-vmware_workstation -l pl
Modu造 j康ra dla VMware Workstation: vmmon i vmnet.

%package -n kernel-smp-misc-vmware_workstation
Summary:	SMP kernel modules for VMware Workstation
Summary(pl):	Modu造 j康ra SMP dla VMware Workstation
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Provides:	kernel(vmmon) = %{version}-%{_build}
Provides:	kernel(vmnet) = %{version}-%{_build}
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:%requires_releq_kernel_smp}

%description -n kernel-smp-misc-vmware_workstation
SMP kernel modules fov VMware Workstation: vmmon-smp and vmnet-smp.

%description -n kernel-smp-misc-vmware_workstation -l pl
Modu造 j康ra SMP dla VMware Workstation: vmmon-smp i vmnet-smp.

%prep
%setup -q -n vmware-distrib
#tar xf lib/modules/source/vmmon.tar
#tar xf lib/modules/source/vmnet.tar

%build
#FLAGS="-D__KERNEL__ -DMODULE -Wall -Wstrict-prototypes \
#	-fomit-frame-pointer -fno-strict-aliasing \
#	-pipe -fno-strength-reduce %{rpmcflags}"
#export FLAGS

# vmmon
#%if %{with smp}
#%{__make} -C vmmon-only \
#	HEADER_DIR=%{_kernelsrcdir}/include \
#	CC_OPTS="$FLAGS -DVMWARE__FIX_IO_APIC_BASE=FIX_IO_APIC_BASE_0 -D__SMP__" \
#	SUPPORT_SMP=1
#mv vmmon-only/driver-*/vmmon-smp-* vmmon-smp.o
#%endif

#%{__make} -C vmmon-only clean
#%{__make} -C vmmon-only \
#	HEADER_DIR=%{_kernelsrcdir}/include \
#	CC_OPTS="$FLAGS -DVMWARE__FIX_IO_APIC_BASE=FIX_IO_APIC_BASE_0"
#mv vmmon-only/driver-*/vmmon-* vmmon.o

# vmnet, makefile passes also -falign-loops=2 -falign-jumps=2 -falign-functions=2
#%if %{with smp}
#%{__make} -C vmnet-only \
#	HEADER_DIR=%{_kernelsrcdir}/include \
#	CFLAGS="$FLAGS "'$(INCLUDE) -D__SMP__' \
#	SUPPORT_SMP=1
#mv vmnet-only/vmnet-smp-* vmnet-smp.o

#%{__make} -C vmnet-only clean
#%{__make} -C vmnet-only \
#	HEADER_DIR=%{_kernelsrcdir}/include \
#	CFLAGS="$FLAGS "'$(INCLUDE)'
#mv vmnet-only/vmnet-up-* vmnet.o

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{,vmware} \
	$RPM_BUILD_ROOT%{_mandir} \
	$RPM_BUILD_ROOT%{_libdir}/vmware \
	$RPM_BUILD_ROOT%{_datadir}/vmware \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver_str}/misc \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver_str}smp/misc

#%{?with_smp:mv vm*-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver_str}smp/misc}
#mv vm*.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc

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
%attr(755,root,root) %{_bindir}/*
%doc doc/*
%{_sysconfdir}/vmware
%dir %{_libdir}/vmware
%dir %{_libdir}/vmware/bin
%attr(755,root,root) %{_libdir}/vmware/bin/vmware
%attr(755,root,root) %{_libdir}/vmware/bin/vmware-mks
# warnning: SUID !!!
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

#%files -n kernel-misc-vmware_workstation
#%defattr(644,root,root,755)
#/lib/modules/%{_kernel_ver}/misc/vmmon.o*
#/lib/modules/%{_kernel_ver}/misc/vmnet.o*

%if %{with smp}
#%files	-n kernel-smp-misc-vmware_workstation
#%defattr(644,root,root,755)
#/lib/modules/%{_kernel_ver}smp/misc/vmmon-smp.o*
#/lib/modules/%{_kernel_ver}smp/misc/vmnet-smp.o*
%endif
