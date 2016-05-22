%global debug_package %{nil}
%define daemon_version 1.1.62

Name:		displaylink
Version:	1.1.65
Release:	3
Summary:	DisplayLink VGA/HDMI driver for DL-5xxx, DL-41xx and DL-3xxx adapters

Group:		User Interface/X Hardware Support
License:	GPL v2.0, LGPL v2.1 and Proprietary
Source0:	https://github.com/DisplayLink/evdi/archive/v%{version}.tar.gz
Source1:	displaylink.service
Source2:	99-displaylink.rules
# From http://www.displaylink.com/downloads/ubuntu.php
Source3:	DisplayLink USB Graphics Software for Ubuntu 1.1.68.zip
ExclusiveArch:	i386 x86_64

BuildRequires:	libdrm-devel
Requires:	dkms, kernel > 3.14, kernel-devel > 3.14

%description
This package installs the DisplayLink "Plug and Display" module for various HDMI/VGA adapters, including Dell's 4-in-1 (DA100). Based on DisplayLink's officially supported Ubuntu driver, and repackaged for Fedora/CentOS/RHEL distros. Module is added to DKMS so that it's recompiled on future kernel updates.

%define logfile /var/log/displaylink/%{name}.log

%prep
%setup -c evdi-%{version}
cd evdi-%{version}
sed -i 's/\r//' README.md

unzip "%{SOURCE3}"
chmod +x displaylink-driver-%{daemon_version}.run
./displaylink-driver-%{daemon_version}.run --noexec --keep
# This creates a displaylink-driver-$version subdirectory

%build

cd evdi-%{version}/library/
make %{?_smp_mflags}

%install

mkdir -p $RPM_BUILD_ROOT/usr/libexec/displaylink/	\
	$RPM_BUILD_ROOT/usr/src/evdi-%{version}/	\
	$RPM_BUILD_ROOT/usr/lib/systemd/system/		\
	$RPM_BUILD_ROOT/etc/udev/rules.d/		\
	$RPM_BUILD_ROOT/var/log/displaylink/

# Kernel driver sources
pushd $RPM_BUILD_ROOT/usr/src/evdi-%{version} ; \
cp -a $OLDPWD/evdi-%{version}/module/* . ; \
popd

# Binaries
# Don't copy libusb-1.0.so.0.1.0 it's already shipped by libusbx
# Don't copy libevdi.so, we compiled it from source

cd evdi-%{version}/displaylink-driver-%{daemon_version}

cp LICENSE ../..

%ifarch x86_64
cp -a x64/DisplayLinkManager $RPM_BUILD_ROOT/usr/libexec/displaylink/
%endif

%ifarch %ix86
cp -a x86/DisplayLinkManager $RPM_BUILD_ROOT/usr/libexec/displaylink/
%endif

# Firmwares
cp -a ella-dock-release.spkg firefly-monitor-release.spkg $RPM_BUILD_ROOT/usr/libexec/displaylink/

# systemd/udev
cp -a %{SOURCE1} $RPM_BUILD_ROOT/usr/lib/systemd/system/
cp -a %{SOURCE2} $RPM_BUILD_ROOT/etc/udev/rules.d/

%post
/usr/bin/systemctl daemon-reload
/usr/bin/systemctl -q is-enabled dkms.service || /usr/bin/systemctl enable dkms.service
for kernel in $(rpm -q kernel --queryformat '%{VERSION}-%{RELEASE}.%{ARCH}\n') ;do
	/sbin/dkms install evdi/%{version} -k $kernel >> %{logfile} 2>&1
done

%files
%doc LICENSE
/usr/lib/systemd/system/displaylink.service
/etc/udev/rules.d/99-displaylink.rules
%dir /usr/src/evdi-%{version}
/usr/src/evdi-%{version}/*
%dir /usr/libexec/displaylink
/usr/libexec/displaylink/*
%dir /var/log/displaylink/

%preun
if [ $1 -eq 0 ] ;then
	/usr/bin/systemctl -q is-active displaylink.service && /usr/bin/systemctl stop displaylink.service
	/sbin/dkms remove evdi/%{version} --all >> %{logfile}
fi

%postun
/usr/bin/systemctl daemon-reload

%changelog
* Sun May 22 2016 Bastien Nocera <bnocera@redhat.com> 1.1.65-3
- Add missing libdrm-devel BR

* Tue May 17 2016 Bastien Nocera <bnocera@redhat.com> 1.1.65-2
- Update to daemon 1.1.62 (with a zip file called 1.1.68, sigh)

* Tue May 17 2016 Bastien Nocera <bnocera@redhat.com> 1.1.65-1
- Update to 1.1.65

* Tue May 10 2016 Bastien Nocera <bnocera@redhat.com> 1.1.61-1
- Update to 1.1.61

* Thu Apr 28 2016 Bastien Nocera <bnocera@redhat.com> 1.0.453-1
- Update to 1.0.453
- Compile the library from source

* Mon Dec 14 2015 Bastien Nocera <bnocera@redhat.com> 1.0.335-1
- Update to 1.0.335

* Mon Sep 07 2015 Bastien Nocera <bnocera@redhat.com> 1.0.138-4
- Disable debuginfo subpackage creation

* Mon Sep 07 2015 Bastien Nocera <bnocera@redhat.com> 1.0.138-3
- Create RPM directly from downloaded zip file
- Add LICENSE
- Create i386 RPM

* Sun Sep 6  2015 Eric Nothen <enothen@gmail.com> - 1.0.138-2
- Modified installed kernels detection section to be more precise

* Wed Sep 2  2015 Eric Nothen <enothen@gmail.com> - 1.0.138-1
- Updated driver to version 1.0.138, as published by DisplayLink

* Wed Aug 19 2015 Eric Nothen <enothen@gmail.com> - 1.0.68-2
- Changed udev rule to detect devices based on vendor rather than model

* Thu Aug 13 2015 Eric Nothen <enothen@gmail.com> - 1.0.68-1
- Initial package based on module version 1.0.68 available at http://www.displaylink.com/downloads/ubuntu.php
