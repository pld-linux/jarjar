# TODO
# - make maven2 plugin package
Summary:	Jar Jar Links utility
Summary(pl.UTF-8):	Narzędzie Jar Jar Links
Name:		jarjar
Version:	0.9
Release:	0.2
License:	GPL
Group:		Development/Languages/Java
Source0:	http://dl.sourceforge.net/jarjar/%{name}-src-%{version}.zip
# Source0-md5:	61825e60d0466e328c7d24a6cef2c643
URL:		http://tonicsystems.com/products/jarjar/
BuildRequires:	ant >= 0:1.6
BuildRequires:	ant-junit >= 0:1.6
BuildRequires:	asm2
BuildRequires:	gnu.regexp
BuildRequires:	jpackage-utils
BuildRequires:	junit
BuildRequires:	unzip
BuildRequires:	maven = 2.0.7
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	asm2
Requires:	gnu.regexp
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Jar Jar Links is a utility that makes it easy to repackage Java
libraries and embed them into your own distribution. This is useful
for two reasons: You can easily ship a single jar file with no
external dependencies. You can avoid problems where your library
depends on a specific version of a library, which may conflict with
the dependencies of another library.

%description -l pl.UTF-8
Jar Jar Links to narzędzie ułatwiające repakietowanie bibliotek Javy
i osadzanie ich we własnych pakietach. Jest to przydatne w dwóch
przypadkach:
- aby stworzyć pojedynczy plik jar bez zewnętrznych zależności,
- zby zapobiec problemom kiedy biblioteka zależy od konkretnej wersji
  innej biblioteki, ale ta może być w konflikcie z zależnościami innej
  biblioteki.

%package javadoc
Summary:	Javadoc for Jar Jar Links
Summary(pl.UTF-8):	Dokumentacja Javadoc do pakietu Jar Jar Links
Group:		Documentation

%description javadoc
Documentation for Jar Jar Links.

%description javadoc -l pl.UTF-8
Dokumentacja Javadoc do pakietu Jar Jar Links.

%prep
%setup -q
find -name '*.jar' | xargs rm -vf

%build
cd lib
ln -sf $(build-classpath gnu-regexp)
ln -sf %{_javadir}/asm2.jar asm.jar
ln -sf %{_javadir}/asm2-commons.jar asm-commons.jar
ln -sf %{_javadir}/asm2-util.jar asm-util.jar
ln -sf %{_datadir}/maven/lib/maven-core-2.0.7-uber.jar maven-plugin-api.jar
cd -
export CLASSPATH=$(build-classpath ant)
%ant jar jar-util javadoc mojo test

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

install dist/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
install dist/%{name}-util-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-util-%{version}.jar
ln -s %{name}-util-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-util.jar

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}-util-%{version}.jar
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-util.jar

%if 0
%files maven2-plugin
%defattr(644,root,root,755)
%{_javadir}/%{name}-maven2-plugin-%{version}.jar
%{_javadir}/%{name}-maven2-plugin.jar
%endif

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
