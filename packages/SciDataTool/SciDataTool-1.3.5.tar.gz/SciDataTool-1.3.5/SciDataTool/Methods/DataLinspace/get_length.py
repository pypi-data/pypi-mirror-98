# -*- coding: utf-8 -*-
from SciDataTool.Functions import AxisError


def get_length(self, is_oneperiod=False, is_antiperiod=False):
    """Returns the length of the axis taking symmetries into account.
    Parameters
    ----------
    self: DataLinspace
        a DataLinspace object
    is_oneperiod: bool
        return values on a single period
    is_antiperiod: bool
        return values on a semi period (only for antiperiodic signals)
    Returns
    -------
    Length of axis
    """

    if self.number is None:
        N = round((self.final - self.initial + self.step) / self.step)
    else:
        N = self.number

    # Rebuild symmetries
    if is_antiperiod:
        if "antiperiod" in self.symmetries:
            return N
        else:
            raise AxisError("ERROR: axis has no antiperiodicity")
    elif is_oneperiod:
        if "antiperiod" in self.symmetries:
            return N * 2
        elif "period" in self.symmetries:
            return N
        else:
            return N
    else:
        if "antiperiod" in self.symmetries:
            return N * self.symmetries["antiperiod"]
        elif "period" in self.symmetries:
            return N * self.symmetries["period"]
        else:
            return N
