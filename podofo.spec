# TODO:
# - system tcpspan (-DPODOFO_DEVENDOR_TCBSPAN), date (-DPODOFO_DEVENDOR_DATE)
#
# Conditional build:
%bcond_without	apidocs			# doxygen based API documentation
%bcond_with	lcms			# ICC profiles support via lcms [undocumented, cmake option missing]
%bcond_without	system_fastfloat	# system fast_floatlibrary
%bcond_without	system_fmt		# system libfmt library
%bcond_without	system_utf8cpp		# system utf8cpp library
%bcond_with	system_utf8proc		# system utf8proc library [requires utf8proc with cmake configs]

Summary:	Library to work with PDF files
Summary(pl.UTF-8):	Biblioteka do obsługi PDF-ów
Name:		podofo
Version:	1.1.1
Release:	1
License:	LGPL v2+ or MPL v2.0 (library), GPL v2+ (tools)
Group:		Libraries
#Source0Download: https://github.com/podofo/podofo/releases
Source0:	https://github.com/podofo/podofo/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	11c4478ed0c2f369fa51463d2b42d3c8
URL:		https://github.com/podofo/podofo
BuildRequires:	cmake >= 3.23
BuildRequires:	cppunit-devel
%{?with_apidocs:BuildRequires:	doxygen}
%{?with_system_fastfloat:BuildRequires:	fast_float-devel}
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel
%{?with_lcms:BuildRequires:	lcms2-devel >= 2}
%{?with_system_fmt:BuildRequires:	libfmt-devel}
BuildRequires:	libidn-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel >= 6:9
BuildRequires:	libtiff-devel
BuildRequires:	libunistring-devel
BuildRequires:	libxml2-devel >= 1:2.15.0
BuildRequires:	lua51-devel
BuildRequires:	openssl-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	texlive-pdftex
%{?with_system_utf8cpp:BuildRequires:	utf8cpp-devel}
%{?with_system_utf8proc:BuildRequires:	utf8proc-devel}
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The PoDoFo library is a free portable C++ library which includes
classes to parse a PDF file and modify its contents into memory. The
changes can be written back to disk easily. PoDoFo is designed to
avoid loading large PDF objects into memory until they are required
and can write large streams immediately to disk, so it is possible to
manipulate quite large files with it. PoDoFo uses and relies on
exceptions, so it must be built with them enabled.

%description -l pl.UTF-8
Biblioteka PoDoFo jest darmową przenośną biblioteką C++ dostarczjącą
klasy do parsowania plików PDF i modyfikowania ich w pamięci. Zmiany
mogą być ponownie łatwo zapisane na dysk. PoDoFo jest zaprojektowane w
sposób, który pozwala na unikanie ładowania dużych plików PDF do
pamięci, jeżeli nie jest to niezbędne. Pozwala również na zapisywanie
dużych strumieni natychmiast na dysk, co umożliwia manipulowanie
całkiem dużymi plikami. PoDoFo używa i zależne jest od wyjątków, więc
konieczna jest jego budowa z włączoną ich obsługą.

%package devel
Summary:	Header files for PoDoFo library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki PodoFo
License:	LGPL v2.0+ or MPL v2.0
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%{?with_system_fastfloat:Requires:	fast_float-devel}
%{?with_lcms:Requires:	lcms2-devel >= 2}
%{?with_system_fmt:Requires:	libfmt-devel}
Requires:	libstdc++-devel >= 6:9
%{?with_system_utf8cpp:Requires:	utf8cpp-devel}
%{?with_system_utf8proc:Requires:	utf8proc-devel}
Obsoletes:	podofo-static < 0.10

%description devel
Header files for PoDoFo library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki PoDoFo.

%package apidocs
Summary:	PoDoFo API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki PoDoFo
Group:		Documentation
BuildArch:	noarch

%description apidocs
API and internal documentation for PoDoFo library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki PoDoFo.

%package progs
Summary:	PoDoFo tools
Summary(pl.UTF-8):	Programy narzędziowe PoDoFo
License:	GPL v2+
Group:		Applications/Publishing
Requires:	%{name} = %{version}-%{release}

