#!/bin/bash
#
# Copyright (c) 2011 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# This file is obtained from https://src.fedoraproject.org/rpms/chromium/
# and modified by Ting-Wei Lan <lantw44@gmail.com>. All modifications are also
# licensed under 3-clause BSD license.

# Let the wrapped binary know that it has been run through the wrapper.
export CHROME_WRAPPER="$(readlink -f "$0")"

# Use system xdg utilities. But first create mimeapps.list if it doesn't
# exist; some systems have bugs in xdg-mime that make it fail without it.
xdg_app_dir="${XDG_DATA_HOME:-$HOME/.local/share/applications}"
mkdir -p "$xdg_app_dir"
[ -f "$xdg_app_dir/mimeapps.list" ] || touch "$xdg_app_dir/mimeapps.list"

export CHROME_VERSION_EXTRA="Built from source for @@BUILDTARGET@@"

CHROMIUM_DISTRO_FLAGS=" --enable-plugins \
                        --enable-extensions \
                        --enable-user-scripts \
                        --enable-printing \
                        --enable-sync"

exec -a "$0" "@@CHROMIUMDIR@@/$(basename "$0" | sed 's/\.sh$//')" $CHROMIUM_DISTRO_FLAGS "$@"
