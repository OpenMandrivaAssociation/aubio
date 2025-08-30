%global	optflags %{optflags} -Wno-incompatible-function-pointer-types
%global	_disable_ld_no_undefined 1

%define	major 5
%define	libname %mklibname %{name} %{major}
%define	develname %mklibname %{name} -d

Summary:	A library for audio labelling
Name:	aubio
Version:	0.4.9
Release:	7
License:	GPLv2+
Group:	Sound
Url:		https://aubio.org/
Source0:	https://aubio.org/pub/%{name}-%{version}.tar.bz2
Patch0:	aubio-0.4.9-ffmpeg-5.0.patch
Patch1:	aubio-python39.patch
Patch2:	https://github.com/aubio/aubio/commit/cdfe9cef2dcc3edf7d05ca2e9c2dbbf8dea21f1c.patch
Patch3:	aubio-0.4.9-ffmpeg-7.0.patch
Patch4:	aubio-0.4.9-fix-python-shebangs.patch
BuildRequires:	docbook-to-man
BuildRequires:	doxygen
BuildRequires:	swig
BuildRequires:	txt2man
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libavdevice)
BuildRequires:	pkgconfig(libavformat)
BuildRequires:	pkgconfig(libavutil)
BuildRequires:	pkgconfig(liblash)
BuildRequires:	pkgconfig(pd)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	python3dist(numpy)
BuildRequires:python3dist(setuptools)
BuildRequires:	python3dist(sphinx)
Requires:	%{libname} = %{version}-%{release}

%description
A library for audio labelling. Its features include segmenting a sound file
before each of its attacks, performing pitch detection, tapping the beat and
producing midi streams from live audio. The name aubio comes from 'audio'
with a typo:  several transcription errors are likely to be found in the
results too.

%files
%doc %{_docdir}/libaubio-doc
%{_bindir}/aubio*
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
%autosetup -p1


%build
%set_build_flags
./waf configure --prefix=%{_prefix} --libdir=%{_libdir}
./waf build -v

# For the python bindings
%py_build


%install
./waf install --destdir=%{buildroot}

# For the python bindings
%py_install

# Fix perms
chmod +x %{buildroot}%{py_platsitedir}/%{name}/{__init__,cmd,cut}.py

# We don't want these
rm %{buildroot}/%{_libdir}/libaubio.a
#find %%{buildroot} -name '*.la' -delete
rm -f %{buildroot}%{_docdir}/libaubio-doc/manual/.buildinfo
