%global scl devtoolset-3
%scl_package %scl
%global dfcommit e90f5f98179410b7262098e4a016aa26dba598af
%global dfshortcommit %(c=%{dfcommit}; echo ${c:0:7})
%global dockerfiledir %{_datadir}/%{scl_prefix}dockerfiles

Summary: Package that installs %scl
Name: %scl_name
Version: 3.1
Release: 12%{?dist}
License: GPLv2+
Group: Applications/File
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/sclorg/rhscl-dockerfiles/archive/%{dfcommit}/rhscl-dockerfiles-%{dfshortcommit}.tar.gz

# The base package must require everything in the collection
Requires: %{scl_prefix}toolchain %{scl_prefix}ide %{scl_prefix}perftools
Obsoletes: %{name} < %{version}-%{release}

BuildRequires: scl-utils-build >= 20120927-11
BuildRequires: iso-codes

%description
This is the main package for %scl Software Collection.

%package runtime
Summary: Package that handles %scl Software Collection.
Group: Applications/File
Requires: scl-utils >= 20120927-11
Obsoletes: %{name}-runtime < %{version}-%{release}
Requires(post): libselinux policycoreutils-python
Requires(postun): libselinux policycoreutils-python
Requires(preun): libselinux policycoreutils-python

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary: Package shipping basic build configuration
Group: Applications/File
Requires: %{scl_prefix}runtime
Requires: scl-utils-build >= 20120927-11
Obsoletes: %{name}-build < %{version}-%{release}
# Java stuff has build-time requirements on these SCLs,
# which are only available for x86_64 arch
%ifarch x86_64
Requires: rh-java-common-scldevel >= 1.1-12
Requires: maven30-scldevel >= 1.1-7
%endif

%description build
Package shipping essential configuration macros to build %scl Software Collection.

%package toolchain
Summary: Package shipping basic toolchain applications
Group: Applications/File
Requires: %{scl_prefix}runtime
Requires: %{scl_prefix}gcc %{scl_prefix}gcc-c++ %{scl_prefix}gcc-gfortran
Requires: %{scl_prefix}binutils %{scl_prefix}gdb %{scl_prefix}strace
Requires: %{scl_prefix}dwz %{scl_prefix}elfutils %{scl_prefix}memstomp
Requires: %{scl_prefix}ltrace
Obsoletes: %{name}-toolchain < %{version}-%{release}

%description toolchain
Package shipping basic toolchain applications (compiler, debugger, ...)

%package ide
Summary: Package shipping Eclipse IDE
Group: Applications/File
Requires: %{scl_prefix}runtime
Requires: %{scl_prefix}eclipse-cdt
Requires: %{scl_prefix}eclipse-cdt-parsers
Requires: %{scl_prefix}eclipse-cdt-sdk
Requires: %{scl_prefix}eclipse-changelog
Requires: %{scl_prefix}eclipse-egit
Requires: %{scl_prefix}eclipse-emf
Requires: %{scl_prefix}eclipse-emf-core
Requires: %{scl_prefix}eclipse-emf-examples
Requires: %{scl_prefix}eclipse-emf-sdk
Requires: %{scl_prefix}eclipse-equinox-osgi
Requires: %{scl_prefix}eclipse-gcov
Requires: %{scl_prefix}eclipse-gef
Requires: %{scl_prefix}eclipse-gef-examples
Requires: %{scl_prefix}eclipse-gef-sdk
Requires: %{scl_prefix}eclipse-gprof
Requires: %{scl_prefix}eclipse-jdt
Requires: %{scl_prefix}eclipse-jgit
Requires: %{scl_prefix}eclipse-linuxtools
Requires: %{scl_prefix}eclipse-manpage
Requires: %{scl_prefix}eclipse-oprofile
Requires: %{scl_prefix}eclipse-pde
Requires: %{scl_prefix}eclipse-perf
Requires: %{scl_prefix}eclipse-platform
Requires: %{scl_prefix}eclipse-rcp
Requires: %{scl_prefix}eclipse-rpm-editor
Requires: %{scl_prefix}eclipse-rse
Requires: %{scl_prefix}eclipse-rse-server
Requires: %{scl_prefix}eclipse-swt
Requires: %{scl_prefix}eclipse-systemtap
Requires: %{scl_prefix}eclipse-valgrind
Requires: %{scl_prefix}eclipse-mylyn
Requires: %{scl_prefix}eclipse-mylyn-builds
Requires: %{scl_prefix}eclipse-mylyn-builds-hudson
Requires: %{scl_prefix}eclipse-mylyn-context-cdt
Requires: %{scl_prefix}eclipse-mylyn-context-java
Requires: %{scl_prefix}eclipse-mylyn-context-pde
Requires: %{scl_prefix}eclipse-mylyn-context-team
Requires: %{scl_prefix}eclipse-mylyn-docs-epub
Requires: %{scl_prefix}eclipse-mylyn-docs-htmltext
Requires: %{scl_prefix}eclipse-mylyn-docs-wikitext
Requires: %{scl_prefix}eclipse-mylyn-ide
Requires: %{scl_prefix}eclipse-mylyn-sdk
Requires: %{scl_prefix}eclipse-mylyn-tasks-bugzilla
Requires: %{scl_prefix}eclipse-mylyn-tasks-trac
Requires: %{scl_prefix}eclipse-mylyn-tasks-web
Requires: %{scl_prefix}eclipse-mylyn-versions
Requires: %{scl_prefix}eclipse-mylyn-versions-cvs
Requires: %{scl_prefix}eclipse-mylyn-versions-git
Obsoletes: %{name}-ide < %{version}-%{release}

%description ide
Package shipping Eclipse IDE

%package perftools
Summary: Package shipping performance tools
Group: Applications/File
Requires: %{scl_prefix}runtime
Requires: %{scl_prefix}oprofile %{scl_prefix}systemtap %{scl_prefix}valgrind
Requires: %{scl_prefix}dyninst
Obsoletes: %{name}-perftools < %{version}-%{release}

%description perftools
Package shipping performance tools (systemtap, oprofile)

%package dockerfiles
Summary: Package shipping Dockerfiles for Developer Toolset
Group: Applications/File

%description dockerfiles
This package provides a set of example Dockerfiles that can be used
with Red Hat Developer Toolset.  Use these examples to stand up
test environments using the Docker container engine.

%prep
%setup -c

%build
# Enable collection script
# ========================
cat <<EOF >enable
# The IDE part of this collection has a runtime dependency on
# the java-common collection, so enable it if present
if test -e /opt/rh/rh-java-common/enable ; then
  . scl_source enable rh-java-common
fi

# General environment variables
export PATH=%{_bindir}\${PATH:+:\${PATH}}
export MANPATH=%{_mandir}:\${MANPATH}
export INFOPATH=%{_infodir}\${INFOPATH:+:\${INFOPATH}}

# Needed by Java Packages Tools to locate java.conf
export JAVACONFDIRS="%{_sysconfdir}/java:\${JAVACONFDIRS:-/etc/java}"

# Required by XMvn to locate its configuration files
export XDG_CONFIG_DIRS="%{_sysconfdir}/xdg:\${XDG_CONFIG_DIRS:-/etc/xdg}"
export XDG_DATA_DIRS="%{_datadir}:\${XDG_DATA_DIRS:-/usr/local/share:/usr/share}"

export PCP_DIR=%{_scl_root}
# Some perl Ext::MakeMaker versions install things under /usr/lib/perl5
# even though the system otherwise would go to /usr/lib64/perl5.
export PERL5LIB=%{_scl_root}/%{perl_vendorarch}:%{_scl_root}/usr/lib/perl5:%{_scl_root}/%{perl_vendorlib}\${PERL5LIB:+:\${PERL5LIB}}
# bz847911 workaround:
# we need to evaluate rpm's installed run-time % { _libdir }, not rpmbuild time
# or else /etc/ld.so.conf.d files?
rpmlibdir=\$(rpm --eval "%%{_libdir}")
# bz1017604: On 64-bit hosts, we should include also the 32-bit library path.
if [ "\$rpmlibdir" != "\${rpmlibdir/lib64/}" ]; then
  rpmlibdir32=":%{_scl_root}\${rpmlibdir/lib64/lib}"
fi
export LD_LIBRARY_PATH=%{_scl_root}\$rpmlibdir\$rpmlibdir32\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}
# duplicate python site.py logic for sitepackages
pythonvers=`python -c 'import sys; print sys.version[:3]'`
export PYTHONPATH=%{_prefix}/lib64/python\$pythonvers/site-packages:%{_prefix}/lib/python\$pythonvers/site-packages\${PYTHONPATH:+:\${PYTHONPATH}}
EOF

