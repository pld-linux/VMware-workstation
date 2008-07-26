#
# TODO:
#	- Dependencies
#	- more files (subpackages?): vmware-authd, vmware-vmci, vmware-vix
#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace utilities
%bcond_with	internal_libs	# internal libs stuff
%bcond_with	verbose		# verbose build (V=1)
#
%include	/usr/lib/rpm/macros.perl

%ifarch %{x8664}
%undefine	with_userspace
%endif

%if !%{with kernel}
%undefine with_dist_kernel
%endif
#
%define		_ver	6.0.4
%define		_build	93057
%define		_rel	0.1
%define		_urel	115
%define		_ccver	%(rpm -q --qf "%{VERSION}" gcc)
#
Summary:	VMware Workstation
Summary(pl.UTF-8):	VMware Workstation - wirtualna platforma dla stacji roboczej
Name:		VMware-workstation
Version:	%{_ver}.%{_build}
Release:	%{_rel}
License:	custom, non-distributable
Group:		Applications/Emulators
Source0:	http://download3.vmware.com/software/wkst/%{name}-%{_ver}-%{_build}.i386.tar.gz
# NoSource0-md5:	a0a8e1d8188f4be03357872a57a767ab
Source1:	http://knihovny.cvut.cz/ftp/pub/vmware/vmware-any-any-update%{_urel}.tar.gz
# Source1-md5:	ab33ff7a799fee77f0f4ba5667cd4b9a
Source2:	%{name}.init
Source3:	%{name}-vmnet.conf
Source4:	%{name}.desktop
Source5:	%{name}-nat.conf
Source6:	%{name}-dhcpd.conf
Patch0:		%{name}-vmmon.patch
Patch1:		%{name}-vmblock.patch
Patch2:		%{name}-run_script.patch
NoSource:	0
URL:		http://www.vmware.com/
%{?with_kernel:BuildRequires:	gcc-c++}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.7}
%{?with_userspace:BuildRequires:	rpm-perlprov}
BuildRequires:	rpmbuild(macros) >= 1.332
BuildRequires:	sed >= 4.0
Requires:	libgnomecanvasmm
Requires:	libview >= 0.5.5-2
Obsoletes:	VMware-workstation-samba
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoprovfiles %{_libdir}/vmware/lib/.*\.so.*

%description
VMware Workstation Virtual Platform is a thin software layer that
allows multiple guest operating systems to run concurrently on a
single standard PC, without repartitioning or rebooting, and without
significant loss of performance.

%description -l pl.UTF-8
VMware Workstation Virtual Platform to cienka warstwa oprogramowania
pozwalająca na jednoczesne działanie wielu gościnnych systemów
operacyjnych na jednym zwykłym PC, bez repartycjonowania ani
rebootowania, bez znacznej utraty wydajności.

%package debug
Summary:	VMware debug utility
Summary(pl.UTF-8):	Narzędzie VMware do odpluskwiania
Group:		Applications/Emulators
Requires:	%{name} = %{version}-%{release}

%description debug
VMware debug utility.

%description debug -l pl.UTF-8
Narzędzie VMware do odpluskwiania.

%package help
Summary:	VMware Workstation help files
Summary(pl.UTF-8):	Pliki pomocy dla VMware Workstation
Group:		Applications/Emulators
Requires:	%{name} = %{version}-%{release}
Requires:	mozilla

%description help
VMware Workstation help files.

%description help -l pl.UTF-8
Pliki pomocy dla VMware Workstation.

%package networking
Summary:	VMware networking utilities
Summary(pl.UTF-8):	Narzędzia VMware do obsługi sieci
Group:		Applications/Emulators
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts
Obsoletes:	VMware-workstation-samba

%description networking
VMware networking utilities.

%description networking -l pl.UTF-8
Narzędzia VMware do obsługi sieci.

%package -n kernel%{_alt_kernel}-misc-vmblock
Summary:	Kernel module for VMware Workstation
Summary(pl.UTF-8):	Moduł jądra dla VMware Workstation
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(vmblock) = %{version}-%{_rel}

%description -n kernel%{_alt_kernel}-misc-vmblock
Kernel module for VMware Workstation - vmblock.

%description -n kernel%{_alt_kernel}-misc-vmblock -l pl.UTF-8
Moduł jądra dla VMware Workstation - vmblock.

%package -n kernel%{_alt_kernel}-misc-vmmon
Summary:	Kernel module for VMware Workstation
Summary(pl.UTF-8):	Moduł jądra dla VMware Workstation
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(vmmon) = %{version}-%{_rel}

