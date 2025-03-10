#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests (installed package required)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define module	zope.hookable
Summary:	Zope hookable module
Summary(pl.UTF-8):	Moduł Zope hookable
Name:		python-%{module}
Version:	5.4
Release:	2
License:	ZPL v2.1
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/z/zope.hookable/zope.hookable-%{version}.tar.gz
# Source0-md5:	2d7a36d27b53c8c33cb938fdcdf62796
URL:		https://www.zope.dev/
%if %{with python2}
BuildRequires:	python >= 1:2.7
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-zope.testing
BuildRequires:	python-zope.testrunner
%endif
%endif
%if %{with python3}
BuildRequires:	python3 >= 1:3.5
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-zope.testing
BuildRequires:	python3-zope.testrunner
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
Requires:	python-modules >= 1:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package supports the efficient creation of "hookable" objects,
which are callable objects that are meant to be optionally replaced.

%description -l pl.UTF-8
Ten pakiet pozwala wydajnie tworzyć obiekty "podczepialne", będące
obiektami wywoływalnymi, które opcjonalnie mogą być podmieniane.

%package -n python3-%{module}
Summary:	Zope hookable module
Summary(pl.UTF-8):	Moduł Zope hookable
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-%{module}
This package supports the efficient creation of "hookable" objects,
which are callable objects that are meant to be optionally replaced.

%description -n python3-%{module} -l pl.UTF-8
Ten pakiet pozwala wydajnie tworzyć obiekty "podczepialne", będące
obiektami wywoływalnymi, które opcjonalnie mogą być podmieniane.

%package apidocs
Summary:	API documentation for Python zope.hookable module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona zope.hookable
Group:		Documentation

%description apidocs
API documentation for Python zope.hookable module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona zope.hookable.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/zope/hookable/*.[ch]
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/zope/hookable/tests
%endif

%if %{with python3}
%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/zope/hookable/*.[ch]
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/zope/hookable/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%dir %{py_sitedir}/zope/hookable
%{py_sitedir}/zope/hookable/*.py[co]
%attr(755,root,root) %{py_sitedir}/zope/hookable/_zope_hookable.so
%{py_sitedir}/zope.hookable-*.egg-info
%{py_sitedir}/zope.hookable-*-nspkg.pth
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%dir %{py3_sitedir}/zope/hookable
%{py3_sitedir}/zope/hookable/*.py
%{py3_sitedir}/zope/hookable/__pycache__
%attr(755,root,root) %{py3_sitedir}/zope/hookable/_zope_hookable.cpython-*.so
%{py3_sitedir}/zope.hookable-*.egg-info
%{py3_sitedir}/zope.hookable-*-nspkg.pth
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
