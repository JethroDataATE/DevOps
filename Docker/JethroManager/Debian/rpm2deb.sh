#!/bin/bash
function Usage {
    echo "Usage: $0 <RPM package>.rpm"
    exit 1
}

function NotRoot {
    echo "$0 could run only as a root, or under fakeroot environment"
    exit 100
}

[ -z "$1" ] &&  echo "Missing RPM package name." && Usage
[ ! -f "$1" ] && echo "$1 does not exists or not a file." && Usage
[ ! -r "$1" ] && echo "'$1' is not a readable file." && Usage
[ "$EUID" -ne 0 ] && NotRoot

DIR_NAME=`basename -s ".x86_64.rpm" $1 | sed  's/-[0-9]*[dpx][_cn6]*\?$//i'`
[ "$DIR_NAME" = "$1" ] && echo "'$1' does not look as an RPM archive." && Usage

echo "rpm2deb starting..."

#Extract files from RPM and debianize package structure:
rm -rf ${DIR_NAME}
EMAIL="packager@jethrodata.com" alien -dksc ${1}

#Build DEB package from conetent of DIR_NAME
pushd $DIR_NAME >/dev/null
sed -i -r 's/\(0(MapR|libhdfs3)\.(.*)-(.*)\)/(\2.\1-\3)/' debian/changelog
debian/rules binary 2>/dev/null
popd >/dev/null

echo "rpm2deb completed."

