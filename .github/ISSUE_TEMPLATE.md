<!-- Please look through existing issues (open and closed) and make sure you are not creating a duplicate issue: -->
  * Are you using the latest DisplayLink driver?
    <!-- (https://www.synaptics.com/products/displaylink-graphics/downloads/ubuntu) -->
  * Are you using the latest EVDI module?
    <!-- (https://github.com/DisplayLink/evdi/releases) -->
  * If you are using a DisplayLink device, have you checked 'troubleshooting'
    on DisplayLink's website?
    <!-- (https://support.displaylink.com/knowledgebase/topics/103927-troubleshooting-ubuntu) -->
  * Is this issue related to evdi/kernel?
    <!-- (Please go to the EVDI repository for support: https://github.com/DisplayLink/evdi) -->
  * Is this issue related to DisplayLinkManager?
    <!-- (If so, please take a look at DisplayLink's support forum
    https://support.displaylink.com or forum https://www.displaylink.org/forum/) -->
  * If you are having an issue upgrading, have you tried to do a clean install of the driver?
    <!-- Do the following for a clean driver install:
           Find the current package installed - `sudo rpm -qa | grep displaylink`
           Remove what is returned: `sudo rpm -evh [package]`

           Clear out anything left over:
            /var/lib/dkms/evdi
            /usr/libexec/displaylink
            /usr/src/evdi-*

            /etc/X11/xorg.conf.d/20-displaylink.conf
            /etc/logrotate.d/displaylink
            /usr/lib/systemd/system/displaylink-driver.service
            /usr/lib/systemd/system-preset/95-displaylink.preset
            /usr/lib/systemd/system-sleep/displaylink.sh
            /etc/udev/rules.d/99-displaylink.rules
            /usr/share/doc/displaylink
            /usr/share/doc/displaylink/LICENSE

            /usr/lib/modules/`uname -r`/weak-updates/evdi.ko.xz
            /usr/lib/modules/`uname -r`/extra/evdi.ko.xz

          Reboot
          Reinstall the RPM package -->


<!-- Provide the following information -->
  * Fedora / CentOS Stream / Rocky Linux / AlmaLinux OS
  * Version
  * Kernel version `(uname -a)`

<!-- Please provide the following logs -->
  * `/var/log/displaylink/displaylink.log`
  * `/var/lib/dkms/evdi/kernel-[version]/log/make.log`

<!-- Please add a good summary of the issue in the Title above -->

<!-- Steps to reproduce -->

<!-- Detailed description -->
