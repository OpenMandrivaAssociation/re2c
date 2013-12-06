Summary:	A tool for generating C-based recognizers from regular expressions
Name:		re2c
Version:	0.13.5
Release:	9
License:	Public Domain
Group:		Development/Other
URL:		http://re2c.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/re2c/re2c-%{version}.tar.gz

%description
re2c is a great tool for writing fast and flexible lexers. It has served many
people well for many years and it deserves to be maintained more actively. re2c
is on the order of 2-3 times faster than a flex based scanner, and its input
model is much more flexible.

%prep

%setup -q

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# fix attribs
chmod 644 doc/* examples/*.c examples/*.re examples/rexx/* CHANGELOG README

find lessons -type f -exec chmod 644 {} \;
find test -type f -exec chmod 644 {} \;

# don't ship windows code
rm -rf lessons/001_upn_calculator/windows

%build

%configure2_5x

%make

#regenerate file scanner.cc
rm -f scanner.cc
./re2c scanner.re > scanner.cc
rm -f re2c scanner.o
%make

%check
make check

%install
%makeinstall_std

%files
%doc doc/* examples CHANGELOG README lessons
%attr(0755,root,root) %{_bindir}/re2c
%{_mandir}/man1/re2c.1*
