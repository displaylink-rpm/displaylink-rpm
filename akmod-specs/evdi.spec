Name:		evdi
Version:	1.10.0
Release:	3%{?dist}
Summary:	User-land library for Extensible Virtual Display Interface Kernel module
URL:		https://github.com/DisplayLink/evdi
Source0:	%{url}/archive/v%{version}.tar.gz
License:	LGPLv2
BuildRequires:	libdrm-devel
Provides:	evdi-kmod-common = %{version}-%{release}
Provides:	libevdi = %{version}-%{release}

%files
%{_libdir}/libevdi.so
%{_libdir}/libevdi.so.0
%{_libdir}/libevdi.so.%{version}
%doc evdi-%{version}/docs/index.md

%global _hardened_build 1

%description
User-land library for Extensible Virtual Display Interface Kernel module

%prep
%setup -q -c evdi-%{version}

%build
pushd evdi-%{version}
CFLAGS="$RPM_OPT_FLAGS" %{make_build} -C library

%install
# Library
pushd evdi-%{version}
LIBDIR=%{_libdir} %{make_install} -C library


%changelog
* Thu Feb 10 2022 ffgiff <ffgiff@gmail.com> 1.10.0-1
- Use latest tagged commit
* Wed Dec 01 2021 ffgiff <ffgiff@gmail.com> 1.9.1-3
- Use latest devel commit to support 5.15
* Sat Jul 24 2021 ffgiff <ffgiff@gmail.com> 1.9.1-2
- Use latest devel commit to support 5.13 and 5.14
* Sat May 01 2021 ffgiff <ffgiff@gmail.com> 1.9.1-1
- First version
