%global debug_package %{nil}

Name:		displaylink
Version:	%{_version}
Release:	%{_release}
Summary:	DisplayLink VGA/HDMI driver for DL-6xxx, DL-5xxx, DL-41xx and DL-3xxx adapters

Group:		User Interface/X Hardware Support
License:	GPL v2.0, LGPL v2.1 and Proprietary
Source0:	https://github.com/DisplayLink/evdi/archive/v%{version}.tar.gz
Source1:	displaylink.service
Source2:	99-displaylink.rules
Source3:    displaylink-sleep-extractor.sh
# From http://www.displaylink.com/downloads/ubuntu.php
Source4:	DisplayLink USB Graphics Software for Ubuntu %{_daemon_version}.zip
Source5:    20-displaylink.conf
ExclusiveArch:	i386 x86_64

BuildRequires:	libdrm-devel
Requires:	dkms, kernel > 4.7, kernel-devel > 4.7

%description
This adds support for HDMI/VGA adapters built upon the DisplayLink DL-6xxx,
DL-5xxx, DL-41xx and DL-3xxx series of chipsets. This includes numerous
docking stations, USB monitors, and USB adapters.

%define logfile /var/log/displaylink/%{name}.log

%prep
%setup -q -c evdi-%{version}
cd evdi-%{version}
sed -i 's/\r//' README.md

unzip "%{SOURCE4}"
chmod +x displaylink-driver-%{_daemon_version}.run
./displaylink-driver-%{_daemon_version}.run --noexec --keep
# This creates a displaylink-driver-$version subdirectory

%build

cd evdi-%{version}/library/
make %{?_smp_mflags}

%install

mkdir -p $RPM_BUILD_ROOT/usr/libexec/displaylink/	\
	$RPM_BUILD_ROOT/usr/src/evdi-%{version}/	\
	$RPM_BUILD_ROOT/usr/lib/systemd/system/		\
	$RPM_BUILD_ROOT/usr/lib/systemd/system-sleep	\
	$RPM_BUILD_ROOT/etc/udev/rules.d/		\
	$RPM_BUILD_ROOT/etc/X11/xorg.conf.d/		\
	$RPM_BUILD_ROOT/var/log/displaylink/

# Kernel driver sources
pushd $RPM_BUILD_ROOT/usr/src/evdi-%{version} ; \
cp -a $OLDPWD/evdi-%{version}/module/* . ; \
popd

# Library
cp evdi-%{version}/library/libevdi.so $RPM_BUILD_ROOT/usr/libexec/displaylink

# Binaries
# Don't copy libusb-1.0.so.0.1.0 it's already shipped by libusbx
# Don't copy libevdi.so, we compiled it from source

cd evdi-%{version}/displaylink-driver-%{_daemon_version}

cp LICENSE ../..

%ifarch x86_64
cp -a x64-ubuntu-1604/DisplayLinkManager $RPM_BUILD_ROOT/usr/libexec/displaylink/
%endif

%ifarch %ix86
cp -a x86-ubuntu-1604/DisplayLinkManager $RPM_BUILD_ROOT/usr/libexec/displaylink/
%endif

# Firmwares
cp -a ella-dock-release.spkg firefly-monitor-release.spkg $RPM_BUILD_ROOT/usr/libexec/displaylink/

# systemd/udev
cp -a %{SOURCE1} $RPM_BUILD_ROOT/usr/lib/systemd/system/
cp -a %{SOURCE2} $RPM_BUILD_ROOT/etc/udev/rules.d/
cp -a %{SOURCE5} $RPM_BUILD_ROOT/etc/X11/xorg.conf.d/

# pm-util
bash %{SOURCE3} displaylink-installer.sh > $RPM_BUILD_ROOT/usr/lib/systemd/system-sleep/displaylink.sh

chmod +x $RPM_BUILD_ROOT/usr/lib/systemd/system-sleep/displaylink.sh

%post
# The displaylink service may crash as dkms rebuilds the module
//usr/bin/systemctl -q is-active displaylink.service && usr/bin/systemctl stop displaylink.service
/usr/bin/systemctl daemon-reload
/usr/bin/systemctl -q is-enabled dkms.service || /usr/bin/systemctl enable dkms.service
for kernel in $(rpm -q kernel --queryformat '%{VERSION}-%{RELEASE}.%{ARCH}\n') ;do
	/sbin/dkms install evdi/%{version} -k $kernel >> %{logfile} 2>&1
done
/usr/bin/systemctl start displaylink.service

%files
%doc LICENSE
/usr/lib/systemd/system/displaylink.service
/usr/lib/systemd/system-sleep/displaylink.sh
/etc/udev/rules.d/99-displaylink.rules
/etc/X11/xorg.conf.d/20-displaylink.conf
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
* Wed Aug 17 2017 Kahlil Hodgson <kahlil.hodgson999@gmail.com> 1.1.4-5
- Restart displaylink service around dkms rebuild
- Make setup quiet as per fedora/redhat guidelines

* Wed Jul 26 2017 Kahlil Hodgson <kahlil.hodgson999@gmail.com> 1.1.4-4
- Give systemd sleep script exec permissions

* Tue Jul 11 2017 Kahlil Hodgson <kahlil.hodgson999@gmail.com> 1.1.4-3
- Disable PageFlip if xorg is using modesetting driver

* Sat Jul 8 2017 Alan Halama <alhalama@gmail.com> 1.3.54
- Bump downloaded version to 1.3.54

* Thu Jun 8 2017 Alan Halama <alhalama@gmail.com> 1.4.1
- Update evdi version to 1.4.1

* Sun Feb 19 2017 Richard Hofer <rofer@rofer.me> 1.3.52
- Bump downloaded version to 1.3.52
- Note support for DL-6xxx devices

* Tue Oct 11 2016 Aaron Aichlmayr <waterfoul@gmail.com> 1.2.64
- Bump downloaded version to 1.2.64

* Tue Oct 04 2016 Victor Rehorst <victor@chuma.org> 1.2.55-2
- Fix systemd-sleep support for DisplayLink driver 1.2.58 (which is now current for v1.2)

* Thu Sep 22 2016 Santiago Saavedra <ssaavedra@gpul.org> 1.2.55-1
- Bump upstream version for both evdi and DisplayLink driver

* Mon May 30 2016 Santiago Saavedra <ssaavedra@gpul.org> 1.1.65-5
- Add systemd-sleep support

* Tue May 24 2016 Bastien Nocera <bnocera@redhat.com> 1.1.65-4
- Really copy the libevdi.so from the sources

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
