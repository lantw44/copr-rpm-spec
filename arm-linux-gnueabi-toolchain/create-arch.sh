#!/bin/sh

srcdir="$(dirname "$0")"
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

create_spec () {
    arg_pkg_name="$1"
    arg_src_spec="$2"
    arg_sub_dir="$3"
    if [ -n "${arg_sub_dir}" ]; then
        var_msg_name="${arg_pkg_name} (version ${arg_sub_dir})"
        var_dst_dir="${new_dir}/${arg_pkg_name}/${arg_sub_dir}"
    else
        var_msg_name="${arg_pkg_name}"
        var_dst_dir="${new_dir}/${arg_pkg_name}"
    fi
    var_dst_spec="${var_dst_dir}/${arg_pkg_name}.spec"
    printf 'Creating RPM spec: %s\n' "${var_msg_name}"
    mkdir -p -- "${var_dst_dir}"
    sed -e "1s ${base_arch} ${new_arch} " \
        -e "2s ${base_triplet} ${new_triplet} " \
        "${arg_src_spec}" > "${var_dst_spec}"
}

for spec in "${srcdir}/../${base_dir}/${base_triplet}"-*/*.spec; do
    base_pkg_name="$(basename -- "$(dirname -- "${spec}")")"
    new_pkg_name="$(printf '%s' "${base_pkg_name}" | sed "s/^${base_triplet}/${new_triplet}/")"
    create_spec "${new_pkg_name}" "${spec}"
done

for spec in "${srcdir}/../${base_dir}/${base_triplet}"-*/*/*.spec; do
    base_sub_dir="$(basename -- "$(dirname -- "${spec}")")"
    base_pkg_name="$(basename -- "$(dirname -- "$(dirname -- "${spec}")")")"
    new_pkg_name="$(printf '%s' "${base_pkg_name}" | sed "s/^${base_triplet}/${new_triplet}/")"
    create_spec "${new_pkg_name}" "${spec}" "${base_sub_dir}"
done

create_boot_spec () {
    arg_pkg_name="$1"
    arg_src_spec="$2"
    arg_spec_hdr="$3"
    arg_sub_dir="$4"
    if [ -n "${arg_sub_dir}" ]; then
        var_msg_name="${arg_pkg_name} (version ${arg_sub_dir})"
        var_dst_dir="${new_dir}/${arg_pkg_name}/${arg_sub_dir}"
    else
        var_msg_name="${arg_pkg_name}"
        var_dst_dir="${new_dir}/${arg_pkg_name}"
    fi
    var_dst_spec="${var_dst_dir}/${arg_pkg_name}.spec"
    printf 'Creating bootstrap RPM spec: %s\n' "${var_msg_name}"
    mkdir -p -- "${var_dst_dir}"
    { printf '%s\n' "${arg_spec_hdr}";
      cat -- "${arg_src_spec}"; } > "${var_dst_spec}"
}

for stage in pass1; do
    base_pkg_name="${new_triplet}-glibc"
    new_pkg_name="${new_triplet}-glibc-${stage}"
    create_boot_spec \
        "${new_pkg_name}" \
        "${new_dir}/${base_pkg_name}/${base_pkg_name}.spec" \
        "%global cross_stage ${stage}"
done

for stage in pass1 pass2; do
    base_pkg_name="${new_triplet}-gcc"
    new_pkg_name="${new_triplet}-gcc-${stage}"
    for sub_dir in "${new_dir}/${base_pkg_name}/"*; do
        version="$(basename -- "${sub_dir}")"
        create_boot_spec \
            "${new_pkg_name}" \
            "${sub_dir}/${base_pkg_name}.spec" \
            "%global cross_stage ${stage}" \
            "${version}"
    done
done
