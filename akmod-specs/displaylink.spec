# SPDX-FileCopyrightText: 2022 ffgiff <ffgiff@gmail.com>
#
# SPDX-License-Identifier: MIT

Name:		displaylink
Version:	5.6.1
%global displaylink_rpm_commit 2628a1db26882f13b1645fa47a58e4aa022c68f0
Release:	1%{?dist}
Summary:	Meta-package for proprietary DisplayLinkManager application
URL:		https://www.synaptics.com/products/displaylink-graphics/downloads/ubuntu
Source0:	https://www.synaptics.com/sites/default/files/exe_files/2022-08/DisplayLink%20USB%20Graphics%20Software%20for%20Ubuntu5.6.1-EXE.zip
Source1:	https://github.com/displaylink-rpm/displaylink-rpm/archive/%{displaylink_rpm_commit}.tar.gz
License:	MIT
Requires:	akmod-evdi, %{name}-config, %{name}-manager

%description
Meta-package to install kernel module and proprietary tools
needed to communicate with and manage DisplayLink USB graphics
adapters along with additional config files.

%files

%build

%global _hardened_build 1

%package manager
Summary:	Proprietary DisplayLink Manager application
License:	Redistributable, no modification permitted
URL:		https://www.synaptics.com/products/displaylink-graphics/downloads/ubuntu
ExclusiveArch:	aarch64 armv7hl i386 x86_64
BuildRequires:	libdrm-devel
# The DisplayLinkManager binary is linked at run-time to a specific version of libevdi
Requires:	libevdi == 1.12.0

%description manager
This contains the proprietary tools needed to communicate with and manage
DisplayLink USB graphics adapters.

%files manager
%license LICENSE
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/DisplayLinkManager
%{_libexecdir}/%{name}/ella-dock-release.spkg
%{_libexecdir}/%{name}/firefly-monitor-release.spkg
%{_libexecdir}/%{name}/ridge-dock-release.spkg
%{_libexecdir}/%{name}/udev.sh
%dir /var/log/%{name}/
%{_prefix}/lib/systemd/system-sleep/displaylink.sh

%package config
Summary:	Supporting config files for DisplayLink USB graphics adapters
License:	MIT
URL:		https://github.com/displaylink-rpm/displaylink-rpm
BuildArch:	noarch
Requires:	%{name}-manager logrotate

%description config
This adds support for HDMI/VGA adapters built upon the DisplayLink DL-6xxx,
DL-5xxx, DL-41xx and DL-3xxx series of chip-sets. This includes numerous
docking stations, USB monitors, and USB adapters.

%preun config
%systemd_preun displaylink-driver.service

%postun config
%systemd_postun_with_restart displaylink-driver.service

%files config
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_unitdir}/displaylink-driver.service
%{_udevrulesdir}/99-displaylink.rules
%{_datadir}/X11/xorg.conf.d/20-displaylink.conf
%{_presetdir}/95-displaylink.preset

%post config
%systemd_post displaylink-driver.service



%prep
%setup -q -T -D -a 1 -c -n %{name}-rpm-%{displaylink_rpm_commit}
for i in displaylink-driver.service	\
	displaylink.logrotate	\
	95-displaylink.preset	\
	99-displaylink.rules	\
	20-displaylink.conf	\
	displaylink-sleep-extractor.sh \
	displaylink-udev-extractor.sh
do
  cp -v %{name}-rpm-%{displaylink_rpm_commit}/$i .
done
unzip "%{SOURCE0}"
chmod +x displaylink-driver-%{version}-59.184.run
./displaylink-driver-%{version}-59.184.run --noexec --keep
chmod 644 displaylink-driver-%{version}-59.184/LICENSE

%install
mkdir -p %{buildroot}%{_libexecdir}/%{name}/			\
	%{buildroot}%{_unitdir}/				\
	%{buildroot}%{_presetdir}/				\
	%{buildroot}%{_prefix}/lib/systemd/system-sleep/	\
	%{buildroot}%{_sysconfdir}/logrotate.d/			\
	%{buildroot}%{_udevrulesdir}/				\
	%{buildroot}%{_datadir}/X11/xorg.conf.d/		\
	%{buildroot}%{_localstatedir}/log/%{name}/

# DisplayLinkManager
pushd displaylink-driver-%{version}-59.184

cp LICENSE ..

%ifarch x86_64
cp -a x64-ubuntu-1604/DisplayLinkManager %{buildroot}%{_libexecdir}/%{name}/
%endif

%ifarch %ix86
cp -a x86-ubuntu-1604/DisplayLinkManager %{buildroot}%{_libexecdir}/%{name}/
%endif

%ifarch armv7hl
cp -a arm-linux-gnueabihf/DisplayLinkManager %{buildroot}%{_libexecdir}/%{name}/
%endif

%ifarch aarch64
cp -a aarch64-linux-gnu/DisplayLinkManager %{buildroot}%{_libexecdir}/%{name}/
%endif

# Firmwares
cp -a ella-dock-release.spkg firefly-monitor-release.spkg ridge-dock-release.spkg %{buildroot}%{_libexecdir}/%{name}/

# pm-util
bash ../displaylink-sleep-extractor.sh displaylink-installer.sh > %{buildroot}%{_prefix}/lib/systemd/system-sleep/displaylink.sh

chmod +x %{buildroot}%{_prefix}/lib/systemd/system-sleep/displaylink.sh

# udev trigger scripts
bash ../displaylink-udev-extractor.sh udev-installer.sh > %{buildroot}%{_libexecdir}/%{name}/udev.sh
chmod +x %{buildroot}%{_libexecdir}/%{name}/udev.sh


popd

# systemd/udev
cp -a displaylink-driver.service %{buildroot}%{_unitdir}
cp -a displaylink.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
cp -a 95-displaylink.preset %{buildroot}%{_presetdir}
cp -a 99-displaylink.rules %{buildroot}%{_udevrulesdir}
cp -a 20-displaylink.conf %{buildroot}%{_datadir}/X11/xorg.conf.d

%changelog
* Mon Oct 31 2022 ffgiff <ffgiff@gmail.com> 5.6.1-1
- Latest 5.6.1 release
* Mon Jun 20 2022 ffgiff <ffgiff@gmail.com> 5.6-1
- Latest 5.6 release
* Tue Mar 22 2022 ffgiff <ffgiff@gmail.com> 5.5-2
- Latest 5.5 release
* Thu Feb 10 2022 ffgiff <ffgiff@gmail.com> 5.5-1
- Latest 5.5 beta for kernel 5.16
* Mon Oct 18 2021 ffgiff <ffgiff@gmail.com> 5.4.1-1
- First version
