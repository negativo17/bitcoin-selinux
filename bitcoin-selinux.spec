%global forgeurl https://github.com/scaronni/%{name}
%global commit eaa9a049c8e3f645dc92797ca37703d95f885db1
%forgemeta

%global selinuxtype targeted
%global modulename bitcoin

Name:           %{modulename}-selinux
Version:        0
Release:        5%{?dist}
Summary:        Bitcoin Core SELinux policy
License:        GPLv3
URL:            %{forgeurl}
BuildArch:      noarch

Source0:        %{forgesource}

Requires:       selinux-policy-%{selinuxtype}
Requires(post): selinux-policy-%{selinuxtype}
BuildRequires:  selinux-policy-devel
%{?selinux_requires}

%description
Bitcoin Core SELinux policy.

%prep
%forgesetup

%build
make -f %{_datadir}/selinux/devel/Makefile %{modulename}.pp
bzip2 -9 %{modulename}.pp

%install
install -D -m 0644 %{modulename}.pp.bz2 %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2

%pre
%selinux_relabel_pre -s %{selinuxtype}

%post
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2
if %{_sbindir}/selinuxenabled ; then
     %{_sbindir}/semanage port -a -t %{modulename}_port_t -p tcp 8332
     %{_sbindir}/semanage port -a -t %{modulename}_port_t -p tcp 8333
     %{_sbindir}/semanage port -a -t %{modulename}_port_t -p tcp 8334
     %{_sbindir}/semanage port -a -t %{modulename}_port_t -p tcp 18332
     %{_sbindir}/semanage port -a -t %{modulename}_port_t -p tcp 18333
fi

%postun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename}
fi
if %{_sbindir}/selinuxenabled ; then
    %{_sbindir}/semanage port -d -t %{modulename}_port_t -p tcp 8332
    %{_sbindir}/semanage port -d -t %{modulename}_port_t -p tcp 8333
    %{_sbindir}/semanage port -d -t %{modulename}_port_t -p tcp 8334
    %{_sbindir}/semanage port -d -t %{modulename}_port_t -p tcp 18332
    %{_sbindir}/semanage port -d -t %{modulename}_port_t -p tcp 18333
fi

%posttrans
%selinux_relabel_post -s %{selinuxtype}

%files
%license LICENSE
%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.*
%ghost %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{modulename}

%changelog
* Sun Mar 14 2021 Simone Caronni <negativo17@gmail.com> - 0-5
- Use forge macros from packaging guidelines.

* Fri Mar 12 2021 Simone Caronni <negativo17@gmail.com> - 0-4.20210312giteaa9a04
- Updated policy.

* Fri Mar 12 2021 Simone Caronni <negativo17@gmail.com> - 0-3.20210312git7d10d99
- Allow connections to tor ports, remove permissive.

* Fri Mar 12 2021 Simone Caronni <negativo17@gmail.com> - 0-2.20210310gitc539073
- Update postuninstall scriptlet with correct ports.

* Wed Mar 10 2021 Simone Caronni <negativo17@gmail.com> - 0.1-1.20210310git5eccc2a
- First build.

