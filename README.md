DisplayLink RPM
===============
[![Build Status](https://travis-ci.org/displaylink-rpm/displaylink-rpm.svg?branch=master)](https://travis-ci.org/displaylink-rpm/displaylink-rpm)

This is the recipe for building the [DisplayLink driver][displaylink]
in a RPM package for Fedora and CentOS. This driver supports the following
device families:
 - DL-6xxx
 - DL-5xxx
 - DL-41xx
 - DL-3xxx

The package includes the Open Source [evdi][evdi] library.

Packages get automatically built by Travis CI and get uploaded to
[GitHub releases][releases].

[displaylink]: http://www.displaylink.com/
[evdi]: https://github.com/DisplayLink/evdi
[releases]: https://github.com/displaylink-rpm/displaylink-rpm/releases

Usage
=====

In order to compile the driver, just use make. The Makefile should
download the file for you.


Development Builds
==================

Generally we want to track the current stable release of the evid library.
However, Fedora kernels are often much newer than those officially supported by
that release and it is not uncommon for a new kernel to completely break the
build.  This can leave you in a situation where you cant upgrade your kernel
without sacrificing your displaylink devices. This is not great if the new
kernel has important security or performance fixes.

Fortunately the evdi developers are usually pretty quick to make the
appropriate fixes on their `devel` branch.  You can build a verison of the rpm
that uses the current edvi `devel` branch with:

    make rawhide

Of course this `devel` branch will also include some experimental and less
tested changes that may break things in other unexpected ways. So you should prefer the
mainline build if it works, but if it breaks, you have the option of making
a `rawhide ` build.


Contributing
============

The easiest way to contribute with the package is to fork it and send
a pull request in GitHub.

There are two main kind of contributions: either a new upstream
version is released or a modification in the packaging is proposed.

There is a variable called `RELEASE` for packaging purposes. That
variable should be set to 1 when contributing a new upstream version
release, and incremented in one when adding any other functionality to
the specfile for the same upstream version.


New Upstream release
--------------------

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
- .travis.yml
  - `VERSION` is the same as in the Makefile
  - `DAEMON_VERSION` is the same version as in Makefile

Also, please update the changelog at the bottom of the
displaylink.spec file.


Packaging change
----------------

When changing a packaging rule, please increment the `RELEASE`
variable by one in both displaylink.spec and .travis.yml (so that
Travis can release the new artifact automatically).

