#
# TODO:
#	- Standarize init script
#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	smp		# without SMP kernel modules
#
%include	/usr/lib/rpm/macros.perl
Summary:	VMware Workstation
Summary(pl):	VMware Workstation - wirtualna platforma dla stacji roboczej
Name:		VMware-workstation
Version:	4.5.1
%define		_build	7568
%define		_rel	0.%{_build}.4
Release:	%{_rel}
License:	custom, non-distributable
Group:		Applications/Emulators
Source0:	http://download3.vmware.com/software/wkst/%{name}-%{version}-%{_build}.tar.gz
Source1:	%{name}.init
NoSource:	0
%define		_urel	56
Source1:	http://knihovny.cvut.cz/ftp/pub/vmware/vmware-any-any-update%{_urel}.tar.gz
# Source1-md5:	bde9dbcfbaaaefe3afb5223eaf911e1d
Patch0:		%{name}-Makefile.patch
URL:		http://www.vmware.com/
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.118
BuildRequires:	%{kgcc_package}
Requires:	kernel(vmmon) = %{version}-%{_rel}
Requires:	kernel(vmnet) = %{version}-%{_rel}
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

%package debug
Summary:	TODO
Summary(pl):	TODO
Group:		Application/Emulators

%description debug
TODO.

%description debug -l pl
TODO.

%package help
Summary:	VMware Workstation help files
Summary(pl):	Pliki pomocy dla VMware Workstation
Group:		Application/Emulators

%description help
VMware Workstation help files.

%description help -l pl
Pliki pomocy dla VMware Workstation.

%package init
Summary:	TODO
Summary(pl):	TODO
Group:		Application/Emulators

%description init
TODO.

%description init -l pl
TODO.

%package -n kernel-misc-vmware-workstation
Summary:	Kernel modules for VMware Workstation
Summary(pl):	Modu造 j康ra dla VMware Workstation
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Provides:	kernel(vmmon) = %{version}-%{_rel}
Provides:	kernel(vmnet) = %{version}-%{_rel}
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:%requires_releq_kernel_up}

%description -n kernel-misc-vmware-workstation
Kernel modules for VMware Workstation: vmmon and vmnet.

%description -n kernel-misc-vmware-workstation -l pl
Modu造 j康ra dla VMware Workstation: vmmon i vmnet.

%package -n kernel-smp-misc-vmware-workstation
Summary:	SMP kernel modules for VMware Workstation
Summary(pl):	Modu造 j康ra SMP dla VMware Workstation
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Provides:	kernel(vmmon) = %{version}-%{_rel}
Provides:	kernel(vmnet) = %{version}-%{_rel}
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:%requires_releq_kernel_smp}

%description -n kernel-smp-misc-vmware-workstation
SMP kernel modules fov VMware Workstation: vmmon-smp and vmnet-smp.

%description -n kernel-smp-misc-vmware-workstation -l pl
Modu造 j康ra SMP dla VMware Workstation: vmmon-smp i vmnet-smp.

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
		%{__make} -C %{_kernelsrcdir} mrproper \
			SUBDIRS=$PWD \
			O=$PWD
		ln -sf %{_kernelsrcdir}/config-$cfg .config
		ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h \
			include/linux/autoconf.h
		touch include/linux/MARKER
		touch includeCheck.h
		%{__make} -C %{_kernelsrcdir} modules \
			%{?with_smp:CPPFLAGS=\"-D__SMP__ SUPPORT_SMP=1\"} \
			SUBDIRS=$PWD \
			O=$PWD \
			VM_KBUILD=26
		mv ${mod}.ko ${mod}-$cfg.ko
		cd ..
	done
done

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT%{_sysconfdir}/vmware \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_libdir}/vmware/{bin,configurator} \
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

install %{SOURCE0} $RPM_BUILD_ROOT/etc/rc.d/init.d/vmware

cp	bin/vmnet-* $RPM_BUILD_ROOT%{_bindir}
cp	bin/vmware-[!cnsu]* $RPM_BUILD_ROOT%{_bindir}

cp	lib/bin/vmware $RPM_BUILD_ROOT%{_bindir}

cp -r	lib/bin/vmware-vmx \
	$RPM_BUILD_ROOT%{_libdir}/vmware/bin

cp -r	lib/{bin-debug,config,floppies,help*,isoimages,licenses,messages,xkeymap} \
	$RPM_BUILD_ROOT%{_libdir}/vmware

cp -r	man/* $RPM_BUILD_ROOT%{_mandir}
gunzip	$RPM_BUILD_ROOT%{_mandir}/man?/*.gz

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

%post init
/sbin/chkconfig --add vmware
if [ -r /var/lock/subsys/vmware ]; then
	/etc/rc.d/init.d/vmware restart >&2
else
	echo "Run \"/etc/rc.d/init.d/vmware start\" to start VMvare service."
fi

%preun init
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/vmware ]; then
		/etc/rc.d/init.d/vmware stop >&2
	fi
	/sbin/chkconfig --del vmware
fi

%post	-n kernel-misc-vmware-workstation
%depmod %{_kernel_ver}

%postun -n kernel-misc-vmware-workstation
%depmod %{_kernel_ver}

%post	-n kernel-smp-misc-vmware-workstation
%depmod %{_kernel_ver}

%postun -n kernel-smp-misc-vmware-workstation
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
%doc lib/configurator/*.conf
%attr(755,root,root) %{_bindir}/vmnet*
%attr(755,root,root) %{_bindir}/vmware
%attr(755,root,root) %{_bindir}/vmware-loop
%attr(755,root,root) %{_bindir}/vmware-mount.pl
%attr(755,root,root) %{_bindir}/vmware-ping
%attr(755,root,root) %{_bindir}/vmware-wizard
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
%doc doc/*
%dir %{_sysconfdir}/vmware
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/vmware/locations
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
%attr(4755,root,root) %{_libdir}/vmware/bin/vmware-vmx

%files help
%defattr(644,root,root,755)
%{_libdir}/vmware/help*

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/vmware

%files -n kernel-misc-vmware-workstation
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*

%if %{with smp} && %{with dist_kernel}
%files	-n kernel-smp-misc-vmware-workstation
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/*
%endif
