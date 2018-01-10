#!/bin/bash

# You probably need to update only this link
ELECTRUM_GIT_URL=git://github.com/NeblioTeam/electrum-nebl.git
BRANCH=master
NAME_ROOT=electrum-nebl


# These settings probably don't need any change
export WINEPREFIX=~/wine64

PYHOME=c:/python27
PYTHON="wine $PYHOME/python.exe -OO -B"


# Let's begin!
cd `dirname $0`
set -e

cd tmp

if [ -d "electrum-nebl-git" ]; then
    # GIT repository found, update it
    echo "Pull"
    cd electrum-nebl-git
    git pull
    git checkout $BRANCH
    cd ..
else
    # GIT repository not found, clone it
    echo "Clone"
    git clone -b $BRANCH $ELECTRUM_GIT_URL electrum-nebl-git
fi

cd electrum-nebl-git
VERSION=2.9.3.1.1
echo "Last commit: $VERSION"

cd ..

rm -rf $WINEPREFIX/drive_c/electrum-nebl
cp -r electrum-nebl-git $WINEPREFIX/drive_c/electrum-nebl
#cp electrum-nebl-git/LICENCE .

# add python packages (built with make_packages)
cp -r ../../../packages $WINEPREFIX/drive_c/electrum-nebl/

# add locale dir
#cp -r ../../../lib/locale $WINEPREFIX/drive_c/electrum-nebl/lib/

# Build Qt resources
wine $WINEPREFIX/drive_c/Python27/Lib/site-packages/PyQt4/pyrcc4.exe C:/electrum-nebl/icons.qrc -o C:/electrum-nebl/lib/icons_rc.py
wine $WINEPREFIX/drive_c/Python27/Lib/site-packages/PyQt4/pyrcc4.exe C:/electrum-nebl/icons.qrc -o C:/electrum-nebl/gui/qt/icons_rc.py

cd ..

rm -rf dist/

# build standalone version
$PYTHON "C:/pyinstaller/pyinstaller.py" --noconfirm --ascii --name $NAME_ROOT-$VERSION.exe -w deterministic.spec

# build NSIS installer
# $VERSION could be passed to the electrum.nsi script, but this would require some rewriting in the script iself.
wine "$WINEPREFIX/drive_c/Program Files (x86)/NSIS/makensis.exe" /DPRODUCT_VERSION=$VERSION electrum.nsi

cd dist
mv electrum-nebl-setup.exe $NAME_ROOT-$VERSION-setup.exe
cd ..

# build portable version
cp portable.patch $WINEPREFIX/drive_c/electrum-nebl
pushd $WINEPREFIX/drive_c/electrum-nebl
patch < portable.patch
popd
$PYTHON "C:/pyinstaller/pyinstaller.py" --noconfirm --ascii --name $NAME_ROOT-$VERSION-portable.exe -w deterministic.spec

echo "Done."
