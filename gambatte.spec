%define		subver		wip2v2

Name:		gambatte
Version:	0.5.0
Release:	%mkrel 0.%{subver}.2
Summary:	Game Boy Color emulator with Qt and SDL frontends
License:	GPLv2
Group:		Emulators
Source0:	%{name}_src-%{version}-%{subver}.tar.gz
Source1:	%{name}.png
Patch0:		gambatte_src-0.5.0-wip2v2-add-missing-linkage.patch
BuildRequires:	scons
BuildRequires:	qt4-devel
BuildRequires:	SDL-devel
BuildRequires:	libxv-devel
BuildRequires:	libxrandr-devel
BuildRequires:	imagemagick

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
%patch0 -p1 -b .linkage~

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
%__rm -rf %{buildroot}
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

%clean
%__rm -rf %{buildroot}

%files
%doc README changelog COPYING
%{_bindir}/gambatte_*
%{_mandir}/man6/*
%{_iconsdir}/*.png
%{_miconsdir}/*.png
%{_liconsdir}/*.png
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop



%changelog
* Fri Mar 09 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.5.0-0.wip2v2.2mdv2012.0
+ Revision: 783588
- add missing linkage (P0)

  + Andrey Bondrov <abondrov@mandriva.org>
    - New version 0.5.0-wip2v2

* Wed Sep 21 2011 Andrey Bondrov <abondrov@mandriva.org> 0.5.0-0.wip1.1
+ Revision: 700725
- imported package gambatte


* Wed Sep 21 2011 Andrey Bondrov <bondrov@math.dvgu.ru> 0.5.0-0.wip1.1mdv2010.2
- Initial build for Mandriva
