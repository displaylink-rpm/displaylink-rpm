Name:		evdi
Version:	1.9.1
Release:	1%{?dist}
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
* Sat May 01 2021 ffgiff <ffgiff@gmail.com> 1.9.1-1
- First version
