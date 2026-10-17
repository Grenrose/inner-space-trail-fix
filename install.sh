#!/bin/sh
# Install SMALL7.FON into a Wine prefix and register it.
# usage: WINEPREFIX=/path/to/prefix ./install.sh
# Registration is required: Wine skips .fon files when it scans the Fonts
# folder and only loads bitmap fonts listed in the registry.
set -e
cd "$(dirname "$0")"
: "${WINEPREFIX:=$HOME/.wine}"
export WINEPREFIX
[ -f SMALL7.FON ] || python3 small7font.py SMALL7.FON
[ -d "$WINEPREFIX/drive_c/windows/Fonts" ] || { echo "no Wine prefix at $WINEPREFIX" >&2; exit 1; }
cp SMALL7.FON "$WINEPREFIX/drive_c/windows/Fonts/"
wine reg add 'HKLM\Software\Microsoft\Windows NT\CurrentVersion\Fonts' \
    /v 'Small Fonts 7px (Inner Space)' /t REG_SZ /d SMALL7.FON /f
wineserver -k 2>/dev/null || true
echo "SMALL7.FON installed in $WINEPREFIX"