%description progs
PoDoFo tools (currently not supported by upstream).

%description progs -l pl.UTF-8
Programy narzędziowe PoDoFo (obecnie bez wsparcia ze strony projektu).

%package examples
Summary:	PoDoFo examples
Summary(pl.UTF-8):	Przykłady do PoDoFo
License:	MIT
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description examples
PoDoFo examples.

%description examples -l pl.UTF-8
Programy przykładowe do PoDoFo.

%prep
%setup -q

%build
%cmake -B build \
	-DINSTALL_LIBDATA_DIR=%{_libdir} \
	-DPODOFO_BUILD_UNSUPPORTED_TOOLS=ON \
	%{?with_system_fastfloat:-DPODOFO_DEVENDOR_FASTFLOAT=ON} \
	%{?with_system_fmt:-DPODOFO_DEVENDOR_FMT=ON} \
	%{?with_system_utf8cpp:-DPODOFO_DEVENDOR_UTF8CPP=ON} \
	%{?with_system_utf8proc:-DPODOFO_DEVENDOR_UTF8PROC=ON} \
	%{?with_lcms:-DPODOFO_WITH_LCMS2=ON}

%{__make} -C build

%if %{with apidocs}
cd build
doxygen
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_examplesdir}/%{name}-%{version},%{_libdir}/cmake/%{name},%{_mandir}/man1}

cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS.md CHANGELOG.md NOTICE README.md SECURITY.md TODO.md
%{_libdir}/libpodofo.so.*.*.*
%ghost %{_libdir}/libpodofo.so.4

%files devel
%defattr(644,root,root,755)
%doc API-MIGRATION.md
%{_libdir}/libpodofo.so
%{_includedir}/podofo
%{_pkgconfigdir}/libpodofo.pc
%{_libdir}/cmake/podofo

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doxygen/documentation/*
%endif

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/podofobox
%attr(755,root,root) %{_bindir}/podofocolor
%attr(755,root,root) %{_bindir}/podofocountpages
%attr(755,root,root) %{_bindir}/podofocrop
%attr(755,root,root) %{_bindir}/podofoencrypt
%attr(755,root,root) %{_bindir}/podofogc
%attr(755,root,root) %{_bindir}/podofoimg2pdf
%attr(755,root,root) %{_bindir}/podofoimgextract
%attr(755,root,root) %{_bindir}/podofoimpose
%attr(755,root,root) %{_bindir}/podofoincrementalupdates
%attr(755,root,root) %{_bindir}/podofomerge
%attr(755,root,root) %{_bindir}/podofonooc
%attr(755,root,root) %{_bindir}/podofopages
%attr(755,root,root) %{_bindir}/podofopdfinfo
%attr(755,root,root) %{_bindir}/podofosign
%attr(755,root,root) %{_bindir}/podofotxt2pdf
%attr(755,root,root) %{_bindir}/podofotxtextract
%attr(755,root,root) %{_bindir}/podofouncompress
%attr(755,root,root) %{_bindir}/podofoxmp
%{_mandir}/man1/podofobox.1*
%{_mandir}/man1/podofocolor.1*
%{_mandir}/man1/podofocountpages.1*
%{_mandir}/man1/podofocrop.1*
%{_mandir}/man1/podofoencrypt.1*
%{_mandir}/man1/podofogc.1*
%{_mandir}/man1/podofoimg2pdf.1*
%{_mandir}/man1/podofoimgextract.1*
%{_mandir}/man1/podofoimpose.1*
%{_mandir}/man1/podofoincrementalupdates.1*
%{_mandir}/man1/podofomerge.1*
%{_mandir}/man1/podofopages.1*
%{_mandir}/man1/podofopdfinfo.1*
%{_mandir}/man1/podofotxt2pdf.1*
%{_mandir}/man1/podofotxtextract.1*
%{_mandir}/man1/podofouncompress.1*
%{_mandir}/man1/podofoxmp.1*

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
