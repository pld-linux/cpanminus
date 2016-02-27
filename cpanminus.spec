#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%include	/usr/lib/rpm/macros.perl
Summary:	Get, unpack, build and install CPAN modules
Name:		cpanminus
Version:	1.7040
Release:	1
License:	GPL+ or Artistic
Group:		Development/Libraries
Source0:	http://www.cpan.org/authors/id/M/MI/MIYAGAWA/App-%{name}-%{version}.tar.gz
# Source0-md5:	8f8e43433f42e78d8c4374e1f0f55d31
Source1:	http://pkgs.fedoraproject.org/cgit/perl-App-cpanminus.git/plain/fatunpack
# Source1-md5:	c69ce04e198446d28e2aaa8ba3291542
URL:		http://search.cpan.org/dist/App-cpanminus/
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:	perl-String-ShellQuote
BuildRequires:	perl-tools-pod
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	perl(ExtUtils::Install) >= 1.46
Requires:	perl(ExtUtils::MakeMaker) >= 6.58
Requires:	perl-CPAN-DistnameInfo
Requires:	perl-CPAN-Meta-Check
Requires:	perl-File-pushd
Requires:	perl-Module-CPANfile
Requires:	perl-Parse-PMFile
Requires:	perl-YAML
Requires:	perl-local-lib
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Why? It's dependency free, requires zero configuration, and stands
alone but it's maintainable and extensible with plug-ins and friendly
to shell scripting. When running, it requires only 10 MB of RAM.

%prep
%setup -q -n App-%{name}-%{version}

%build
# Unbundle fat-packed modules
podselect lib/App/cpanminus.pm > lib/App/cpanminus.pod

for F in bin/cpanm lib/App/cpanminus/fatscript.pm; do
	%{__perl} %{SOURCE1} --libdir lib --filter '^App/cpanminus' "$F" > "${F}.stripped"
	perl -c -Ilib "${F}.stripped"
	mv "${F}.stripped" "$F"
done

# strip remains of fatpack
%{__sed} -i -e '/DO NOT EDIT/,/END OF FATPACK CODE/d' bin/cpanm

%{__perl} Makefile.PL INSTALLDIRS=vendor

# strip pod, already in manual
%{__sed} -i -e '/__END__/,$d' bin/cpanm

%{__make}
%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/auto/App/cpanminus/.packlist
%{__rm} $RPM_BUILD_ROOT%{perl_vendorlib}/App/cpanminus.pod
# same as bindir/cpanm
%{__rm} $RPM_BUILD_ROOT%{perl_vendorlib}/App/cpanminus/fatscript.pm

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README LICENSE
%attr(755,root,root) %{_bindir}/cpanm
%{perl_vendorlib}/App/cpanminus.pm
%{perl_vendorlib}/App/cpanminus
%{_mandir}/man1/cpanm.1*
%{_mandir}/man3/App::cpanminus*
