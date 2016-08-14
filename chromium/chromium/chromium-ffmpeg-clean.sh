#!/usr/bin/env bash
# Copyright 2013-2015 Tomas Popela <tpopela@redhat.com>
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
#  * Rename: clean_ffmpeg.sh -> chromium-ffmpeg-clean.sh.
#  * The shebang line no longer hardcodes the path to bash.

# $1 files
# $2 verbose
function copy_files() {
	for file in $1
	do
		dir_name=`echo $file | sed 's%/[^/]*$%/%'`
		if [[ $dir_name == */* ]]; then
			tmp_dir_name="tmp_"$dir_name
			mkdir -p ../tmp_ffmpeg/$tmp_dir_name
		else
			tmp_dir_name=$file
		fi

		if [ "$2" -eq 1 ]; then
			cp $file ../tmp_ffmpeg/$tmp_dir_name
		else
			cp $file ../tmp_ffmpeg/$tmp_dir_name > /dev/null 2>&1
		fi
	done
}

where=`pwd`

generated_files=`./chromium-ffmpeg-free-sources.py $1 $2`
# As the build system files does not contain the header files, cheat here
# and generate the header files names from source files. These that does not
# exist will be later skipped while copying.
generated_files_headers="${generated_files//.c/.h}"
generated_files_headers="$generated_files_headers ${generated_files//.c/_internal.h}"
if [ "$2" -ne "1" ]; then
	generated_files_headers="$generated_files_headers ${generated_files//.S/.h}"
fi
generated_files_headers="$generated_files_headers ${generated_files//.asm/.h}"

header_files="	libavcodec/x86/inline_asm.h \
		libavcodec/x86/mathops.h \
		libavcodec/x86/vp56_arith.h \
		libavcodec/avcodec.h \
		libavcodec/blockdsp.h \
		libavcodec/bytestream.h \
		libavcodec/dct.h \
		libavcodec/error_resilience.h \
		libavcodec/fdctdsp.h \
		libavcodec/fft.h \
		libavcodec/fft-internal.h \
		libavcodec/fft_table.h \
		libavcodec/flac.h \
		libavcodec/frame_thread_encoder.h \
		libavcodec/get_bits.h \
		libavcodec/h263dsp.h \
		libavcodec/h264chroma.h \
		libavcodec/idctdsp.h \
		libavcodec/internal.h \
		libavcodec/mathops.h \
		libavcodec/me_cmp.h \
		libavcodec/motion_est.h \
		libavcodec/mpegpicture.h \
		libavcodec/mpegutils.h \
		libavcodec/mpegvideo.h \
		libavcodec/mpegvideodsp.h \
		libavcodec/mpegvideoencdsp.h \
		libavcodec/options_table.h \
		libavcodec/pcm_tablegen.h \
		libavcodec/pixblockdsp.h \
		libavcodec/pixels.h \
		libavcodec/put_bits.h \
		libavcodec/qpeldsp.h \
		libavcodec/ratecontrol.h \
		libavcodec/rectangle.h \
		libavcodec/rl.h \
		libavcodec/rnd_avg.h \
		libavcodec/thread.h \
		libavcodec/version.h \
		libavcodec/vp3data.h \
		libavcodec/vp56.h \
		libavcodec/vp56dsp.h \
		libavcodec/vp8data.h \
		libavformat/audiointerleave.h \
		libavformat/avformat.h \
		libavformat/dv.h \
		libavformat/internal.h \
		libavformat/pcm.h \
		libavformat/rdt.h \
		libavformat/rtp.h \
		libavformat/rtpdec.h \
		libavformat/spdif.h \
		libavformat/srtp.h \
		libavformat/options_table.h \
		libavformat/version.h \
		libavformat/w64.h \
		libavutil/x86/asm.h \
		libavutil/x86/bswap.h \
		libavutil/x86/cpu.h \
		libavutil/x86/emms.h
		libavutil/x86/intreadwrite.h \
		libavutil/x86/intmath.h
		libavutil/x86/timer.h \
		libavutil/atomic.h \
		libavutil/atomic_gcc.h \
		libavutil/attributes.h \
		libavutil/audio_fifo.h \
		libavutil/avassert.h \
		libavutil/avutil.h \
		libavutil/bswap.h \
		libavutil/common.h \
		libavutil/colorspace.h \
		libavutil/cpu.h \
		libavutil/cpu_internal.h \
		libavutil/dynarray.h \
		libavutil/internal.h \
		libavutil/intfloat.h \
		libavutil/intreadwrite.h \
		libavutil/libm.h \
		libavutil/lls.h \
		libavutil/macros.h \
		libavutil/pixfmt.h \
		libavutil/qsort.h \
		libavutil/replaygain.h \
		libavutil/thread.h \
		libavutil/timer.h \
		libavutil/timestamp.h \
		libavutil/version.h \
		libswresample/swresample.h \
		libswresample/version.h \
		compat/va_copy.h "

manual_files="	libavcodec/x86/hpeldsp_rnd_template.c \
		libavcodec/x86/rnd_template.c \
		libavcodec/x86/videodsp_init.c \
		libavcodec/x86/vorbisdsp_init.c \
		libavcodec/bit_depth_template.c \
		libavcodec/fft_template.c \
		libavcodec/h264pred_template.c \
		libavcodec/hpel_template.c \
		libavcodec/mdct_template.c \
		libavcodec/pel_template.c \
		libavcodec/utils.c \
		libavcodec/videodsp_template.c \
		libavformat/options.c \
		libavformat/pcm.c \
		libavformat/utils.c \
		libavutil/cpu.c \
		libavutil/x86/cpu.c \
		libavutil/x86/float_dsp_init.c \
		libavutil/x86/x86inc.asm \
		libavutil/x86/x86util.asm "

other_files="	BUILD.gn \
		Changelog \
		COPYING.GPLv2 \
		COPYING.GPLv3 \
		COPYING.LGPLv2.1 \
		COPYING.LGPLv3 \
		CREDITS \
		CREDITS.chromium \
		ffmpeg.gyp \
		ffmpeg_generated.gypi \
		ffmpeg_generated.gni \
		ffmpeg_options.gni \
		ffmpegsumo.ver \
		INSTALL.md \
		LICENSE.md \
		MAINTAINERS \
		OWNERS \
		README.chromium \
		README.md \
		RELEASE \
		xcode_hack.c "

cd $1/third_party/ffmpeg

copy_files "$generated_files" 0
copy_files "$generated_files_headers" 0
copy_files "$manual_files" 1
copy_files "$other_files" 1
copy_files "$header_files" 1

mkdir -p ../tmp_ffmpeg/tmp_chromium/config
cp -r chromium/config ../tmp_ffmpeg/tmp_chromium

cd ../tmp_ffmpeg
for tmp_directory in $(find . -type d -name 'tmp_*')
	do
		new_name=`echo $tmp_directory | sed 's/tmp_//'`
		mv $tmp_directory $new_name
	done

cd $where

rm -rf $1/third_party/ffmpeg
mv $1/third_party/tmp_ffmpeg $1/third_party/ffmpeg
