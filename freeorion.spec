%define oname FreeOrion
%define pre 20120910

Name:		freeorion
Version:	0.4.2
Release:	0.pre%{pre}.1
Summary:	Turn-based space empire and galactic conquest
License:	GPLv2
Group:		Games/Strategy
URL:		http://www.freeorion.org
Source0:	%{oname}-%{version}_pre%{pre}.tar.bz2
Source1:	%{name}.png
Requires:	%{name}-data = %{version}
Requires:	ogre
BuildRequires:	cmake
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(bullet)
BuildRequires:	pkgconfig(freealut)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(GiGi)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(OGRE)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(vorbis)

%description
FreeOrion is a free, open source, turn-based space empire and galactic conquest
(4X) computer game being designed and built by the FreeOrion project. FreeOrion
is inspired by the tradition of the Master of Orion games, but is not a clone
or remake of that series or any other game.

%package data
Summary:	FreeOrion game data files
Group:		Games/Strategy
BuildArch:	noarch
License:	CC-BY-SA

%description data
Data files for FreeOrion game

%prep
%setup -q -n %{oname}-%{version}_pre%{pre}
sed -e "s:PluginFolder=.:PluginFolder=$(pkg-config --variable=plugindir OGRE):" -i ogre_plugins.cfg

%build
# System resource usage is extremely high so disable extra flags and parallel build
%global optflags -O2
%cmake -DBUILD_DEBUG:BOON=ON
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

install -m 644 ogre_plugins.cfg %{buildroot}%{_gamesdatadir}/%{name}

%files
%doc changelog.txt
%{_iconsdir}/%{name}.png
%{_gamesbindir}/freeorion*
%{_gamesdatadir}/freeorion/ogre_plugins.cfg
%{_datadir}/applications/mandriva-freeorion.desktop

%files data
%{_gamesdatadir}/freeorion
%exclude %{_gamesdatadir}/freeorion/ogre_plugins.cfg

