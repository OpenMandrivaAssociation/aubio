%define major 5
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	A library for audio labelling
Name:		aubio
Version:	0.4.9
Release:	1
License:	GPLv2+
Group:		Sound
Url:		http://aubio.org/
Source0:	http://aubio.org/pub/%{name}-%{version}.tar.bz2
BuildRequires:	swig
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(lash-1.0)
BuildRequires:	pkgconfig(pd)
BuildRequires:	docbook-to-man
Requires:	%{libname} = %{version}-%{release}

%description
A library for audio labelling. Its features include segmenting 
a sound file before each of its attacks, performing pitch 
detection, tapping the beat and producing midi streams from 
live audio. The name aubio comes from 'audio' with a typo: 
several transcription errors are likely to be found in the 
results too.

%package -n %{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n %{libname}
Main library for %{name}.

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{develname}
Development files and headers for %{name}.

%package -n python-%{name}
Summary:	Python bindings for %{name}
Group:		Development/Python
Requires:	%{libname} = %{version}-%{release}
BuildRequires: pkgconfig(python3)
BuildRequires: python-setuptools
BuildRequires: python-numpy
BuildRequires: python-numpy-devel

%description -n python-%{name}
Python bindings for %{name}.

%prep
%setup -q
%autopatch -p1

%build
%define _disable_ld_no_undefined 1
%set_build_flags
./waf configure --prefix=%{_prefix} \
    --libdir=%{_libdir}
./waf build -v

# python3
%py_build

%install
./waf install --destdir=%{buildroot}

# python3
%py_install

%files
%{_bindir}/*

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files -n python-%{name}
%{python_sitearch}/*