# Sudo script
# ===========
cat <<EOF >sudo
#! /bin/sh
# TODO: parse & pass-through sudo options from \$@
sudo_options="-E"

for arg in "\$@"
do
   case "\$arg" in
    *\'*)
      arg=`echo "\$arg" | sed "s/'/'\\\\\\\\''/g"` ;;
   esac
   cmd_options="\$cmd_options '\$arg'" 
done
exec /usr/bin/sudo \$sudo_options LD_LIBRARY_PATH=\$LD_LIBRARY_PATH PATH=\$PATH scl enable %{scl} "\$cmd_options"
EOF

# " (Fix vim syntax coloring.)

# Java configuration
# ==================
cat <<EOF >java.conf
JAVA_LIBDIR=%{_datadir}/java
JNI_LIBDIR=%{_prefix}/lib/java
JVM_ROOT=%{_prefix}/lib/jvm
EOF

# Ivy configuration
# =================
cat <<EOF >ivysettings.xml
<!-- Ivy configuration file for %{scl} software collection
     Artifact resolution order is:
      1. %{scl} collection
      2. java-common collection
      3. maven30 collection
      4. base operating system
-->
<ivysettings>
  <settings defaultResolver="default"/>
  <resolvers>
    <filesystem name="%{scl}-public">
      <ivy pattern="\${ivy.conf.dir}/lib/[module]/apache-ivy-[revision].xml" />
      <artifact pattern="%{_datadir}/java/\[artifact].[ext]" />
    </filesystem>
    <filesystem name="java-common-public">
      <ivy pattern="\${ivy.conf.dir}/lib/[module]/apache-ivy-[revision].xml" />
      <artifact pattern="/opt/rh/rh-java-common/root/%{_root_datadir}/java/\[artifact].[ext]" />
    </filesystem>
    <filesystem name="maven30-public">
      <ivy pattern="\${ivy.conf.dir}/lib/[module]/apache-ivy-[revision].xml" />
      <artifact pattern="/opt/rh/maven30/root/%{_root_datadir}/java/\[artifact].[ext]" />
    </filesystem>
    <filesystem name="public">
      <ivy pattern="\${ivy.conf.dir}/lib/[module]/apache-ivy-[revision].xml" />
      <artifact pattern="%{_root_datadir}/java/\[artifact].[ext]" />
    </filesystem>
    <chain name="main" dual="true">
      <resolver ref="%{scl}-public"/>
      <resolver ref="java-common-public"/>
      <resolver ref="maven30-public"/>
      <resolver ref="public"/>
    </chain>
  </resolvers>
  <include url="\${ivy.default.settings.dir}/ivysettings-local.xml"/>
  <include url="\${ivy.default.settings.dir}/ivysettings-default-chain.xml"/>
</ivysettings>
EOF

# XMvn configuration
# =================
cat <<EOF >configuration.xml
<?xml version="1.0" encoding="US-ASCII"?>
<!-- XMvn configuration file for %{scl} software collection
     Artifact resolution order is:
      1. %{scl} collection
      2. java-common collection
      3. maven30 collection
      4. base operating system
-->
<configuration xmlns="http://fedorahosted.org/xmvn/CONFIG/2.0.0">
  <resolverSettings>
    <prefixes>
      <prefix>%{_scl_root}</prefix>
      <prefix>/</prefix>
    </prefixes>
    <metadataRepositories>
      <repository>%{_scl_root}/usr/share/maven-metadata</repository>
    </metadataRepositories>
  </resolverSettings>
  <installerSettings>
    <metadataDir>opt/rh/%{scl}/root/usr/share/maven-metadata</metadataDir>
  </installerSettings>
  <repositories>
    <repository>
      <id>resolve-%{scl}</id>
      <type>compound</type>
      <properties>
        <prefix>%{_scl_root}</prefix>
        <namespace>%{scl}</namespace>
      </properties>
      <configuration>
        <repositories>
          <repository>base-resolve</repository>
        </repositories>
      </configuration>
    </repository>
    <repository>
      <id>resolve</id>
      <type>compound</type>
      <properties>
        <prefix>/</prefix>
      </properties>
      <configuration>
        <repositories>
	  <!-- Put resolvers in order you want to use them, from
	       highest to lowest preference. (resolve-local is
	       resolver that resolves from local Maven repository in
	       .xm2 in current directory.) -->
          <repository>resolve-local</repository>
          <repository>resolve-%{scl}</repository>
          <repository>resolve-java-common</repository>
          <repository>resolve-maven30</repository>
          <repository>base-resolve</repository>
        </repositories>
      </configuration>
    </repository>
    <repository>
      <id>install</id>
      <type>compound</type>
      <properties>
        <prefix>opt/rh/%{scl}/root</prefix>
        <namespace>%{scl}</namespace>
      </properties>
      <configuration>
        <repositories>
          <repository>base-install</repository>
        </repositories>
      </configuration>
    </repository>
  </repositories>
