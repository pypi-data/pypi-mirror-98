# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020, Maximilian Köhl <koehl@cs.uni-saarland.de>

from __future__ import annotations

import typing as t

import dataclasses


NumberT = t.TypeVar("NumberT")


@dataclasses.dataclass(frozen=True)
class Interval(t.Generic[NumberT]):
    infimum: NumberT
    supremum: NumberT
    infimum_included: bool = True
    supremum_included: bool = True
