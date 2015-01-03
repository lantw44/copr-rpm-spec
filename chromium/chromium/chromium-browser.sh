#!/bin/sh

# Chromium launcher

# Authors:
#  Fabien Tassin <fta@sofaraway.org>
# License: GPLv2 or later

# This file is obtained from https://repos.fedorapeople.org/repos/spot/chromium/
# and modified by Ting-Wei Lan <lantw44@gmail.com>. All modifications are also
# licensed under GPLv2 or later.

APPNAME=chromium-browser
LIBDIR=@@CHROMIUMDIR@@
GDB=/usr/bin/gdb

usage () {
  echo "$APPNAME [-h|--help] [-g|--debug] [options] [URL]"
  echo
  echo "        -g or --debug           Start within $GDB"
  echo "        -h or --help            This help screen"
  echo "        --temp-profile          Start with a new and temporary profile"
  echo
  echo " Other supported options are:"
  MANWIDTH=80 man chromium-browser | sed -e '1,/OPTIONS/d; /ENVIRONMENT/,$d'
  echo " See 'man chromium-browser' for more details"
}

CHROMIUM_FLAGS=""

# Prefer user defined CHROMIUM_USER_FLAGS (fron env) over system
# default CHROMIUM_FLAGS
CHROMIUM_FLAGS=${CHROMIUM_USER_FLAGS:-"$CHROMIUM_FLAGS"}

# FFmpeg needs to know where its libs are located
if [ "Z$LD_LIBRARY_PATH" != Z ] ; then
  LD_LIBRARY_PATH=$LIBDIR:$LD_LIBRARY_PATH
else
  LD_LIBRARY_PATH=$LIBDIR
fi

export LD_LIBRARY_PATH

# For the Default Browser detection to work, we need to give access
# to xdg-settings. Also set CHROME_WRAPPER in case xdg-settings is
# not able to do anything useful
export PATH="$LIBDIR:$PATH"
export CHROME_WRAPPER="`readlink -f "$0"`"
export CHROME_DESKTOP=$APPNAME.desktop

# Set CHROME_VERSION_EXTRA visible in the About dialog and in about:version
export CHROME_VERSION_EXTRA="Built from source for @@BUILDTARGET@@"

want_debug=0
want_temp_profile=0
while [ $# -gt 0 ]; do
  case "$1" in
    -h | --help | -help )
      usage
      exit 0 ;;
    -g | --debug )
      want_debug=1
      shift ;;
    --temp-profile )
      want_temp_profile=1
      shift ;;
    -- ) # Stop option prcessing
      shift
      break ;;
    * )
      break ;;
  esac
done

if [ $want_temp_profile -eq 1 ] ; then
  TEMP_PROFILE=`mktemp -d`
  CHROMIUM_FLAGS="$CHROMIUM_FLAGS --user-data-dir=$TEMP_PROFILE"
fi

if [ $want_debug -eq 1 ] ; then
  if [ ! -x $GDB ] ; then
    echo "Sorry, can't find usable $GDB. Please install it."
    exit 1
  fi
  tmpfile=`mktemp /tmp/chromiumargs.XXXXXX` || { echo "Cannot create temporary file" >&2; exit 1; }
  trap " [ -f \"$tmpfile\" ] && /bin/rm -f -- \"$tmpfile\"" 0 1 2 3 13 15
  echo "set args $CHROMIUM_FLAGS ${1+"$@"}" > $tmpfile
  echo "# Env:"
  echo "#     LD_LIBRARY_PATH=$LD_LIBRARY_PATH"
  echo "#                PATH=$PATH"
  echo "#            GTK_PATH=$GTK_PATH"
  echo "# CHROMIUM_USER_FLAGS=$CHROMIUM_USER_FLAGS"
  echo "#      CHROMIUM_FLAGS=$CHROMIUM_FLAGS $@"
  echo "$GDB $LIBDIR/$APPNAME -x $tmpfile"
  $GDB "$LIBDIR/$APPNAME" -x $tmpfile
  if [ $want_temp_profile -eq 1 ] ; then
    rm -rf $TEMP_PROFILE
  fi
  exit $?
else
  if [ $want_temp_profile -eq 0 ] ; then
    exec $LIBDIR/$APPNAME $CHROMIUM_FLAGS "$@"
  else
    # we can't exec here as we need to clean-up the temporary profile
    $LIBDIR/$APPNAME $CHROMIUM_FLAGS "$@"
    rm -rf $TEMP_PROFILE
  fi
fi

