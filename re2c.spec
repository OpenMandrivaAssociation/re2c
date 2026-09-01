%global optflags %{optflags} -O3
# PGO with re2c 4.6 and Clang 23: larger binaries, no meaningful speedup
# (and a regression on combined Unicode-identifier DFAs). Do not retry
# until the next major compiler update.

Summary:	A tool for generating C-based recognizers from regular expressions
Name:		re2c
Version:	4.6
Release:	1
License:	Public Domain
Group:		Development/Other
Url:		https://re2c.org/
Source0:	https://github.com/skvadrik/re2c/releases/download/%{version}/%{name}-%{version}.tar.xz
BuildSystem:	autotools
BuildOption:	--enable-libs
BuildOption:	--enable-java
BuildRequires:	slibtool
BuildRequires:	make
BuildRequires:	bash
BuildRequires:	python
BuildRequires:	pkgconfig(re2)
BuildRequires:	jdk-current

%description
re2c is a great tool for writing fast and flexible lexers. It has served many
people well for many years and it deserves to be maintained more actively. re2c
is on the order of 2-3 times faster than a flex based scanner, and its input
model is much more flexible.

%prep -a
for i in $(find . -type d -name CVS) $(find . -type f -name .cvs\*) $(find . -type f -name .#\*); do
	if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

find doc -type d |xargs chmod 0755
find doc -type f |xargs chmod 0644

find test -type f -exec chmod 644 {} \;

%check
make -C _OMV_rpm_build check || cat _OMV_rpm_build/test-suite.log

%install -a
%libpackages

P='%%'
for language in d go haskell java js ocaml python rust swift v zig; do
	case $language in
	haskell)
		lng=hs
		;;
	python)
		lng=py
		;;
	*)
		lng=$language
		;;
	esac
	cat >%{specpartsdir}/$language.specpart <<EOF
${P}package re2$lng
Summary:	A tool for generating $language-based recognizers from regular expressions

${P}description re2$lng
A tool for generating $language-based recognizers from regular expressions

${P}files re2$lng
%{_bindir}/re2$lng
%{_mandir}/man1/re2$lng.1*
%{_datadir}/re2c/stdlib/$language
EOF
done

%files
%doc doc/* examples CHANGELOG
%attr(0755,root,root) %{_bindir}/re2c
%{_mandir}/man1/re2c.1*
%dir %{_datadir}/re2c/stdlib
%{_datadir}/re2c/stdlib/c
%{_datadir}/re2c/stdlib/unicode_categories.re
%{_datadir}/re2c/stdlib/unicode_blocks.re
%{_datadir}/re2c/stdlib/unicode_properties.re
