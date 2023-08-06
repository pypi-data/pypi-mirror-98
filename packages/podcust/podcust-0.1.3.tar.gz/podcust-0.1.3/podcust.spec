
%global pypi_name podcust

Name:           %{pypi_name}
Version:        0.1.3
Release:        1%{?dist}
Summary:        Python utility to handle podman containers within Fedora

License:        Parity Public License v7.0.0
URL:            https://github.com/Iolaum/fcust
Source0:        %{URL}/archive/v%{Version}.tar.gz#/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(black)
BuildRequires:  python3dist(check-manifest)
BuildRequires:  python3dist(click)
BuildRequires:  python3dist(coverage)
BuildRequires:  python3dist(flake8)
BuildRequires:  python3dist(mypy)
BuildRequires:  python3dist(pip)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-runner)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(twine)
BuildRequires:  python3dist(wheel)
BuildRequires:  python3dist(yamllint)
BuildRequires:  python3dist(sphinx)
BuildRequires:  hadolint

Requires: podman

%description
 Podman Custodian Python utility to handle podman containers within Fedora.

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build
# generate html and man docs
PYTHONPATH=${PWD} sphinx-build-3 docs html
PYTHONPATH=${PWD} sphinx-build-3 docs man
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py3_install

%check
%{__python3} setup.py test

%files -n %{pypi_name}
%license License.md
%doc html
%{_mandir}/man1/podcust.1.gz
%{_bindir}/podcust
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

%changelog
* Sun Mar 14 2021 Nikolaos Perrakis <nikperrakis@gmail.com> - 0.1.3-1
- Add functionality to delete transmission image data and service unit file.

* Sun Mar 14 2021 Nikolaos Perrakis <nikperrakis@gmail.com> - 0.1.2-1
- Recreate transmission kubernetes template for podman 3.0.

* Sun Mar 07 2021 Nikolaos Perrakis <nikperrakis@gmail.com> - 0.1.1-1
- Fix service file issue.

* Sun Mar 07 2021 Nikolaos Perrakis <nikperrakis@gmail.com> - 0.1.0-2
- Adding systemd user service unit to perform maintenance and updates for transmission container.

* Mon Mar 01 2021 Nikolaos Perrakis <nikperrakis@gmail.com> - 0.0.33-1
- Adding barebones transmission container functionality.

* Fri Feb 26 2021 Nikolaos Perrakis <nikperrakis@gmail.com> - 0.0.27-1
- Initial fedora package.
