#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	Library to work with PDF files
Summary(pl.UTF-8):	Biblioteka do obsługi PDF-ów
Name:		podofo
Version:	0.10.1
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://github.com/podofo/podofo/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a609bd974b8907d7f23f4b2eb8e22bc9
URL:		https://github.com/podofo/podofo
# for examples only, with -DWANT_BOOST=ON
#BuildRequires:	boost-devel
BuildRequires:	cmake >= 3.16
BuildRequires:	cppunit-devel
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel
BuildRequires:	libidn-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel >= 6:8.1
BuildRequires:	libtiff-devel
BuildRequires:	libunistring-devel
BuildRequires:	lua51-devel
BuildRequires:	openssl-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	texlive-pdftex
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
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:8.1
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
Group:		Applications/Publishing
Requires:	%{name} = %{version}-%{release}

%description progs
PoDoFo tools (currently not supported by upstream).

%description progs -l pl.UTF-8
Programy narzędziowe PoDoFo (obecnie bez wsparcia ze strony projektu).

%package examples
Summary:	PoDoFo examples
Summary(pl.UTF-8):	Przykłady do PoDoFo
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
	-DPODOFO_BUILD_TOOLS=ON

%{__make} -C build

%if %{with apidocs}
doxygen
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_examplesdir}/%{name}-%{version},%{_libdir}/cmake/%{name},%{_mandir}/man1}

cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

%{__mv} $RPM_BUILD_ROOT%{_datadir}/%{name}/*.cmake $RPM_BUILD_ROOT%{_libdir}/cmake/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS.md CHANGELOG.md CODING-STYLE.md README.md TODO.md
%attr(755,root,root) %{_libdir}/libpodofo.so.*.*.*
%ghost %attr(755,root,root) %{_libdir}/libpodofo.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpodofo.so
%{_includedir}/podofo
%{_pkgconfigdir}/libpodofo.pc
%{_libdir}/cmake/%{name}

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html
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
