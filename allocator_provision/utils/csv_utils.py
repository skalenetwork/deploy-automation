#   -*- coding: utf-8 -*-
#
#   This file is part of deploy-automation
#
#   Copyright (C) 2020 SKALE Labs
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import csv
from utils.helper import str_to_bool


def load_csv_lines(path_to_file):
    rows = []
    with open(path_to_file, mode='r') as infile:
        read = csv.reader(infile)
        for row in read:
            rows.append(row)
    return rows


def load_csv_dict(path_to_file):
    items = []
    with open(path_to_file, mode='r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            if row['name'] != '' and str_to_bool(row['added']) is False:
                items.append(dict(row))
        return items
