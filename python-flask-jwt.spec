%global pypi_name Flask-JWT

%if 0%{?fedora}
%global with_python3 1
%else
# EL doesn't have Python 3
%global with_python3 0
%endif

%if 0%{?rhel} && 0%{?rhel} < 7
# EL 6 doesn't have this macro
%global __python2       %{__python}
%global python2_sitelib %{python_sitelib}
%endif

Name:           python-flask-jwt
Version:        0.3.2
Release:        1%{?dist}
Summary:        Flask support for JSON Web Tokens

License:        MIT
URL:            https://github.com/mattupstate/flask-jwt
Source0:        https://pypi.python.org/packages/source/F/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%if %{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif # if with_python3

%global _description\
Flask-JWT is a Flask extension that adds basic Json Web Token features to any application.

%description %_description

%package -n python2-flask-jwt
Summary: %summary
Requires:       python-flask
Requires:       python-jwt
%{?python_provide:%python_provide python2-flask-jwt}

%description -n python2-flask-jwt %_description

%if 0%{?with_python3}
%package -n     python3-flask-jwt
Summary:        Flask support for JSON Web Tokens

Requires:       python3-flask
Requires:       python-jwt

%description -n python3-flask-jwt %_description
%endif # with_python3


%prep
%setup -q -n %{pypi_name}-%{version}
rm -rf %{pypi_name}.egg-info


%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'

%endif # with_python3


%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python3

%{__python2} setup.py install --skip-build --root %{buildroot}



%files -n python2-flask-jwt
%doc README.markdown
%license LICENSE
%{python2_sitelib}/*
%if 0%{?with_python3}

%files -n python3-flask-jwt
%doc README.markdown
%license LICENSE
%{python3_sitelib}/*
%endif # with_python3


%changelog
* Wed Dec 13 2017 Brian C. Lane <bcl@redhat.com> - 0.3.2-1
- Initial creation for COPR build


