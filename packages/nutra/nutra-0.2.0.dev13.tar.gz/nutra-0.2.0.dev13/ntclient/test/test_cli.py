# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 15:19:53 2020

@author: shane

This file is part of nutra, a nutrient analysis program.
    https://github.com/nutratech/cli
    https://pypi.org/project/nutra/

nutra is an extensible nutrient analysis and composition application.
Copyright (C) 2018-2020  Shane Jaroch

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import pytest

from .. import __db_target_nt__, __db_target_usda__
from ..persistence.sql.nt import funcs as nt_funcs
from ..persistence.sql.usda import funcs as usda_funcs
from ..services import _init

# TODO: integration tests.. create user, recipe, log.. analyze & compare


def test_0_init():
    result = _init()
    assert result


def test_1_usda_sqlfuncs():
    version = usda_funcs.usda_ver()
    assert version == __db_target_usda__
    result = usda_funcs.nutrients_details()
    assert len(result[1]) == 186

    result = usda_funcs.servings([9050, 9052])
    assert len(result) == 3

    result = usda_funcs.analyze_foods([23567, 23293])
    assert len(result) == 188

    result = usda_funcs.sort_foods(789)
    assert len(result) == 415
    result = usda_funcs.sort_foods(789, [100])
    assert len(result) == 1

    result = usda_funcs.sort_foods_by_kcal(789)
    assert len(result) == 246
    result = usda_funcs.sort_foods_by_kcal(789, [1100])
    assert len(result) == 127


def test_2_nt_sqlfuncs():
    version = nt_funcs.nt_ver()
    assert version == __db_target_nt__
