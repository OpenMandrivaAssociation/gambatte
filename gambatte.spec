%define		name		gambatte
%define		version		0.5.0
%define		subver		wip1

Name:		%{name}
License:	GPLv2
Group:		Emulators
Version:	%{version}
Release:	%mkrel 0.%{subver}.1
Summary:	Game Boy Color emulator with Qt and SDL frontends
Source:		%{name}_src-%{version}-%{subver}.tar.gz
Source1:	%{name}.png
BuildRequires:	scons
BuildRequires:	qt4-devel
BuildRequires:	SDL-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
Gambatte is an accuracy-focused, open-source, cross-platform
Game Boy / Game Boy Color emulator written in C++. It is based on hundreds of
corner case hardware tests, as well as previous documentation and reverse
engineering efforts.

The core emulation code is contained in a separate library back-end
(libgambatte) written in platform-independent C++. There is currently a GUI
front-end (gambatte_qt) using Trolltech's Qt4 toolkit, and a simple 
command-line SDL front-end (gambatte_sdl).

%prep
%setup -q -n %{name}_src-%{version}-%{subver}

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
cd libgambatte
%scons
cd ../gambatte_qt
%qmake_qt4
%make
cd ../gambatte_sdl
%scons

%install
%__install -d -m 755 %{buildroot}%{_bindir}
%__install -m 755 gambatte_qt/bin/gambatte_qt %{buildroot}%{_bindir}
%__install -m 755 gambatte_sdl/gambatte_sdl %{buildroot}%{_bindir}
%__install -d -m 755 %{buildroot}%{_mandir}/man6
%__install -m 644 gambatte_qt/man/* %{buildroot}%{_mandir}/man6/
%__install -m 644 gambatte_sdl/man/* %{buildroot}%{_mandir}/man6/

# install menu entries
%__mkdir_p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Gambatte
Comment=Game Boy Color Emulator
Exec=%{name}_qt
Icon=%{name}
Type=Application
Terminal=false
Categories=X-MandrivaLinux-MoreApplications-Emulators;Emulator;
EOF

#Icons
%__mkdir_p %{buildroot}%{_datadir}/pixmaps/
%__install -c -m 644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/%{name}.png

%__mkdir_p %{buildroot}/%{_miconsdir} \
         %{buildroot}/%{_liconsdir} \
         %{buildroot}/%{_iconsdir}

%__install -m 644 %{SOURCE1} %{buildroot}/%{_miconsdir}/%{name}.png
%__install -m 644 %{SOURCE1} %{buildroot}/%{_iconsdir}/%{name}.png
%__install -m 644 %{SOURCE1} %{buildroot}/%{_liconsdir}/%{name}.png
convert %{buildroot}%{_miconsdir}/%{name}.png -resize 16x16 %{buildroot}%{_miconsdir}/%{name}.png
convert %{buildroot}%{_iconsdir}/%{name}.png -resize 32x32 %{buildroot}%{_iconsdir}/%{name}.png

%files
%defattr(-,root,root)
%doc README changelog COPYING
%{_bindir}/gambatte_*
%{_mandir}/man6/*
%{_iconsdir}/*.png
%{_miconsdir}/*.png
%{_liconsdir}/*.png
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop

