# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import os
import sys


# Set this to the path of the 'lawwenda' module (so it must end with
# "/lawwenda"). This directory contains "server.py" and some others.
lawwendadir = {lawwendadir}

# Set this to the path of the Lawwenda configuration directory, or `None` if you
# want to use the default location.
cfgpath = {cfgpath}

os.chdir(lawwendadir)  # not required but security paranoia :)
sys.path.append(os.path.dirname(lawwendadir))
import lawwenda.server
application = lawwenda.server.Server(cfgpath=cfgpath)
