%bcond_without pgo
%global optflags %{optflags} -O3

Summary:	A tool for generating C-based recognizers from regular expressions
Name:		re2c
Version:	2.1.1
Release:	1
License:	Public Domain
Group:		Development/Other
Url:		http://re2c.org/
Source0:	https://github.com/skvadrik/re2c/archive/%{version}.tar.gz
BuildRequires:	bison
BuildRequires:	bash

%description
re2c is a great tool for writing fast and flexible lexers. It has served many
people well for many years and it deserves to be maintained more actively. re2c
is on the order of 2-3 times faster than a flex based scanner, and its input
model is much more flexible.

%package re2go
Summary:	A tool for generating Go-based recognizers from regular expressions
BuildRequires:	golang

%description re2go
A tool for generating Go-based recognizers from regular expressions

%prep
%autosetup -p1

for i in $(find . -type d -name CVS) $(find . -type f -name .cvs\*) $(find . -type f -name .#\*); do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

find doc -type d |xargs chmod 0755
find doc -type f |xargs chmod 0644

find test -type f -exec chmod 644 {} \;

%build
./autogen.sh

%if %{with pgo}
export LLVM_PROFILE_FILE=%{name}-%p.profile.d
export LD_LIBRARY_PATH="$(pwd)"
CFLAGS="%{optflags} -fprofile-instr-generate" \
CXXFLAGS="%{optflags} -fprofile-instr-generate" \
LDFLAGS="%{ldflags} -fprofile-instr-generate" \
%configure
%make_build
# (tpg) try to fix tests
sed -i -e 's#re2c=.*$#re2c="$(dirname $0)/re2c"#g' run_tests.sh
make check || cat test-suite.log

unset LD_LIBRARY_PATH
unset LLVM_PROFILE_FILE
llvm-profdata merge --output=%{name}.profile *.profile.d
rm -f *.profile.d

make clean

CFLAGS="%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
CXXFLAGS="%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
LDFLAGS="%{ldflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
%endif
%configure
%make_build

%check
make check || cat test-suite.log

%install
%make_install

%files
%doc doc/* examples CHANGELOG
%attr(0755,root,root) %{_bindir}/re2c
%{_mandir}/man1/re2c.1*
%{_datadir}/re2c/stdlib/unicode_categories.re

%files re2go
%{_bindir}/re2go
%{_mandir}/man1/re2go.1*
