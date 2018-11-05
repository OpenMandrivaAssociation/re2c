Summary:	A tool for generating C-based recognizers from regular expressions
Name:		re2c
Version:	1.1.1
Release:	2
License:	Public Domain
Group:		Development/Other
Url:		http://re2c.org/
Source0:	https://github.com/skvadrik/re2c/releases/download/%{version}/%{name}-%{version}.tar.gz

%description
re2c is a great tool for writing fast and flexible lexers. It has served many
people well for many years and it deserves to be maintained more actively. re2c
is on the order of 2-3 times faster than a flex based scanner, and its input
model is much more flexible.

%prep
%autosetup -p1

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

find doc -type d |xargs chmod 0755
find doc -type f |xargs chmod 0644

# fix attribs
chmod 644 examples/*.c examples/*.re CHANGELOG README

find test -type f -exec chmod 644 {} \;

%build
%configure

%make_build

#regenerate file scanner.cc
rm -f scanner.cc
cd test
../re2c scanner.re > ../scanner.cc
cd ..
rm -f re2c scanner.o
%make_build

%check
make check

%install
%make_install

%files
%doc doc/* examples CHANGELOG README
%attr(0755,root,root) %{_bindir}/re2c
%{_mandir}/man1/re2c.1*
