#
# Conditional build:
# _without_dist_kernel - without distribution kernel
# _without_smp         - without UP  kernel modules
# _without_up          - without SMP kernel modules
#

%define	_build	4460

%include	/usr/lib/rpm/macros.perl
Summary:	VMware Workstation
Summary(pl):	VMware Workstation - wirtualna platforma dla stacji roboczej
Name:		VMware-workstation
Version:	4.0.0
%define _rel	%{_build}.2
Release:	%{_rel}
License:	custom, non-distributable
Group:		Applications/Emulators
Source0:	http://vmware-chil.www.conxion.com/software/%{name}-%{version}-%{_build}.tar.gz
URL:		http://www.vmware.com/
NoSource:	0
BuildRequires:	rpm-perlprov
BuildRequires:	%{kgcc_package}
Requires:	kernel(vmmon) = %{version}-%{_build}
Requires:	kernel(vmnet) = %{version}-%{_build}
%{!?_without_dist_kernel:BuildRequires:         kernel-headers}
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
%{!?_without_dist_kernel:%requires_releq_kernel_up}

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
%{!?_without_dist_kernel:%requires_releq_kernel_smp}

%description -n kernel-smp-misc-vmware_workstation
SMP kernel modules fov VMware Workstation: vmmon-smp and vmnet-smp.

%description -n kernel-smp-misc-vmware_workstation -l pl
Modu造 j康ra SMP dla VMware Workstation: vmmon-smp i vmnet-smp.

%prep
%setup -q -n vmware-distrib
tar xf lib/modules/source/vmmon.tar
tar xf lib/modules/source/vmnet.tar

%build
FLAGS="-D__KERNEL__ -DMODULE -Wall -Wstrict-prototypes \
	-fomit-frame-pointer -fno-strict-aliasing \
	-pipe -fno-strength-reduce %{rpmcflags}"
export FLAGS

# vmmon
%if %{?!_without_smp:1}0
%{__make} -C vmmon-only \
	HEADER_DIR=%{_kernelsrcdir}/include \
	CC_OPTS="$FLAGS -DVMWARE__FIX_IO_APIC_BASE=FIX_IO_APIC_BASE_0 -D__SMP__" \
	SUPPORT_SMP=1
mv vmmon-only/driver-*/vmmon-smp-* vmmon-smp.o
%endif

%if %{?!_without_up:1}0
%{__make} -C vmmon-only clean
%{__make} -C vmmon-only \
	HEADER_DIR=%{_kernelsrcdir}/include \
	CC_OPTS="$FLAGS -DVMWARE__FIX_IO_APIC_BASE=FIX_IO_APIC_BASE_0"
mv vmmon-only/driver-*/vmmon-* vmmon.o
%endif

# vmnet, makefile passes also -falign-loops=2 -falign-jumps=2 -falign-functions=2
%if %{?!_without_smp:1}0
%{__make} -C vmnet-only \
	HEADER_DIR=%{_kernelsrcdir}/include \
	CFLAGS="$FLAGS "'$(INCLUDE) -D__SMP__' \
	SUPPORT_SMP=1
mv vmnet-only/vmnet-smp-* vmnet-smp.o
%endif

%if %{?!_without_up:1}0
%{__make} -C vmnet-only clean
%{__make} -C vmnet-only \
	HEADER_DIR=%{_kernelsrcdir}/include \
	CFLAGS="$FLAGS "'$(INCLUDE)'
mv vmnet-only/vmnet-up-* vmnet.o
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_sysconfdir} \
	$RPM_BUILD_ROOT%{_mandir} \
	$RPM_BUILD_ROOT%{_libdir}/vmware \
	$RPM_BUILD_ROOT%{_datadir}/vmware \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc

%{?!_without_smp:mv vm*-smp.o	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc}
%{?!_without_up: mv vm*.o	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc}

cp    bin/* $RPM_BUILD_ROOT%{_bindir}
cp -r etc   $RPM_BUILD_ROOT%{_sysconfdir}/vmware
cp -r man/* $RPM_BUILD_ROOT%{_mandir}

cp -r lib/{bin*,config*,floppies,isoimages,lib,licenses,messages,smb,xkeymap} \
	$RPM_BUILD_ROOT%{_libdir}/vmware

gunzip $RPM_BUILD_ROOT%{_mandir}/man?/*.gz

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-misc-vmware_workstation
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}

%postun -n kernel-misc-vmware_workstation
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}

%post	-n kernel-smp-misc-vmware_workstation
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}

%postun -n kernel-smp-misc-vmware_workstation
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}

%files
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%dir %{_sysconfdir}/vmware
%ghost %{_sysconfdir}/vmware/not_configured
%attr(755,root,root) %{_sysconfdir}/vmware/*.sh

%dir %{_libdir}/vmware
%dir %{_libdir}/vmware/bin*
%attr(755,root,root) %{_libdir}/vmware/bin*/*
%{_libdir}/vmware/config
%{_libdir}/vmware/configurator
%{_libdir}/vmware/floppies
%{_libdir}/vmware/isoimages
%{_libdir}/vmware/lib
%{_libdir}/vmware/licenses
%dir %{_libdir}/vmware/messages
%lang(ja) %{_libdir}/vmware/messages/ja
%{_libdir}/vmware/smb
%{_libdir}/vmware/xkeymap

%if %{?!_without_up:1}0
%files -n kernel-misc-vmware_workstation
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vmmon.o*
/lib/modules/%{_kernel_ver}/misc/vmnet.o*
%endif

%if %{?!_without_smp:1}0
%files	-n kernel-smp-misc-vmware_workstation
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/vmmon-smp.o*
/lib/modules/%{_kernel_ver}smp/misc/vmnet-smp.o*
%endif
