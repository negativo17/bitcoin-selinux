%global commit0 7d10d99270b3886dc93ed35664286250c991b2c5
%global date 20210312
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%global selinuxtype targeted
%global moduletype contrib
%global modulename bitcoin

Name:           %{modulename}-selinux
Version:        0
Release:        3%{?shortcommit0:.%{date}git%{shortcommit0}}%{?dist}
Summary:        Bitcoin Core SELinux policy
License:        GPLv3
URL:            https://github.com/scaronni/%{name}
BuildArch:      noarch

%if 0%{!?commit0}
Source0:        https://github.com/scaronni/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Source0:        https://github.com/scaronni/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
%endif

Requires:       selinux-policy-%{selinuxtype}
Requires(post): selinux-policy-%{selinuxtype}
BuildRequires:  selinux-policy-devel
%{?selinux_requires}

%description
Bitcoin Core SELinux policy.

%prep
%if 0%{!?commit0}
%autosetup -n %{name}-%{version}
%else
%autosetup -n %{name}-%{commit0}
%endif

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
* Fri Mar 12 2021 Simone Caronni <negativo17@gmail.com> - 0-3.20210312git7d10d99
- Allow connections to tor ports, remove permissive.

* Fri Mar 12 2021 Simone Caronni <negativo17@gmail.com> - 0-2.20210310gitc539073
- Update postuninstall scriptlet with correct ports.

* Wed Mar 10 2021 Simone Caronni <negativo17@gmail.com> - 0.1-1.20210310git5eccc2a
- First build.

