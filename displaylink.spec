Name:		displaylink
Version:	1.0.138
Release:	2
Summary:	DisplayLink VGA/HDMI driver for DL-5xxx, DL-41xx and DL-3xxx adapters

Group:		User Interface/X Hardware Support
License:	GPL v2.0, LGPL v2.1 and others
URL:		http://www.nothen.com.ar
Source0:	displaylink-1.0.138.txz

Requires:	dkms, kernel > 3.14, kernel-devel > 3.14

%description
This package installs the DisplayLink "Plug and Display" module for various HDMI/VGA adapters, including Dell's 4-in-1 (DA100). Based on DisplayLink's officially supported Ubuntu driver, and repackaged for Fedora/CentOS/RHEL distros. Module is added to DKMS so that it's recompiled on future kernel updates.

%define logfile /var/log/displaylink/%{name}.log

%prep

%build

%install
tar -xJpvf %{SOURCE0} -C $RPM_BUILD_ROOT

%post
/usr/bin/systemctl daemon-reload
/usr/bin/systemctl -q is-enabled dkms.service || /usr/bin/systemctl enable dkms.service
for kernel in $(rpm -q kernel --queryformat '%{VERSION}-%{RELEASE}.%{ARCH}\n') ;do
	/sbin/dkms install evdi/%{version} -k $kernel >> %{logfile} 2>&1
done

%files
/etc/systemd/system/displaylink.service
/etc/udev/rules.d/99-displaylink.rules
%dir /usr/src/evdi-1.0.138
/usr/src/evdi-1.0.138/*
%dir /usr/lib/displaylink
/usr/lib/displaylink/*
%dir /var/log/displaylink/

%preun
if [ $1 -eq 0 ] ;then
	/usr/bin/systemctl -q is-active displaylink.service && /usr/bin/systemctl stop displaylink.service
	/sbin/dkms remove evdi/%{version} --all >> %{logfile}
fi

%postun
/usr/bin/systemctl daemon-reload

%changelog
* Sun Sep 6  2015 Eric Nothen <enothen@gmail.com> - 1.0.138-2
- Modified installed kernels detection section to be more precise

* Wed Sep 2  2015 Eric Nothen <enothen@gmail.com> - 1.0.138-1
- Updated driver to version 1.0.138, as published by DisplayLink

* Wed Aug 19 2015 Eric Nothen <enothen@gmail.com> - 1.0.68-2
- Changed udev rule to detect devices based on vendor rather than model

* Thu Aug 13 2015 Eric Nothen <enothen@gmail.com> - 1.0.68-1
- Initial package based on module version 1.0.68 available at http://www.displaylink.com/downloads/ubuntu.php
