#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define module	zope.hookable
Summary:	Zope hookable module
Summary(pl.UTF-8):	Moduł Zope hookable
Name:		python3-%{module}
Version:	7.0
Release:	1
License:	ZPL v2.1
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/z/zope.hookable/zope_hookable-%{version}.tar.gz
# Source0-md5:	e257047373df230a484c38b03674ee40
URL:		https://www.zope.dev/
BuildRequires:	python3 >= 1:3.8
BuildRequires:	python3-devel >= 1:3.8
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-zope.testing
BuildRequires:	python3-zope.testrunner
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme >= 1
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package supports the efficient creation of "hookable" objects,
which are callable objects that are meant to be optionally replaced.

%description -l pl.UTF-8
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
%setup -q -n zope_hookable-%{version}

%build
%py3_build

%if %{with tests}
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
zope-testrunner-3 --test-path=src
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/zope/hookable/*.[ch]
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/zope/hookable/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%dir %{py3_sitedir}/zope/hookable
%{py3_sitedir}/zope/hookable/*.py
%{py3_sitedir}/zope/hookable/__pycache__
%attr(755,root,root) %{py3_sitedir}/zope/hookable/_zope_hookable.cpython-*.so
%{py3_sitedir}/zope.hookable-*.egg-info
%{py3_sitedir}/zope.hookable-*-nspkg.pth

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
