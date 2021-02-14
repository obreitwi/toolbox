#!/bin/sh

SRCFLD=$(dirname "$(readlink -m "$0")")
TGTFLD="${HOME}/.cargo"

if ! which sccache >/dev/null; then
    echo "WARN: sccache not found!" >&2
fi

[ ! -d "${TGTFLD}" ] && mkdir -vp "${TGTFLD}"

ln -s -f -v "${SRCFLD}/config" "${TGTFLD}"
