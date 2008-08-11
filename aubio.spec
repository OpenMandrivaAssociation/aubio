%define major 2
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	A library for audio labelling
Name:		aubio
Version:	0.3.2
Release:	%mkrel 2
License:	GPLv2+
Group:		Sound
Url:		http://aubio.org/
Source0:	http://aubio.org/pub/aubio-0.3.2.tar.bz2
BuildRequires:	fftw3-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	libalsa-devel
BuildRequires:	swig
BuildRequires:	lash-devel
BuildRequires:	pd-devel
%py_requires -d
Requires:	%{libname} = %{version}-%{release}
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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

%description -n python-%{name}
Python bindings for %{name}.

%prep
%setup -q %{name}-%{version}

%build
%configure2_5x

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS README THANKS TODO
%{_bindir}/*
%{_datadir}/sounds/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/*.*a
%{_libdir}/pkgconfig/*.pc

%files -n python-%{name}
%defattr(-,root,root)
%{python_sitelib}/*
