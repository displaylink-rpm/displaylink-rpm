Name:		evdi
Version:	1.9.1
Release:	3%{?dist}
Summary:	User-land library for Extensible Virtual Display Interface Kernel module
URL:		https://github.com/DisplayLink/evdi
Source0:	%{url}/archive/d6b28414a4ceb41a904077318b48fa8a7d8981d1.tar.gz
License:	LGPLv2
BuildRequires:	libdrm-devel
Provides:	evdi-kmod-common = %{version}-%{release}
Provides:	libevdi = %{version}-%{release}

%files
%{_libdir}/libevdi.so
%{_libdir}/libevdi.so.0
%{_libdir}/libevdi.so.%{version}
%doc evdi-d6b28414a4ceb41a904077318b48fa8a7d8981d1/docs/index.md

%global _hardened_build 1

%description
User-land library for Extensible Virtual Display Interface Kernel module

%prep
%setup -q -c evdi-d6b28414a4ceb41a904077318b48fa8a7d8981d1

%build
pushd evdi-d6b28414a4ceb41a904077318b48fa8a7d8981d1
CFLAGS="$RPM_OPT_FLAGS" %{make_build} -C library

%install
# Library
pushd evdi-d6b28414a4ceb41a904077318b48fa8a7d8981d1
LIBDIR=%{_libdir} %{make_install} -C library


%changelog
* Wed Dec 01 2021 ffgiff <ffgiff@gmail.com> 1.9.1-3
- Use latest devel commit to support 5.15
* Sat Jul 24 2021 ffgiff <ffgiff@gmail.com> 1.9.1-2
- Use latest devel commit to support 5.13 and 5.14
* Sat May 01 2021 ffgiff <ffgiff@gmail.com> 1.9.1-1
- First version
