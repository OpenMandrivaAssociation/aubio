%define major 2
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	A library for audio labelling
Name:		aubio
Version:	0.3.2
Release:	8
License:	GPLv2+
Group:		Sound
Url:		http://aubio.org/
Source0:	http://aubio.org/pub/%{name}-%{version}.tar.bz2
Patch0:		%{name}-0.3.2-format_not_a_string_literal_and_no_format_arguments.patch
Patch1:		aubio-0.3.2-fix-link.patch
Patch2:		aubio-linking.patch
Patch3:		aubio-numarray-gnuplot.patch
BuildRequires:	swig
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(lash-1.0)
BuildRequires:	pd-devel
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
BuildRequires: python-devel

%description -n python-%{name}
Python bindings for %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p1

%build
%define _disable_ld_no_undefined 1
export CPPFLAGS="%{optflags} -I%{_includedir}/pd"
%configure2_5x --disable-static

%make

%install
%makeinstall_std

%ifarch x86_64
mv -f %{buildroot}%{_prefix}/lib/pd %{buildroot}%{_libdir}/pd
%endif

%files
%doc AUTHORS README THANKS TODO
%{_bindir}/*
%{_datadir}/sounds/*
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/*.so.%{major}*
%{_libdir}/pd

%files -n %{develname}
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files -n python-%{name}
%{python_sitelib}/*

