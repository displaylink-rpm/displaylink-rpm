# SPDX-FileCopyrightText: 2022 ffgiff <ffgiff@gmail.com>
#
# SPDX-License-Identifier: MIT

# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%global buildforkernels akmod
%global debug_package %{nil}

Name:		evdi-kmod
Version:	1.11.0
# Taken over by kmodtool
Release:	1%{?dist}
Summary:	Extensible Virtual Display Interface Kernel module
License:	GPLv2
URL:		https://github.com/DisplayLink/evdi
Source0:	%{url}/archive/v%{version}.tar.gz
# libevdi CI tests from kernel 4.15 to 5.15
Requires:	kernel >= 4.15, kernel <= 5.18
# get the needed BuildRequires (in parts depending on what we build for)
%global AkmodsBuildRequires %{_bindir}/kmodtool
BuildRequires:	%{AkmodsBuildRequires}
BuildRequires:	libdrm-devel

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
The evdi %{version} display driver kernel module.
This is primarily used by DisplayLink graphics devices.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null
%setup -q -c -T -a 0
for kernel_version  in %{?kernel_versions} ; do
	cp -a evdi-%{version}/module _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
	pushd _kmod_build_${kernel_version%%___*}/
	CFLAGS="$CFLAGS -fno-pic -Wno-error=format-security" KVER=${kernel_version%%___*} %{make_build} module
	popd
done


%install
for kernel_version in %{?kernel_versions}; do
	mkdir -p  $RPM_BUILD_ROOT/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
	install -D -m 0755 _kmod_build_${kernel_version%%___*}/evdi*.ko \
	$RPM_BUILD_ROOT/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
done
%{?akmod_install}


%changelog
* Mon Jun 20 2022 ffgiff <ffgiff@gmail.com> 1.11.0-1
- Use latest tagged commit
* Tue Mar 22 2022 ffgiff <ffgiff@gmail.com> 1.10.1-1
- Use latest tagged commit
* Thu Feb 10 2022 ffgiff <ffgiff@gmail.com> 1.10.0-1
- Use latest tagged commit
* Wed Dec 01 2021 ffgiff <ffgiff@gmail.com> 1.9.1-3
- Use latest devel commit to support 5.15
* Sat Jul 24 2021 ffgiff <ffgiff@gmail.com> 1.9.1-2
- Use latest devel commit to support 5.13 and 5.14
* Sat May 01 2021 ffgiff <ffgiff@gmail.com> 1.9.1-1
- First version

