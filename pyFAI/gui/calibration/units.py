# coding: utf-8
# /*##########################################################################
# Copyright (C) 2016-2018 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ############################################################################*/

__authors__ = ["V. Valls"]
__license__ = "MIT"
__date__ = "20/08/2018"


import enum
import numpy


class Dimentionality(enum.Enum):

    ANGLE = "Angle"

    LENGTH = "Length"

    WAVELENGTH = "Wavelength"

    @property
    def fullname(self):
        return self.value


class Unit(enum.Enum):

    DEGREE = ("Degree", u"deg", Dimentionality.ANGLE),

    RADIAN = ("Radian", u"rad", Dimentionality.ANGLE),

    METER = ("Meter", u"m", Dimentionality.LENGTH),

    ANGSTROM = ("Ångström", u"Å", Dimentionality.WAVELENGTH),

    @property
    def fullname(self):
        return self.value[0][0]

    @property
    def symbol(self):
        return self.value[0][1]

    @property
    def dimensionality(self):
        return self.value[0][2]

    @classmethod
    def get_units(cls, dimensionality):
        result = []
        for unit in cls:
            if unit.dimensionality is dimensionality:
                result.append(unit)
        return result


_converters = None


def _initConverters():
    global _converters
    _converters = {}
    _converters[(Unit.RADIAN, Unit.DEGREE)] = lambda v: v * 180.0 / numpy.pi
    _converters[(Unit.DEGREE, Unit.RADIAN)] = lambda v: v * numpy.pi / 180.0


def convert(value, inputUnit, outputUnit):
    if inputUnit is outputUnit:
        return value
    if value is None:
        return None

    if _converters is None:
        _initConverters()

    converter = _converters.get((inputUnit, outputUnit), None)
    if converter is None:
        raise TypeError("Impossible to convert from %s to %s" % (inputUnit.name, outputUnit.name))

    return converter(value)
