Name:		freeorion
Version:	0.3.16
Release:	%mkrel 1
Summary:	Turn-based space empire and galactic conquest
License:	GPLv2
Group:		Games/Strategy
URL:		http://www.freeorion.org
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}.png
#Patch0:     freeorion-0.3.15-fix-link.patch
#Patch1:     freeorion-0.3.15-fix-ogre-configuration-location.patch
#Patch2:     freeorion-0.3.15-force-data-location.patch
Requires:   %{name}-data = %{version}
Requires:   ogre
BuildRequires:	python-devel
BuildRequires:	freetype2-devel
BuildRequires:	devil-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libogg-devel
BuildRequires:	openal-devel
BuildRequires:	SDL-devel
BuildRequires:	log4cpp-devel
BuildRequires:	freealut-devel
BuildRequires:	boost-devel >= 1.37.0
BuildRequires:	ogre-devel >= 1.4.6
BuildRequires:	gigi-devel
BuildRequires:	bullet-devel
BuildRequires:	cmake
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}

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
%setup -q -n trunk/FreeOrion
# % patch0 -p 2
# % patch1 -p 2
# % patch2 -p 2

%build
export CXXFLAGS="%optflags -DBOOST_FILESYSTEM_VERSION=2"
%cmake \
    -DCMAKE_MODULE_PATH=%{_datadir}/cmake/Modules/GG
%make

%install
rm -rf %{buildroot}

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
perl -pi \
    -e 's|PluginFolder=.*|PluginFolder=%{_libdir}/OGRE|' \
    %{buildroot}%{_gamesdatadir}/%{name}/ogre_plugins.cfg


#perl -pi -e '1d;2i#!/usr/bin/python' \
#    % {buildroot} % {_gamesdatadir}/ % {name}/default/AI/AIstate.py

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc RELEASE-NOTES-V03.txt 
%{_iconsdir}/%{name}.png
%{_gamesbindir}/freeorion*
%{_gamesdatadir}/freeorion/ogre_plugins.cfg
%{_datadir}/applications/mandriva-freeorion.desktop


%files data
%defattr(-,root,root)
%{_gamesdatadir}/freeorion
%exclude %{_gamesdatadir}/freeorion/ogre_plugins.cfg
