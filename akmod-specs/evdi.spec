Name:		evdi
Version:	1.9.1
Release:	2%{?dist}
Summary:	User-land library for Extensible Virtual Display Interface Kernel module
URL:		https://github.com/DisplayLink/evdi
Source0:	%{url}/archive/b0b2c80eb63f9b858b71afa772135f434aea192a.tar.gz
License:	LGPLv2
BuildRequires:	libdrm-devel
Provides:	evdi-kmod-common = %{version}-%{release}
Provides:	libevdi = %{version}-%{release}

%files
%{_libdir}/libevdi.so
%{_libdir}/libevdi.so.0
%{_libdir}/libevdi.so.%{version}
%doc evdi-b0b2c80eb63f9b858b71afa772135f434aea192a/docs/index.md

%global _hardened_build 1

%description
User-land library for Extensible Virtual Display Interface Kernel module

%prep
%setup -q -c evdi-b0b2c80eb63f9b858b71afa772135f434aea192a

%build
pushd evdi-b0b2c80eb63f9b858b71afa772135f434aea192a
CFLAGS="$RPM_OPT_FLAGS" %{make_build} -C library

%install
# Library
pushd evdi-b0b2c80eb63f9b858b71afa772135f434aea192a
LIBDIR=%{_libdir} %{make_install} -C library


%changelog
* Sat Jul 25 2021 ffgiff <ffgiff@gmail.com> 1.9.1-2
- Use latest devel commit to support 5.13 and 5.14
* Sat May 01 2021 ffgiff <ffgiff@gmail.com> 1.9.1-1
- First version
