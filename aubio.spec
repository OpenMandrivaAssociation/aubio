%global	optflags %{optflags} -Wno-incompatible-function-pointer-types
%global	_disable_ld_no_undefined 1

%define	major 5
%define	libname %mklibname %{name} %{major}
%define	develname %mklibname %{name} -d
%define	gitdate	20251120

Summary:	A library for audio labelling
Name:	aubio
Version:	0.5.0
Release:	0.%{gitdate}.2
License:	GPLv2+
Group:	Sound
Url:		https://aubio.org/
# Use a git snapshot to pick up 4 years of updates
#Source0:	https://aubio.org/pub/%%{name}-%%{version}.tar.bz2
Source0:	%{name}-%{gitdate}.tar.xz
Patch0:		aubio-0.5.0-drop-alpha-from-pc-file-version.patch
Patch1:		aubio-0.5.0-fix-doc-building.patch
Patch2:		aubio-0.5.0-fix-python-shebangs.patch
BuildRequires:	docbook-to-man
BuildRequires:	doxygen
BuildRequires:	swig
BuildRequires:	txt2man
BuildRequires:	waf
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libavdevice)
BuildRequires:	pkgconfig(libavformat)
BuildRequires:	pkgconfig(libavutil)
BuildRequires:	pkgconfig(liblash)
BuildRequires:	pkgconfig(libswresample)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(pd)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(rubberband)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(vorbisenc)
BuildRequires:	python%{pyver}dist(numpy)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(sphinx)
BuildRequires:	python%{pyver}dist(wheel)
Requires:	%{libname} = %{version}-%{release}

%description
A library for audio labelling. Its features include segmenting a sound file
before each of its attacks, performing pitch detection, tapping the beat and
producing midi streams from live audio. The name aubio comes from 'audio'
with a typo:  several transcription errors are likely to be found in the
results too.

%files
%doc ChangeLog README.md
%license COPYING
%doc %{_docdir}/libaubio-doc
%{_bindir}/%{name}*
%{_mandir}/man1/%{name}*

#-----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n %{libname}
Main library for %{name}.

%files -n %{libname}
%{_libdir}/libaubio.so.%{major}*

#-----------------------------------------------------------------------------

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{develname}
Development files and headers for %{name}.

%files -n %{develname}
%{_includedir}/%{name}
%{_libdir}/libaubio.so
%{_libdir}/pkgconfig/%{name}.pc

#-----------------------------------------------------------------------------

%package -n python-%{name}
Summary:	Python bindings for %{name}
Group:		Development/Python
Requires:	%{libname} = %{version}-%{release}

%description -n python-%{name}
Python bindings for %{name}.

%files -n python-%{name}
%{py_platsitedir}/%{name}/*
%{py_platsitedir}/%{name}-%{version}-*.egg-info

#-----------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{gitdate}


%build
%set_build_flags
waf configure --prefix=%{_prefix} --libdir=%{_libdir} --enable-fftw3
%waf  -v

# For the python bindings
%py_build


%install
%waf_install

# For the python bindings
%py_install

# Fix perms
chmod +x %{buildroot}%{py_platsitedir}/%{name}/{__init__,cmd,cut}.py

# We don't want these
rm -f %{buildroot}/%{_libdir}/libaubio.a
rm -f %{buildroot}%{_docdir}/libaubio-doc/manual/.buildinfo