</configuration>
EOF

%if 0%{?rhel} < 7
# OSGi auto-{provides,requires} macros
# ====================================
cat <<EOF >macros.%{scl}-osgi-config
%%osgi_find_provides_and_requires %%{expand: \\
%%global _use_internal_dependency_generator 0
%%global __find_provides %{_rpmconfigdir}/osgi.prov
%%global __find_requires %{_rpmconfigdir}/osgi.req
}
EOF
%endif

%install
(%{scl_install})

mkdir -p %{buildroot}%{_scl_root}/etc/alternatives %{buildroot}%{_scl_root}/var/lib/alternatives

install -d -m 755 %{buildroot}%{_scl_scripts}
install -p -m 755 enable %{buildroot}%{_scl_scripts}/

install -d -m 755 %{buildroot}%{_scl_scripts}
install -p -m 755 sudo %{buildroot}%{_bindir}/

install -d -m 755 %{buildroot}%{_sysconfdir}/java
install -p -m 644 java.conf %{buildroot}%{_sysconfdir}/java/

install -d -m 755 %{buildroot}%{_sysconfdir}/ivy
install -p -m 644 ivysettings.xml %{buildroot}%{_sysconfdir}/ivy/

install -d -m 755 %{buildroot}%{_sysconfdir}/xdg/xmvn
install -p -m 644 configuration.xml %{buildroot}%{_sysconfdir}/xdg/xmvn/

install -d %{buildroot}%{dockerfiledir}

collections="devtoolset-3 devtoolset-3-toolchain devtoolset-3-dyninst \
             devtoolset-3-elfutils devtoolset-3-oprofile devtoolset-3-systemtap \
             devtoolset-3-valgrind"
