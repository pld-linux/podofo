#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	Library to work with PDF files
Summary(pl.UTF-8):	Biblioteka do obsługi PDF-ów
Name:		podofo
Version:	0.7.0
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/podofo/%{name}-%{version}.tar.gz
# Source0-md5:	b9623fd9279fca49f7cdd5c1fed182b1
URL:		http://podofo.sourceforge.net/
BuildRequires:	cmake
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	openssl-devel
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

%package devel
Summary:	Header files for PoDoFo library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki PodoFo
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

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

%description apidocs
API and internal documentation for PoDoFo library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki PoDoFo.

%package progs
Summary:	PoDoFo tools
Summary(pl.UTF-8):	Programy narzędziowe PodoFo
Group:		Applications
Requires:	%{name} = %{version}-%{release}

%description progs
Header files for PoDoFo library.

%description progs -l pl.UTF-8
Pliki nagłówkowe biblioteki PoDoFo.

%package examples
Summary:	PoDoFo examples
Summary(pl.UTF-8):	Przykłady do PoDoFo
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}

%description examples
PoDoFo examples.

%description examples -l pl.UTF-8
Programy przykładowe do PoDoFo.

%prep
%setup -q

%build
mkdir build
cd build
%cmake .. \
        -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
        -DCMAKE_VERBOSE_MAKEFILE=ON \
        -DPODOFO_BUILD_SHARED:BOOL=TRUE \
        -DPODOFO_BUILD_STATIC:BOOL=TRUE \
        -DINSTALL_LIB_DIR=%{_lib} \
        -DINSTALL_LIBDATA_DIR=%{_libdir} \
%if "%{_lib}" == "lib64"
	-DWANT_LIB64=TRUE \
%endif
        %{?debug:-DCMAKE_BUILD_TYPE="Debug"}
%{__make}
cd ..

%if %{with apidocs}
doxygen
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

cd build
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc FAQ.html README.html
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%{_libdir}/lib*.so
%{_includedir}/podofo

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html
%endif

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
