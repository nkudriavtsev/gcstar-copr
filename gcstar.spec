Name:           gcstar
Version:        1.8.0
Release:        1%{?dist}
Summary:        Personal collections manager

# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:        GPL-2.0-or-later
URL:            https://gitlab.com/GCstar/GCstar.git
Source0:        https://gitlab.com/GCstar/GCstar/-/archive/v%{version}/GCstar-v%{version}.tar.gz
Patch0:         gcstar.path.patch
# We patch gcstar to allow comic volumes to number 1000000
# https://bugzilla.redhat.com/show_bug.cgi?id=1232956
Patch1:         gcstar-comics-volume.patch
BuildArch:      noarch

Requires:      hicolor-icon-theme
Requires:      perl-Gtk3
Requires:      perl-Gtk3-SimpleList
Requires:      perl-XML-Simple
Requires:      perl-Archive-Tar
Requires:      perl-Archive-Zip
Requires:      perl-IO-Compress
Requires:      perl-Date-Calc
Requires:      perl-DateTime-Format-Strptime
Requires:      perl-Digest-MD5
Requires:      perl-GD
Requires:      perl-GDGraph
Requires:      perl-GDTextUtil
Requires:      perl-Image-ExifTool
Requires:      perl-MIME-Base64
Requires:      perl-MP3-Info
Requires:      perl-Time-Piece
Requires:      perl-JSON
Requires:      perl-Locale-Codes
Provides:      perl(GCItemsLists::GCImageLists) = %{version}
Provides:      perl(GCItemsLists::GCTextLists) = %{version}
Provides:      perl(GCPlugins::GCfilms::GCThemoviedb) = %{version}
Provides:      perl(GCItemsLists::GCListOptions) = %{version}
Provides:      perl(GCItemsLists::GCImageListComponents) = %{version}
Provides:      perl(GCGraphicComponents::GCDoubleLists) = %{version}
Provides:      perl(GCGraphicComponents::GCBaseWidgets) = %{version}
# The last version of gcfilms was 6.4
Obsoletes:     gcfilms <= 6.4
BuildRequires: coreutils
BuildRequires: desktop-file-utils
BuildRequires: perl-generators

%description
GCstar is an application for managing your personal collections.
Detailed information on each item can be automatically retrieved
from the internet and you can store additional data, depending on
the collection type. And also who you've lent your them to. You
may also search and filter your collection by criteria.

%prep
%setup -q -n GCstar-v%{version}
%patch -P0 -p1 -b .path
%patch -P1 -p1


%build

%install
%{__mkdir_p} %{buildroot}%{_prefix}
%{__install} -d %{buildroot}%{_bindir}
%{__install} bin/gcstar %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_datadir}
%{__cp} -a share/gcstar %{buildroot}%{_datadir}
chmod 755 %{buildroot}%{_datadir}/%{name}/xslt/applyXSLT.pl
%{__install} -d %{buildroot}%{_datadir}/%{name}/lib
%{__cp} -a lib/gcstar/* %{buildroot}%{_datadir}/%{name}/lib
%{__install} -d %{buildroot}%{_mandir}/man1
%{__install} -m 644 man/gcstar.1 %{buildroot}%{_mandir}/man1
gzip %{buildroot}%{_mandir}/man1/gcstar.1

# Install menu entry
%{__cat} > %{name}.desktop << EOF
[Desktop Entry]
Name=GCstar
Comment=Manage your collections
GenericName=Personal collections manager
Exec=gcstar
Icon=gcstar
Terminal=false
Type=Application
MimeType=application/x-gcstar
Categories=Application;Office;
Encoding=UTF-8
EOF

%{__mkdir_p} %{buildroot}%{_datadir}/applications
desktop-file-install \
    --dir %{buildroot}%{_datadir}/applications  \
    %{name}.desktop

#Mime Type
%{__cat} > %{name}.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
        <mime-type type="application/x-gcstar">
                <comment>GCstar collection</comment>
                <glob pattern="*.gcs"/>
        </mime-type>
</mime-info>
EOF

%{__mkdir_p} %{buildroot}%{_datadir}/mime/packages
cp %{name}.xml %{buildroot}%{_datadir}/mime/packages

# Install app icons
for i in 16 22 24 32 36 48 64 72 96 128 192 256; do
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
    %{__install} -m 644 share/gcstar/icons/%{name}_${i}x${i}.png %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
done

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
%{__install} -m 644 share/gcstar/icons/gcstar_scalable.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%files
%doc CHANGELOG README
%license LICENSE
%{_datadir}/gcstar
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_mandir}/man1/gcstar.1.gz
%attr(0755,root,root) %{_bindir}/gcstar
%attr(0755,root,root) %{_datadir}/gcstar/helpers/xdg-open
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml

%changelog
%autochangelog
