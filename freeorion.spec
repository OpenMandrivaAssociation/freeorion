%define version 0.3.13
%define revision 3383
%define release %mkrel 0.svn%{revision}.1 
%define libname %mklibname %name 0 


Summary:	Turn-based space empire and galactic conquest game (4X)
Name:		freeorion
Version:	%{version}
Release:	%{release}
Source0:	%{name}-%{version}-0.svn%{revision}.tar.lzma
Source1:	%{name}.png
Patch0:		freeorion-0.3.13-version-fix.patch
Patch1:		freeorion-0.3.13-ogre-plugin-fix.patch
License:	GPL & CC-BY-SA
Group:		Games/Strategy
URL:		http://www.freeorion.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}

Requires:	python graphviz gigi ogre 
Requires:	%{name}-data = %{version}-%{release}
BuildRequires:	scons 
BuildRequires:	python-devel 
BuildRequires:	freetype2-devel 
BuildRequires:	libvorbis-devel
BuildRequires:	SDL-devel 
BuildRequires:	graphviz-devel 
BuildRequires:	openal-devel 
BuildRequires:	libogg-devel
BuildRequires:	log4cpp-devel
BuildRequires:	freealut-devel
BuildRequires:	gigi-devel
BuildRequires:	boost-devel >= 1.37.0
BuildRequires:	ogre-devel >= 1.4.6
BuildRequires:	bullet-devel
##### Description #####
%description
FreeOrion is a free, open source, turn-based space empire and galactic 
conquest (4X) computer game being designed and built by the FreeOrion 
project. FreeOrion is inspired by the tradition of the Master of Orion 
games, but is not a clone or remake of that series or any other game. 

PLEASE be aware that this is work in progress and lot of important game
parts don't work/aren't implemented yet, and that whole game should be 
considered pre-alpha stage at this time and that includes battles tech
demo! Don't be mad at us, we warned you.

##### Subpackages ... game + data #####
%package -n     %{name}-data
Summary:	FreeOrion game data files
Group:		Games/Strategy
BuildArch:	noarch
%description -n %{name}-data
Data files for FreeOrion game

##### Prep, Setup, Build, Install #####

%prep
%setup -q -n FreeOrion
%patch0 -p0
%patch1 -p0

%configure_scons bindir=%{_gamesbindir} datadir=%{_gamesdatadir}/freeorion \
with_gg=%{_libdir} --install=%{buildroot} 

%build

%scons bindir=%{_gamesbindir} datadir=%{_gamesdatadir}/freeorion \
--install=%{buildroot} boost_lib_suffix=-mt


%install

rm -rf %{buildroot}
%scons_install --install=%{buildroot}

mkdir -p %{buildroot}/%{_iconsdir}
cp %{SOURCE1} %{buildroot}/%{_iconsdir}
cp ogre_plugins.cfg %{buildroot}/%{_gamesbindir}/
echo PluginFolder=%{_libdir}/OGRE >> %{buildroot}/%{_gamesbindir}/ogre_plugins.cfg

mkdir -p %{buildroot}%{_datadir}/applications

cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=FreeOrion
Comment=Space empire and galactic conquest (4X) game
Exec=%{_gamesbindir}/%{name}
Path=%{_gamesbindir}
Icon=%{name}.png
Terminal=false
Type=Application
Categories=Game;StrategyGame;
EOF

##### Clean #####
%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%endif

##### Files #####

%files
%defattr(-,root,root)
%{_iconsdir}/%{name}.png
%{_gamesbindir}/freeorion*
%{_gamesbindir}/ogre_plugins.cfg
%{_datadir}/applications/mandriva-freeorion.desktop
%doc RELEASE-NOTES-V03.txt 

%files -n %{name}-data
%defattr(-,root,root)
%dir %{_gamesdatadir}/freeorion
%{_gamesdatadir}/%{name}/*
