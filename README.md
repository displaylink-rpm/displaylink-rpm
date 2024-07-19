# DisplayLink RPM

[![Build Status](https://github.com/displaylink-rpm/displaylink-rpm/actions/workflows/buildcheck.yml/badge.svg)](https://github.com/displaylink-rpm/displaylink-rpm/actions/workflows/buildcheck.yml)
[![Build Status](https://github.com/displaylink-rpm/displaylink-rpm/actions/workflows/mainbuild.yml/badge.svg)](https://github.com/displaylink-rpm/displaylink-rpm/actions/workflows/mainbuild.yml)
[![Build Status](https://github.com/displaylink-rpm/displaylink-rpm/actions/workflows/rawhidebuilds.yml/badge.svg)](https://github.com/displaylink-rpm/displaylink-rpm/actions/workflows/rawhidebuilds.yml)

This is the recipe for building the [DisplayLink driver][displaylink]
in a RPM package for Fedora, CentOS Stream, Rocky Linux and AlmaLinux OS. This driver supports the following
device families:

- DL-7xxx
- DL-6xxx
- DL-5xxx
- DL-41xx
- DL-3xxx

The package includes the Open Source [evdi][evdi] library.

Packages get automatically built by GitHub Actions and get uploaded to
[GitHub releases][releases].

[displaylink]: http://www.displaylink.com/
[evdi]: https://github.com/DisplayLink/evdi
[releases]: https://github.com/displaylink-rpm/displaylink-rpm/releases

## Usage

> NOTE: Now buildable cleanly via .spec file (in mock f.e.). Download files
> via `make srpm`.

In order to create the driver rpm package you can run the command `make` from
within the checked out directory. The Makefile should download the files needed
for you and create an RPM.

A default `make` will use the evdi driver that is bundled with the Displaylink
driver package. If you need to use a newer released version from the evdi Github
repo and it is not currently present in the Displaylink driver package, you can
do so by running:

```bash
make github-release
```

### Secure boot on Fedora

To use displaylink-rpm and the evdi kernel module with secure boot enabled on
Fedora you need to sign the module with an enrolled Machine Owner Key (MOK).

Before continue please verify if Secure boot is enabled on your system:
`mokutil --sb-state`

If the answer is yes, please continue with the below guide, 
otherwise enrolled of MOK is not required and you can ignore this instruction.

From DKMS version [3.0.4](https://github.com/dell/dkms/releases/tag/v3.0.4) there is no need to create MOK manually,
DKMS during installation generates its own key that needs to be enrolled only once by the user. 

To enroll the key please follow this instruction:

1. Install mokutil and dkms tool from repository `sudo dnf install mokutil dkms`.
2. Import the key by executing `mokutil --import /var/lib/dkms/mok.pub` and follow the instruction enrollment instruction available on [DKMS github page](https://github.com/dell/dkms?tab=readme-ov-file#secure-boot) (system reboot will be required).
3. After system reboot execute `sudo dkms autoinstall` command in order to build and sign evdi module by MOK.
4. Now evdi modul should be signed and ready to use (hdmi and/or dvi ports on your docking station should work). You can verify that by executing `sudo dkms status` or `sudo systemctl status displaylink-driver.service`.

## Hardware-specific behavior

### Dell D6000

When used with the Dell D6000 docking station, DisplayLink 5.1.26 regularly
loses communication with attached monitors, causing them to go blank and enter
power-saving mode.  At the time the monitors blank, the kernel logs two error
messages:

``` bash
kernel: usb <xxx>: Disable of device-initiated U1 failed.
kernel: usb <xxx>: Disable of device-initiated U2 failed.
```

To [work around this issue][workaround], disable power management for the audio
device by commenting out a line in `/etc/pulse/default.pa`:

``` bash
### Automatically suspend sinks/sources that become idle for too long
# load-module module-suspend-on-idle
```

[workaround]: https://displaylink.org/forum/showpost.php?p=85116

## Development Builds

Generally we want to track the current stable release of the evdi library.
However, Fedora kernels are often much newer than those officially supported by
that release and it is not uncommon for a new kernel to completely break the
build. This can leave you in a situation where you cannot upgrade your kernel
without sacrificing your displaylink devices. This is not great if the new
kernel has important security or performance fixes.

The evdi developers use the `main` branch as their main branch for all changes.

To pull the latest code from the `main` branch and use it to build, do the
following:

``` bash
make main

make github-release
```

Of course this `main` branch will also include some experimental and less
tested changes that may break things in other unexpected ways. So you should
prefer the mainline build if it works, but if it breaks, you have the option of
making a `main` build.

If you are using Fedora Rawhide, you can create a build which will automatically
download from the `main` branch and build by running:

``` bash
make rawhide
```

> In the past, code in the `main` branch would be tagged and that version is what
> would be included in the Displaylink driver package.
>
> Recently, we are seeing newer changes appear in the Displaylink driver package
> without the evdi library version being changed. This has created some confusion
> and difficulty when it comes to maintenance updates.
>
> The evdi folks have [acknowledged this issue][roadmap_discussion] and are
> working on making the process more transparent.

[roadmap_discussion]: https://github.com/DisplayLink/evdi/issues/309#issuecomment-979831346

## Contributing

The easiest way to contribute with the package is to fork it and send
a pull request in GitHub.

There are two main kind of contributions: either a new upstream
version is released or a modification in the packaging is proposed.

There is a variable called `RELEASE` for packaging purposes. That
variable should be set to 1 when contributing a new upstream version
release, and incremented in one when adding any other functionality to
the specfile for the same upstream version.

### New Upstream release

From time to time, DisplayLink will update their driver. We try to do
so, but for that we usually rely on pull requests.

We manage three different upstream numbers for versioning:

1. evdi kernel driver version
2. DisplayLinkManager daemon and libraries version
3. Download ID number from DisplayLink (for automatic zip retrieval)

These variables need to be changed in the following places:

- Makefile
  - `DAEMON_VERSION` is the DisplayLinkManager version
  - `VERSION` is currently the evdi driver version
  - `DOWNLOAD_ID` is the `?download_id=` query parameter in
    DisplayLink website to download the zip

Also, please update the changelog at the bottom of the
displaylink.spec file.

### Packaging change

When changing a packaging rule, please increment the `RELEASE`
variable by one in displaylink.spec
