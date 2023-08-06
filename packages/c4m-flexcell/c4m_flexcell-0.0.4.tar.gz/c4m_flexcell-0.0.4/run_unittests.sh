#!/bin/sh
# SPDX-License-Identifier: GPL-2.0-or-later OR AGPL-3.0-or-later OR CERN-OHL-S-2.0+
coverage run --include='c4m/*' -m unittest discover
coverage report -m
