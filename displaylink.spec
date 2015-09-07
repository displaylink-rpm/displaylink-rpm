Name:		displaylink
Version:	1.0.138
Release:	3
Summary:	DisplayLink VGA/HDMI driver for DL-5xxx, DL-41xx and DL-3xxx adapters

Group:		User Interface/X Hardware Support
License:	GPL v2.0, LGPL v2.1 and others
URL:		http://www.nothen.com.ar
# From http://www.displaylink.com/downloads/ubuntu.php
Source0:	DisplayLink-Ubuntu-1.0.138.zip
Source1:	displaylink.service
Source2:	99-displaylink.rules
ExclusiveArch:	i386 x86_64

Requires:	dkms, kernel > 3.14, kernel-devel > 3.14

%description
This package installs the DisplayLink "Plug and Display" module for various HDMI/VGA adapters, including Dell's 4-in-1 (DA100). Based on DisplayLink's officially supported Ubuntu driver, and repackaged for Fedora/CentOS/RHEL distros. Module is added to DKMS so that it's recompiled on future kernel updates.

%define logfile /var/log/displaylink/%{name}.log

%prep
%setup -c %{name}-%{version} -T

unzip %{SOURCE0}
chmod +x displaylink-driver-%{version}.run
./displaylink-driver-%{version}.run --noexec --keep
# This creates a displaylink-driver-$version subdirectory

%build

%install

cd displaylink-driver-%{version}
mkdir -p $RPM_BUILD_ROOT/usr/libexec/displaylink/	\
	$RPM_BUILD_ROOT/usr/src/evdi-%{version}/	\
	$RPM_BUILD_ROOT/usr/lib/systemd/system/		\
	$RPM_BUILD_ROOT/etc/udev/rules.d/		\
	$RPM_BUILD_ROOT/var/log/displaylink/

# Binaries
# Don't copy libusb-1.0.so.0.1.0 it's already shipped by libusbx

%ifarch x86_64
cp -a x64/DisplayLinkManager x64/libevdi.so $RPM_BUILD_ROOT/usr/libexec/displaylink/
%endif

%ifarch %ix86
cp -a x86/DisplayLinkManager x86/libevdi.so $RPM_BUILD_ROOT/usr/libexec/displaylink/
%endif

# Firmwares
cp -a ella-dock-release.spkg firefly-monitor-release.spkg $RPM_BUILD_ROOT/usr/libexec/displaylink/

# Kernel driver sources
pushd $RPM_BUILD_ROOT/usr/src/evdi-%{version} ; \
tar xvzf $OLDPWD/evdi-1.0.138-src.tar.gz ; \
popd

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
