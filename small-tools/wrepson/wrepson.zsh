#!/bin/zsh

FILENAME="$0"

usage() {
cat <<EOF
Usage: ${FILENAME} [--duplex] [--config=<config>] [--folder=$PWD] [--name=<filename>]

    Wrap epsonscan2 on the command line for a sane experience.
EOF
}

zmodload zsh/zutil
zparseopts -D -E - h=arg_help -help=arg_help -duplex=arg_duplex -folder:=arg_folder -name:=arg_name -config:=arg_config \

alias clear_color='sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g"'

if (( $# )); then
    end_opts=$@[(i)(--|-)]
    if [[ -n ${invalid_opt::=${(M)@[0,end_opts-1]#-}} ]]; then
        echo >&2 "Invalid options: $invalid_opt"
        exit 1
    fi
    set -- "${@[0,end_opts-1]}" "${@[end_opts+1,-1]}"
fi

set -euo pipefail

if [ -n "${arg_help}" ]; then
    usage
    exit 0
fi

if ! which jq>/dev/null; then
    echo "ERROR: jq not found!" >&2
    exit 1
fi

if (( ${#arg_config} > 1 )); then
    config="${arg_config[-1]}"
else
    config="$HOME/.config/epsonscan2/DefaultSettings.SF2"
fi

if (( ${#arg_folder} > 1 )); then
    folder="$(readlink -m "${arg_folder[-1]}")"
else
    folder="$(pwd -P)"
fi

if (( ${#arg_name} > 1 )); then
    filename="${arg_name[-1]}"
else
    filename="scan"
fi

if [ -n "${arg_duplex}" ]; then
    duplex=1
else
    duplex=0
fi

file_jq_filter=$(mktemp jq-filter-XXXXXXXX.jq)
file_epsonscan_cfg=$(mktemp epsonscan2-XXXXXXXX.SF2)

>"${file_jq_filter}" <<EOF
.["Preset"][0]["0"][0]["UserDefinePath"]["string"] = "${folder}" |\
.["Preset"][0]["0"][0]["FileNamePrefix"]["string"] = "${filename}" |\
.["Preset"][0]["0"][0]["DuplexType"]["int"] = "${duplex}"
EOF

TRAPEXIT() {
    rm -v "${file_jq_filter}" "${file_epsonscan_cfg}"
}

jq -f "${file_jq_filter}" <"${config}" >"${file_epsonscan_cfg}"

epsonscan2 -s "${file_epsonscan_cfg}"
