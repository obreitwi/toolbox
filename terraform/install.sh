#!/bin/sh

SRCFLD=$(dirname "$(readlink -m "$0")")
TGTFLD="${HOME}/.local/bin"

[ ! -d "${TGTFLD}" ] && mkdir -vp "${TGTFLD}"

ln -s -f -v "${SRCFLD}/terraform" "${TGTFLD}"
