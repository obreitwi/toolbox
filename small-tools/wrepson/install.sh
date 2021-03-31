#!/bin/sh

SRCFLD=$(dirname "$(readlink -m "$0")")
TGTFLD="${HOME}/.local/bin"

ln -s -f -v "${SRCFLD}/wrepson.zsh" "${TGTFLD}/wrepson"
