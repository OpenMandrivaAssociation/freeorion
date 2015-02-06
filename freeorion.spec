%define _enable_debug_packages %{nil}
%define debug_package %{nil}

%define oname FreeOrion

Summary:	Turn-based space empire and galactic conquest
Name:		freeorion
Version:	0.4.3
Release:	2
License:	GPLv2+
Group:		Games/Strategy
Url:		http://www.freeorion.org
# From SVN, rev 6318
Source0:	%{oname}-%{version}.tar.bz2
Source1:	%{name}.png
Requires:	%{name}-data = %{version}
Requires:	ogre
BuildRequires:	cmake
BuildRequires:	boost-devel
BuildRequires:	jpeg-devel
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

%description
FreeOrion is a free, open source, turn-based space empire and galactic conquest
(4X) computer game being designed and built by the FreeOrion project. FreeOrion
is inspired by the tradition of the Master of Orion games, but is not a clone
or remake of that series or any other game.

%files
%doc changelog.txt
%{_iconsdir}/%{name}.png
%{_gamesbindir}/freeorion*
%{_gamesdatadir}/freeorion/ogre_plugins.cfg
%{_datadir}/applications/mandriva-freeorion.desktop

#----------------------------------------------------------------------------

%package data
Summary:	FreeOrion game data files
Group:		Games/Strategy
BuildArch:	noarch
License:	CC-BY-SA

%description data
Data files for FreeOrion game

%files data
%{_gamesdatadir}/freeorion
%exclude %{_gamesdatadir}/freeorion/ogre_plugins.cfg

#----------------------------------------------------------------------------

%prep
%setup -q -n %{oname}-%{version}
#patch0 -p1
sed -e "s:PluginFolder=.*:PluginFolder=$(pkg-config --variable=plugindir OGRE):" -i ogre_plugins.cfg.in

%build
# System resource usage is extremely high so disable extra flags and parallel build
%global optflags -O2
%cmake \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DBUILD_DEBUG:BOON=ON \
	-DUSE_STATIC_LIBS:BOOL=ON \
	-DBUILD_SHARED_LIBS:BOOL=OFF
make VERBOSE=1

%install
install -d -m 755 %{buildroot}%{_gamesbindir}
install -m 755 build/freeorion %{buildroot}%{_gamesbindir}/freeorion.real
install -m 755 build/freeoriond %{buildroot}%{_gamesbindir}/freeoriond
install -m 755 build/freeorionca %{buildroot}%{_gamesbindir}/freeorionca

cat > %{buildroot}%{_gamesbindir}/freeorion <<EOF
#!/bin/sh
cd %{_gamesdatadir}/%{name}
%{_gamesbindir}/freeorion.real
EOF
chmod +x %{buildroot}%{_gamesbindir}/freeorion

install -d -m 755 %{buildroot}%{_gamesdatadir}/%{name}
cp -ar default %{buildroot}%{_gamesdatadir}/%{name}

install -d -m 755 %{buildroot}%{_iconsdir}
install -m 644 %{SOURCE1} %{buildroot}%{_iconsdir}

install -d -m 755 %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Type=Application
Encoding=UTF-8
Name=FreeOrion
Comment=Turn-based space empire and galactic conquest
Exec=%{_gamesbindir}/%{name}
Path=%{_gamesbindir}
Icon=%{name}
Terminal=false
Categories=Game;StrategyGame;
EOF

install -m 644 ogre_plugins.cfg.in %{buildroot}%{_gamesdatadir}/%{name}/ogre_plugins.cfg

