#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	Library to work with PDF files
Summary(pl.UTF-8):	Biblioteka do obsługi PDF-ów
Name:		podofo
Version:	0.10.1
Release:	1
License:	LGPL
Group:		Libraries
Source0:	https://github.com/podofo/podofo/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a609bd974b8907d7f23f4b2eb8e22bc9
URL:		https://github.com/podofo/podofo
# for examples only, with -DWANT_BOOST=ON
#BuildRequires:	boost-devel
BuildRequires:	cmake >= 2.6
BuildRequires:	cppunit-devel
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel
BuildRequires:	libidn-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libunistring-devel
BuildRequires:	lua51-devel
BuildRequires:	openssl-devel
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
Requires:	libstdc++-devel

%description devel
Header files for PoDoFo library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki PoDoFo.

%package static
Summary:	Static PoDoFo library
Summary(pl.UTF-8):	Statyczna biblioteka FOO
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static PoDoFo library.

%description static -l pl.UTF-8
Statyczna biblioteka PoDoFo.

%package apidocs
Summary:	PoDoFo API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki PoDoFo
Group:		Documentation
BuildArch:	noarch

%description apidocs
API and internal documentation for PoDoFo library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki PoDoFo.

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
install -d build
cd build
%cmake .. \
	-DINSTALL_LIBDATA_DIR=%{_libdir} \
%if "%{_lib}" == "lib64"
	-DWANT_LIB64=TRUE
%endif

%{__make}
cd ..

%if %{with apidocs}
doxygen
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_examplesdir}/%{name}-%{version},%{_libdir}/cmake/%{name}}

cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_datadir}/%{name}/*.cmake $RPM_BUILD_ROOT%{_libdir}/cmake/%{name}/

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

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
