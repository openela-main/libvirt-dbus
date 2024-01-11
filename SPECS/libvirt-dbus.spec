# -*- rpm-spec -*-

%global glib2_version 2.44.0
%global libvirt_version 3.0.0
%global libvirt_glib_version 0.0.7
%global system_user libvirtdbus

Name: libvirt-dbus
Version: 1.3.0
Release: 2%{?dist}%{?extra_release}
Summary: libvirt D-Bus API binding
License: LGPLv2+
URL: https://libvirt.org/
Source0: https://libvirt.org/sources/dbus/%{name}-%{version}.tar.xz

BuildRequires: git
BuildRequires: gcc
BuildRequires: libtool
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: libvirt-devel >= %{libvirt_version}
BuildRequires: libvirt-glib-devel >= %{libvirt_glib_version}
BuildRequires: /usr/bin/pod2man

Requires: dbus
Requires: glib2 >= %{glib2_version}
Requires: libvirt-libs >= %{libvirt_version}
Requires: libvirt-glib >= %{libvirt_glib_version}
Requires: polkit

Requires(pre): shadow-utils

%description
This package provides D-Bus API for libvirt

%prep
%autosetup -S git_am -N

git config gc.auto 0

%autopatch


%build
%configure
%make_build

%install
%make_install

%pre
getent group %{system_user} >/dev/null || groupadd -r %{system_user}
getent passwd %{system_user} >/dev/null || \
    useradd -r -g %{system_user} -d / -s /sbin/nologin \
    -c "Libvirt D-Bus bridge" %{system_user}
exit 0

%files
%doc README.md HACKING.md AUTHORS NEWS
%license COPYING
%{_sbindir}/libvirt-dbus
%{_datadir}/dbus-1/services/org.libvirt.service
%{_datadir}/dbus-1/system-services/org.libvirt.service
%{_datadir}/dbus-1/system.d/org.libvirt.conf
%{_datadir}/dbus-1/interfaces/org.libvirt.*.xml
%{_datadir}/polkit-1/rules.d/libvirt-dbus.rules
%{_mandir}/man8/libvirt-dbus.8*

%changelog
* Thu Sep 2 2021 Danilo C. L. de Paula <ddepaula@redhat.com> - 1.3.0-2.el8
- Resolves: bz#2000225
  (Rebase virt:rhel module:stream based on AV-8.6)

* Mon Apr 27 2020 Danilo C. L. de Paula <ddepaula@redhat.com> - 1.3.0
- Resolves: bz#1810193
  (Upgrade components in virt:rhel module:stream for RHEL-8.3 release)

* Fri Jun 28 2019 Danilo de Paula <ddepaula@redhat.com> - 1.2.0-3
- Rebuild all virt packages to fix RHEL's upgrade path
- Resolves: rhbz#1695587
  (Ensure modular RPM upgrade path)

* Fri Jan 18 2019 Pavel Hrdina <phrdina@redhat.com> - 1.2.0-2
- util: fix virtDBusUtilDecodeUUID (rhbz#1647823)

* Thu Sep 20 2018 Pavel Hrdina <phrdina@redhat.com> - 1.2.0-1
- Rebased to libvirt-dbus-1.2.0 (rhbz#1630196)

* Thu May 17 2018 Pavel Hrdina <phrdina@redhat.com> - 1.0.0-1
- Rebase from Fedora
