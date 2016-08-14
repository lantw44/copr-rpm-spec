#!/usr/bin/env python2
# Copyright 2010,2015-2016 Tom Callaway <tcallawa@redhat.com>
# Copyright 2013-2016 Tomas Popela <tpopela@redhat.com>
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# This file is obtained from official Chromium packages distributed by Fedora:
# http://pkgs.fedoraproject.org/cgit/rpms/chromium.git/commit/?id=8a15fdf
#
# This script has been and modified by Ting-Wei Lan <lantw44@gmail.com> for
# using in lantw44/chromium Copr repository.
#
# List of changes:
#  * The shebang line no longer hardcodes the path to python2.
#  * http:// URLs are replaced by https:// URLs.
#  * MD5 hash checking is replaced by SHA512 hash checking.
#  * xz -9 command is replaced by xz -0 command to reduce memory requirement.
#  * Function nacl_versions and download_chrome_latest_rpm are removed.

try:
  import argparse
  optparse = False
except ImportError:
  from optparse import OptionParser
  optparse = True
import csv
import glob
import hashlib
import locale
import os
import shutil
import StringIO
import sys
import urllib

chromium_url = "https://commondatastorage.googleapis.com/chromium-browser-official/"

chromium_root_dir = "."
version_string = "stable"

name = 'Chromium Latest (lantw44/chromium)'
script_version = 0.8
my_description = '{0} {1}'.format(name, script_version)


def dlProgress(count, blockSize, totalSize):

  if (totalSize <= blockSize):
    percent = int(count * 100)
  else:
    percent = int(count * blockSize * 100 / totalSize)
  sys.stdout.write("\r" + "Downloading ... %d%%" % percent)
  sys.stdout.flush()


def delete_chromium_dir(ch_dir):

  full_dir = "%s/%s" % (latest_dir, ch_dir)
  print 'Deleting %s ' % full_dir
  if os.path.isdir(full_dir):
    shutil.rmtree(full_dir)
    print '[DONE]'
  else:
    print '[NOT FOUND]'


def delete_chromium_files(files):

  full_path = "%s/%s" % (latest_dir, files)
  print 'Deleting ' + full_path + ' ',
  for filename in glob.glob(full_path):
    print 'Deleting ' + filename + ' ',
    os.remove(filename)
    print '[DONE]'


def check_omahaproxy(channel="stable"):

  version = 0
  status_url = "https://omahaproxy.appspot.com/all?os=linux&channel=" + channel

  usock = urllib.urlopen(status_url)
  status_dump = usock.read()
  usock.close()
  status_list = StringIO.StringIO(status_dump)
  status_reader = list(csv.reader(status_list, delimiter=','))
  linux_channels = [s for s in status_reader if "linux" in s]
  linux_channel = [s for s in linux_channels if channel in s]
  version = linux_channel[0][2]

  if version == 0:
    print 'I could not find the latest %s build. Bailing out.' % channel
    sys.exit(1)
  else:
    print 'Latest Chromium Version on %s at %s is %s' % (channel, status_url, version)
    return version


def remove_file_if_exists(filename):

  filepath = "%s/%s" % (chromium_root_dir, filename)
  if os.path.isfile(filepath):
    try:
      os.remove(filepath)
    except Exception:
      pass


