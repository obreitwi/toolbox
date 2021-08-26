#!/bin/sh

SRCFLD=$(dirname "$(readlink -m "$0")")
TGTFLD="${HOME}"

ln -s -f -v "${SRCFLD}/inputrc" "${TGTFLD}/.inputrc"