%description -n kernel%{_alt_kernel}-misc-vmmon
Kernel module for VMware Workstation - vmmon.

%description -n kernel%{_alt_kernel}-misc-vmmon -l pl.UTF-8
Moduł jądra dla VMware Workstation - vmmon.

%package -n kernel%{_alt_kernel}-misc-vmnet
Summary:	Kernel module for VMware Workstation
Summary(pl.UTF-8):	Moduł jądra dla VMware Workstation
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(vmnet) = %{version}-%{_rel}

%description -n kernel%{_alt_kernel}-misc-vmnet
Kernel module for VMware Workstation - vmnet.

%description -n kernel%{_alt_kernel}-misc-vmnet -l pl.UTF-8
Moduł jądra dla VMware Workstation - vmnet.

%prep
%setup -q -n vmware-distrib -a1
#%setup -qDT -n vmware-distrib -a1
#mkdir vmware-any-any-update%{_urel}
cd vmware-any-any-update%{_urel}
tar xf vmblock.tar
tar xf vmmon.tar
tar xf vmnet.tar
#tar xf ../lib/modules/source/vmmon.tar
#tar xf ../lib/modules/source/vmnet.tar
%patch0 -p1
%patch1 -p1
cd -
#%patch2 -p1

%build
sed -i 's:vm_db_answer_LIBDIR:VM_LIBDIR:g;s:vm_db_answer_BINDIR:VM_BINDIR:g' bin/vmware

cd vmware-any-any-update%{_urel}
chmod u+w ../lib/bin/vmware-vmx ../lib/bin-debug/vmware-vmx ../bin/vmnet-bridge

%if 0
rm -f update
%{__cc} %{rpmldflags} %{rpmcflags} -o update update.c
./update vmx		../lib/bin/vmware-vmx
./update vmxdebug	../lib/bin-debug/vmware-vmx
./update bridge		../bin/vmnet-bridge
%endif

%if %{with kernel}
rm -rf built
mkdir built

%define ModuleBuildArgs VMWARE_VER=VME_V6 SRCROOT=$PWD VM_KBUILD=26 VM_CCVER=%{_ccver}

%build_kernel_modules -c -C vmblock-only -m vmblock %{ModuleBuildArgs} <<'EOF'
rm -f */*.o *.o
EOF
%build_kernel_modules -c -C vmmon-only -m vmmon %{ModuleBuildArgs} <<'EOF'
rm -f */*.o *.o
EOF
%build_kernel_modules -c -C vmnet-only -m vmnet %{ModuleBuildArgs} <<'EOF'
rm -f *.o
EOF
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d \
	$RPM_BUILD_ROOT%{_sysconfdir}/vmware \
	$RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet8/{nat,dhcpd} \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_libdir}/vmware/{bin,share/{icons,pixmaps}} \
	$RPM_BUILD_ROOT%{_mandir} \
	$RPM_BUILD_ROOT%{_pixmapsdir} \
	$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT/etc/rc.d/init.d \
	$RPM_BUILD_ROOT/var/run/vmware
%endif

