Name:          evdi
Version:       1.9.1
Release:	1%{?dist}
Summary:       User-land library for Extensible Virtual Display Interface Kernel module
URL:           https://github.com/DisplayLink/evdi
# FIXME: since upstream tagged a bad commit, use a commit id instead of the tag
%global commit 3c9add5fa438ac18c575bfa4d39b17be0fdfe208
Source0:       %{url}/archive/%{commit}.tar.gz
#Source0:       %{url}/archive/v%{version}.tar.gz
License:       LGPLv2
BuildRequires:  libdrm-devel
Provides:	evdi-kmod-common = %{version}-%{release}
Provides:	libevdi = %{version}-%{release}

%files
%{_libdir}/libevdi.so
%{_libdir}/libevdi.so.0
%{_libdir}/libevdi.so.%{version}

%global _hardened_build 1

%description
The evdi %{version} display driver user-land library

%prep
# FIXME: since upstream tagged a bad commit, use a commit id instead of the tag
%setup -q -c evdi-%{commit}
#%setup -q -c evdi-%{version}

%build
# FIXME: since upstream tagged a bad commit, use a commit id instead of the tag
pushd evdi-%{commit}
#pushd evdi-%{version}
CFLAGS="$RPM_OPT_FLAGS" %{make_build} -C library

%install
# Library
# FIXME: since upstream tagged a bad commit, use a commit id instead of the tag
pushd evdi-%{commit}
#pushd evdi-%{version}
LIBDIR=%{_libdir} %{make_install} -C library


%changelog
* Thu Apr 08 2021 ffgiff <ffgiff@gmail.com> 1.9.1-1
- First version
