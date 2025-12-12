#define _enable_debug_packages %{nil}
#define debug_package %{nil}
%define _empty_manifest_terminate_build 0

# Workaround duplicate symbols
%global optflags %{optflags} -fcommon

%define oname FreeOrion
%define _disable_ld_no_undefined %nil

Summary:	Turn-based space empire and galactic conquest
Name:		freeorion
Version:	0.5.1.1
Release:	3
License:	GPLv2+
Group:		Games/Strategy
Url:		https://www.freeorion.org
Source0:	https://github.com/freeorion/freeorion/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:		https://patch-diff.githubusercontent.com/raw/freeorion/freeorion/pull/5287.patch

Requires:	%{name}-data = %{version}
Requires:	ogre

BuildSystem:	cmake
BuildOption:	-DRELEASE_COMPILE_FLAGS="%{optflags}"
BuildOption:	-DBUILD_SHARED_LIBS=OFF
BuildRequires:	boost-devel
BuildRequires:  boost-python-devel
BuildRequires:	jpeg-devel
BuildRequires:  pkgconfig(python3)
BuildRequires:	pkgconfig(bullet)
BuildRequires:	pkgconfig(freealut)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(OGRE)
BuildRequires:	pkgconfig(OIS)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(libunwind-llvm)

%description
FreeOrion is a free, open source, turn-based space empire and galactic conquest
(4X) computer game being designed and built by the FreeOrion project. FreeOrion
is inspired by the tradition of the Master of Orion games, but is not a clone
or remake of that series or any other game.

%files
%{_datadir}/icons/*/*/*/org.freeorion.FreeOrion.png
%{_bindir}/freeorion*
%{_datadir}/applications/org.freeorion.FreeOrion.desktop
%{_datadir}/metainfo/org.freeorion.FreeOrion.metainfo.xml

#----------------------------------------------------------------------------

%package data
Summary:	FreeOrion game data files
Group:		Games/Strategy
BuildArch:	noarch
License:	CC-BY-SA

%description data
Data files for FreeOrion game

%files data
%{_datadir}/freeorion

#----------------------------------------------------------------------------

%conf -p
sed -e "s/-O3//" -i CMakeLists.txt
# System resource usage is extremely high so disable extra flags and parallel build
#global optflags -O2
# (but the build boxes can handle it...)
export LDFLAGS="%{ldflags} -Wl,--as-needed"

%install -a
install -d -m 755 %{buildroot}%{_bindir}
install -m 755 _OMV_rpm_build/freeorion %{buildroot}%{_bindir}/freeorion.real
install -m 755 _OMV_rpm_build/freeoriond %{buildroot}%{_bindir}/freeoriond
install -m 755 _OMV_rpm_build/freeorionca %{buildroot}%{_bindir}/freeorionca
#install -m755 _OMV_rpm_build/*.so %{buildroot}%{_libdir}/%{name}/

# No point in shipping the static libs
rm %{buildroot}%{_libdir}/*.a %{buildroot}%{_libdir}/%{name}/*.a

cat > %{buildroot}%{_bindir}/freeorion <<EOF
#!/bin/sh
cd %{_datadir}/%{name}
%{_bindir}/freeorion.real
EOF
chmod +x %{buildroot}%{_bindir}/freeorion

install -d -m 755 %{buildroot}%{_datadir}/%{name}
cp -ar default %{buildroot}%{_datadir}/%{name}
