# -*- coding: utf-8 -*-

from SciDataTool.Functions.Plot.plot_4D import plot_4D
from SciDataTool.Functions.Plot.plot_3D import plot_3D
from SciDataTool.Functions.Plot import unit_dict, norm_dict, axes_dict
from numpy import where, meshgrid, unique, max as np_max, min as np_min, array2string


def plot_3D_Data(
    self,
    *arg_list,
    is_norm=False,
    unit="SI",
    save_path=None,
    x_min=None,
    x_max=None,
    y_min=None,
    y_max=None,
    z_min=None,
    z_max=None,
    z_range=None,
    is_auto_ticks=True,
    is_auto_range=True,
    is_2D_view=False,
    is_same_size=False,
    N_stem=100,
    fig=None,
    ax=None,
    is_show_fig=None,
    is_logscale_x=False,
    is_logscale_y=False,
    is_logscale_z=False,
    thresh=0.02,
    is_switch_axes=False,
    colormap="RdBu_r",
):
    """Plots a field as a function of two axes

    Parameters
    ----------
    data : Data
        a Data object
    *arg_list : list of str
        arguments to specify which axes to plot
    is_norm : bool
        boolean indicating if the field must be normalized
    unit : str
        unit in which to plot the field
    save_path : str
        full path including folder, name and extension of the file to save if save_path is not None
    x_min : float
        minimum value for the x-axis
    x_max : float
        maximum value for the x-axis
    y_min : float
        minimum value for the y-axis
    y_max : float
        maximum value for the y-axis
    z_min : float
        minimum value for the z-axis
    z_max : float
        maximum value for the z-axis
    z_range : float
        range to use for the z-axis
    is_auto_ticks : bool
        in fft, adjust ticks to freqs (deactivate if too close)
    is_auto_range : bool
        in fft, display up to 1% of max
    is_2D_view : bool
        True to plot Data in xy plane and put z as colormap
    is_same_size : bool
        True to have all color blocks with same size in 2D view
    N_stem : int
        number of harmonics to plot (only for stem plots)
    fig : Matplotlib.figure.Figure
        existing figure to use if None create a new one
    ax : Matplotlib.axes.Axes object
        ax on which to plot the data
    is_show_fig : bool
        True to show figure after plot
    is_logscale_x : bool
        boolean indicating if the x-axis must be set in logarithmic scale
    is_logscale_y : bool
        boolean indicating if the y-axis must be set in logarithmic scale
    is_logscale_z : bool
        boolean indicating if the z-axis must be set in logarithmic scale
    thresh : float
        threshold for automatic fft ticks
    is_switch_axes : bool
        to switch x and y axes
    """

    if len(arg_list) == 1 and type(arg_list[0]) == tuple:
        arg_list = arg_list[0]  # if called from another script with *arg_list

    # Set unit
    if unit == "SI":
        unit = self.unit

    # Detect fft
    is_fft = False
    if any("wavenumber" in s for s in arg_list) or any("freqs" in s for s in arg_list):
        is_fft = True
        if "dB" in unit:
            if "ref" in self.normalizations:
                ref = self.normalizations["ref"]
            else:
                ref = 1
            unit_str = "[" + unit + " re. " + str(ref) + self.unit + "]"
        else:
            unit_str = "[" + unit + "]"
        if self.symbol == "Magnitude":
            zlabel = "Magnitude " + unit_str
        else:
            zlabel = r"$|\widehat{" + self.symbol + "}|$ " + unit_str
        title1 = "FFT2 of " + self.name.lower() + " "
    else:
        if is_norm:
            zlabel = (
                r"$\frac{" + self.symbol + "}{" + self.symbol + "_0}\, [" + unit + "]$"
            )
        else:
            zlabel = r"$" + self.symbol + "\, [" + unit + "]$"
        title1 = "Surface plot of " + self.name.lower() + " "

    # Extract field and axes
    if is_fft:
        if is_2D_view:
            result = self.get_magnitude_along(arg_list, unit=unit, is_norm=is_norm)
        else:
            result = self.get_harmonics(
                N_stem, arg_list, unit=unit, is_norm=is_norm, is_flat=True
            )
    else:
        result = self.get_along(arg_list, unit=unit, is_norm=is_norm)
    axes_list = result["axes_list"]
    axes_dict_other = result["axes_dict_other"]
    Xdata = result[axes_list[0].name]
    Ydata = result[axes_list[1].name]
    Zdata = result[self.symbol]
    if is_fft and not is_2D_view:
        X_flat = Xdata
        Y_flat = Ydata
        Z_flat = Zdata

    else:
        Y_map, X_map = meshgrid(Ydata, Xdata)
        X_flat = X_map.flatten()
        Y_flat = Y_map.flatten()
        Z_flat = Zdata.flatten()
    if x_min is None:
        x_min = np_min(Xdata)
    if x_max is None:
        x_max = np_max(Xdata)
    if y_min is None:
        y_min = np_min(Ydata)
    if y_max is None:
        y_max = np_max(Ydata)
    if z_range is None:
        if z_min is None:
            z_min = np_min(Zdata)
        if z_max is None:
            z_max = np_max(Zdata)
    else:
        if z_min is None and z_max is None:
            z_max = np_max(Zdata)
        if z_max is None:
            z_max = z_min + z_range
        if z_min is None:
            z_min = z_max - z_range

    # Build labels and titles
    axis = axes_list[0]
    if axis.name in axes_dict:
        name = axes_dict[axis.name]
    else:
        name = axis.name
    title2 = "over " + name.lower()
    if axis.unit == "SI":
        unit = unit_dict[axis.name]
        xlabel = name.capitalize() + " [" + unit + "]"
    elif axis.unit in norm_dict:
        xlabel = norm_dict[axis.unit]
    else:
        unit = axis.unit
        xlabel = name.capitalize() + " [" + unit + "]"
    if (
        axis.name == "angle"
        and axis.unit == "°"
        and round(np_max(axis.values) / 6) % 5 == 0
    ):
        xticks = [i * round(np_max(axis.values) / 6) for i in range(7)]
    else:
        xticks = None

    axis = axes_list[1]
    if axis.name in axes_dict:
        name = axes_dict[axis.name]
    else:
        name = axis.name
    title3 = " and " + axis.name.lower()
    if axis.unit == "SI":
        unit = unit_dict[axis.name]
        ylabel = name.capitalize() + " [" + unit + "]"
    elif axis.unit in norm_dict:
        ylabel = norm_dict[axis.unit]
    else:
        unit = axis.unit
        ylabel = name.capitalize() + " [" + unit + "]"
    if (
        axis.name == "angle"
        and axis.unit == "°"
        and round(np_max(axis.values) / 6) % 5 == 0
    ):
        yticks = [i * round(np_max(axis.values) / 6) for i in range(7)]
    else:
        yticks = None

    title4 = " for "
    for axis in axes_list[2:]:
        if axis.unit == "SI":
            unit = unit_dict[axis.name]
        elif axis.unit in norm_dict:
            unit = norm_dict[axis.unit]
        else:
            unit = axis.unit
        title4 += (
            axis.name
            + "="
            + array2string(
                result[axis.name],
                formatter={"float_kind": "{:.2g}".format},
            ).replace(" ", ", ")
            + " ["
            + unit
            + "], "
        )
    title5 = ""
    for axis_name in axes_dict_other:
        title5 += (
            axis_name
            + "="
            + array2string(
                axes_dict_other[axis_name][0],
                formatter={"float_kind": "{:.2g}".format},
            ).replace(" ", ", ")
            + " ["
            + axes_dict_other[axis_name][1]
            + "], "
        )

    if title4 == " for " and title5 == "":
        title4 = ""

    title = title1 + title2 + title3 + title4 + title5
    title = title.rstrip(", ")

    if is_fft:
        indices = where(Z_flat > abs(thresh * np_max(Zdata)))[0]
        xticks = unique(X_flat[indices])
        yticks = unique(Y_flat[indices])
        if is_auto_range:
            if len(xticks) > 0:
                x_min = -0.1 * xticks[-1]
                x_max = xticks[-1] * 1.1
            if len(yticks) > 0:
                y_min = -yticks[-1] * 1.1
                y_max = yticks[-1] * 1.1
        else:
            x_min = x_min - x_max * 0.05
            x_max = x_max * 1.05
            y_min = y_min - y_max * 0.2
            y_max = y_max * 1.2
        if not is_auto_ticks:
            xticks = None
            yticks = None
        if is_2D_view:
            plot_4D(
                X_flat,
                Y_flat,
                Z_flat,
                Sdata=None,
                is_same_size=is_same_size,
                x_min=x_min,
                x_max=x_max,
                y_min=y_min,
                y_max=y_max,
                z_max=z_max,
                z_min=z_min,
                title=title,
                xticks=xticks,
                yticks=yticks,
                xlabel=xlabel,
                ylabel=ylabel,
                zlabel=zlabel,
                fig=fig,
                ax=ax,
                type_plot="scatter",
                save_path=save_path,
                is_show_fig=is_show_fig,
                is_logscale_x=is_logscale_x,
                is_logscale_y=is_logscale_y,
                is_logscale_z=is_logscale_z,
                is_switch_axes=is_switch_axes,
                colormap=colormap,
            )
        else:
            plot_3D(
                X_flat,
                Y_flat,
                Z_flat,
                fig=fig,
                ax=ax,
                x_min=x_min,
                x_max=x_max,
                y_min=y_min,
                y_max=y_max,
                z_min=0,
                z_max=z_max,
                title=title,
                xticks=xticks,
                yticks=yticks,
                xlabel=xlabel,
                ylabel=ylabel,
                zlabel=zlabel,
                type_plot="stem",
                save_path=save_path,
                is_show_fig=is_show_fig,
                is_logscale_x=is_logscale_x,
                is_logscale_y=is_logscale_y,
                is_logscale_z=is_logscale_z,
                is_switch_axes=is_switch_axes,
                colormap=colormap,
            )
    else:
        if is_2D_view:
            plot_3D(
                Xdata,
                Ydata,
                Zdata,
                x_min=x_min,
                x_max=x_max,
                y_min=y_min,
                y_max=y_max,
                z_max=z_max,
                z_min=z_min,
                xlabel=xlabel,
                ylabel=ylabel,
                zlabel=zlabel,
                title=title,
                xticks=xticks,
                yticks=yticks,
                fig=fig,
                ax=ax,
                type_plot="pcolor",
                save_path=save_path,
                is_show_fig=is_show_fig,
                is_logscale_x=is_logscale_x,
                is_logscale_y=is_logscale_y,
                is_logscale_z=is_logscale_z,
                is_switch_axes=is_switch_axes,
                colormap=colormap,
            )
        else:
            plot_3D(
                X_map,
                Y_map,
                Zdata,
                fig=fig,
                ax=ax,
                x_min=x_min,
                x_max=x_max,
                y_min=y_min,
                y_max=y_max,
                z_min=z_min,
                z_max=z_max,
                title=title,
                xlabel=xlabel,
                ylabel=ylabel,
                zlabel=zlabel,
                yticks=yticks,
                type_plot="surf",
                save_path=save_path,
                is_show_fig=is_show_fig,
                is_logscale_x=is_logscale_x,
                is_logscale_y=is_logscale_y,
                is_logscale_z=is_logscale_z,
                is_switch_axes=is_switch_axes,
                colormap=colormap,
            )
