# -*- coding: utf-8 -*-
from SciDataTool.Functions.conversions import convert
from SciDataTool.Functions.interpolations import get_common_base
from SciDataTool.Functions.symmetries import rebuild_symmetries_axis
from SciDataTool.Classes.DataPattern import DataPattern
from SciDataTool.Functions import AxisError
from numpy import array, ndarray
from importlib import import_module


def get_axis(self, axis, is_real):
    """Computes the vector 'axis' in the unit required, using conversions and symmetries if needed.
    Parameters
    ----------
    self: RequestedAxis
        a RequestedAxis object
    axis: Axis
        an Axis object
    """
    if isinstance(axis, DataPattern):
        self.is_pattern = True
        self.rebuild_indices = axis.rebuild_indices
        self.is_step = axis.is_step
    is_components = getattr(axis, "is_components", False)
    if is_components:
        values = axis.get_values()
        if not self.extension in ["sum", "rss", "mean", "rms", "integrate"]:
            self.extension = "list"
        if self.indices is not None:
            self.values = values[self.indices]
        else:
            self.values = values
    else:
        if self.extension == "pattern":
            if not self.is_pattern:
                raise AxisError(
                    "ERROR: [pattern] cannot be called with non DataPattern axis"
                )
            else:
                is_smallestperiod = True
                is_oneperiod = False
                is_antiperiod = False
                self.extension = "smallestperiod"
        elif self.extension == "smallestperiod":
            if isinstance(axis, DataPattern):
                raise AxisError(
                    "ERROR: [smallestperiod] cannot be called with DataPattern axis"
                )
            else:
                is_smallestperiod = True
                is_oneperiod = False
                is_antiperiod = False
        elif self.extension == "antiperiod":
            if isinstance(axis, DataPattern):
                raise AxisError(
                    "ERROR: [antiperiod] cannot be called with DataPattern axis"
                )
            else:
                is_smallestperiod = False
                is_oneperiod = False
                is_antiperiod = True
        elif self.extension == "oneperiod" or self.transform == "fft":
            if isinstance(axis, DataPattern):
                raise AxisError(
                    "ERROR: [oneperiod] cannot be called with DataPattern axis"
                )
            else:
                is_smallestperiod = False
                is_oneperiod = True
                is_antiperiod = False
        elif self.extension in ["sum", "rss", "mean", "rms", "integrate"]:
            is_smallestperiod = False
            is_oneperiod = False
            is_antiperiod = False
        else:
            if self.input_data is not None and not self.is_step:
                axis_values = axis.get_values(is_smallestperiod=True)
                if min(self.input_data) >= min(axis_values) and max(
                    self.input_data
                ) <= max(axis_values):
                    is_smallestperiod = True
                    is_oneperiod = False
                    is_antiperiod = False
                else:
                    axis_values = axis.get_values(is_oneperiod=True)
                    if min(self.input_data) >= min(axis_values) and max(
                        self.input_data
                    ) <= max(axis_values):
                        is_smallestperiod = False
                        is_oneperiod = True
                        is_antiperiod = False
                        self.extension = "oneperiod"
                    else:
                        is_smallestperiod = False
                        is_oneperiod = False
                        is_antiperiod = False
                        if not self.is_pattern:
                            self.extension = "interval"
            elif self.transform == "ifft":  # Ignore symmetries in ifft case
                is_smallestperiod = True
                is_oneperiod = False
                is_antiperiod = False
            else:
                is_smallestperiod = False
                is_oneperiod = False
                is_antiperiod = False
        # Get original values of the axis
        if self.operation is not None:
            module = import_module("SciDataTool.Functions.conversions")
            func = getattr(module, self.operation)  # Conversion function
            values = array(
                func(
                    axis.get_values(
                        is_oneperiod=is_oneperiod,
                        is_antiperiod=is_antiperiod,
                        is_smallestperiod=is_smallestperiod,
                    ),
                    is_real=is_real,
                )
            )
        else:
            values = array(
                axis.get_values(
                    is_oneperiod=is_oneperiod,
                    is_antiperiod=is_antiperiod,
                    is_smallestperiod=is_smallestperiod,
                )
            )
        # Unit conversions and normalizations
        unit = self.unit
        if unit == self.corr_unit or unit == "SI":
            pass
        elif unit in axis.normalizations:
            if axis.normalizations.get(unit) == "indices":
                values = array([i for i in range(len(values))])
            elif isinstance(axis.normalizations.get(unit), ndarray):
                values = axis.normalizations.get(unit)
            else:
                values = values / axis.normalizations.get(unit)
        else:
            values = convert(values, self.corr_unit, unit)
        # Rebuild symmetries in fft case
        if self.transform == "fft":
            if "period" in axis.symmetries:
                if axis.name != "time":
                    values = values * axis.symmetries["period"]
            elif "antiperiod" in axis.symmetries:
                if axis.name != "time":
                    values = values * axis.symmetries["antiperiod"] / 2
        # Rebuild symmetries in ifft case
        if self.transform == "ifft":
            # if "antiperiod" in axis.symmetries:
            #     axis.symmetries["antiperiod"] = int(axis.symmetries["antiperiod"]/2)
            if (
                self.extension != "smallestperiod"
                and self.extension != "oneperiod"
                and self.extension != "antiperiod"
            ):
                values = rebuild_symmetries_axis(values, axis.symmetries)
            if "period" in axis.symmetries:
                if axis.name != "freqs":
                    values = values * axis.symmetries["period"]
            elif "antiperiod" in axis.symmetries:
                if axis.name != "freqs":
                    values = values * axis.symmetries["antiperiod"] / 2
        # Interpolate axis with input data
        if self.input_data is None:
            self.values = values
        else:
            # if self.is_step:
            #     values = values[axis.rebuild_indices]
            if len(self.input_data) == 2 and self.extension != "axis_data":
                indices = [
                    i
                    for i, x in enumerate(values)
                    if x >= self.input_data[0] and x <= self.input_data[-1]
                ]
                if self.indices is None:
                    self.indices = indices
                else:
                    indices_new = []
                    for i in self.indices:
                        if i in indices:
                            indices_new.append(i)
                    self.indices = indices_new
                self.input_data = None
            else:
                self.values = values
        if self.indices is not None:
            self.values = values[self.indices]
            if self.extension in ["sum", "rss", "mean", "rms", "integrate"]:
                self.indices = None
