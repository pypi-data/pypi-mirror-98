# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import os
import typing as t


lawwendadir = os.path.abspath(f"{__file__}/..")

auxdir = os.path.abspath(f"{lawwendadir}/_aux")

metadir = os.path.abspath(f"{lawwendadir}/../../_meta")
metadir = metadir if os.path.isdir(metadir) else None


def find_data_file(fname: str, searchdirs: t.Optional[t.Iterable[str]] = None) -> t.Optional[str]:
    if searchdirs is None:
        searchdirs = [auxdir]
        if metadir:
            searchdirs.append(f"{metadir}/misc")
    for searchdir in searchdirs:
        ff = f"{searchdir}/{fname}"
        if os.path.exists(ff):
            return ff