%if %{with kernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc

cd vmware-any-any-update%{_urel}

%install_kernel_modules -m vmblock-only/vmblock,vmmon-only/vmmon,vmnet-only/vmnet -d misc

cd -
%endif

%if %{with userspace}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/vmnet
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet.conf
install %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet8/nat/nat.conf
install %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet8/dhcpd/dhcpd.conf

touch $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet8/dhcpd/dhcpd.leases
touch $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet8/dhcpd/dhcpd.leases~

install lib/share/pixmaps/* $RPM_BUILD_ROOT%{_libdir}/vmware/share/pixmaps
install lib/share/icons/hicolor/48x48/apps/vmware-workstation.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png
# required for starting vmware
install doc/EULA $RPM_BUILD_ROOT%{_libdir}/vmware/share/EULA.txt

install bin/*-* $RPM_BUILD_ROOT%{_bindir}
install lib/bin/vmware-vmx $RPM_BUILD_ROOT%{_libdir}/vmware/bin

install lib/lib/libvmwarebase.so.0/libvmwarebase.so.0 $RPM_BUILD_ROOT%{_libdir}
install lib/lib/libvmwareui.so.0/libvmwareui.so.0 $RPM_BUILD_ROOT%{_libdir}

cp -r	lib/{bin-debug,config,floppies,help*,isoimages,licenses,messages,xkeymap} \
	$RPM_BUILD_ROOT%{_libdir}/vmware

cp -r	lib/share/icons/* $RPM_BUILD_ROOT%{_libdir}/vmware/share/icons
cp -r	man/* $RPM_BUILD_ROOT%{_mandir}
gunzip	$RPM_BUILD_ROOT%{_mandir}/man?/*.gz

cat > $RPM_BUILD_ROOT%{_sysconfdir}/vmware/locations <<EOF
VM_BINDIR=%{_bindir}
VM_LIBDIR=%{_libdir}/vmware
EOF

%if %{with internal_libs}
install bin/vmware $RPM_BUILD_ROOT%{_bindir}
install lib/bin/vmware $RPM_BUILD_ROOT%{_libdir}/vmware/bin
install lib/bin/vmware-tray $RPM_BUILD_ROOT%{_libdir}/vmware/bin
cp -r	lib/lib $RPM_BUILD_ROOT%{_libdir}/vmware
cp -r	lib/libconf $RPM_BUILD_ROOT%{_libdir}/vmware
%else
install lib/bin/vmware $RPM_BUILD_ROOT%{_bindir}
install lib/bin/vmware-tray $RPM_BUILD_ROOT%{_bindir}
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post networking
/sbin/chkconfig --add vmnet
%service vmnet restart "VMware networking service"

%preun networking
if [ "$1" = "0" ]; then
	%service vmnet stop
	/sbin/chkconfig --del vmnet
fi

%post	-n kernel%{_alt_kernel}-misc-vmblock
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-misc-vmblock
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-misc-vmmon
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-misc-vmmon
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-misc-vmnet
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-misc-vmnet
%depmod %{_kernel_ver}

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc doc/* lib/configurator/vmnet-{dhcpd,nat}.conf
%dir %{_sysconfdir}/vmware
%{_sysconfdir}/vmware/locations
%attr(755,root,root) %{_bindir}/vmware
%attr(755,root,root) %{_bindir}/vmware-loop
%attr(755,root,root) %{_bindir}/vmware-mount.pl
%attr(755,root,root) %{_bindir}/vmware-tray
%attr(755,root,root) %{_bindir}/vmware-vdiskmanager
%attr(755,root,root) %{_libdir}/libvmwarebase.so.*
%attr(755,root,root) %{_libdir}/libvmwareui.so.*

%dir %{_libdir}/vmware
%dir %{_libdir}/vmware/bin
# warning: SUID !!!
%attr(4755,root,root) %{_libdir}/vmware/bin/vmware-vmx
%{_libdir}/vmware/config
%{_libdir}/vmware/floppies
%{_libdir}/vmware/isoimages
%if %{with internal_libs}
%attr(755,root,root) %{_libdir}/vmware/bin/vmware
%dir %{_libdir}/vmware/lib
%{_libdir}/vmware/lib/lib*
%attr(755,root,root) %{_libdir}/vmware/lib/wrapper-gtk24.sh
%endif
%{_libdir}/vmware/licenses
%dir %{_libdir}/vmware/messages
%{_libdir}/vmware/messages/en
%lang(ja) %{_libdir}/vmware/messages/ja
%{_libdir}/vmware/share
%{_libdir}/vmware/xkeymap
%{_mandir}/man1/*
%attr(1777,root,root) %dir /var/run/vmware
%{_pixmapsdir}/*.png
%{_desktopdir}/%{name}.desktop

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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vmware/vmnet.conf
%attr(754,root,root) /etc/rc.d/init.d/vmnet
%attr(755,root,root) %{_bindir}/vmnet-bridge
%attr(755,root,root) %{_bindir}/vmnet-detect
%attr(755,root,root) %{_bindir}/vmnet-dhcpd
%attr(755,root,root) %{_bindir}/vmnet-natd
%attr(755,root,root) %{_bindir}/vmnet-netifup
%attr(755,root,root) %{_bindir}/vmnet-sniffer
%attr(755,root,root) %{_bindir}/vmware-ping
%dir %{_sysconfdir}/vmware/vmnet8
%dir %{_sysconfdir}/vmware/vmnet8/dhcpd
%dir %{_sysconfdir}/vmware/vmnet8/nat
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vmware/vmnet8/dhcpd/dhcpd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vmware/vmnet8/nat/nat.conf
%verify(not md5 mtime size) %{_sysconfdir}/vmware/vmnet8/dhcpd/dhcpd.leases*
%endif

%if %{with kernel} || %{with dist_kernel}
%files -n kernel%{_alt_kernel}-misc-vmblock
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vmblock.ko*

%if %{with kernel} || %{with dist_kernel}
%files -n kernel%{_alt_kernel}-misc-vmmon
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vmmon.ko*

%files -n kernel%{_alt_kernel}-misc-vmnet
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vmnet.ko*
%endif
