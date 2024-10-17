%define subver r550

Summary:	Game Boy Color emulator with Qt and SDL frontends
Name:		gambatte
Version:	0.5.0
Release:	1.%{subver}.1
License:	GPLv2+
Group:		Emulators
Url:		https://sourceforge.net/projects/gambatte/
Source0:	%{name}_src-%{subver}.tar.gz
Source1:	%{name}.png
BuildRequires:	imagemagick
BuildRequires:	scons
BuildRequires:	qt4-devel
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xv)

%description
Gambatte is an accuracy-focused, open-source, cross-platform
Game Boy / Game Boy Color emulator written in C++. It is based on hundreds of
corner case hardware tests, as well as previous documentation and reverse
engineering efforts.

The core emulation code is contained in a separate library back-end
(libgambatte) written in platform-independent C++. There is currently a GUI
front-end (gambatte_qt) using Trolltech's Qt4 toolkit, and a simple 
command-line SDL front-end (gambatte_sdl).

%files
%doc README changelog COPYING
%{_bindir}/gambatte_*
%{_iconsdir}/*.png
%{_miconsdir}/*.png
%{_liconsdir}/*.png
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}_src-%{subver}

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
install -d -m 755 %{buildroot}%{_bindir}
install -m 755 gambatte_qt/bin/gambatte_qt %{buildroot}%{_bindir}
install -m 755 gambatte_sdl/gambatte_sdl %{buildroot}%{_bindir}

# install menu entries
mkdir -p %{buildroot}%{_datadir}/applications
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
mkdir -p %{buildroot}%{_datadir}/pixmaps/
install -c -m 644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/%{name}.png

mkdir -p %{buildroot}%{_miconsdir}
mkdir -p %{buildroot}%{_liconsdir}
mkdir -p %{buildroot}%{_iconsdir}

install -m 644 %{SOURCE1} %{buildroot}%{_miconsdir}/%{name}.png
install -m 644 %{SOURCE1} %{buildroot}%{_iconsdir}/%{name}.png
install -m 644 %{SOURCE1} %{buildroot}%{_liconsdir}/%{name}.png
convert %{buildroot}%{_miconsdir}/%{name}.png -resize 16x16 %{buildroot}%{_miconsdir}/%{name}.png
convert %{buildroot}%{_iconsdir}/%{name}.png -resize 32x32 %{buildroot}%{_iconsdir}/%{name}.png

