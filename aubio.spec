%global optflags %{optflags} -Wno-incompatible-function-pointer-types

%define major 5
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	A library for audio labelling
Name:		aubio
Version:	0.4.9
Release:	4
License:	GPLv2+
Group:		Sound
Url:		https://aubio.org/
Source0:	http://aubio.org/pub/%{name}-%{version}.tar.bz2
Patch0:		aubio-0.4.9-ffmpeg-5.0.patch
Patch1:		%{name}-python39.patch
Patch2:		https://github.com/aubio/aubio/commit/cdfe9cef2dcc3edf7d05ca2e9c2dbbf8dea21f1c.patch
Patch3:		aubio-0.4.9-ffmpeg-7.0.patch

BuildRequires:	doxygen
BuildRequires:	docbook-to-man
BuildRequires:  txt2man
BuildRequires:	swig
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(lash-1.0)
BuildRequires:  pkgconfig(jack)
BuildRequires:	pkgconfig(pd)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavdevice)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
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
BuildRequires: pkgconfig(python)
BuildRequires: python3dist(sphinx)
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

# we don't want these
find %{buildroot} -name '*.la' -delete
rm %{buildroot}/%{_libdir}/libaubio.a

%files
%doc %{_docdir}/libaubio-doc
%{_bindir}/*
%{_mandir}/man1/aubio*

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files -n python-%{name}
%{python_sitearch}/*
