# -*- rpm-spec -*-

%global meson_version 0.49.0
%global glib2_version 2.44.0
%global libvirt_version 3.0.0
%global libvirt_glib_version 0.0.7
%global system_user libvirtdbus

Name: libvirt-dbus
Version: 1.4.1
Release: 5%{?dist}%{?extra_release}
Summary: libvirt D-Bus API binding
License: LGPLv2+
URL: https://libvirt.org/
Source0: https://libvirt.org/sources/dbus/%{name}-%{version}.tar.xz


BuildRequires: git
BuildRequires: gcc
BuildRequires: meson >= %{meson_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: libvirt-devel >= %{libvirt_version}
BuildRequires: libvirt-glib-devel >= %{libvirt_glib_version}
%if 0%{?rhel} == 7
BuildRequires: python36-docutils
%else
BuildRequires: python3-docutils
%endif

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
%meson \
    -Dinit_script=systemd
%meson_build

%install
%meson_install

%pre
getent group %{system_user} >/dev/null || groupadd -r %{system_user}
getent passwd %{system_user} >/dev/null || \
    useradd -r -g %{system_user} -d / -s /sbin/nologin \
    -c "Libvirt D-Bus bridge" %{system_user}
exit 0

%files
%doc AUTHORS.rst NEWS.rst
%license COPYING
%{_sbindir}/libvirt-dbus
%{_unitdir}/libvirt-dbus.service
%{_prefix}/lib/systemd/user/libvirt-dbus.service
%{_datadir}/dbus-1/services/org.libvirt.service
%{_datadir}/dbus-1/system-services/org.libvirt.service
%{_datadir}/dbus-1/system.d/org.libvirt.conf
%{_datadir}/dbus-1/interfaces/org.libvirt.*.xml
%{_datadir}/polkit-1/rules.d/libvirt-dbus.rules
%{_mandir}/man8/libvirt-dbus.8*

%changelog
* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 1.4.1-5
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Jul 02 2021 Pavel Hrdina <phrdina@redhat.com> - 1.4.1-4
- Add missing file for RHEL-9 gating tests (rhbz#1950602)

* Thu Jul 01 2021 Pavel Hrdina <phrdina@redhat.com> - 1.4.1-3
- FIX: RHEL: Add gating tests for RHEL-9 (rhbz#1950602)

* Wed Jun 30 2021 Pavel Hrdina <phrdina@redhat.com> - 1.4.1-2
- RHEL: Add gating tests for RHEL-9 (rhbz#1950602)

* Wed Jun 30 2021 Pavel Hrdina <phrdina@redhat.com> - 1.4.1-1
- Rebased to libvirt-dbus-1.4.1 (rhbz#1977337)

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 1.4.0-4
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 05 2020 Pavel Hrdina <phrdina@redhat.com> - 1.4.0-1
- Update to 1.4.0 release

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Pavel Hrdina <phrdina@redhat.com> - 1.3.0-1
- Update to 1.3.0 release

* Wed Aug 29 2018 Pavel Hrdina <phrdina@redhat.com> - 1.2.0-1
- Update to 1.2.0 release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Pavel Hrdina <phrdina@redhat.com> - 1.1.0-1
- Update to 1.1.0 release

* Thu May 17 2018 Pavel Hrdina <phrdina@redhat.com> - 1.0.0-1
- Update to 1.0.0 release

* Tue Mar 27 2018 Pavel Hrdina <phrdina@redhat.com> - 0.0.1-1
- Initial RPM build
