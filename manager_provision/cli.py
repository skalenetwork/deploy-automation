#   -*- coding: utf-8 -*-
#
#   This file is part of deploy-automation
#
#   Copyright (C) 2019 SKALE Labs
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

#   -*- coding: utf-8 -*-
#
#   This file is part of allcator-cli
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

import click
from core import list_validators


@click.group()
def cli():
    pass


@click.argument('endpoint')
@click.option('--all', is_flag=True, help='Show trusted & untrusted validators')
@click.option('--wei', '-w', is_flag=True, help='Show balances in wei')
@cli.command('list-validators', help='Show validators list')
def _list_validators(endpoint, all, wei):
    list_validators(endpoint, all, wei)


if __name__ == '__main__':
    cmd_collection = click.CommandCollection(sources=[cli])
    try:
        cmd_collection()
    except Exception as err:
        print(f'Command execution failed with {err}. Recheck your inputs')
