#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%include	/usr/lib/rpm/macros.perl
Summary:	Get, unpack, build and install CPAN modules
Name:		cpanminus
Version:	1.7001
Release:	1
License:	GPL+ or Artistic
Group:		Development/Libraries
Source0:	http://www.cpan.org/authors/id/M/MI/MIYAGAWA/App-%{name}-%{version}.tar.gz
# Source0-md5:	4655c5903e2885085262cf5f15ff5ae3
Source1:	http://pkgs.fedoraproject.org/cgit/perl-App-cpanminus.git/plain/fatunpack
# Source1-md5:	c6c93648af22e2e47f94d391868cef06
URL:		http://search.cpan.org/dist/App-cpanminus/
BuildRequires:	%{_bindir}/podselect
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(Getopt::Long)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
BuildRequires:	rpm-perlprov >= 4.1-13
# Run-time:
# Nothing special. The tests are very poor. But we run perl -c at built-time
# to check for correct unpacking. So we need non-optional run-time
# dependencies at build-time too:
BuildRequires:	perl(Config)
BuildRequires:	perl(aliased)
BuildRequires:	perl(constant)
# CPAN::DistnameInfo not needed for compilation
# CPAN::Meta not needed for copmilation
# CPAN::Meta::Check not needed for compilation
# CPAN::Meta::Prereqs not needed for compilation
BuildRequires:	perl(CPAN::Meta::Requirements)
# CPAN::Meta::YAML not needed for compilation
BuildRequires:	perl(Cwd)
# Digest::SHA not needed for compilation
# Dumpvalue not needed for compilation
# ExtUtils::Manifest not needed for compilation
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Copy)
BuildRequires:	perl(File::Find)
# File::pushd not needed for compilation
BuildRequires:	perl(File::Temp)
# HTTP::Tiny not needed for compilation
# JSON::PP not needed for compilation
# local::lib not needed for compilation
# Module::CoreList not needed for compilation
# Module::CPANfile not needed for compilation
# Module::Metadata not needed for compilation
BuildRequires:	perl(Parse::CPAN::Meta)
# POSIX not needed for compilation
# Safe not needed for compilation
BuildRequires:	perl(String::ShellQuote)
BuildRequires:	perl(Symbol)
BuildRequires:	perl(version)
# version::vpp not needed for compilation
BuildRequires:	perl(warnings::register)
# YAML not needed for compilation
# Tests:
BuildRequires:	perl(Test::More)
# Current dependency generator cannot parse compressed code. Use PPI to find them, and list them manually:
# Archive::Tar is optional
# Archive::Zip is optional
# Compress::Zlib is optional
Requires:	perl(CPAN::DistnameInfo)
Requires:	perl(CPAN::Meta)
Requires:	perl(CPAN::Meta::Check)
Requires:	perl(CPAN::Meta::Prereqs)
Requires:	perl(CPAN::Meta::YAML)
Requires:	perl(Digest::SHA)
Requires:	perl(ExtUtils::Install) >= 1.46
Requires:	perl(ExtUtils::MakeMaker) >= 6.31
Requires:	perl(ExtUtils::Manifest)
# File::HomeDir is optional
Requires:	perl(File::pushd)
# HTTP getter by LWP::UserAgent or wget or curl or HTTP::Tiny
Requires:	perl(HTTP::Tiny)
Requires:	perl(local::lib)
# LWP::Protocol::https is optional
# LWP::UserAgent is optional
Requires:	perl(Module::Build)
Requires:	perl(Module::CPANfile)
Requires:	perl(Module::CoreList)
Requires:	perl(Module::Metadata)
# Module::Signature is optional
Requires:	perl(version::vpp)
# Win32 not used
Requires:	perl(YAML)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Why? It's dependency free, requires zero configuration, and stands
alone but it's maintainable and extensible with plug-ins and friendly
to shell scripting. When running, it requires only 10 MB of RAM.

%prep
%setup -q -n App-%{name}-%{version}
# Unbundle fat-packed modules
podselect lib/App/cpanminus.pm > lib/App/cpanminus.pod

for F in bin/cpanm lib/App/cpanminus/fatscript.pm; do
	%{__perl} %{SOURCE1} --libdir lib --filter '^App/cpanminus' "$F" > "${F}.stripped"
	perl -c -Ilib "${F}.stripped"
	mv "${F}.stripped" "$F"
done

%build
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
%doc Changes README
%attr(755,root,root) %{_bindir}/cpanm
%{perl_vendorlib}/App/cpanminus.pm
%{perl_vendorlib}/App/cpanminus
%{_mandir}/man1/cpanm.1*
%{_mandir}/man3/App::cpanminus*
