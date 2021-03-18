%global _daemon_version 5.3.1.34
%global _version 1.7.2
%global _release 2

%global debug_package %{nil}
%if 0%{?rhel} && 0%{?rhel} <= 7
%global kernel_pkg_name kernel-ml
%else
%global kernel_pkg_name kernel
%endif

Name:		displaylink
Version:	%{_version}
Release:	%{_release}
Summary:	DisplayLink VGA/HDMI driver for DL-6xxx, DL-5xxx, DL-41xx and DL-3xxx adapters

License:	GPL v2.0, LGPL v2.1 and Proprietary
Source0:	https://github.com/DisplayLink/evdi/archive/v%{version}.tar.gz
Source1:	displaylink.service
Source2:	99-displaylink.rules
Source3:	displaylink-sleep-extractor.sh
# From http://www.displaylink.com/downloads/ubuntu.php
Source4:	DisplayLink USB Graphics Software for Ubuntu %{_daemon_version}.zip
Source5:	20-displaylink.conf
Source6:	95-displaylink.preset
Source7:	%{name}.logrotate

BuildRequires:	gcc-c++
BuildRequires:	libdrm-devel
BuildRequires:	make

%if 0%{?fedora} < 30 || 0%{?rhel}
BuildRequires:	systemd
%else
BuildRequires:	systemd-rpm-macros
%endif

%if 0%{?rhel}
Requires:	epel-release
%endif

Requires:	dkms
Requires:	%{kernel_pkg_name} >= 4.15, %{kernel_pkg_name}-devel >= 4.15
Requires:	make
Conflicts:	xorg-x11-server-Xorg = 1.20.1

%description
This adds support for HDMI/VGA adapters built upon the DisplayLink DL-6xxx,
DL-5xxx, DL-41xx and DL-3xxx series of chipsets. This includes numerous
docking stations, USB monitors, and USB adapters.

%define logfile %{_localstatedir}/log/%{name}/%{name}.log

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
%make_build

%install

mkdir -p %{buildroot}%{_libexecdir}/%{name}/			\
	%{buildroot}%{_prefix}/src/evdi-%{version}/		\
	%{buildroot}%{_unitdir}/				\
	%{buildroot}%{_prefix}/lib/systemd/system-preset/	\
	%{buildroot}%{_prefix}/lib/systemd/system-sleep/	\
	%{buildroot}%{_sysconfdir}/logrotate.d/			\
	%{buildroot}%{_sysconfdir}/udev/rules.d/		\
	%{buildroot}%{_sysconfdir}/X11/xorg.conf.d/		\
	%{buildroot}%{_localstatedir}/log/%{name}/