install -d -p -m 755 %{buildroot}%{dockerfiledir}/rhel{6,7}
for d in $collections; do
   install -d -p -m 755 %{buildroot}%{dockerfiledir}/rhel{6,7}/$d
   install -p -m 644 rhscl-dockerfiles-%{dfcommit}/rhel6.$d/* %{buildroot}%{dockerfiledir}/rhel6/$d
   install -p -m 644 rhscl-dockerfiles-%{dfcommit}/rhel7.$d/* %{buildroot}%{dockerfiledir}/rhel7/$d
done

# BZ#1194557: Don't ship systemtap container for RHEL6.
rm -rf %{buildroot}%{dockerfiledir}/rhel6/devtoolset-3-systemtap

%files

%files runtime
%scl_files
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_sysconfdir}/selinux-equiv.created
%{_sysconfdir}/ivy
%{_sysconfdir}/java
%dir %{_scl_root}/etc/alternatives

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}*

%files toolchain

%files ide

%files perftools

%if 0%{?rhel} >= 7
%files dockerfiles
%{dockerfiledir}
%endif

%post runtime
if [ ! -f %{_sysconfdir}/selinux-equiv.created ]; then
  /usr/sbin/semanage fcontext -a -e / %{_scl_root}
  restorecon -R %{_scl_root}
  touch %{_sysconfdir}/selinux-equiv.created
fi

%preun runtime
[ $1 = 0 ] && rm -f %{_sysconfdir}/selinux-equiv.created || :

%postun runtime
if [ $1 = 0 ]; then
  /usr/sbin/semanage fcontext -d %{_scl_root}
  [ -d %{_scl_root} ] && restorecon -R %{_scl_root} || :
fi

%changelog
* Thu May 07 2015 Marek Polacek <polacek@redhat.com> - 3.1-12
- Update rhscl-dockerfiles from git (#1194663)

* Wed May 06 2015 Mat Booth <mat.booth@redhat.com> - 3.1-11
- Resolves: rhbz#1218605 - Avoid BR on javapackages-tools

* Wed Apr 15 2015 Marek Polacek <polacek@redhat.com> - 3.1-10
- Bump Release to mollify #1211655

* Wed Apr 8 2015 Marek Polacek <polacek@redhat.com> - 3.1-9
- Add Obsoletes (#1208867)

* Mon Feb 23 2015 Marek Polacek <polacek@redhat.com> - 3.1-8
- Don't ship devtoolset-3-dockerfiles subpackage on RHEL6 (#1194558)

* Fri Feb 20 2015 Marek Polacek <polacek@redhat.com> - 3.1-7
- Don't ship systemtap container for RHEL6 (#1194557)

* Wed Feb 11 2015 Marek Polacek <polacek@redhat.com> - 3.1-6
- Add devtoolset-3-{dyninst,elfutils,valgrind,oprofile,systemtap}
  dockerfiles (#1180659)

* Tue Feb 10 2015 Marek Polacek <polacek@redhat.com> - 3.1-5
- Add devtoolset-3-dockerfiles (#1180657)

* Tue Jan 13 2015 Mat Booth <mat.booth@redhat.com> - 3.1-3
- Resolves: rhbz#1178915 - Rebuild to get correct disttag
- Add BR to Fix unexpanded java dir macros in java.conf
- Don't enable maven30 SCL, as recommended by maven30 maintainer

* Wed Jan 07 2015 Mat Booth <mat.booth@redhat.com> - 3.1-2
- Resolves: rhbz#1178915
- Add missing xmvn resolver setting for metadata repo.
- Make package archful to make sure lib64 dirs are owned.
- Only require java-common and maven30 SCLs when on x86_64.

* Thu Dec 18 2014 Mat Booth <mat.booth@redhat.com> - 3.1-1
- Initial build for DTS 3.1
- Add build-time deps on java-common and mvn30 SCLs
- Update xmvn and ivy config for latest javapackages/xmvn
- Fix file listed twice warning for xmvn/config.xml

* Fri Jun 20 2014 Roland Grunberg <rgrunber@redhat.com> - 3.0-16
- Add macro for enablement of osgi auto-{provides,requires}.

* Wed Jun 04 2014 Marek Polacek <polacek@redhat.com> 3.0-15
- Drop the -vc subpackage (#1104342)

* Tue Jun 03 2014 Mat Booth <mat.booth@redhat.com> - 3.0-14
- Prevent premature command substitution (#1102796)

* Tue Jun 03 2014 Marek Polacek <polacek@redhat.com> 3.0-13
- Create alternatives directories (#1101246)

* Tue Jun 03 2014 Mat Booth <mat.booth@redhat.com> - 3.0-12
- Fix MANPATH variable (#1102741)

* Fri May 30 2014 Alexander Kurtakov <akurtako@redhat.com> 3.0-11
- Reenable mylyn-docs-epub.

* Tue May 27 2014 Alexander Kurtakov <akurtako@redhat.com> 3.0-10
- Comment mylyn-epub as the new version has huge dependency chain.

* Tue May 27 2014 Alexander Kurtakov <akurtako@redhat.com> 3.0-9
- Drop eclipse-xsd as it's no longer part of emf.
- Drop eclipse-rpmstubby as it's merged into rpm-editor.

* Wed May 21 2014 Mat Booth <mat.booth@redhat.com> - 3.0-8
- Revert ant_home fix temporarily

* Mon May 19 2014 Marek Polacek <polacek@redhat.com> 3.0-7
- Require ltrace (#1098247, #1098249)
- Properly set ANT_HOME (#1087654)

* Fri May 16 2014 Mat Booth <mat.booth@redhat.com> - 3.0-6
- Don't require maven30 runtime as this breaks archful packages

* Fri May 16 2014 Mat Booth <mat.booth@redhat.com> - 3.0-5
- Require newest version of scl-utils

* Fri May 16 2014 Mat Booth <mat.booth@redhat.com> - 3.0-4
- Conditionally enable maven30 collection
- Add maven scl macros for other packages to use

* Thu May 15 2014 Mat Booth <mat.booth@redhat.com> - 3.0-3
- Add collection-specific maven, java, ivy configuration

* Thu May 15 2014 Alexander Kurtakov <akurtako@redhat.com> 3.0-2
- Build subpackage should R: scl-utils.

* Tue Mar 4 2014 Marek Polacek <polacek@redhat.com> 3.0-1
- Initial package
