
%define	_build	4460

%include	/usr/lib/rpm/macros.perl
Summary:	VMware Workstation
#Summary(pl):	
Name:		VMware-workstation
Version:	4.0.0
Release:	%{_build}.1
License:	custom, non-distributable
Group:		Applications/Emulators
Source0:	http://vmware-chil.www.conxion.com/software/%{name}-%{version}-%{_build}.tar.gz
URL:		http://www.vmware.com/
BuildRequires:	rpm-perlprov
#BuildRequires:	
#BuildRequires:	
#BuildRequires:	
#BuildRequires:	
#PreReq:		-
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
VMware Workstation Virtual Platform is a thin software layer that allows
multiple guest operating systems to run concurrently on a single standard
PC, without repartitioning or rebooting, and without significant loss
of performance.

# %description -l pl

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
make -C vmmon-only \
	HEADER_DIR=%{_kernelsrcdir}/include \
	CC_OPTS="$FLAGS -DVMWARE__FIX_IO_APIC_BASE=FIX_IO_APIC_BASE_0 -D__SMP__" \
	SUPPORT_SMP=1
mv vmmon-only/driver-*/vmmon-smp-* vmmon-smp.o
make -C vmmon-only clean

make -C vmmon-only \
	HEADER_DIR=%{_kernelsrcdir}/include \
	CC_OPTS="$FLAGS -DVMWARE__FIX_IO_APIC_BASE=FIX_IO_APIC_BASE_0"
mv vmmon-only/driver-*/vmmon-* vmmon.o
make -C vmmon-only clean

# vmnet, makefile passes also -falign-loops=2 -falign-jumps=2 -falign-functions=2
make -C vmnet-only \
	HEADER_DIR=%{_kernelsrcdir}/include \
	CFLAGS="$FLAGS "'$(INCLUDE) -D__SMP__' \
	SUPPORT_SMP=1
mv vmnet-only/vmnet-smp-* vmnet-smp.o
make -C vmnet-only clean

make -C vmnet-only \
	HEADER_DIR=%{_kernelsrcdir}/include \
	CFLAGS="$FLAGS "'$(INCLUDE)'
mv vmnet-only/vmnet-up-* vmnet.o
make -C vmnet-only clean

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_sysconfdir} \
	$RPM_BUILD_ROOT%{_mandir} \
	$RPM_BUILD_ROOT%{_libdir}/vmware \
	$RPM_BUILD_ROOT%{_datadir}/vmware

cp    bin/* $RPM_BUILD_ROOT%{_bindir}
cp -r etc   $RPM_BUILD_ROOT%{_sysconfdir}/vmware
cp -r man/* $RPM_BUILD_ROOT%{_mandir}

cp -r lib/{bin*,config*,floppies,isoimages,lib,licenses,messages,smb,xkeymap} \
	$RPM_BUILD_ROOT%{_libdir}/vmware

gunzip $RPM_BUILD_ROOT%{_mandir}/man?/*.gz

%clean
rm -rf $RPM_BUILD_ROOT

# %post depmod
# %postun

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
