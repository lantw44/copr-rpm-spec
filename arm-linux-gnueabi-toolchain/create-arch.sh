#!/bin/sh

srcdir="`dirname "$0"`"
test -z "${srcdir}" && srcdir=.

base_arch="arm"
base_triplet="arm-linux-gnueabi"
base_dir="${base_triplet}-toolchain"

if [ "$#" '!=' "3" ]; then
    echo 'Usage:   create-arch.sh ARCH  TRIPLET             OUTPUT_DIRECTORY'
    echo 'Example: create-arch.sh arm   arm-linux-gnueabihf /home/copr/armhf'
    echo 'Example: create-arch.sh arm64 aarch64-linux-gnu   /home/copr/arm64'
    exit 1
fi

new_arch="$1"
new_triplet="$2"
new_dir="$3"

for spec in "${srcdir}/../${base_dir}/${base_triplet}"*/*.spec; do
    base_pkg_name="`basename "${spec}" | sed 's/\.spec$//'`"
    new_pkg_name="`echo "${base_pkg_name}" | sed "s/^${base_triplet}/${new_triplet}/"`"
    echo "Creating RPM spec: ${new_pkg_name}"
    mkdir -p "${new_dir}/${new_pkg_name}"
    sed -e "1s/${base_arch}/${new_arch}/" -e "2s/${base_triplet}/${new_triplet}/" \
        "${spec}" > "${new_dir}/${new_pkg_name}/${new_pkg_name}.spec"
done

for boot_spec in bootstrap; do
    base_pkg_name="${new_triplet}-glibc"
    new_pkg_name="${new_triplet}-glibc-headers"
    echo "Creating bootstrap RPM spec: ${new_pkg_name}"
    mkdir -p "${new_dir}/${new_pkg_name}"
    { echo '%define bootstrap 1';
      cat "${new_dir}/${base_pkg_name}/${base_pkg_name}.spec"; } > \
      "${new_dir}/${new_pkg_name}/${new_pkg_name}.spec"
done

for boot_spec in pass1 pass2; do
    base_pkg_name="${new_triplet}-gcc"
    new_pkg_name="${new_triplet}-gcc-${boot_spec}"
    echo "Creating bootstrap RPM spec: ${new_pkg_name}"
    mkdir -p "${new_dir}/${new_pkg_name}"
    { echo "%define cross_stage ${boot_spec}";
      cat "${new_dir}/${base_pkg_name}/${base_pkg_name}.spec"; } > \
      "${new_dir}/${new_pkg_name}/${new_pkg_name}.spec"
done