# Kernel driver sources
pushd %{buildroot}%{_prefix}/src/evdi-%{version} ; \
cp -a $OLDPWD/evdi-%{version}/module/* . ; \
popd

# Turn off weak modules symlink being added for dkms build of evdi
echo "NO_WEAK_MODULES=yes" >> %{buildroot}%{_prefix}/src/evdi-%{version}/dkms.conf

# Library
cp -a evdi-%{version}/library/libevdi.so.%{version} %{buildroot}%{_libexecdir}/%{name}/
ln -s %{_libexecdir}/%{name}/libevdi.so.%{version} %{buildroot}%{_libexecdir}/%{name}/libevdi.so

# Binaries
# Don't copy libusb-1.0.so.0.1.0 it's already shipped by libusbx
# Don't copy libevdi.so, we compiled it from source

cd evdi-%{version}/displaylink-driver-%{_daemon_version}

cp -a LICENSE ../..

%ifarch x86_64
cp -a x64-ubuntu-1604/DisplayLinkManager %{buildroot}%{_libexecdir}/%{name}/
%endif

%ifarch %ix86
cp -a x86-ubuntu-1604/DisplayLinkManager %{buildroot}%{_libexecdir}/%{name}/
%endif

# Firmwares
cp -a ella-dock-release.spkg firefly-monitor-release.spkg ridge-dock-release.spkg %{buildroot}%{_libexecdir}/%{name}/

# systemd/udev
cp -a %{SOURCE1} %{buildroot}%{_unitdir}/
cp -a %{SOURCE2} %{buildroot}%{_sysconfdir}/udev/rules.d/
cp -a %{SOURCE5} %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/
cp -a %{SOURCE6} %{buildroot}%{_prefix}/lib/systemd/system-preset/
cp -a %{SOURCE7} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# pm-util
bash %{SOURCE3} displaylink-installer.sh > %{buildroot}%{_prefix}/lib/systemd/system-sleep/displaylink.sh

chmod +x %{buildroot}%{_prefix}/lib/systemd/system-sleep/displaylink.sh

%post
%systemd_post displaylink.service
%{_sbindir}/dkms add evdi/%{version} --rpm_safe_upgrade >> %{logfile} 2>&1
%{_sbindir}/dkms build evdi/%{version} >> %{logfile} 2>&1
%{_sbindir}/dkms install evdi/%{version} >> %{logfile} 2>&1
%{_bindir}/systemctl start displaylink.service

%files
%doc LICENSE
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_unitdir}/displaylink.service
%{_prefix}/lib/systemd/system-preset/95-displaylink.preset
%{_prefix}/lib/systemd/system-sleep/displaylink.sh
%{_sysconfdir}/udev/rules.d/99-displaylink.rules
%{_sysconfdir}/X11/xorg.conf.d/20-displaylink.conf

%dir %{_prefix}/src/evdi-%{version}
%{_prefix}/src/evdi-%{version}/Kconfig
%{_prefix}/src/evdi-%{version}/LICENSE
%{_prefix}/src/evdi-%{version}/Makefile
%{_prefix}/src/evdi-%{version}/dkms.conf
%{_prefix}/src/evdi-%{version}/evdi_connector.c
%{_prefix}/src/evdi-%{version}/evdi_cursor.c
%{_prefix}/src/evdi-%{version}/evdi_cursor.h
%{_prefix}/src/evdi-%{version}/evdi_debug.c
%{_prefix}/src/evdi-%{version}/evdi_debug.h
%{_prefix}/src/evdi-%{version}/evdi_drm.h
%{_prefix}/src/evdi-%{version}/evdi_drv.c
%{_prefix}/src/evdi-%{version}/evdi_drv.h
%{_prefix}/src/evdi-%{version}/evdi_encoder.c
%{_prefix}/src/evdi-%{version}/evdi_fb.c
%{_prefix}/src/evdi-%{version}/evdi_gem.c
%{_prefix}/src/evdi-%{version}/evdi_ioc32.c
%{_prefix}/src/evdi-%{version}/evdi_main.c
%{_prefix}/src/evdi-%{version}/evdi_modeset.c
%{_prefix}/src/evdi-%{version}/evdi_painter.c
%{_prefix}/src/evdi-%{version}/evdi_params.c
%{_prefix}/src/evdi-%{version}/evdi_params.h

%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/DisplayLinkManager
%{_libexecdir}/%{name}/ella-dock-release.spkg
%{_libexecdir}/%{name}/firefly-monitor-release.spkg
%{_libexecdir}/%{name}/libevdi.so
%{_libexecdir}/%{name}/libevdi.so.%{version}
%{_libexecdir}/%{name}/ridge-dock-release.spkg

%dir %{_localstatedir}/log/%{name}/

%preun
%systemd_preun displaylink.service
%{_sbindir}/dkms remove evdi/%{version} --all --rpm_safe_upgrade >> %{logfile}

%postun
%systemd_postun_with_restart displaylink.service

%changelog
* Thu Jan 14 2021 Michael L. Young <elgueromexicano@gmail.com> 1.7.2-2
- Prevent DKMS from adding a symlink for weak modules on Fedora.
  See DKMS documentation.

* Fri Dec 11 2020 Michael L. Young <elgueromexicano@gmail.com> 1.7.2-1
- Update to evdi driver version 1.7.2

* Tue Dec 08 2020 Michael L. Young <elgueromexicano@gmail.com> 1.7.2-1
- Add the requirement for epel if distro is RHEL based
- Remove requirement for 'ml' kernel for RHEL distro greater than 7

* Mon Dec 07 2020 Michael L. Young <elgueromexicano@gmail.com> 1.7.2-1
- Remove hard coded libevdi.so.1.7.0 reference in the files section

* Mon Jun 22 2020 Michael L. Young <elgueromexicano@gmail.com> 1.7.0-2
- Add 'make' as a requirement for installing the RPM since DKMS needs it to
  build the evdi module.

* Sat May 30 2020 Mitya Eremeev <mitossvyaz@mail.ru> 1.7.0-2
- fix typo in kernel package name
- tested package in CentOS 8

* Mon May 11 2020 Michael L. Young <elgueromexicano@gmail.com> 1.7.0-1
- Update to evdi driver version 1.7.0.
- Update to Displaylink driver 5.3.1.
- The minimum kernel supported in evdi is now 4.15. Adjusting spec to match.
- Fix support for DL-6xxx devices. The firmware image was not being copied from
  the DisplayLink driver package.
- Adjust how we use dkms inside the rpm to follow recommended way in documentation.
- Switch spec to using macro for buildroot instead of variable for consistency.
- Change hardcoded paths to rpm macros
- List out files instead of using a wild card.  This Will help catch potential
  issues if files are missing or changed with new version releases.
- Use systemd scriplets for handling systemd unit file
- Use systemd preset file to enable displaylink.service by default
- Remove calls to enable dkms service since this is already enabled by policy
  on Fedora.
- Add logrotate config file

* Thu Apr 16 2020 Michael L. Young <elgueromexicano@gmail.com> 1.6.4-3
- Remove patches that are no longer needed.  This restores the ability
  to build against rawhide.

* Fri Feb 07 2020 Michael L. Young <elgueromexicano@gmail.com> 1.6.4-2
- Apply patches contributed by abucodonosor and severach on GitHub to get evdi
  working on kernel 5.4.
  See https://github.com/DisplayLink/evdi/issues/172#issuecomment-561394805
  See https://github.com/DisplayLink/evdi/issues/172#issuecomment-561964789

* Fri Jan 10 2020 Alan Halama <alhalama@gmail.com> 1.6.4-1
- Update the evdi driver to 1.6.4

* Tue Nov 05 2019 Michael L. Young <elgueromexicano@gmail.com> 1.6.3-1
- Update the evdi driver to 1.6.3

* Mon Aug 19 2019 Michael L. Young <elgueromexicano@gmail.com> 1.6.2-2
- Update Displaylink driver to 5.2.14

* Mon Jul 08 2019 Michael L. Young <elgueromexicano@gmail.com> 1.6.2-1
- Update evdi to 1.6.2

* Wed May 08 2019 Michael L. Young <elgueromexicano@gmail.com> 1.6.1-1
- Update evdi to 1.6.1

* Mon Mar 25 2019 Peter Janes <peter.janes@autodata.net> 1.6.0-2
- Add trigger on kernel postinstall to compile evdi via dkms for the new version

* Tue Feb 19 2019 Michael L. Young <elgueromexicano@gmail.com> 1.6.0-1
- Update DisplayLink Manager to 5.1.26
- Update evdi to 1.6.0

* Tue Dec 11 2018 Orsiris de Jong <ozy@netpower.fr> 1.5.1-2
- Add make and gcc-c++ build requirements

* Mon Nov 05 2018 okay_awright <okay_awright@ddcr.biz> 1.5.1-2
- Removed workaround for xorg-server 1.20.1 and glamorgl acceleration with evdi now that fedora ships xorg-server 1.20.3 which fixes the problem

* Tue Oct 30 2018 okay_awright <okay_awright@ddcr.biz> 1.5.1
- Update evdi version to 1.5.1
- Bump downloaded version to 4.4.24
- Workaround for xorg-server > 1.19 and glamorgl acceleration with evdi: https://github.com/DisplayLink/evdi/issues/133#issuecomment-428573850

* Wed Jan 17 2018 fgiff <ffgiff@gmail.com> 1.5.0-2
- Bump downloaded version to 4.1.9

* Tue Oct 10 2017 Alan Halama <alhalama@gmail.com> 1.5
- Update evdi version to 1.5
- Bump downloaded version to 1.4

* Thu Aug 17 2017 Kahlil Hodgson <kahlil.hodgson999@gmail.com> 1.1.4-5
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