def download_file_and_compare_hashes(file_to_download):

  hashes_file = '%s.hashes' % file_to_download

  if (args.clean):
    remove_file_if_exists(file_to_download)
    remove_file_if_exists(hashes_file)

  # Let's make sure we haven't already downloaded it.
  tarball_local_file = "%s/%s" % (chromium_root_dir, file_to_download)
  if os.path.isfile(tarball_local_file):
    print "%s already exists!" % file_to_download
  else:
    path = '%s%s' % (chromium_url, file_to_download)
    print "Downloading %s" % path
    # Perhaps look at using python-progressbar at some point?
    info=urllib.urlretrieve(path, tarball_local_file, reporthook=dlProgress)[1]
    urllib.urlcleanup()
    print ""
    if (info["Content-Type"] != "application/x-tar"):
      print 'Chromium tarballs for %s are not on servers.' % file_to_download
      remove_file_if_exists (file_to_download)
      sys.exit(1)

  hashes_local_file = "%s/%s" % (chromium_root_dir, hashes_file)
  if not os.path.isfile(hashes_local_file):
    path = '%s%s' % (chromium_url, hashes_file)
    print "Downloading %s" % path
    # Perhaps look at using python-progressbar at some point?
    info=urllib.urlretrieve(path, hashes_local_file, reporthook=dlProgress)[1]
    urllib.urlcleanup()
    print ""

  if os.path.isfile(hashes_local_file):
    with open(hashes_local_file, "r") as input_file:
      while True:
        hash_line = input_file.readline().split()
        if len(hash_line) == 0:
          print "Cannot compare SHA512 hash for %s!" % file_to_download
        if hash_line[0] == 'sha512':
          sha512sum = hash_line[1]
          break
      sha512 = hashlib.sha512()
      with open(tarball_local_file, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
          sha512.update(block)
        if (sha512sum == sha512.hexdigest()):
          print "SHA512 matches for %s!" % file_to_download
        else:
          print "SHA512 mismatch for %s!" % file_to_download
          sys.exit(1)
  else:
    print "Cannot compare hashes for %s!" % file_to_download


def download_version(version):

  download_file_and_compare_hashes ('chromium-%s.tar.xz' % version)

  if (args.tests):
    download_file_and_compare_hashes ('chromium-%s-testdata.tar.xz' % version)


# This is where the magic happens
if __name__ == '__main__':

  # Locale magic
  locale.setlocale(locale.LC_ALL, '')

  # Create the parser object
  if optparse:
    parser = OptionParser(description=my_description)
    parser_add_argument = parser.add_option
  else:
    parser = argparse.ArgumentParser(description=my_description)
    parser_add_argument = parser.add_argument

  parser.add_argument(
      'work_dir', type=str, nargs='?',
      help='Root of the working directory (default: current working directory)')
  parser_add_argument(
      '--ffmpegarm', action='store_true',
      help='Leave arm sources when cleaning ffmpeg')
  parser_add_argument(
      '--beta', action='store_true',
      help='Get the latest beta Chromium source')
  parser_add_argument(
      '--clean', action='store_true',
      help='Re-download all previously downloaded sources')
  parser_add_argument(
      '--cleansources', action='store_true',
      help='Get the latest Chromium release from given channel and clean various directories to from unnecessary or unwanted stuff')
  parser_add_argument(
      '--dev', action='store_true',
      help='Get the latest dev Chromium source')
  parser_add_argument(
      '--ffmpegclean', action='store_true',
      help='Get the latest Chromium release from given channel and cleans ffmpeg sources from proprietary stuff')
  parser_add_argument(
      '--prep', action='store_true',
      help='Prepare everything, but don\'t compress the result')
  parser_add_argument(
      '--stable', action='store_true',
      help='Get the latest stable Chromium source')
  parser_add_argument(
      '--tests', action='store_true',
      help='Get the additional data for running tests')
  parser_add_argument(
      '--version',
      help='Download a specific version of Chromium')

  # Parse the args
  if optparse:
    args, options = parser.parse_args()
  else:
    args = parser.parse_args()

  if args.work_dir:
    chromium_root_dir = args.work_dir

  if args.stable:
    version_string = "stable"
  elif args.beta:
    version_string = "beta"
  elif args.dev:
    version_string = "dev"
  elif (not (args.stable or args.beta or args.dev)):
    if (not args.version):
      print 'No version specified, downloading STABLE'

  chromium_version = args.version if args.version else check_omahaproxy(version_string)

  latest = 'chromium-%s.tar.xz' % chromium_version

  download_version(chromium_version)

  # Lets make sure we haven't unpacked it already
  latest_dir = "%s/chromium-%s" % (chromium_root_dir, chromium_version)
  if (args.clean and os.path.isdir(latest_dir)):
    shutil.rmtree(latest_dir)

  if os.path.isdir(latest_dir):
    print "%s already exists, perhaps %s has already been unpacked?" % (latest_dir, latest)
  else:
    print "Unpacking %s into %s, please wait." % (latest, latest_dir)
    if (os.system("cd %s && tar -xJf %s" % (chromium_root_dir, latest)) != 0):
      print "%s is possibly corrupted, exiting." % (latest)
      sys.exit(1)

  if (args.cleansources):
    junk_dirs = ['third_party/WebKit/Tools/Scripts/webkitpy/layout_tests',
                 'webkit/data/layout_tests', 'third_party/hunspell/dictionaries',
                 'chrome/test/data', 'native_client/tests',
                 'third_party/WebKit/LayoutTests']

    # First, the dirs:
    for directory in junk_dirs:
      delete_chromium_dir(directory)

  # There has got to be a better, more portable way to do this.
  os.system("find %s -depth -name reference_build -type d -exec rm -rf {} \;" % latest_dir)

  # I could not find good bindings for xz/lzma support, so we system call here too.
  chromium_clean_xz_file = "chromium-" + chromium_version + "-clean.tar.xz"

  remove_file_if_exists(chromium_clean_xz_file)

  if (args.ffmpegclean):
    print("Cleaning ffmpeg from proprietary things...")
    os.system("./chromium-ffmpeg-clean.sh %s %d" % (latest_dir, 0 if args.ffmpegarm else 1))
    print "Done!"

  if (not args.prep):
    print "Compressing cleaned tree, please wait..."
    os.chdir(chromium_root_dir)
    os.system("tar --exclude=\.svn -cf - chromium-%s | xz -0 -T 0 -f > %s" % (chromium_version, chromium_clean_xz_file))

  print "Finished!"
