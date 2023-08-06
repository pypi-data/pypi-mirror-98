# -*- coding: utf-8 -*-
from SciDataTool.Functions.conversions import convert
from SciDataTool.Functions.symmetries import rebuild_symmetries_axis
from SciDataTool.Functions import AxisError
from numpy import linspace


def get_values(
    self, unit="SI", is_oneperiod=False, is_antiperiod=False, is_smallestperiod=False
):
    """Returns the vector 'axis' by rebuilding the linspace, symmetries and unit included.
    Parameters
    ----------
    self: DataLinspace
        a DataLinspace object
    unit: str
        requested unit
    is_oneperiod: bool
        return values on a single period
    is_antiperiod: bool
        return values on a semi period (only for antiperiodic signals)
    Returns
    -------
    Vector of axis values
    """
    initial = self.initial
    if self.number == None:
        final = self.final
        number = (final - initial + self.step) / self.step
    elif self.final == None:
        number = self.number
        final = self.initial + (number - 1) * self.step
    else:
        number = self.number
        final = self.final
    values = linspace(initial, final, int(number), endpoint=self.include_endpoint)

    # Unit conversion
    if unit != "SI" and unit != self.unit:
        values = convert(values, self.unit, unit)

    # Ignore symmetries if fft axis
    if self.name == "freqs" or self.name == "wavenumber":
        is_smallestperiod = True

    # Rebuild symmetries
    if is_smallestperiod:
        return values
    elif is_antiperiod:
        if "antiperiod" in self.symmetries:
            return values
        else:
            raise AxisError("ERROR: axis has no antiperiodicity")
    elif is_oneperiod:
        if "antiperiod" in self.symmetries:
            nper = self.symmetries["antiperiod"]
            self.symmetries["antiperiod"] = 2
            values = rebuild_symmetries_axis(values, self.symmetries)
            self.symmetries["antiperiod"] = nper
            return values
        elif "period" in self.symmetries:
            return values
        else:
            return values
    else:
        values = rebuild_symmetries_axis(values, self.symmetries)
        return values
