%define		product	pycharm
%include	/usr/lib/rpm/macros.java
Summary:	Python IDE for Professional Developers
Name:		%{product}-community
Version:	5.0.3
Release:	0.2
# TODO: figure out what's the licensing and redistribution
License:	?
Group:		Development/Tools
Source0:	https://download.jetbrains.com/python/%{name}-%{version}.tar.gz
# NoSource0-md5:	9a62285ee71fdc00a928e131e4d55839
NoSource:	0
#Source1:	%{product}.desktop
#Source2:	%{name}.py
Patch0:		pld.patch
URL:		https://www.jetbrains.com/pycharm/
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	unzip
Requires:	desktop-file-utils
Requires:	jre-X11 >= 1.7
Requires:	which
Suggests:	cvs
Suggests:	git-core
Suggests:	java-jdbc-mysql
Suggests:	subversion
Conflicts:	java-jdbc-mysql < 5.1.22
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# don't strip fsnotifier, it's size is checked for "outdated binary"
# https://bugs.archlinux.org/task/34703
# http://git.jetbrains.org/?p=idea/community.git;a=blob;f=platform/platform-impl/src/com/intellij/openapi/vfs/impl/local/FileWatcher.java;h=004311b96a35df1ffc2c87baba78a8b2a8809f7d;hb=376b939fd6d6ec4c12191a5f90503d9d62c501da#l173
%define		_noautostrip	.*/fsnotifier.*

# use /usr/lib, 64bit files do not conflict with 32bit files (64 suffix)
# this allows to install both arch files and to use 32bit jdk on 64bit os
%define		_appdir		%{_prefix}/lib/%{name}

%description
PyCharm is an Integrated Development Environment (IDE) used for
programming in Python.

It provides code analysis, a graphical debugger, an integrated unit
tester, integration with version control systems (VCSes), and supports
web development with Django.

%prep
%setup -q

# keep only single arch files (don't want to pull 32bit deps by default),
# if you want to mix, install rpm from both arch
%ifarch %{ix86}
rm bin/fsnotifier64
#rm bin/libyjpagent-linux64.so
rm bin/%{product}64.vmoptions
rm -r lib/libpty/linux/x86_64
%endif
%ifarch %{x8664}
rm bin/fsnotifier
#rm bin/libyjpagent-linux.so
rm bin/%{product}.vmoptions
rm -r lib/libpty/linux/x86
%endif
rm -r lib/libpty/{macosx,win}
rm bin/fsnotifier-arm
%patch0 -p1
chmod a+rx bin/fsnotifier* lib/libpty/linux/*/libpty.so
mv bin/%{product}.png .

# hopefully not needed
rm -rv lib/src

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_bindir},%{_pixmapsdir},%{_desktopdir}}
cp -l build.txt $RPM_BUILD_ROOT/cp-test && l=l && rm -f $RPM_BUILD_ROOT/cp-test
cp -a$l bin help helpers lib license plugins $RPM_BUILD_ROOT%{_appdir}
ln -s %{_pixmapsdir}/%{product}.png $RPM_BUILD_ROOT%{_appdir}/bin/%{product}.png
cp -p %{product}.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{product}.png
#cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
#install -p %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/%{name}
ln -s %{_appdir}/bin/%{product}.sh $RPM_BUILD_ROOT%{_bindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database

%postun
%update_desktop_database

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_appdir}
%{_appdir}/help
%{_appdir}/plugins
%{_appdir}/helpers
%doc %{_appdir}/license
%dir %{_appdir}/bin
%{_appdir}/bin/%{product}*.vmoptions
%{_appdir}/bin/%{product}.png
%{_appdir}/bin/idea.properties
%{_appdir}/bin/log.xml
%attr(755,root,root) %{_appdir}/bin/%{product}.sh
%attr(755,root,root) %{_appdir}/bin/inspect.sh
%attr(755,root,root) %{_appdir}/bin/fsnotifier*
%dir %{_appdir}/lib
%{_appdir}/lib/*.jar
%dir %{_appdir}/lib/ext
%{_appdir}/lib/ext/*.jar
%dir %{_appdir}/lib/libpty
%dir %{_appdir}/lib/libpty/linux
%dir %{_appdir}/lib/libpty/linux/x86*
%attr(755,root,root) %{_appdir}/lib/libpty/linux/x86*/libpty.so
#%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{product}.png
