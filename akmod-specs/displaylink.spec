Name:		displaylink
Version:	5.4
%global config_release 1
Release:	1%{?dist}
Summary:	Metapackage for proprietary DisplayLink Manager application
URL:		https://www.synaptics.com/products/displaylink-graphics/downloads/ubuntu
# The DisplayLink proprietary software can be obtained using:
# curl -LO https://www.synaptics.com/sites/default/files/exe_files/2021-04/DisplayLink%20USB%20Graphics%20Software%20for%20Ubuntu5.4-EXE.zip
Source0:	DisplayLink%20USB%20Graphics%20Software%20for%20Ubuntu%{version}-EXE.zip
#Source1:	https://github.com/displaylink-rpm/displaylink-rpm/archive/v%{version}-%{config_release}.tar.gz
Source1:	https://github.com/displaylink-rpm/displaylink-rpm/archive/v5.3.1-%{config_release}.tar.gz
License:	MIT
Requires:	akmod-evdi, %{name}-config, %{name}-manager

%description
Metapackage to install akmod and proprietary tools needed to communicate with and manage
DisplayLink USB graphics adapters along with additional config files.

%files

%global _hardened_build 1

%package manager
Summary:	Proprietary DisplayLink Manager application
License:	Redistributable, no modification permitted
URL:		https://www.synaptics.com/products/displaylink-graphics/downloads/ubuntu
ExclusiveArch:	armv7hl i386 x86_64
BuildRequires:	libdrm-devel
# The DisplayLinkManager binary is linked at run-time to a specific version of libevdi
Requires:	libevdi == 1.9.1
Requires:	libusbx

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
%dir /var/log/%{name}/
%{_prefix}/lib/systemd/system-sleep/displaylink.sh

%package config
Summary:	Supporting config files for DisplayLink USB graphics adapters
License:	MIT
URL:		https://github.com/displaylink-rpm/displaylink-rpm
BuildArch:	noarch
Requires:	%{name}-manager

%description config
This adds support for HDMI/VGA adapters built upon the DisplayLink DL-6xxx,
DL-5xxx, DL-41xx and DL-3xxx series of chipsets. This includes numerous
docking stations, USB monitors, and USB adapters.

%preun config
%systemd_preun displaylink.service

%postun config
%systemd_postun_with_restart displaylink.service

%files config
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_unitdir}/displaylink.service
%{_udevrulesdir}/99-displaylink.rules
%{_datadir}/X11/xorg.conf.d/20-displaylink.conf
%{_presetdir}/95-displaylink.preset

%post config
%systemd_post displaylink-service



%prep
#%setup -q -T -D -a 1 -c -n %{name}-rpm-%{version}-%{config_release}
%setup -q -T -D -a 1 -c -n %{name}-rpm-5.3.1-%{config_release}
for i in displaylink.service  \
         displaylink.logrotate  \
         95-displaylink.preset \
         99-displaylink.rules \
         20-displaylink.conf  \
         displaylink-sleep-extractor.sh
do
#  cp -v displaylink-rpm-%{version}-%{config_release}/$i .
  cp -v displaylink-rpm-5.3.1-%{config_release}/$i .
done
unzip "%{SOURCE0}"
chmod +x displaylink-driver-%{version}.0-55.153.run
./displaylink-driver-%{version}.0-55.153.run --noexec --keep

%install
mkdir -p %{buildroot}%{_libexecdir}/%{name}/		\
        %{buildroot}%{_unitdir}/				\
        %{buildroot}%{_presetdir}/				\
        %{buildroot}%{_prefix}/lib/systemd/system-sleep/	\
        %{buildroot}%{_sysconfdir}/logrotate.d/			\
        %{buildroot}%{_udevrulesdir}/				\
        %{buildroot}%{_datadir}/X11/xorg.conf.d/		\
        %{buildroot}%{_localstatedir}/log/%{name}/

# DisplayLinkManager
pushd displaylink-driver-%{version}.0-55.153

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

# Firmwares
cp -a ella-dock-release.spkg firefly-monitor-release.spkg ridge-dock-release.spkg %{buildroot}%{_libexecdir}/%{name}/

# pm-util
bash ../displaylink-sleep-extractor.sh displaylink-installer.sh > %{buildroot}%{_prefix}/lib/systemd/system-sleep/displaylink.sh

chmod +x %{buildroot}%{_prefix}/lib/systemd/system-sleep/displaylink.sh

popd

# systemd/udev
cp -a displaylink.service %{buildroot}%{_unitdir}
cp -a displaylink.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
cp -a 95-displaylink.preset %{buildroot}%{_presetdir}
cp -a 99-displaylink.rules %{buildroot}%{_udevrulesdir}
cp -a 20-displaylink.conf %{buildroot}%{_datadir}/X11/xorg.conf.d

%changelog
* Thu Apr 08 2021 ffgiff <ffgiff@gmail.com> 5.4-1
- First version
